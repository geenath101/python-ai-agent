from dotenv import load_dotenv
from google.genai import types


def get_file_content(working_directory, file_path):
    import os
    try:
        trimmed_agent_path = get_dir_path(working_directory,file_path)
        path = os.path.join(working_directory, trimmed_agent_path)
        abs_path = os.path.abspath(path)
        print(f"get_file_content file path is {abs_path}")
        if working_directory not in abs_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        long_file = f'[...File "{file_path}" truncated at 10000 characters].'
        load_dotenv()
        MAX_CHARS = int(os.environ.get("MAX_CHARS"))  # type: ignore
        character_count = 0
        file_content = ""
        with open(abs_path,"r",encoding="utf-8") as f:
            while chunk := f.read(8192):
                character_count += len(chunk)
                if len(file_content) <= MAX_CHARS:
                    needed = MAX_CHARS - len(file_content)
                    file_content += chunk[:needed]
        if character_count > MAX_CHARS:
            file_content += long_file
        return file_content      
    except FileNotFoundError as e:
        print(e)



schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the content of a file in a given working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be read,relative to the working_directory"),
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