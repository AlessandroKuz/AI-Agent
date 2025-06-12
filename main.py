import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_functions import available_functions, call_function
from config import MAX_AUTO_PROMPTING


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main(prompt_base):
    if len(prompt_base) < 2:
        print("No prompt provided")
        sys.exit(1)
    prompt = prompt_base[1]

    verbose = False
    if len(prompt_base) >= 3 and prompt_base[2] in ['--verbose', '-v']:
        verbose = True

    model_name = "gemini-2.0-flash-001"
    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    # response = client.models.generate_content(
    #     model=model_name,
    #     contents=messages,
    #     config=types.GenerateContentConfig(
    #         system_instruction=[system_prompt],
    #         tools=[available_functions],
    #     ),
    # )
    # if verbose:
    #     print(f"User prompt: {prompt}")
    #     print('-' * 50)
    # print(response.text)
    # print('*' * 50)
    # if not response.function_calls:
    #     raise Exception("No function calls found")
    # for function_call_part in response.function_calls:
    #     function_call_result = call_function(function_call_part, verbose=verbose)
    #     function_call_result.parts[0].function_response.response
    #
    # if verbose:
    #     print(f"-> {function_call_result.parts[0].function_response.response.get('result')}")
    #     token_count = response.usage_metadata.prompt_token_count
    #     response_count = response.usage_metadata.candidates_token_count
    #     print(f"Prompt tokens: {token_count}")
    #     print(f"Response tokens: {response_count}")

    # for i in range(MAX_AUTO_PROMPTING):
    if verbose:
        print('='*100)
        print('STEPS:', '-'*100, sep='\n')
    for i in range(MAX_AUTO_PROMPTING):
        response = client.models.generate_content(
            model=model_name,
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=[system_prompt],
                tools=[available_functions],
            ),
        )
        if not response:
            break
        print('-----', f'STEP N.{i+1}', '-----', sep='\n')
        if not response.function_calls:
            print("=" * 100)
            print("FINAL ANSWER:")
            print(response.text)
            print("=" * 100)
            break
        for candidate in response.candidates:
            if len(candidate.content.parts) > 0 and candidate.content.parts[0].text:
                response_text = candidate.content.parts[0].text
                if verbose:
                    print(f"RESPONSE: {response_text}", "-"*100, sep='\n')
                messages.append(response_text)
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose=verbose)
            function_call_response_text = function_call_result.parts[0].function_response.response.get('result')
            if verbose:
                print(f"FUNCTION RESULT: {function_call_response_text}", "-"*100, sep='\n')
            messages.append(function_call_response_text)


if __name__ == "__main__":
    main(sys.argv)
