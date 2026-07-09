from __future__ import annotations

from typing import Annotated

import typer

from adrlane.agents.registry import normalize_agent_selection
from adrlane.agents.skills import (
    SkillsResult,
    SkillsScope,
    is_adrlane_repository,
    resolve_skills_target,
    run_skills,
)

skills_app = typer.Typer(
    name="skills",
    help="Install or upgrade adrlane agent skills globally or in the current repository.",
    no_args_is_help=True,
)


def _parse_scope(*, local: bool, global_install: bool) -> SkillsScope:
    if local == global_install:
        raise typer.BadParameter("Specify exactly one of --local or --global.")
    return SkillsScope.LOCAL if local else SkillsScope.GLOBAL


def _validate_local_target(target) -> None:
    if not is_adrlane_repository(target):
        raise typer.BadParameter(
            "Current directory is not an adrlane repository. "
            "Run `adrlane init` first, or use `adrlane skills install --global`."
        )


def _echo_skills_result(result: SkillsResult, *, dry_run: bool, action: str) -> None:
    if dry_run:
        typer.echo(f"Planned skills {action}:")
    else:
        typer.echo(f"Skills {action} complete.")

    for item in result.created:
        typer.echo(f"  + {item}")
    for item in result.updated:
        typer.echo(f"  * {item} (updated)")
    for item in result.skipped:
        typer.echo(f"  ~ {item} (already exists, skipped)")

    if not result.created and not result.updated and not result.skipped:
        typer.echo("  (no actions)")


@skills_app.command("install")
def skills_install_command(
    local: Annotated[
        bool,
        typer.Option("--local", help="Install skills in the current repository."),
    ] = False,
    global_install: Annotated[
        bool,
        typer.Option("--global", help="Install skills in the user home directory."),
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
    """Install adrlane agent skills without overwriting existing files."""
    scope = _parse_scope(local=local, global_install=global_install)
    target = resolve_skills_target(scope)

    if scope is SkillsScope.LOCAL:
        _validate_local_target(target)

    try:
        agents = normalize_agent_selection(agent)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc

    result = run_skills(target, agents, upgrade=False, dry_run=False)
    _echo_skills_result(result, dry_run=False, action="install")


@skills_app.command("upgrade")
def skills_upgrade_command(
    local: Annotated[
        bool,
        typer.Option("--local", help="Upgrade skills in the current repository."),
    ] = False,
    global_install: Annotated[
        bool,
        typer.Option("--global", help="Upgrade skills in the user home directory."),
    ] = False,
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Show planned skill updates without writing files."),
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
    """Upgrade adrlane agent skills, overwriting packaged skill files."""
    scope = _parse_scope(local=local, global_install=global_install)
    target = resolve_skills_target(scope)

    if scope is SkillsScope.LOCAL:
        _validate_local_target(target)

    try:
        agents = normalize_agent_selection(agent)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc

    result = run_skills(target, agents, upgrade=True, dry_run=dry_run)
    _echo_skills_result(result, dry_run=dry_run, action="upgrade")
