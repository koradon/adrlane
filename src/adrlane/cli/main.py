from __future__ import annotations

from pathlib import Path

import typer

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
    path: Path = typer.Option(
        Path.cwd(),
        "--path",
        "-p",
        help="Repository root to bootstrap.",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show planned bootstrap actions without writing files.",
    ),
) -> None:
    """Bootstrap documentation scaffolding in a repository."""
    result = run_bootstrap(path, dry_run=dry_run)

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
