from __future__ import annotations

from pathlib import Path

from adrlane import __version__
from adrlane.bootstrap import run_bootstrap


def test_bootstrap_skips_existing_adrlane_directory(repo: Path) -> None:
    marker_dir = repo / ".adrlane"
    marker_dir.mkdir()

    result = run_bootstrap(repo)

    assert marker_dir in result.skipped
    assert marker_dir.is_dir()


def test_bootstrap_does_not_overwrite_existing_bootstrap_version(repo: Path) -> None:
    marker_dir = repo / ".adrlane"
    marker_dir.mkdir()
    marker_file = marker_dir / "bootstrap-version"
    marker_file.write_text("9.9.9\n", encoding="utf-8")

    result = run_bootstrap(repo)

    assert marker_file.read_text(encoding="utf-8") == "9.9.9\n"
    assert marker_file in result.skipped


def test_bootstrap_writes_current_version_when_marker_missing(repo: Path) -> None:
    run_bootstrap(repo)

    marker_file = repo / ".adrlane" / "bootstrap-version"
    assert marker_file.read_text(encoding="utf-8") == f"{__version__}\n"
