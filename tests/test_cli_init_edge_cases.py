from __future__ import annotations

import os
from pathlib import Path

from helpers import invoke_cli, plain_output


def test_init_rejects_file_path(runner, repo: Path) -> None:
    file_path = repo / "not-a-dir.txt"
    file_path.write_text("x\n", encoding="utf-8")

    result = invoke_cli(runner, ["init", "--path", str(file_path)])

    assert result.exit_code != 0
    assert result.exit_code == 2


def test_init_rejects_nonexistent_path(runner, repo: Path) -> None:
    missing = repo / "missing-repo"

    result = invoke_cli(runner, ["init", "--path", str(missing)])

    assert result.exit_code != 0
    assert result.exit_code == 2


def test_init_uses_cwd_when_no_path(runner, repo: Path) -> None:
    old_cwd = os.getcwd()
    try:
        os.chdir(repo)
        result = invoke_cli(runner, ["init"])

        assert result.exit_code == 0
        assert "Bootstrap complete." in plain_output(result)
    finally:
        os.chdir(old_cwd)


def test_init_does_not_overwrite_existing_ideas_readme(runner, repo: Path) -> None:
    ideas_readme = repo / "docs" / "ideas" / "README.md"
    ideas_readme.parent.mkdir(parents=True)
    ideas_readme.write_text("custom ideas\n", encoding="utf-8")

    result = invoke_cli(runner, ["init", "--path", str(repo)])

    assert result.exit_code == 0
    assert ideas_readme.read_text(encoding="utf-8") == "custom ideas\n"
    assert "already exists, skipped" in plain_output(result)
