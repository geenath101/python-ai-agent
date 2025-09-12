import os


def get_files_info(working_directory,directory="."):
    try:
        path = os.path.join(working_directory,directory)
        abs_path = os.path.abspath(path)
        if not path.startswith("calculator") or "calculator" not in abs_path:
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
                
    
