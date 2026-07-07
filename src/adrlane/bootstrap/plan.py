from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from adrlane import __version__


@dataclass(frozen=True)
class BootstrapAction:
    path: Path
    kind: str
    content: str | None = None

    def describe(self) -> str:
        if self.kind == "dir":
            return f"create directory: {self.path}"
        if self.kind == "file":
            return f"create file: {self.path}"
        raise ValueError(f"unknown bootstrap action kind: {self.kind}")


def bootstrap_plan(target: Path) -> list[BootstrapAction]:
    """Return bootstrap actions for a repository root.

    Docs and agent contract files are added in a follow-up issue; this
    establishes the bootstrap marker and directory layout hook.
    """
    return [
        BootstrapAction(path=target / ".adrlane", kind="dir"),
        BootstrapAction(
            path=target / ".adrlane" / "bootstrap-version",
            kind="file",
            content=f"{__version__}\n",
        ),
    ]
