from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from adrlane import __version__
from adrlane.cli.main import app


def test_init_help(runner: CliRunner) -> None:
    result = runner.invoke(app, ["init", "--help"])

    assert result.exit_code == 0
    assert "--dry-run" in result.stdout
    assert "--path" in result.stdout


def test_init_creates_bootstrap_files(runner: CliRunner, repo: Path) -> None:
    result = runner.invoke(app, ["init", "--path", str(repo)])

    assert result.exit_code == 0
    assert "Bootstrap complete." in result.stdout
    assert (repo / ".adrlane" / "bootstrap-version").read_text(encoding="utf-8") == (
        f"{__version__}\n"
    )


def test_init_dry_run_prints_plan_without_writing(
    runner: CliRunner,
    repo: Path,
) -> None:
    result = runner.invoke(app, ["init", "--path", str(repo), "--dry-run"])

    assert result.exit_code == 0
    assert "Planned bootstrap actions:" in result.stdout
    assert not (repo / ".adrlane").exists()


def test_init_is_idempotent(runner: CliRunner, repo: Path) -> None:
    first = runner.invoke(app, ["init", "--path", str(repo)])
    second = runner.invoke(app, ["init", "--path", str(repo)])

    assert first.exit_code == 0
    assert second.exit_code == 0
    assert "already exists, skipped" in second.stdout
