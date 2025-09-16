from dotenv import load_dotenv


def get_file_content(working_directory, file_path):
    import os
    try:
        path = os.path.join(working_directory, file_path)
        abs_path = os.path.abspath(path)
        if not path.startswith("calculator") or "calculator" not in abs_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        long_file = f'[...File "{file_path}" truncated at 10000 characters].'
        load_dotenv()
        MAX_CHARS = int(os.environ.get("MAX_CHARS"))
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