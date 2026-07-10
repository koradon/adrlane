from __future__ import annotations

from pathlib import Path

from agent_expectations import AGENT_ACTION_COUNT
from bootstrap_expectations import (
    BOOTSTRAP_ACTION_COUNT,
    EXPECTED_DOC_DIRS,
    EXPECTED_DOC_FILES,
)

from adrlane import __version__
from adrlane.bootstrap.plan import bootstrap_plan


def test_bootstrap_plan_returns_expected_action_count(repo: Path) -> None:
    actions = bootstrap_plan(repo)

    assert len(actions) == BOOTSTRAP_ACTION_COUNT


def test_bootstrap_plan_includes_agent_actions_when_requested(repo: Path) -> None:
    actions = bootstrap_plan(repo, agents=("cursor", "claude-code"))

    assert len(actions) == BOOTSTRAP_ACTION_COUNT + AGENT_ACTION_COUNT


def test_bootstrap_plan_starts_with_marker_directory_and_version_file(repo: Path) -> None:
    actions = bootstrap_plan(repo)

    assert actions[0].kind == "dir"
    assert actions[0].path == repo / ".adrlane"
    assert actions[1].kind == "file"
    assert actions[1].path == repo / ".adrlane" / "bootstrap-version"
    assert actions[1].content == f"{__version__}\n"


def test_bootstrap_plan_includes_all_documentation_directories(repo: Path) -> None:
    actions = bootstrap_plan(repo)
    dir_paths = {action.path for action in actions if action.kind == "dir"}

    for relative_path in EXPECTED_DOC_DIRS:
        assert repo / relative_path in dir_paths


def test_bootstrap_plan_includes_all_template_files(repo: Path) -> None:
    actions = bootstrap_plan(repo)
    file_paths = {action.path for action in actions if action.kind == "file"}

    for relative_path in EXPECTED_DOC_FILES:
        assert repo / relative_path in file_paths


def test_bootstrap_plan_has_no_duplicate_paths(repo: Path) -> None:
    actions = bootstrap_plan(repo)
    paths = [action.path for action in actions]

    assert len(paths) == len(set(paths))


def test_bootstrap_plan_template_files_have_content(repo: Path) -> None:
    actions = bootstrap_plan(repo)

    for action in actions:
        if action.kind != "file":
            continue
        if action.path.name == "bootstrap-version":
            continue
        assert action.content
        assert action.content.strip()


def test_bootstrap_plan_workspace_adds_workspace_config(repo: Path) -> None:
    from bootstrap_expectations import WORKSPACE_BOOTSTRAP_ACTION_COUNT

    from adrlane.bootstrap.plan import _WORKSPACE_CONFIG_TEMPLATE

    assert _WORKSPACE_CONFIG_TEMPLATE.is_file()

    actions = bootstrap_plan(repo, workspace=True)
    file_paths = {action.path for action in actions if action.kind == "file"}

    assert len(actions) == WORKSPACE_BOOTSTRAP_ACTION_COUNT
    assert repo / ".adrlane" / "workspace.yaml" in file_paths
