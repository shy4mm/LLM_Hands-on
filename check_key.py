import os
from dotenv import load_dotenv

found = load_dotenv()          # True if a .env file was found and read
print("env file found:", found)

for name in ("OPENROUTER_API_KEY", "ANTHROPIC_API_KEY"):
    value = os.getenv(name)
    if value:
        print(f"{name}: loaded, starts with {value[:6]}..., length {len(value)}")
    else:
        print(f"{name}: NOT set")
