import os
from google.genai import types


def get_files_info(working_directory,directory="."):
    try:
        trimmed_agent_path = get_dir_path(working_directory,directory)
        path = os.path.join(working_directory,trimmed_agent_path)
        abs_path = os.path.abspath(path)
        print(f"get_files_info file path is {abs_path}")
        if working_directory not in abs_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(path):
            return f'Error: "{directory}" is not a directory'
        itemList = os.scandir(path)
        out_put_string = ""
        print(f"Result for '{directory}' directory:")
        for entry in itemList:
           out_put_string +=f"\t- {entry.name}: file_size={os.path.getsize(entry.path)} bytes, is_dir={entry.is_dir()}"
           out_put_string +="\n"
        return out_put_string
    except FileNotFoundError as e:
        print(e)


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
        },
    ),
)

def get_dir_path(working_directory,agent_provided_path):
        splited_directory = agent_provided_path.split('/');
        trimmed_agent_path="."
        if splited_directory and splited_directory[0] == working_directory:
            print("matched directories trimming the agent provided path ")
            for i in range(len(splited_directory) -1):
                trimmed_agent_path +="/"+ splited_directory[i+1]
            print(f'trimmed path {trimmed_agent_path}')
        return trimmed_agent_path
                
    
