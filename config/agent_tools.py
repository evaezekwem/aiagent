from google.genai import types
import tools

# Define a Tool that aggregates all available function schemas
available_functions_schema = types.Tool(
    function_declarations=[
        tools.get_files_info.schema_get_files_info,
        tools.get_file_content.schema_get_file_content,
        tools.write_file.schema_write_file,
        tools.run_python_file.schema_run_python_file,
        tools.get_current_temperature.schema_get_current_temperature
    ]
)

# Map function names to their implementations for easy lookup and invocation
available_functions_dict = {
    "get_files_info": tools.get_files_info.get_files_info,
    "get_file_content": tools.get_file_content.get_file_content,
    "write_file": tools.write_file.write_file,
    "run_python_file": tools.run_python_file.run_python_file,
    "get_current_temperature": tools.get_current_temperature.get_current_temperature
}
