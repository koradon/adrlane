from __future__ import annotations

from pathlib import Path

from adrlane import __version__
from adrlane.bootstrap import run_bootstrap


def test_bootstrap_creates_marker_files(repo: Path, bootstrap_marker: Path) -> None:
    result = run_bootstrap(repo)

    assert (repo / ".adrlane").is_dir()
    assert bootstrap_marker.is_file()
    assert bootstrap_marker.read_text(encoding="utf-8") == f"{__version__}\n"
    assert len(result.created) == 2
    assert result.skipped == []


def test_bootstrap_dry_run_does_not_write_files(repo: Path, bootstrap_marker: Path) -> None:
    result = run_bootstrap(repo, dry_run=True)

    assert not (repo / ".adrlane").exists()
    assert not bootstrap_marker.exists()
    assert len(result.created) == 2
    assert result.skipped == []


def test_bootstrap_is_idempotent(repo: Path, bootstrap_marker: Path) -> None:
    first = run_bootstrap(repo)
    second = run_bootstrap(repo)

    assert len(first.created) == 2
    assert first.skipped == []
    assert second.created == []
    assert len(second.skipped) == 2
    assert bootstrap_marker.read_text(encoding="utf-8") == f"{__version__}\n"
