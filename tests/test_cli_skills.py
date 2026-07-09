from __future__ import annotations

from pathlib import Path

from agent_expectations import agent_skill_path, agent_skill_paths
from helpers import invoke_cli, plain_output

from adrlane.bootstrap import run_bootstrap


def test_skills_help_lists_install_and_upgrade(runner) -> None:
    result = invoke_cli(runner, ["skills", "--help"])
    output = plain_output(result)

    assert result.exit_code == 0
    assert "install" in output
    assert "upgrade" in output


def test_skills_install_requires_scope_flag(runner) -> None:
    result = invoke_cli(runner, ["skills", "install"])

    assert result.exit_code == 2
    assert "exactly one of --local or --global" in plain_output(result)


def test_skills_install_local_requires_adrlane_repository(runner, repo: Path, monkeypatch) -> None:
    monkeypatch.chdir(repo)

    result = invoke_cli(runner, ["skills", "install", "--local"])

    assert result.exit_code == 2
    assert "not an adrlane repository" in plain_output(result)


def test_skills_install_local_creates_skills(runner, repo: Path, monkeypatch) -> None:
    monkeypatch.chdir(repo)
    (repo / ".adrlane").mkdir()

    result = invoke_cli(runner, ["skills", "install", "--local", "--agent", "cursor"])

    assert result.exit_code == 0
    for relative_path in agent_skill_paths("cursor"):
        assert (repo / relative_path).is_file()


def test_skills_install_global_writes_to_home(runner, tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    result = invoke_cli(runner, ["skills", "install", "--global", "--agent", "cursor"])

    assert result.exit_code == 0
    assert (tmp_path / agent_skill_path("cursor", "adrlane-dev-context")).is_file()


def test_skills_upgrade_local_overwrites_existing_skill(runner, repo: Path, monkeypatch) -> None:
    monkeypatch.chdir(repo)
    run_bootstrap(repo, agents=("cursor",))
    skill_path = repo / agent_skill_path("cursor", "adrlane-write-spec")
    skill_path.write_text("stale\n", encoding="utf-8")

    result = invoke_cli(runner, ["skills", "upgrade", "--local", "--agent", "cursor"])

    assert result.exit_code == 0
    assert "updated" in plain_output(result)
    assert "acceptance.feature" in skill_path.read_text(encoding="utf-8")


def test_skills_upgrade_global_dry_run_lists_updates(
    runner,
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    skill_path = tmp_path / agent_skill_path("claude-code", "adrlane-dev-context")
    skill_path.parent.mkdir(parents=True)
    skill_path.write_text("stale\n", encoding="utf-8")

    result = invoke_cli(
        runner, ["skills", "upgrade", "--global", "--agent", "claude-code", "--dry-run"]
    )

    assert result.exit_code == 0
    output = plain_output(result)
    assert "Planned skills upgrade" in output
    assert str(skill_path) in output
    assert skill_path.read_text(encoding="utf-8") == "stale\n"


def test_skills_install_rejects_unknown_agent(runner, tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    result = invoke_cli(runner, ["skills", "install", "--global", "--agent", "opencode"])

    assert result.exit_code == 2
