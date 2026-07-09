from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from adrlane.bootstrap.agents_loader import agent_bootstrap_actions


class SkillsScope(str, Enum):
    LOCAL = "local"
    GLOBAL = "global"


@dataclass(frozen=True)
class SkillsResult:
    created: list[Path]
    skipped: list[Path]
    updated: list[Path]


def resolve_skills_target(scope: SkillsScope) -> Path:
    if scope is SkillsScope.LOCAL:
        return Path.cwd().resolve()
    return Path.home()


def is_adrlane_repository(target: Path) -> bool:
    return (target / ".adrlane").is_dir() or (
        target / "docs" / "llm" / "AGENT_PROTOCOL.md"
    ).is_file()


def run_skills(
    target: Path,
    agents: tuple[str, ...],
    *,
    upgrade: bool = False,
    dry_run: bool = False,
) -> SkillsResult:
    created: list[Path] = []
    skipped: list[Path] = []
    updated: list[Path] = []

    for action in agent_bootstrap_actions(target, agents):
        if action.path.exists():
            if upgrade:
                if not dry_run:
                    action.path.parent.mkdir(parents=True, exist_ok=True)
                    action.path.write_text(action.content or "", encoding="utf-8")
                updated.append(action.path)
            else:
                skipped.append(action.path)
            continue

        if not dry_run:
            action.path.parent.mkdir(parents=True, exist_ok=True)
            action.path.write_text(action.content or "", encoding="utf-8")
        created.append(action.path)

    return SkillsResult(created=created, skipped=skipped, updated=updated)
