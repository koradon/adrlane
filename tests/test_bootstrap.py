from __future__ import annotations

from pathlib import Path

import pytest
from bootstrap_expectations import (
    BOOTSTRAP_ACTION_COUNT,
    EXPECTED_DOC_DIRS,
    EXPECTED_DOC_FILES,
    REMOVED_LEGACY_PATHS,
)

from adrlane import __version__
from adrlane.bootstrap import bootstrap_plan, run_bootstrap


def test_bootstrap_creates_marker_and_docs(repo: Path, bootstrap_marker: Path) -> None:
    result = run_bootstrap(repo)

    assert (repo / ".adrlane").is_dir()
    assert bootstrap_marker.is_file()
    assert bootstrap_marker.read_text(encoding="utf-8") == f"{__version__}\n"

    for relative_path in EXPECTED_DOC_DIRS:
        assert (repo / relative_path).is_dir()

    for relative_path in EXPECTED_DOC_FILES:
        assert (repo / relative_path).is_file()

    assert len(result.created) == BOOTSTRAP_ACTION_COUNT
    assert result.skipped == []


def test_bootstrap_dry_run_does_not_write_files(repo: Path, bootstrap_marker: Path) -> None:
    result = run_bootstrap(repo, dry_run=True)

    assert not (repo / ".adrlane").exists()
    assert not bootstrap_marker.exists()
    assert not (repo / "docs").exists()
    assert len(result.created) == BOOTSTRAP_ACTION_COUNT
    assert result.skipped == []


def test_bootstrap_is_idempotent(repo: Path, bootstrap_marker: Path) -> None:
    first = run_bootstrap(repo)
    second = run_bootstrap(repo)

    assert len(first.created) == BOOTSTRAP_ACTION_COUNT
    assert first.skipped == []
    assert second.created == []
    assert len(second.skipped) == BOOTSTRAP_ACTION_COUNT


def test_bootstrap_creates_only_missing_files_on_second_partial_run(repo: Path) -> None:
    first = run_bootstrap(repo)
    custom_spec = repo / "docs" / "specs" / "custom.md"
    custom_spec.write_text("custom spec\n", encoding="utf-8")

    second = run_bootstrap(repo)

    assert len(first.created) == BOOTSTRAP_ACTION_COUNT
    assert second.created == []
    assert len(second.skipped) == BOOTSTRAP_ACTION_COUNT
    assert custom_spec.read_text(encoding="utf-8") == "custom spec\n"


def test_bootstrap_does_not_create_removed_legacy_paths(repo: Path) -> None:
    run_bootstrap(repo)

    for relative_path in REMOVED_LEGACY_PATHS:
        assert not (repo / relative_path).exists()


@pytest.mark.parametrize("relative_path", EXPECTED_DOC_DIRS)
def test_bootstrap_skips_existing_directories(repo: Path, relative_path: str) -> None:
    target = repo / relative_path
    target.mkdir(parents=True)

    result = run_bootstrap(repo)

    assert target in result.skipped
    assert target.is_dir()


@pytest.mark.parametrize("relative_path", EXPECTED_DOC_FILES)
def test_bootstrap_does_not_overwrite_existing_files(repo: Path, relative_path: str) -> None:
    target = repo / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("CUSTOM\n", encoding="utf-8")

    result = run_bootstrap(repo)

    assert target.read_text(encoding="utf-8") == "CUSTOM\n"
    assert target in result.skipped


def test_bootstrap_partial_existing_structure_creates_missing_only(repo: Path) -> None:
    existing = [
        repo / "docs" / "README.md",
        repo / "docs" / "specs",
        repo / "docs" / "llm" / "AGENT_PROTOCOL.md",
    ]
    for path in existing:
        if path.suffix:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("CUSTOM\n", encoding="utf-8")
        else:
            path.mkdir(parents=True)

    result = run_bootstrap(repo)

    assert len(result.created) == BOOTSTRAP_ACTION_COUNT - len(existing)
    assert len(result.skipped) == len(existing)
    assert (repo / "docs" / "README.md").read_text(encoding="utf-8") == "CUSTOM\n"
    assert (repo / "docs" / "plans").is_dir()
    assert (repo / "docs" / "llm" / "templates" / "acceptance.feature").is_file()


def test_bootstrap_dry_run_with_partial_existing_marks_skipped_paths(repo: Path) -> None:
    readme = repo / "docs" / "README.md"
    readme.parent.mkdir(parents=True)
    readme.write_text("CUSTOM\n", encoding="utf-8")

    result = run_bootstrap(repo, dry_run=True)

    assert readme in result.skipped
    assert not (repo / "docs" / "plans").exists()
    assert (repo / "docs" / "plans") in result.created


def test_bootstrap_written_files_are_non_empty(repo: Path) -> None:
    run_bootstrap(repo)

    for relative_path in EXPECTED_DOC_FILES:
        content = (repo / relative_path).read_text(encoding="utf-8")
        assert content.strip()


def test_bootstrap_contract_documents_idea_to_spec_to_plan_flow(repo: Path) -> None:
    run_bootstrap(repo)

    protocol = (repo / "docs" / "llm" / "AGENT_PROTOCOL.md").read_text(encoding="utf-8")
    templates = (repo / "docs" / "llm" / "TEMPLATES.md").read_text(encoding="utf-8")
    spec_template = (repo / "docs" / "llm" / "templates" / "spec.md").read_text(encoding="utf-8")
    acceptance_template = (repo / "docs" / "llm" / "templates" / "acceptance.feature").read_text(
        encoding="utf-8"
    )

    assert "Idea → spec → plan" in protocol
    assert "acceptance.feature" in templates
    assert "## User stories" in spec_template
    assert "Feature:" in acceptance_template


def test_bootstrap_plan_matches_executor_result_paths(repo: Path) -> None:
    planned_paths = {action.path for action in bootstrap_plan(repo)}
    result = run_bootstrap(repo)
    created_paths = set(result.created)

    assert planned_paths == created_paths
