from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from adrlane import __version__
from adrlane.agents.registry import AGENT_ADAPTERS, SUPPORTED_AGENTS
from adrlane.agents.skills import is_adrlane_repository
from adrlane.bootstrap.agents_loader import agent_bootstrap_actions
from adrlane.bootstrap.templates_loader import template_bootstrap_actions


@dataclass(frozen=True)
class DoctorCheck:
    name: str
    ok: bool
    detail: str = ""


@dataclass(frozen=True)
class DoctorReport:
    checks: list[DoctorCheck]

    @property
    def issues(self) -> list[DoctorCheck]:
        return [check for check in self.checks if not check.ok]


def run_doctor(target: Path) -> DoctorReport:
    """Report documentation and agent-adapter health without blocking.

    Read-only: never writes files. Findings point at `adrlane upgrade` (or,
    for user-owned seed files that upgrade never touches, manual recreation).
    """
    root = target.resolve()

    if not is_adrlane_repository(root):
        return DoctorReport(
            checks=[
                DoctorCheck(
                    name="adrlane repository",
                    ok=False,
                    detail="Not an adrlane repository. Run `adrlane init` first.",
                )
            ]
        )

    checks = [
        *_docs_layout_checks(root),
        _bootstrap_version_check(root),
        *_agent_adapter_checks(root),
    ]
    workspace_check = _workspace_config_check(root)
    if workspace_check is not None:
        checks.append(workspace_check)

    return DoctorReport(checks=checks)


_FRAMEWORK_DIR = ("docs", "llm")


def _docs_layout_checks(root: Path) -> list[DoctorCheck]:
    checks: list[DoctorCheck] = []

    for action in template_bootstrap_actions(root):
        relative = action.path.relative_to(root)
        if action.path.is_file():
            checks.append(DoctorCheck(name=str(relative), ok=True))
            continue

        if relative.parts[:2] == _FRAMEWORK_DIR:
            detail = f"{relative} is missing. Run `adrlane upgrade` to restore it."
        else:
            detail = (
                f"{relative} is missing. Recreate it manually "
                "(`adrlane upgrade` does not touch it)."
            )
        checks.append(DoctorCheck(name=str(relative), ok=False, detail=detail))

    return checks


def _bootstrap_version_check(root: Path) -> DoctorCheck:
    marker = root / ".adrlane" / "bootstrap-version"
    name = ".adrlane/bootstrap-version"

    if not marker.is_file():
        return DoctorCheck(
            name=name,
            ok=False,
            detail="Missing. Run `adrlane upgrade` to record the installed version.",
        )

    try:
        installed = marker.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeDecodeError) as exc:
        return DoctorCheck(
            name=name,
            ok=False,
            detail=f"Could not read {name}: {exc}",
        )

    if installed != __version__:
        return DoctorCheck(
            name=name,
            ok=False,
            detail=f"Recorded version {installed} does not match installed adrlane {__version__}. "
            "Run `adrlane upgrade`.",
        )

    return DoctorCheck(name=name, ok=True)


def _agent_adapter_checks(root: Path) -> list[DoctorCheck]:
    checks: list[DoctorCheck] = []
    any_installed = False

    for agent_name in SUPPORTED_AGENTS:
        adapter = AGENT_ADAPTERS[agent_name]
        if not (root / adapter.skill_prefix).is_dir():
            continue
        any_installed = True

        for action in agent_bootstrap_actions(root, (agent_name,)):
            relative = action.path.relative_to(root)
            if not action.path.is_file():
                checks.append(
                    DoctorCheck(
                        name=str(relative),
                        ok=False,
                        detail=(
                            f"Missing. Run `adrlane upgrade --agent {agent_name}` to restore it."
                        ),
                    )
                )
            else:
                try:
                    current_content = action.path.read_text(encoding="utf-8")
                except (OSError, UnicodeDecodeError) as exc:
                    checks.append(
                        DoctorCheck(
                            name=str(relative),
                            ok=False,
                            detail=f"Could not read {relative}: {exc}",
                        )
                    )
                    continue

                if current_content != action.content:
                    checks.append(
                        DoctorCheck(
                            name=str(relative),
                            ok=False,
                            detail=(
                                f"Outdated. Run `adrlane upgrade --agent {agent_name}` "
                                "to refresh it."
                            ),
                        )
                    )
                else:
                    checks.append(DoctorCheck(name=str(relative), ok=True))

    if not any_installed:
        checks.append(
            DoctorCheck(
                name="agent adapters",
                ok=True,
                detail="No agent adapters installed. Run `adrlane init` to add one.",
            )
        )

    return checks


def _workspace_config_check(root: Path) -> DoctorCheck | None:
    workspace_path = root / ".adrlane" / "workspace.yaml"
    if not workspace_path.is_file():
        return None

    name = ".adrlane/workspace.yaml"
    try:
        content = workspace_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return DoctorCheck(
            name=name,
            ok=False,
            detail=f"Could not read {name}: {exc}",
        )

    if not content.strip():
        return DoctorCheck(
            name=name,
            ok=False,
            detail=(
                "Workspace config is empty. Add `project_docs` "
                "(and optional `repo_roots`) or remove the file."
            ),
        )

    return DoctorCheck(name=name, ok=True)
