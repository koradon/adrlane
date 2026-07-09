from __future__ import annotations

from pathlib import Path

import pytest
from agent_expectations import (
    AGENT_ACTION_COUNT,
    AGENT_SKILL_FILES,
    AGENT_SKILL_NAMES,
    SKILLS_PER_AGENT,
    agent_skill_path,
    agent_skill_paths,
)

from adrlane.agents.registry import normalize_agent_selection, validate_agent_names
from adrlane.bootstrap import run_bootstrap
from adrlane.bootstrap.agents_loader import agent_bootstrap_actions


def test_normalize_agent_selection_defaults_to_all_supported_agents() -> None:
    assert normalize_agent_selection(None) == ("cursor", "claude-code")


def test_normalize_agent_selection_deduplicates_while_preserving_order() -> None:
    selected = normalize_agent_selection(["cursor", "claude-code", "cursor"])

    assert selected == ("cursor", "claude-code")


def test_validate_agent_names_rejects_unknown_agent() -> None:
    with pytest.raises(ValueError, match="Unknown agent\\(s\\): opencode"):
        validate_agent_names(["opencode"])


def test_agent_bootstrap_actions_installs_all_cursor_skills(repo: Path) -> None:
    actions = agent_bootstrap_actions(repo, ("cursor",))

    assert len(actions) == SKILLS_PER_AGENT
    paths = {action.path for action in actions}
    for skill_name in AGENT_SKILL_NAMES:
        assert repo / agent_skill_path("cursor", skill_name) in paths


def test_agent_bootstrap_actions_installs_both_agent_skills(repo: Path) -> None:
    actions = agent_bootstrap_actions(repo, ("cursor", "claude-code"))

    assert len(actions) == AGENT_ACTION_COUNT
    for agent in ("cursor", "claude-code"):
        for relative_path in agent_skill_paths(agent):
            assert repo / relative_path in {action.path for action in actions}


def test_run_bootstrap_without_agents_does_not_install_skills(repo: Path) -> None:
    run_bootstrap(repo)

    for agent in ("cursor", "claude-code"):
        for relative_path in agent_skill_paths(agent):
            assert not (repo / relative_path).exists()


def test_run_bootstrap_with_agents_installs_all_skills(repo: Path) -> None:
    run_bootstrap(repo, agents=("cursor", "claude-code"))

    ambient = (repo / agent_skill_path("cursor", "adrlane-dev-context")).read_text(encoding="utf-8")
    write_adr = (repo / agent_skill_path("claude-code", "adrlane-write-adr")).read_text(
        encoding="utf-8"
    )

    assert "docs/llm/DECISION_RULES.md" in ambient
    assert "docs/llm/templates/adr-standard.md" in write_adr


def test_run_bootstrap_agent_install_is_idempotent(repo: Path) -> None:
    run_bootstrap(repo)
    skill_path = repo / AGENT_SKILL_FILES["cursor"]
    first = run_bootstrap(repo, agents=("cursor",))
    second = run_bootstrap(repo, agents=("cursor",))

    assert skill_path in first.created
    assert second.created == []
    assert skill_path in second.skipped


def test_run_bootstrap_does_not_overwrite_existing_agent_skill(repo: Path) -> None:
    skill_path = repo / AGENT_SKILL_FILES["cursor"]
    skill_path.parent.mkdir(parents=True)
    skill_path.write_text("custom skill\n", encoding="utf-8")

    result = run_bootstrap(repo, agents=("cursor",))

    assert skill_path.read_text(encoding="utf-8") == "custom skill\n"
    assert skill_path in result.skipped
