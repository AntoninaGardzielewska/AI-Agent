import os
import argparse
from dotenv import load_dotenv
from google import genai

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt to chatbot")
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("GEMINI_API_KEY was not found in environment variables")

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-2.5-flash", contents=args.user_prompt
)
print(f"User prompt: {args.user_prompt}")
if response.usage_metadata is not None:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
else:
    raise RuntimeError("Failed API request")

print(f"Response:\n{response.text}")

# def main():
#    print("Hello from ai-agent!")


# if __name__ == "__main__":
#    main()
