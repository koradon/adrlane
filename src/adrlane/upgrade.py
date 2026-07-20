from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from adrlane import __version__
from adrlane.agents.skills import run_skills
from adrlane.bootstrap.actions import BootstrapAction
from adrlane.bootstrap.templates_loader import framework_bootstrap_actions


@dataclass(frozen=True)
class UpgradeResult:
    created: list[Path]
    updated: list[Path]


def run_upgrade(
    target: Path,
    agents: tuple[str, ...],
    *,
    dry_run: bool = False,
) -> UpgradeResult:
    """Refresh package-owned bootstrap content to the current adrlane version.

    Overwrites docs/llm/* contract files, .adrlane/bootstrap-version, and agent
    skill files. Never touches user-owned content: docs/README.md,
    docs/ideas/README.md, docs/roadmap/README.md, docs/{specs,plans,adr,ideas,
    roadmap} contents, or .adrlane/workspace.yaml.
    """
    root = target.resolve()
    created: list[Path] = []
    updated: list[Path] = []

    version_action = BootstrapAction(
        path=root / ".adrlane" / "bootstrap-version",
        kind="file",
        content=f"{__version__}\n",
    )

    for action in (version_action, *framework_bootstrap_actions(root)):
        existed = action.path.exists()
        if not dry_run:
            action.path.parent.mkdir(parents=True, exist_ok=True)
            action.path.write_text(action.content or "", encoding="utf-8")
        (updated if existed else created).append(action.path)

    skills_result = run_skills(root, agents, upgrade=True, dry_run=dry_run)
    created.extend(skills_result.created)
    updated.extend(skills_result.updated)

    return UpgradeResult(created=created, updated=updated)
