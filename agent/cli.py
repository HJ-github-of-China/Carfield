from __future__ import annotations

import asyncio
from typing import Optional

import typer
from rich.console import Console

from .app import run_app
from .bootstrap import PermissionMode, RunMode, bootstrap_app


VERSION = "0.1.0"
app = typer.Typer(add_completion=False, no_args_is_help=False)
console = Console()


@app.callback(invoke_without_command=True)
def cli(
    prompt: Optional[str] = typer.Argument(None, help="Prompt to send to the agent."),
    version: bool = typer.Option(False, "--version", "-v", "-V", help="Show version and exit."),
    print_mode: bool = typer.Option(False, "--print", "-p", help="Print response and exit."),
    cwd: Optional[str] = typer.Option(None, "--cwd", help="Working directory."),
    model: str = typer.Option("default", "--model", help="Model name or alias."),
    permission_mode: PermissionMode = typer.Option(
        PermissionMode.default,
        "--permission-mode",
        help="Permission mode for this session.",
    ),
    config: Optional[str] = typer.Option(None, "--config", help="Path to config file."),
    debug: bool = typer.Option(False, "--debug", help="Enable debug output."),
) -> None:
    if version:
        console.print(f"{VERSION} (Carfield)")
        raise typer.Exit(0)

    mode = RunMode.print if print_mode else RunMode.interactive

    try:
        ctx = bootstrap_app(
            mode=mode,
            cwd=cwd,
            model=model,
            permission_mode=permission_mode,
            debug=debug,
            config_file=config,
            prompt=prompt,
        )
        exit_code = asyncio.run(run_app(ctx))
    except KeyboardInterrupt:
        raise typer.Exit(130) from None
    except Exception as exc:
        console.print(f"[red]Error:[/red] {exc}")
        if debug:
            console.print_exception()
        raise typer.Exit(1) from exc

    raise typer.Exit(exit_code)


def main() -> None:
    app()
