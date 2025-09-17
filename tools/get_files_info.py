import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The base working directory. The function will only list files within this directory or its subdirectories.",
            ),
        },
        required=["working_directory"],
    ),
)


def get_files_info(working_directory, directory="."):
    """Get information about files in the specified directory.

    Args:
        working_directory (str): The base working directory.
        directory (str): The target directory relative to the working directory.

    Returns:
        list: A list of dictionaries containing file information (name, size, and last modified time).
    """
    try:
        # Build the full path and resolve absolute paths
        full_path = os.path.join(working_directory, directory)
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        # Guardrail: Ensure directory is within working_directory
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Guardrail: Ensure the path is a directory
        if not os.path.isdir(abs_full_path):
            return f'Error: "{directory}" is not a directory'

        # List directory contents
        entries = []
        for entry in os.listdir(abs_full_path):
            entry_path = os.path.join(abs_full_path, entry)
            try:
                file_size = os.path.getsize(entry_path)
                is_dir = os.path.isdir(entry_path)
                entries.append(f'{entry}: file_size={file_size} bytes, is_dir={is_dir}')
            except Exception as e:
                entries.append(f'Error: Could not access "{entry}": {e}')

        return "\n".join(entries)
    except Exception as e:
        return f'Error: {e}'
