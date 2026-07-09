from __future__ import annotations

from pathlib import Path

from adrlane import __version__
from adrlane.bootstrap.actions import BootstrapAction
from adrlane.bootstrap.agents_loader import agent_bootstrap_actions
from adrlane.bootstrap.templates_loader import template_bootstrap_actions


def bootstrap_plan(
    target: Path,
    agents: tuple[str, ...] = (),
) -> list[BootstrapAction]:
    """Return bootstrap actions for a repository root."""
    actions: list[BootstrapAction] = [
        BootstrapAction(path=target / ".adrlane", kind="dir"),
        BootstrapAction(
            path=target / ".adrlane" / "bootstrap-version",
            kind="file",
            content=f"{__version__}\n",
        ),
    ]
    for name in ("specs", "plans", "adr", "ideas", "roadmap"):
        actions.append(BootstrapAction(path=target / "docs" / name, kind="dir"))
    actions.extend(template_bootstrap_actions(target))
    if agents:
        actions.extend(agent_bootstrap_actions(target, agents))
    return actions
