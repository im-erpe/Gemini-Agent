from google.genai import types
from functions.get_files_info import schema_get_files_info,get_files_info
from functions.get_file_content import schema_get_file_content,get_file_content
from functions.run_python_file import schema_run_python_file,run_python_file
from functions.write_file import schema_write_file,write_file
import json
from collections.abc import Callable

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file],
)

def call_function(tool_call,verbose: bool = False) -> dict:
    function_name = tool_call.name
    function_args = dict(tool_call.args or {})

    if verbose:
        print (f" - Calling function: {function_name}({function_args})")
    else:
        print (f" - Calling function: {function_name}")

    function_map: dict[str, Callable[..., str]] = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if function_name not in function_map:
        return types.Content(
            role="tool", 
            parts=[types.Part.from_function_response(name=function_name,response={"error": f'Unknown function: {function_name}'})]
            )
    else:
        function_args["working_directory"] = "./calculator"
        result = function_map[function_name](**function_args)
        return types.Content(
            role="tool", 
            parts=[types.Part.from_function_response(name=function_name,response={"result": result})]
            )