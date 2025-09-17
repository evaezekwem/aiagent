from google.genai import types
from tools.get_files_info import schema_get_files_info, get_files_info
from tools.get_file_content import schema_get_file_content, get_file_content
from tools.write_file import schema_write_file, write_file
from tools.run_python_file import schema_run_python_file, run_python_file
from tools.get_current_temperature import get_current_temperature_declaration, get_current_temperature

# Define a Tool that aggregates all available function schemas
available_functions_schema = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
        get_current_temperature_declaration
    ]
)

# Map function names to their implementations for easy lookup and invocation
available_functions_dict = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
    "get_current_temperature": get_current_temperature
}
