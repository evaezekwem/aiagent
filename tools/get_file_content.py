
import os
from config.config import MAX_FILE_CONTENT_LENGTH
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the content of a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The base directory from which to read files. This is automatically provided and should not be specified by the user."
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file within the working directory whose content is to be retrieved."
            )
        },
        required=["working_directory", "file_path"]
    )
)


def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        # Guardrail: Ensure file_path is within working_directory
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        # Guardrail: Ensure file_path is a regular file
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(abs_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if len(content) > MAX_FILE_CONTENT_LENGTH:
            truncated_content = content[:MAX_FILE_CONTENT_LENGTH]
            trunc_msg = f'\n[...File "{file_path}" truncated at {MAX_FILE_CONTENT_LENGTH} characters]'
            return truncated_content + trunc_msg
        return content
    except Exception as e:
        return f'Error: {e}'
