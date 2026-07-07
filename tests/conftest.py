from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from adrlane import __version__
from adrlane.bootstrap import run_bootstrap
from adrlane.cli.main import app


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    return tmp_path


@pytest.fixture
def bootstrap_marker(repo: Path) -> Path:
    return repo / ".adrlane" / "bootstrap-version"
