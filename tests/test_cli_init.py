from __future__ import annotations

from pathlib import Path

from adrlane import __version__
from helpers import invoke_cli, plain_output


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


def test_init_dry_run_prints_plan_without_writing(
    runner,
    repo: Path,
) -> None:
    result = invoke_cli(runner, ["init", "--path", str(repo), "--dry-run"])

    assert result.exit_code == 0
    assert "Planned bootstrap actions:" in plain_output(result)
    assert not (repo / ".adrlane").exists()


def test_init_is_idempotent(runner, repo: Path) -> None:
    first = invoke_cli(runner, ["init", "--path", str(repo)])
    second = invoke_cli(runner, ["init", "--path", str(repo)])

    assert first.exit_code == 0
    assert second.exit_code == 0
    assert "already exists, skipped" in plain_output(second)
