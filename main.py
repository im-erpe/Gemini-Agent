import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import available_functions,call_function


def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    #generate_content(client, messages, args.verbose)

    for i in range(20):
        final_response = generate_content(client, messages, args.verbose)
        if final_response is not None:
            print("Final response:")
            print(final_response)
            break
    else:
        print("Problem was not solved!")
        sys.exit(0)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
            )
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    messages.append(response.candidates[0].content)    

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
        print("Response:")



    if not response.function_calls:
        return response.text
    else:
        for function_call in response.function_calls:
            result_message = call_function(function_call, verbose)
            if not result_message.parts[0].function_response.response:
                raise RuntimeError("Function call returned no content")

            messages.append(result_message)

            if verbose:
                print(f"-> {result_message.parts[0].function_response.response}")
                

        


if __name__ == "__main__":
    main()
