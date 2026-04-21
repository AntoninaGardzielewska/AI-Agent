import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types, errors


class AIAgent(object):
    def __init__(self):
        self.user_prompt = args.user_prompt
        self.verbose = args.verbose
        self.response = None
        self._api_key = self.get_api_key()

    def show_data(self, response):
        print(f"User prompt: {self.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    def get_api_key(self):
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key is None:
            raise RuntimeError("GEMINI_API_KEY was not found in environment variables")
        return api_key

    def get_model_response(self):
        messages = [
            types.Content(role="user", parts=[types.Part(text=self.user_prompt)])
        ]
        client = genai.Client(api_key=self._api_key)
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=messages
            )
        except errors.APIError as e:
            print(f"Error code: {e.code}")        # HTTP status code (e.g., 404)
            print(f"Error status: {e.status}")    # Status string (e.g., 'NOT_FOUND')
            print(f"Error message: {e.message}")  # Human-readable error message
            print(f"Error details: {e.details}")  # Full error response
        if response.usage_metadata is None:
            raise RuntimeError("Failed API request")
        if self.verbose:
            self.show_data(response)
        print(f"Response:\n{response.text}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt to chatbot")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    agent = AIAgent()
    agent.get_model_response()
