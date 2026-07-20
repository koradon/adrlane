from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from adrlane.agents.registry import normalize_agent_selection
from adrlane.agents.skills import is_adrlane_repository
from adrlane.bootstrap import run_bootstrap
from adrlane.cli.skills import skills_app
from adrlane.upgrade import run_upgrade

app = typer.Typer(
    name="adrlane",
    help="Documentation-as-code bootstrap for AI agents.",
    no_args_is_help=True,
)

app.add_typer(skills_app)


@app.callback()
def main() -> None:
    """Bootstrap documentation scaffolding for AI-assisted development."""


@app.command("init")
def init_command(
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
    workspace: Annotated[
        bool,
        typer.Option(
            "--workspace",
            help=(
                "Enable multi-repo workspace routing "
                "(creates .adrlane/workspace.yaml at the workspace root)."
            ),
        ),
    ] = False,
) -> None:
    """Bootstrap documentation scaffolding in the current repository."""
    target = Path.cwd().resolve()

    try:
        agents = normalize_agent_selection(agent)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc

    result = run_bootstrap(target, dry_run=dry_run, agents=agents, workspace=workspace)

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


@app.command("upgrade")
def upgrade_command(
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            help="Show planned upgrade actions without writing files.",
        ),
    ] = False,
    agent: Annotated[
        list[str] | None,
        typer.Option(
            "--agent",
            help=(
                "Agent adapter to upgrade (repeatable). "
                "Supported: cursor, claude-code. "
                "Defaults to all supported agents when omitted."
            ),
        ),
    ] = None,
) -> None:
    """Refresh docs/llm/* contract files, bootstrap-version, and agent skills."""
    target = Path.cwd().resolve()

    if not is_adrlane_repository(target):
        raise typer.BadParameter(
            "Current directory is not an adrlane repository. Run `adrlane init` first."
        )

    try:
        agents = normalize_agent_selection(agent)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc

    result = run_upgrade(target, agents, dry_run=dry_run)

    if dry_run:
        typer.echo("Planned upgrade actions:")
    else:
        typer.echo("Upgrade complete.")

    for item in result.created:
        typer.echo(f"  + {item}")
    for item in result.updated:
        typer.echo(f"  * {item} (updated)")

    if not result.created and not result.updated:
        typer.echo("  (no actions)")
