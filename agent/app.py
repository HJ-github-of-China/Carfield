from __future__ import annotations

import asyncio
from rich.console import Console

from .bootstrap import RuntimeContext, RunMode


console = Console()


async def run_app(ctx: RuntimeContext) -> int:
    if ctx.config.debug:
        console.print("[dim]runtime context[/dim]")
        console.print(ctx)

    if ctx.config.mode is RunMode.print:
        return await run_print_once(ctx)

    return await run_repl(ctx)


async def run_print_once(ctx: RuntimeContext) -> int:
    prompt = ctx.config.prompt or ""
    if not prompt.strip():
        console.print("[red]Error:[/red] --print mode requires a prompt.")
        return 2

    # 第 04 章会把这里替换为 AgentLoop.run_once()
    await asyncio.sleep(0)
    console.print(f"[bold]User:[/bold] {prompt}")
    console.print("[bold]Assistant:[/bold] model loop is not implemented yet.")
    return 0


async def run_repl(ctx: RuntimeContext) -> int:
    console.print("[bold]Carfield[/bold]")
    console.print("[dim]Type /exit to quit.[/dim]")

    while True:
        try:
            user_input = input("> ")
        except EOFError:
            console.print()
            return 0
        except KeyboardInterrupt:
            console.print()
            return 130

        text = user_input.strip()
        if not text:
            continue
        if text in {"/exit", "/quit"}:
            return 0

        # 第 02 章会把这里改成追加 UserMessage。
        # 第 04 章会把这里改成调用 AgentLoop。
        console.print(f"[bold]Assistant:[/bold] received: {text}")
