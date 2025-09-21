def get_dir_path(working_directory,agent_provided_path):
        splited_directory = agent_provided_path.split('/');
        trimmed_agent_path="."
        if splited_directory and splited_directory[0] == working_directory:
            print("matched directories trimming the agent provided path ")
            for i in range(len(splited_directory) -1):
                trimmed_agent_path +="/"+ splited_directory[i+1]
            print(f'trimmed path {trimmed_agent_path}')
        return trimmed_agent_path