from __future__ import annotations

from pathlib import Path

from agent_expectations import SKILLS_PER_AGENT, agent_skill_path, agent_skill_paths

from adrlane.agents.skills import (
    SkillsScope,
    is_adrlane_repository,
    resolve_skills_target,
    run_skills,
)
from adrlane.bootstrap import run_bootstrap


def test_is_adrlane_repository_accepts_bootstrap_marker(repo: Path) -> None:
    (repo / ".adrlane").mkdir()

    assert is_adrlane_repository(repo)


def test_is_adrlane_repository_accepts_agent_protocol(repo: Path) -> None:
    protocol = repo / "docs" / "llm" / "AGENT_PROTOCOL.md"
    protocol.parent.mkdir(parents=True)
    protocol.write_text("# Agent Protocol\n", encoding="utf-8")

    assert is_adrlane_repository(repo)


def test_is_adrlane_repository_rejects_empty_directory(repo: Path) -> None:
    assert not is_adrlane_repository(repo)


def test_resolve_skills_target_local_uses_current_directory(repo: Path, monkeypatch) -> None:
    monkeypatch.chdir(repo)

    assert resolve_skills_target(SkillsScope.LOCAL) == repo.resolve()


def test_resolve_skills_target_global_uses_home(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    assert resolve_skills_target(SkillsScope.GLOBAL) == tmp_path


def test_run_skills_install_creates_local_skills(repo: Path) -> None:
    run_bootstrap(repo)

    result = run_skills(repo, ("cursor",), upgrade=False)

    assert len(result.created) == SKILLS_PER_AGENT
    assert result.skipped == []
    assert result.updated == []
    assert (repo / agent_skill_path("cursor", "adrlane-dev-context")).is_file()


def test_run_skills_install_skips_existing_local_skills(repo: Path) -> None:
    run_bootstrap(repo, agents=("cursor",))
    skill_path = repo / agent_skill_path("cursor", "adrlane-dev-context")
    original = skill_path.read_text(encoding="utf-8")

    result = run_skills(repo, ("cursor",), upgrade=False)

    assert result.created == []
    assert len(result.skipped) == SKILLS_PER_AGENT
    assert skill_path.read_text(encoding="utf-8") == original


def test_run_skills_upgrade_overwrites_existing_local_skills(repo: Path) -> None:
    run_bootstrap(repo, agents=("cursor",))
    skill_path = repo / agent_skill_path("cursor", "adrlane-write-adr")
    skill_path.write_text("stale skill\n", encoding="utf-8")

    result = run_skills(repo, ("cursor",), upgrade=True)

    assert result.created == []
    assert len(result.updated) == SKILLS_PER_AGENT
    assert "docs/llm/templates/adr-standard.md" in skill_path.read_text(encoding="utf-8")


def test_run_skills_upgrade_creates_missing_local_skills(repo: Path) -> None:
    run_bootstrap(repo)

    result = run_skills(repo, ("cursor",), upgrade=True)

    assert len(result.created) == SKILLS_PER_AGENT
    assert result.updated == []


def test_run_skills_install_writes_global_skills(tmp_path: Path) -> None:
    result = run_skills(tmp_path, ("claude-code",), upgrade=False)

    assert len(result.created) == SKILLS_PER_AGENT
    for relative_path in agent_skill_paths("claude-code"):
        assert (tmp_path / relative_path).is_file()


def test_run_skills_upgrade_dry_run_does_not_write(repo: Path) -> None:
    run_bootstrap(repo, agents=("cursor",))
    skill_path = repo / agent_skill_path("cursor", "adrlane-dev-context")
    skill_path.write_text("custom\n", encoding="utf-8")

    result = run_skills(repo, ("cursor",), upgrade=True, dry_run=True)

    assert len(result.updated) == SKILLS_PER_AGENT
    assert skill_path.read_text(encoding="utf-8") == "custom\n"
