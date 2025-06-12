import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_functions import available_functions, call_function


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

    model_name = "gemini-2.0-flash-001"
    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

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
    if not response.function_calls:
        raise Exception("No function calls found")
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose=verbose)
        function_call_result.parts[0].function_response.response

    if verbose:
        print(f"-> {function_call_result.parts[0].function_response.response.get('result')}")
        token_count = response.usage_metadata.prompt_token_count
        response_count = response.usage_metadata.candidates_token_count
        print(f"Prompt tokens: {token_count}")
        print(f"Response tokens: {response_count}")


if __name__ == "__main__":
    main(sys.argv)
