import os
from dotenv import load_dotenv
load_dotenv(override=True)

from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

resp = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a terse assistant. Answer in one sentence."},
        {"role": "user", "content": "What is the capital of France?"},
    ],
    temperature=0.2,
    max_tokens=100,
)

print("REPLY:", resp.choices[0].message.content)
print("USAGE:", resp.usage)
print("STOP REASON:", resp.choices[0].finish_reason)
