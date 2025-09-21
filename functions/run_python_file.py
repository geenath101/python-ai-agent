import os
import subprocess
from google.genai import types


def run_python_file(working_directory,file_path,args=[]):
    try:
        trimmed_agent_path = get_dir_path(working_directory,file_path)
        local_path = os.path.join(working_directory,trimmed_agent_path)
        abs_path = os.path.abspath(local_path)
        print(f"run_python_file file path is {abs_path}")
        if working_directory not  in abs_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(abs_path):
            return f'Error: File "{file_path}" not found.'
        main_path,extention = os.path.splitext(file_path)
        if not extention == ".py":
            return f'Error: "{file_path}" is not a Python file.'
        command = "uv run "+ abs_path
        #print(f'arg length {len(args)}')
        arguments = "".join(args)
        command = command+" "+arguments
        #print(f'complete command and arguements: {command}')
        complete_object = subprocess.run(command,capture_output=True,timeout=30,shell=True,text=True)
        out = ""
        if complete_object.stdout:
            out = f'STDOUT:{complete_object.stdout}' 
        if complete_object.stderr:
            out = f'STDERR:{complete_object.stderr}'
        #print(f'reutn code is  {complete_object.returncode}')
        if complete_object.returncode != 0:
            out = f'Process exited with code {complete_object.returncode}'
        if not out:
            out = 'No output produced'
        return out
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a Python file in a given directory with optional command-line arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to run, relative to the working_directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the Python file."
            ),
        }
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


