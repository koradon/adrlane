from __future__ import annotations

import os
from pathlib import Path

import pytest
from agent_expectations import AGENT_ACTION_COUNT
from bootstrap_expectations import BOOTSTRAP_ACTION_COUNT, EXPECTED_DOC_FILES
from helpers import invoke_cli, plain_output

from adrlane import __version__


def test_adrlane_help_lists_init_command(runner) -> None:
    result = invoke_cli(runner, ["--help"])
    output = plain_output(result)

    assert result.exit_code == 0
    assert "init" in output


def test_adrlane_without_subcommand_shows_help(runner) -> None:
    result = invoke_cli(runner, [])

    assert result.exit_code == 2


def test_init_help(runner) -> None:
    result = invoke_cli(runner, ["init", "--help"])
    output = plain_output(result)

    assert result.exit_code == 0
    assert "--dry-run" in output
    assert "--path" in output


def test_init_creates_bootstrap_files(runner, repo: Path) -> None:
    result = invoke_cli(runner, ["init", "--path", str(repo)])

    assert result.exit_code == 0
    assert "Bootstrap complete." in plain_output(result)
    assert (repo / ".adrlane" / "bootstrap-version").read_text(encoding="utf-8") == (
        f"{__version__}\n"
    )


def test_init_short_path_option(runner, repo: Path) -> None:
    result = invoke_cli(runner, ["init", "-p", str(repo)])

    assert result.exit_code == 0
    assert (repo / "docs" / "README.md").is_file()


def test_init_dry_run_prints_plan_without_writing(runner, repo: Path) -> None:
    result = invoke_cli(runner, ["init", "--path", str(repo), "--dry-run"])
    output = plain_output(result)

    assert result.exit_code == 0
    assert "Planned bootstrap actions:" in output
    assert "  + " in output
    assert not (repo / ".adrlane").exists()


def test_init_dry_run_lists_expected_paths(runner, repo: Path) -> None:
    result = invoke_cli(runner, ["init", "--path", str(repo), "--dry-run"])
    output = plain_output(result)

    assert str(repo / "docs" / "llm" / "AGENT_PROTOCOL.md") in output
    assert str(repo / "docs" / "llm" / "templates" / "acceptance.feature") in output


def test_init_is_idempotent(runner, repo: Path) -> None:
    first = invoke_cli(runner, ["init", "--path", str(repo)])
    second = invoke_cli(runner, ["init", "--path", str(repo)])

    assert first.exit_code == 0
    assert second.exit_code == 0
    assert "already exists, skipped" in plain_output(second)


def test_init_after_full_bootstrap_reports_only_skipped_paths(runner, repo: Path) -> None:
    first = invoke_cli(runner, ["init", "--path", str(repo)])
    second = invoke_cli(runner, ["init", "--path", str(repo)])
    output = plain_output(second)

    assert first.exit_code == 0
    assert second.exit_code == 0
    assert output.count("already exists, skipped") == BOOTSTRAP_ACTION_COUNT + AGENT_ACTION_COUNT
    assert "  + " not in output


def test_init_rejects_file_path(runner, repo: Path) -> None:
    file_path = repo / "not-a-dir.txt"
    file_path.write_text("x\n", encoding="utf-8")

    result = invoke_cli(runner, ["init", "--path", str(file_path)])

    assert result.exit_code == 2


def test_init_rejects_nonexistent_path(runner, repo: Path) -> None:
    missing = repo / "missing-repo"

    result = invoke_cli(runner, ["init", "--path", str(missing)])

    assert result.exit_code == 2


def test_init_uses_cwd_when_no_path(runner, repo: Path) -> None:
    old_cwd = os.getcwd()
    try:
        os.chdir(repo)
        result = invoke_cli(runner, ["init"])
    finally:
        os.chdir(old_cwd)

    assert result.exit_code == 0
    assert (repo / "docs" / "README.md").is_file()


def test_init_dry_run_with_partial_existing_marks_skipped_in_output(runner, repo: Path) -> None:
    readme = repo / "docs" / "README.md"
    readme.parent.mkdir(parents=True)
    readme.write_text("custom docs\n", encoding="utf-8")

    result = invoke_cli(runner, ["init", "--path", str(repo), "--dry-run"])
    output = plain_output(result)

    assert result.exit_code == 0
    assert "already exists, skipped" in output
    assert str(repo / "docs" / "plans") in output


@pytest.mark.parametrize("relative_path", EXPECTED_DOC_FILES)
def test_init_does_not_overwrite_existing_template_files(
    runner,
    repo: Path,
    relative_path: str,
) -> None:
    target = repo / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("CUSTOM\n", encoding="utf-8")

    result = invoke_cli(runner, ["init", "--path", str(repo)])

    assert result.exit_code == 0
    assert target.read_text(encoding="utf-8") == "CUSTOM\n"
    assert "already exists, skipped" in plain_output(result)
