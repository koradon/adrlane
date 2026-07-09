from __future__ import annotations

from pathlib import Path, PurePosixPath

from adrlane.agents.registry import AGENT_ADAPTERS
from adrlane.bootstrap.actions import BootstrapAction

_AGENT_TEMPLATE_ROOT = Path(__file__).resolve().parent / "templates" / "agents"
_SHARED_SKILLS_ROOT = _AGENT_TEMPLATE_ROOT / "skills"


def agent_bootstrap_actions(target: Path, agents: tuple[str, ...]) -> list[BootstrapAction]:
    actions: list[BootstrapAction] = []

    for agent_name in agents:
        adapter = AGENT_ADAPTERS[agent_name]
        for skill_dir in sorted(_SHARED_SKILLS_ROOT.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_file = skill_dir / "SKILL.md"
            if not skill_file.is_file():
                continue
            relative = PurePosixPath(adapter.skill_prefix) / skill_dir.name / "SKILL.md"
            actions.append(
                BootstrapAction(
                    path=target / relative,
                    kind="file",
                    content=skill_file.read_text(encoding="utf-8"),
                )
            )

    return actions
