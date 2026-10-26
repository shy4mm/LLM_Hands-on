from llm import client, MODEL

MAX_TOKENS = 300

messages = [{"role": "system", "content": "You are a helpful assistant."}]
session_in = 0
session_out = 0

while True:
    question = input("you> ").strip()
    if question in {"quit", "exit"}:
        break
    if not question:
        continue

    messages.append({"role": "user", "content": question})

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=MAX_TOKENS,
        )
    except Exception as e:
        print("ERROR:", e)
        messages.pop()          # remove the question that failed
        continue

    reply = resp.choices[0].message.content
    print("bot>", reply)
    messages.append({"role": "assistant", "content": reply})

    u = resp.usage
    session_in += u.prompt_tokens
    session_out += u.completion_tokens
    print(
        f"[input={u.prompt_tokens} output={u.completion_tokens} "
        f"total={u.total_tokens} max_tokens={MAX_TOKENS} "
        f"stop={resp.choices[0].finish_reason} "
        f"cost={getattr(u, 'cost', 'n/a')}]"
    )
    print(f"[session so far: input={session_in} output={session_out}]\n")
