from __future__ import annotations

from pathlib import Path

from adrlane import __version__
from adrlane.bootstrap.actions import BootstrapAction
from adrlane.bootstrap.agents_loader import agent_bootstrap_actions
from adrlane.bootstrap.templates_loader import template_bootstrap_actions

_WORKSPACE_CONFIG_TEMPLATE = (
    Path(__file__).resolve().parent / "templates" / "workspace" / "workspace.yaml"
)


def bootstrap_plan(
    target: Path,
    agents: tuple[str, ...] = (),
    *,
    workspace: bool = False,
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
    if workspace:
        actions.append(
            BootstrapAction(
                path=target / ".adrlane" / "workspace.yaml",
                kind="file",
                content=_WORKSPACE_CONFIG_TEMPLATE.read_text(encoding="utf-8"),
            )
        )
    if agents:
        actions.extend(agent_bootstrap_actions(target, agents))
    return actions
