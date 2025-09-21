from functions.call_function import call_function
from google.genai import types

def main():
    print(call_function(types.FunctionCall(\
        name="test_function",
        args={"param1":"value1"}),True))





if __name__ ==  "__main__":
    main()