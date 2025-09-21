import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

sytem_prompt = """
You are a helpful AI coding agent.
PLEASE , DONT GIVE ME INTERMEDIATE RESULTS OR GIVE ANY COMMENTS OR TRY TO GET THE CONFIRMATION OF THE EXECUTION FLOW , PLEASE CARRY ON WITH YOUR TASKS AND GET BACK TO ME WITH THE RESULTS.
FIRST OF ALL DONT FORGET TO LIST OUT CURRENT FILES AND DIRECTORIES BEFORE YOU DO ANYTHING IT WILL HELP YOU TO FIGURE OUT WHERE TO FIND THE APPROPRIATE FILES.
When a user asks a question or makes a request, make a function call plan.dont get the confirmation just execute the task if you can find the operation. availablle operations as follows:
- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files
Dont ask where to where you can check for files and any other questions , all the the operations and tools are provided to you.
"""

# sytem_prompt = """
# You are a helpful AI coding agent. Your primary goal is to complete tasks by interacting with a file system.

# **Your first step should always be to use the `get_files_info` function to understand the contents of the current directory.** Do not assume any files exist.

# After you have a list of files, you can decide whether to read a file, write a file, or run a python script to complete the user's request.

# All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
# """

input = sys.argv[1]

messages = [
    types.Content(role="user", parts=[types.Part(text=input)]),
]

available_functions = types.Tool(function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

client = genai.Client(api_key=api_key)

for step in range(20):
    try:    
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(system_instruction = sytem_prompt,tools=[available_functions])    
        )
        if response.text:
            print(f"Got the final respose ...{response.text}")
            break
        else:    
            for cand in response.candidates: # type: ignore #type ignore
                print(f"Going throught the candidate messages...")
                str_response = "".join([part.text for part in cand.content.parts if part.text]) #type: ignore
                print(f"got message ... {str_response}")
                messages.append(types.Content(role="model",parts=[types.Part(text=str_response)]))

            if response.function_calls:
                for call in response.function_calls:
                    print(f"Calling function: {call.name}({call.args})")
                    func_response = call_function(types.FunctionCall(name=call.name,args=call.args))
                    ai_response = func_response.parts[0].function_response.response # type: ignore
                    print(f"got function call response ... {ai_response}")
                    if ai_response is None: 
                        raise Exception(" rasponse is empty for some reason")

                    messages.append(func_response) # type:ignore

                    if len(sys.argv)>2 and sys.argv[2] == "--verbose":
                        print(f"-> {ai_response}") # type:ignore
    except Exception as e:
        print(f"Exception occurred .... {e}")