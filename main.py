import os
from dotenv import load_dotenv
from google import genai
import argparse

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if(api_key is None):
    raise RuntimeError("API KEY not found")
client = genai.Client(api_key=api_key)

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`
    
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=args.user_prompt
        )
    
    if response.usage_metadata is not None:
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}')
        print(response.text)
    else:
        raise RuntimeError('failed API request')


if __name__ == "__main__":
    main()
