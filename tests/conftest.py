from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    return tmp_path


@pytest.fixture
def in_repo(repo: Path, monkeypatch) -> Path:
    monkeypatch.chdir(repo)
    return repo


@pytest.fixture
def bootstrap_marker(repo: Path) -> Path:
    return repo / ".adrlane" / "bootstrap-version"
