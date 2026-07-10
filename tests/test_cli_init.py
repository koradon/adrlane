from __future__ import annotations

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
    assert "--agent" in output
    assert "--path" not in output


def test_init_creates_bootstrap_files(runner, in_repo: Path) -> None:
    result = invoke_cli(runner, ["init"])

    assert result.exit_code == 0
    assert "Bootstrap complete." in plain_output(result)
    assert (in_repo / ".adrlane" / "bootstrap-version").read_text(encoding="utf-8") == (
        f"{__version__}\n"
    )


def test_init_dry_run_prints_plan_without_writing(runner, in_repo: Path) -> None:
    result = invoke_cli(runner, ["init", "--dry-run"])
    output = plain_output(result)

    assert result.exit_code == 0
    assert "Planned bootstrap actions:" in output
    assert "  + " in output
    assert not (in_repo / ".adrlane").exists()


def test_init_dry_run_lists_expected_paths(runner, in_repo: Path) -> None:
    result = invoke_cli(runner, ["init", "--dry-run"])
    output = plain_output(result)

    assert str(in_repo / "docs" / "llm" / "AGENT_PROTOCOL.md") in output
    assert str(in_repo / "docs" / "llm" / "templates" / "acceptance.feature") in output


def test_init_is_idempotent(runner, in_repo: Path) -> None:
    first = invoke_cli(runner, ["init"])
    second = invoke_cli(runner, ["init"])

    assert first.exit_code == 0
    assert second.exit_code == 0
    assert "already exists, skipped" in plain_output(second)


def test_init_after_full_bootstrap_reports_only_skipped_paths(runner, in_repo: Path) -> None:
    first = invoke_cli(runner, ["init"])
    second = invoke_cli(runner, ["init"])
    output = plain_output(second)

    assert first.exit_code == 0
    assert second.exit_code == 0
    assert output.count("already exists, skipped") == BOOTSTRAP_ACTION_COUNT + AGENT_ACTION_COUNT
    assert "  + " not in output


def test_init_dry_run_with_partial_existing_marks_skipped_in_output(runner, in_repo: Path) -> None:
    readme = in_repo / "docs" / "README.md"
    readme.parent.mkdir(parents=True)
    readme.write_text("custom docs\n", encoding="utf-8")

    result = invoke_cli(runner, ["init", "--dry-run"])
    output = plain_output(result)

    assert result.exit_code == 0
    assert "already exists, skipped" in output
    assert str(in_repo / "docs" / "plans") in output


@pytest.mark.parametrize("relative_path", EXPECTED_DOC_FILES)
def test_init_does_not_overwrite_existing_template_files(
    runner,
    in_repo: Path,
    relative_path: str,
) -> None:
    target = in_repo / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("CUSTOM\n", encoding="utf-8")

    result = invoke_cli(runner, ["init"])

    assert result.exit_code == 0
    assert target.read_text(encoding="utf-8") == "CUSTOM\n"
    assert "already exists, skipped" in plain_output(result)
