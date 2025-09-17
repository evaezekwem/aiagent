import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from config.prompts import system_prompt
from config.config import MAX_ITERATIONS, WORKING_DIRECTORY
from config.agent_tools import available_functions_schema
from config.agent_tools import available_functions_dict

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

class Agent:
    """A simple AI agent that can process prompts, use tools, and generate responses using the Gemini API.
    """
    def __init__(self, api_key, system_prompt, user_prompt,model_name="gemini-2.0-flash-001", verbose=False):
        """
        Initialize the Agent.

        Args:
            api_key (str): Gemini API key for authentication.
            system_prompt (str): System prompt to guide the model's behavior.
            model_name (str, optional): Name of the Gemini model to use. Defaults to "gemini-2.0-flash-001".
            verbose (bool, optional): If True, enables verbose output. Defaults to False.

        Returns:
            None
        """
        self.client = genai.Client(api_key=api_key)
        self.system_prompt = system_prompt
        self.verbose = verbose
        self.model_name = model_name
        self.config = self._config()
        self.max_iterations = int(MAX_ITERATIONS)
        self.working_directory = WORKING_DIRECTORY
        self.messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    
    def _config(self):
        """
        Build the configuration object for Gemini content generation.

        Args:
            None

        Returns:
            google.genai.types.GenerateContentConfig: Configuration object with tool schemas and system instructions.
        """
        return types.GenerateContentConfig(
            tools=[available_functions_schema],
            system_instruction=self.system_prompt
        )

    def _call_function(self, function_call_part):
        """
        Dispatches a function call to the appropriate tool and returns the result.

        Args:
            function_call_part (google.genai.types.FunctionCall): The function call part containing the function name and arguments.

        Returns:
            google.genai.types.Content: Content object containing the function response or error.
        """
        function_call_part.args['working_directory'] = self.working_directory
        if self.verbose:
            print(f" - Calling function: {function_call_part.name} with args: {function_call_part.args}")
        else:
            print(f" - Calling function: {function_call_part.name}")

        if not function_call_part.name in available_functions_dict:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"error": f"Unknown function: {function_call_part.name}"},
                    )
                ],
            )

        
        try:
            func = available_functions_dict.get(function_call_part.name)
            result = func(**function_call_part.args)
            
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"result": result},
                    )
                ],
            )

        except Exception as e:
            return f'Error: {e}'

    def generate_response(self):
        """
        Generates a response from the Gemini model, handling any tool calls as needed.

        Returns:
            google.genai.types.GenerateContentResponse: The final response from the Gemini model.
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=self.messages,
            config=self.config
        )

        if self.verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        print(f"Response received with {len(response.candidates)} candidate(s).")
        if response.candidates:
            for candidate_index in range(len(response.candidates)):
                candidate = response.candidates[candidate_index]
                
                if self.verbose:
                    print(f"------------Processing candidate {candidate_index+1} with {len(candidate.content.parts)} parts.------------")
                function_call_content = candidate.content 
                self.messages.append(function_call_content)

            if not response.function_calls:
                return response.text
            
            function_responses = []
            for function_call_part in response.function_calls:
                function_call_result = self._call_function(function_call_part)
                
                if not function_call_result.parts[0].function_response.response or 'Error' in function_call_result.parts[0].function_response.response:
                        raise Exception(
                            f"Function call failed: {function_call_result.parts[0].function_response.response.get('error') or 'Unknown error'}"
                        )
                if not function_call_result.parts[0].function_response:
                    raise Exception("empty function call result")
                
                if function_call_result.parts[0].function_response.response and self.verbose:
                    print(f"  -> {function_call_result.parts[0].function_response.response}")

                function_responses.append(function_call_result)

            if not function_responses:
                raise Exception("No function responses generated")
            
            self.messages.append(types.Content(role="user", parts=[fr.parts[0] for fr in function_responses]))

    def run(self):
        """
        Runs the agent on the given prompt and prints the final response.

        Returns:
            None
        """
        iters = 0
        while True:
            iters += 1
            if iters > self.max_iterations:
                raise Exception(f"Reached maximum iterations ({self.max_iterations}). Stopping.")

            try:
                final_response = self.generate_response()
                if final_response:
                    print("Final response:")
                    print(final_response)
                    break
            except Exception as e:
                print(f"Error during response generation: {e}")

def parse_args(args):
    verbose = False
    if '--verbose' in args:
        verbose = True
        args.remove('--verbose')
    prompt = " ".join(args)
    return prompt, verbose

def main():
    # Parse command line arguments and run the agent
    if len(sys.argv) < 2:
        raise Exception("Error: No prompt provided. Usage: python main.py <prompt> [--verbose]")
        
    prompt, verbose = parse_args(sys.argv[1:])
    agent = Agent(api_key=api_key, system_prompt=system_prompt, user_prompt=prompt, verbose=verbose)
    agent.run()


if __name__ == "__main__":
    main()
           
                             