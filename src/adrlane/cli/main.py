from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from adrlane.agents.registry import normalize_agent_selection
from adrlane.bootstrap import run_bootstrap

app = typer.Typer(
    name="adrlane",
    help="Documentation-as-code bootstrap for AI agents.",
    no_args_is_help=True,
)


@app.callback()
def main() -> None:
    """Bootstrap documentation scaffolding for AI-assisted development."""


@app.command("init")
def init_command(
    path: Annotated[
        Path | None,
        typer.Option(
            "--path",
            "-p",
            help="Repository root to bootstrap.",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
        ),
    ] = None,
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            help="Show planned bootstrap actions without writing files.",
        ),
    ] = False,
    agent: Annotated[
        list[str] | None,
        typer.Option(
            "--agent",
            help=(
                "Agent adapter to install (repeatable). "
                "Supported: cursor, claude-code. "
                "Defaults to all supported agents when omitted."
            ),
        ),
    ] = None,
) -> None:
    """Bootstrap documentation scaffolding in a repository."""
    target = path or Path.cwd()

    try:
        agents = normalize_agent_selection(agent)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc

    result = run_bootstrap(target, dry_run=dry_run, agents=agents)

    if dry_run:
        typer.echo("Planned bootstrap actions:")
    else:
        typer.echo("Bootstrap complete.")

    for item in result.created:
        typer.echo(f"  + {item}")
    for item in result.skipped:
        typer.echo(f"  ~ {item} (already exists, skipped)")

    if not result.created and not result.skipped:
        typer.echo("  (no actions)")
