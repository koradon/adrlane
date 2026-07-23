from __future__ import annotations

from pathlib import Path

from agent_expectations import agent_skill_path
from helpers import invoke_cli, plain_output

from adrlane import __version__
from adrlane.bootstrap import run_bootstrap


def test_doctor_requires_adrlane_repository(runner, repo: Path, monkeypatch) -> None:
    monkeypatch.chdir(repo)

    result = invoke_cli(runner, ["doctor"])
    output = plain_output(result)

    assert result.exit_code == 0
    assert "not an adrlane repository" in output.lower()


def test_doctor_reports_no_issues_on_healthy_repo(runner, repo: Path, monkeypatch) -> None:
    monkeypatch.chdir(repo)
    run_bootstrap(repo, agents=("cursor",))

    result = invoke_cli(runner, ["doctor"])
    output = plain_output(result)

    assert result.exit_code == 0
    assert "No issues found." in output


def test_doctor_flags_stale_framework_file(runner, repo: Path, monkeypatch) -> None:
    monkeypatch.chdir(repo)
    run_bootstrap(repo, agents=("cursor",))
    protocol_path = repo / "docs" / "llm" / "AGENT_PROTOCOL.md"
    protocol_path.unlink()

    result = invoke_cli(runner, ["doctor"])
    output = plain_output(result)

    assert result.exit_code == 0
    assert "docs/llm/AGENT_PROTOCOL.md" in output
    assert "adrlane upgrade" in output
    assert "1 issue(s) found." in output


def test_doctor_flags_stale_bootstrap_version(runner, repo: Path, monkeypatch) -> None:
    monkeypatch.chdir(repo)
    run_bootstrap(repo, agents=("cursor",))
    marker_path = repo / ".adrlane" / "bootstrap-version"
    marker_path.write_text("0.0.1\n", encoding="utf-8")

    result = invoke_cli(runner, ["doctor"])
    output = plain_output(result)

    assert result.exit_code == 0
    assert f"Recorded version 0.0.1 does not match installed adrlane {__version__}" in output


def test_doctor_flags_outdated_agent_skill(runner, repo: Path, monkeypatch) -> None:
    monkeypatch.chdir(repo)
    run_bootstrap(repo, agents=("cursor",))
    skill_path = repo / agent_skill_path("cursor", "adrlane-write-spec")
    skill_path.write_text("stale\n", encoding="utf-8")

    result = invoke_cli(runner, ["doctor"])
    output = plain_output(result)

    assert result.exit_code == 0
    assert agent_skill_path("cursor", "adrlane-write-spec") in output
    assert "Outdated" in output


def test_doctor_flags_missing_agent_skill(runner, repo: Path, monkeypatch) -> None:
    monkeypatch.chdir(repo)
    run_bootstrap(repo, agents=("cursor",))
    skill_path = repo / agent_skill_path("cursor", "adrlane-write-spec")
    skill_path.unlink()

    result = invoke_cli(runner, ["doctor"])
    output = plain_output(result)

    assert result.exit_code == 0
    assert agent_skill_path("cursor", "adrlane-write-spec") in output
    assert "Missing" in output


def test_doctor_does_not_flag_uninstalled_agent(runner, repo: Path, monkeypatch) -> None:
    monkeypatch.chdir(repo)
    run_bootstrap(repo, agents=("cursor",))

    result = invoke_cli(runner, ["doctor"])
    output = plain_output(result)

    assert result.exit_code == 0
    assert ".claude/skills" not in output
    assert "No agent adapters installed" not in output


def test_doctor_flags_empty_workspace_config(runner, repo: Path, monkeypatch) -> None:
    monkeypatch.chdir(repo)
    run_bootstrap(repo, agents=("cursor",), workspace=True)
    workspace_path = repo / ".adrlane" / "workspace.yaml"
    workspace_path.write_text("", encoding="utf-8")

    result = invoke_cli(runner, ["doctor"])
    output = plain_output(result)

    assert result.exit_code == 0
    assert ".adrlane/workspace.yaml" in output
    assert "empty" in output.lower()


def test_doctor_accepts_healthy_workspace_config(runner, repo: Path, monkeypatch) -> None:
    monkeypatch.chdir(repo)
    run_bootstrap(repo, agents=("cursor",), workspace=True)

    result = invoke_cli(runner, ["doctor"])
    output = plain_output(result)

    assert result.exit_code == 0
    assert "No issues found." in output
