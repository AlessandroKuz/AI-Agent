import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")



def main(prompt_base):
    if len(prompt_base) < 2:
        print("No prompt provided")
        sys.exit(1)
    prompt = prompt_base[1]

    verbose = False
    if len(prompt_base) >= 3 and prompt_base[2] == '--verbose':
        verbose = True

    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. 
You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    model_name = "gemini-2.0-flash-001"
    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description=("The directory to list files from, relative to the working directory. "
                                "If not provided, lists files in the working directory itself."),
                ),
            },
        ),
    )

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )

    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=[system_prompt],
            tools=[available_functions],
        ),
    )
    if verbose:
        print(f"User prompt: {prompt}")
        print('-' * 50)
    print(response.text)
    print('*' * 50)
    function_call_part = response.function_calls[0]
    print(function_call_part)
    print('*' * 50)
    print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    print('-' * 50)
    if verbose:
        token_count = response.usage_metadata.prompt_token_count
        response_count = response.usage_metadata.candidates_token_count
        print(f"Prompt tokens: {token_count}")
        print(f"Response tokens: {response_count}")


if __name__ == "__main__":
    main(sys.argv)
