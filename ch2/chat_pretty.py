from rich.console import Console
from rich.markdown import Markdown
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

from llm import client, MODEL

MAX_TOKENS = 300
console = Console()


def main():
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    session_in = 0
    session_out = 0
    turns = 0

    console.print(Panel.fit(
        f"[bold cyan]LLM Chat[/bold cyan]\nmodel: [green]{MODEL}[/green]   "
        f"max_tokens: [yellow]{MAX_TOKENS}[/yellow]\n"
        "type [bold]quit[/bold] or press Ctrl+C to exit",
        border_style="cyan",
    ))

    while True:
        try:
            question = Prompt.ask("[bold green]you[/bold green]").strip()
        except (KeyboardInterrupt, EOFError):
            break
        if question in {"quit", "exit"}:
            break
        if not question:
            continue

        messages.append({"role": "user", "content": question})

        try:
            with console.status("[bold cyan]thinking...[/bold cyan]"):
                resp = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    max_tokens=MAX_TOKENS,
                )
        except KeyboardInterrupt:
            console.print("[yellow]request cancelled[/yellow]\n")
            messages.pop()
            continue
        except Exception as e:
            console.print(Panel(escape(str(e)), title="error", border_style="red"))
            messages.pop()
            continue

        reply = resp.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        console.print(Panel(Markdown(reply), title="bot", border_style="blue"))

        u = resp.usage
        stop = resp.choices[0].finish_reason
        session_in += u.prompt_tokens
        session_out += u.completion_tokens
        turns += 1

        table = Table(show_header=True, header_style="bold magenta", box=None)
        for col in ("input", "output", "total", "max_tokens", "stop", "cost", "turn"):
            table.add_column(col, justify="right")
        table.add_row(
            str(u.prompt_tokens),
            str(u.completion_tokens),
            str(u.total_tokens),
            str(MAX_TOKENS),
            f"[red]{stop}[/red]" if stop == "length" else f"[green]{stop}[/green]",
            str(getattr(u, "cost", "n/a")),
            str(turns),
        )
        console.print(table)
        console.print(f"[dim]session total: input={session_in}  output={session_out}[/dim]\n")

    console.print(
        f"\n[bold cyan]bye![/bold cyan] [dim]{turns} turns, "
        f"{session_in} input tokens, {session_out} output tokens[/dim]"
    )


if __name__ == "__main__":
    main()
