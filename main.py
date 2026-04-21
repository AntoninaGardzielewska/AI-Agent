import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types


class AIAgent(object):
    def __init__(self, user_prompt: str, verbose: bool = False):
        self.user_prompt = user_prompt
        self.verbose = verbose
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
            print(f"Error code: {e.code}")  # HTTP status code (e.g., 404)
            print(f"Error status: {e.status}")  # Status string (e.g., 'NOT_FOUND')
            print(f"Error message: {e.message}")  # Human-readable error message
            print(f"Error details: {e.details}")  # Full error response
            return
        if response.usage_metadata is None:
            raise RuntimeError("Failed API request")
        if self.verbose:
            self.show_data(response)
        print(f"Response:\n{response.text}")

    def get_files_info(
        self,
        working_directory: str | os.PathLike[str],
        target_directory: str | os.PathLike[str],
    ) -> list[str] | str:
        working_directory_abs_path = os.path.abspath(working_directory)
        target_directory_abs_path = os.path.normpath(
            os.path.join(working_directory_abs_path, target_directory)
        )

        valid_target_dir = (
            os.path.commonpath([working_directory_abs_path, target_directory_abs_path])
            == working_directory_abs_path
        )
        if not valid_target_dir:
            return f'Error: Cannot list "{target_directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_directory_abs_path):
            return f'Error: "{target_directory}" is not a directory'
        entries = []
        for name in os.listdir(target_directory_abs_path):
            full_path = os.path.join(target_directory_abs_path, name)
            entries.append(
                f"{name}: file_size={os.path.getsize(full_path)} bytes, is_dir={os.path.isdir(full_path)}"
            )

        return entries


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt to chatbot")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    args = parser.parse_args()
    agent = AIAgent(user_prompt=args.user_prompt, verbose=args.verbose)
    agent.get_files_info("calculator", ".")
    agent.get_files_info("calculator", "pkg")
    agent.get_files_info("calculator", "/bin")
    agent.get_files_info("calculator", "../")
    # agent.get_model_response()
