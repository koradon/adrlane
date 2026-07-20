from __future__ import annotations

from pathlib import Path

from agent_expectations import agent_skill_path
from helpers import invoke_cli, plain_output

from adrlane import __version__
from adrlane.bootstrap import run_bootstrap


def test_upgrade_requires_adrlane_repository(runner, repo: Path, monkeypatch) -> None:
    monkeypatch.chdir(repo)

    result = invoke_cli(runner, ["upgrade"])

    assert result.exit_code == 2
    assert "not an adrlane repository" in plain_output(result)


def test_upgrade_overwrites_stale_framework_file(runner, repo: Path, monkeypatch) -> None:
    monkeypatch.chdir(repo)
    run_bootstrap(repo, agents=("cursor",))
    protocol_path = repo / "docs" / "llm" / "AGENT_PROTOCOL.md"
    protocol_path.write_text("stale\n", encoding="utf-8")

    result = invoke_cli(runner, ["upgrade", "--agent", "cursor"])

    assert result.exit_code == 0
    assert protocol_path.read_text(encoding="utf-8") != "stale\n"
    assert "updated" in plain_output(result)


def test_upgrade_rewrites_bootstrap_version(runner, repo: Path, monkeypatch) -> None:
    monkeypatch.chdir(repo)
    run_bootstrap(repo, agents=("cursor",))
    marker_path = repo / ".adrlane" / "bootstrap-version"
    marker_path.write_text("0.0.1\n", encoding="utf-8")

    invoke_cli(runner, ["upgrade", "--agent", "cursor"])

    assert marker_path.read_text(encoding="utf-8") == f"{__version__}\n"


def test_upgrade_overwrites_stale_skill_file(runner, repo: Path, monkeypatch) -> None:
    monkeypatch.chdir(repo)
    run_bootstrap(repo, agents=("cursor",))
    skill_path = repo / agent_skill_path("cursor", "adrlane-write-spec")
    skill_path.write_text("stale\n", encoding="utf-8")

    result = invoke_cli(runner, ["upgrade", "--agent", "cursor"])

    assert result.exit_code == 0
    assert skill_path.read_text(encoding="utf-8") != "stale\n"


def test_upgrade_does_not_touch_user_owned_docs(runner, repo: Path, monkeypatch) -> None:
    monkeypatch.chdir(repo)
    run_bootstrap(repo, agents=("cursor",))
    readme_path = repo / "docs" / "README.md"
    readme_path.write_text("my custom map\n", encoding="utf-8")
    spec_path = repo / "docs" / "specs" / "my-spec.md"
    spec_path.write_text("my spec\n", encoding="utf-8")

    invoke_cli(runner, ["upgrade", "--agent", "cursor"])

    assert readme_path.read_text(encoding="utf-8") == "my custom map\n"
    assert spec_path.read_text(encoding="utf-8") == "my spec\n"


def test_upgrade_does_not_touch_workspace_config(runner, repo: Path, monkeypatch) -> None:
    monkeypatch.chdir(repo)
    run_bootstrap(repo, agents=("cursor",), workspace=True)
    workspace_path = repo / ".adrlane" / "workspace.yaml"
    workspace_path.write_text("custom: true\n", encoding="utf-8")

    invoke_cli(runner, ["upgrade", "--agent", "cursor"])

    assert workspace_path.read_text(encoding="utf-8") == "custom: true\n"


def test_upgrade_dry_run_reports_without_writing(runner, repo: Path, monkeypatch) -> None:
    monkeypatch.chdir(repo)
    run_bootstrap(repo, agents=("cursor",))
    protocol_path = repo / "docs" / "llm" / "AGENT_PROTOCOL.md"
    protocol_path.write_text("stale\n", encoding="utf-8")

    result = invoke_cli(runner, ["upgrade", "--agent", "cursor", "--dry-run"])
    output = plain_output(result)

    assert result.exit_code == 0
    assert "Planned upgrade actions:" in output
    assert str(protocol_path) in output
    assert protocol_path.read_text(encoding="utf-8") == "stale\n"
