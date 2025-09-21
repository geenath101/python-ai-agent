from google.genai import types
from functions.get_file_content  import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file

function_map = {
    "get_file_content":get_file_content,
    "get_files_info":get_files_info,
    "run_python_file": run_python_file,
    "write_file":write_file
}


def call_function(function_call_part:types.FunctionCall, verbose=False):
    func_name = function_call_part.name
    if func_name is None:
        return "func_name cannot be none"
    args = function_call_part.args
    if args is None:
        return "args cannot be none"
    if verbose:
        print(f"Calling function:{function_call_part.name}({function_call_part.args})")
    else:
        print(f"- Calling function:{function_call_part.name}")
    
    func = function_map.get(func_name) 
    try:
        py_args = dict(args)
        py_args["working_directory"] = "calculator"  
        result = func(**py_args)   # type: ignore 
        return types.Content(role="tool",parts=[
                    types.Part.from_function_response(
                    name=func_name,
                    response={"result": result},)],)
    except Exception as e:
        print(f"more error details {e}")
        return types.Content(
               role="tool",
               parts=[
                    types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unknown function: {func_name}"},)],
)

