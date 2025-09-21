import os
from google.genai import types


def write_file(working_directory,file_path,content):
    try:
        trimmed_agent_path = get_dir_path(working_directory,file_path)
        abs_path = os.path.join(working_directory,trimmed_agent_path)
        print(f"write_file file path is {abs_path}")
        if working_directory not in abs_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        directory_path = os.path.dirname(abs_path)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        with open(abs_path,"w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error:{e}'

    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the given content to a given file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file where the content should be written"),
            "content": types.Schema(
                type=types.Type.STRING,
                description="String content"),    
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