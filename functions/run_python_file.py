import os
import subprocess
import shlex
def run_python_file(working_directory,file_path,args=[]):
    try:
        local_path = os.path.join(working_directory,file_path)
        abs_path = os.path.abspath(local_path)
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


