from main import AIAgent

import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types


if __name__ == "__main__":
    agent = AIAgent(user_prompt="test")
    print(agent.get_files_info("calculator", "."))
    print(agent.get_files_info("calculator", "pkg"))
    print(agent.get_files_info("calculator", "/bin"))
    print(agent.get_files_info("calculator", "../"))