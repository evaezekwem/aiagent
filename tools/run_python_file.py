import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a specified Python file within the working directory and return its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The base directory from which to execute the Python file. This is automatically provided and should not be specified by the user."
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the Python file within the working directory to be executed."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A list of string arguments to pass to the Python file when executing it."
            )
        },
        required=["working_directory", "file_path"]
    )
)

def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        # Guardrail: Ensure file_path is within working_directory
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        # Guardrail: Ensure file exists
        if not os.path.isfile(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        # Guardrail: Ensure file is a Python file
        if not abs_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        # Build command
        cmd = ['python', abs_file_path] + args
        try:
            completed = subprocess.run(
                cmd,
                cwd=abs_working_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
        except Exception as e:
            return f"Error: executing Python file: {e}"
        output = []
        if completed.stdout:
            output.append(f"Code executed successfully\nSTDOUT:\n{completed.stdout}")
        if completed.stderr:
            output.append(f"STDERR:\n{completed.stderr}")
        if completed.returncode != 0:
            output.append(f"Process exited with code {completed.returncode}")
        if not output:
            return "No output produced."
        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"
