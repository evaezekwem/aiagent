import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The base directory from which to write files. This is automatically provided and should not be specified by the user."
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file within the working directory where the content is to be written."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the specified file."
            )
        },
        required=["working_directory", "file_path", "content"]
    )
)

def write_file(working_directory, file_path, content):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        # Guardrail: Ensure file_path is within working_directory
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        # Create parent directories if needed
        parent_dir = os.path.dirname(abs_file_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
        # Write content to file
        with open(abs_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
