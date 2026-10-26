import os
from dotenv import load_dotenv
load_dotenv(override=True)

from openai import OpenAI

MODEL = "openai/gpt-4o-mini"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
