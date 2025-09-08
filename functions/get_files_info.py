import os


def get_files_info(working_directory,directory="."):
    try:
        path = os.path.join(working_directory,directory)
        os.listdir(path)
        itemList = os.scandir(path) 
        print(f"Result for current directory")
        for entry in itemList:
            print(f" - {entry.name}: file_size={os.path.getsize(entry.path)} bytes, is_dir={entry.is_dir()}")
    except FileNotFoundError:
                
    



def main():
    get_files_info("/home/geenath/projects/python-ai-agent/python-ai-agent-proj/functions",".")



if __name__ == "__main__":
    main()