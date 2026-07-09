from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from adrlane.bootstrap.actions import BootstrapAction
from adrlane.bootstrap.plan import bootstrap_plan


@dataclass(frozen=True)
class BootstrapResult:
    created: list[Path]
    skipped: list[Path]


def run_bootstrap(
    target: Path,
    *,
    dry_run: bool = False,
    agents: tuple[str, ...] = (),
) -> BootstrapResult:
    root = target.resolve()
    created: list[Path] = []
    skipped: list[Path] = []

    for action in bootstrap_plan(root, agents=agents):
        outcome = _apply_action(action, dry_run=dry_run)
        if outcome == "created":
            created.append(action.path)
        elif outcome == "skipped":
            skipped.append(action.path)

    return BootstrapResult(created=created, skipped=skipped)


def _apply_action(action: BootstrapAction, *, dry_run: bool) -> str:
    if action.kind == "dir":
        if action.path.exists():
            return "skipped"
        if not dry_run:
            action.path.mkdir(parents=True, exist_ok=True)
        return "created"

    if action.kind == "file":
        if action.path.exists():
            return "skipped"
        if not dry_run:
            action.path.parent.mkdir(parents=True, exist_ok=True)
            action.path.write_text(action.content or "", encoding="utf-8")
        return "created"

    raise ValueError(f"unknown bootstrap action kind: {action.kind}")
