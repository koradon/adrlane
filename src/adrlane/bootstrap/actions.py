from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


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
