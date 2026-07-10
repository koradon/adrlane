from __future__ import annotations

from pathlib import Path

import pytest
from agent_expectations import (
    AGENT_SKILL_FILES,
    AGENT_SKILL_NAMES,
    agent_skill_path,
    agent_skill_paths,
)
from helpers import invoke_cli, plain_output


def test_init_help_lists_agent_flag(runner) -> None:
    result = invoke_cli(runner, ["init", "--help"])
    output = plain_output(result)

    assert result.exit_code == 0
    assert "--agent" in output


def test_init_installs_all_agent_adapters_by_default(runner, in_repo: Path) -> None:
    result = invoke_cli(runner, ["init"])

    assert result.exit_code == 0
    for agent in ("cursor", "claude-code"):
        for relative_path in agent_skill_paths(agent):
            assert (in_repo / relative_path).is_file()


def test_init_installs_only_cursor_adapter_when_selected(runner, in_repo: Path) -> None:
    result = invoke_cli(runner, ["init", "--agent", "cursor"])

    assert result.exit_code == 0
    for relative_path in agent_skill_paths("cursor"):
        assert (in_repo / relative_path).is_file()
    assert not (in_repo / agent_skill_path("claude-code", AGENT_SKILL_NAMES[0])).exists()


def test_init_installs_only_claude_code_adapter_when_selected(runner, in_repo: Path) -> None:
    result = invoke_cli(runner, ["init", "--agent", "claude-code"])

    assert result.exit_code == 0
    for relative_path in agent_skill_paths("claude-code"):
        assert (in_repo / relative_path).is_file()
    assert not (in_repo / agent_skill_path("cursor", AGENT_SKILL_NAMES[0])).exists()


def test_init_supports_repeatable_agent_flag(runner, in_repo: Path) -> None:
    result = invoke_cli(
        runner,
        ["init", "--agent", "cursor", "--agent", "claude-code"],
    )

    assert result.exit_code == 0
    for agent in ("cursor", "claude-code"):
        for relative_path in agent_skill_paths(agent):
            assert (in_repo / relative_path).is_file()


def test_init_rejects_unknown_agent(runner, in_repo: Path) -> None:
    result = invoke_cli(runner, ["init", "--agent", "opencode"])

    assert result.exit_code == 2


def test_init_dry_run_lists_agent_adapter_paths(runner, in_repo: Path) -> None:
    result = invoke_cli(runner, ["init", "--dry-run"])
    output = plain_output(result)

    assert result.exit_code == 0
    assert str(in_repo / AGENT_SKILL_FILES["cursor"]) in output
    assert str(in_repo / agent_skill_path("claude-code", "adrlane-write-spec")) in output


def test_init_does_not_overwrite_existing_cursor_skill(runner, in_repo: Path) -> None:
    skill_path = in_repo / AGENT_SKILL_FILES["cursor"]
    skill_path.parent.mkdir(parents=True)
    skill_path.write_text("custom skill\n", encoding="utf-8")

    result = invoke_cli(runner, ["init", "--agent", "cursor"])

    assert result.exit_code == 0
    assert skill_path.read_text(encoding="utf-8") == "custom skill\n"
    assert "already exists, skipped" in plain_output(result)


@pytest.mark.parametrize("agent_name", ["cursor", "claude-code"])
def test_init_agent_skills_reference_docs_contract(
    runner,
    in_repo: Path,
    agent_name: str,
) -> None:
    result = invoke_cli(runner, ["init", "--agent", agent_name])

    assert result.exit_code == 0

    ambient = (in_repo / agent_skill_path(agent_name, "adrlane-dev-context")).read_text(
        encoding="utf-8"
    )
    write_spec = (in_repo / agent_skill_path(agent_name, "adrlane-write-spec")).read_text(
        encoding="utf-8"
    )

    assert "docs/llm/AGENT_PROTOCOL.md" in ambient
    assert "acceptance.feature" in write_spec
