from llm import client, MODEL

resp = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "Answer in exactly one word."},
        {"role": "user", "content": "What is a database index?"},
    ],
    max_tokens=20,
)

print("REPLY:", resp.choices[0].message.content)
print("USAGE:", resp.usage)
