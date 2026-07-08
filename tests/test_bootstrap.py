from __future__ import annotations

from pathlib import Path

from adrlane import __version__
from adrlane.bootstrap import run_bootstrap

EXPECTED_DOC_FILES = [
    "docs/README.md",
    "docs/ideas/README.md",
    "docs/roadmap/README.md",
    "docs/llm/AGENT_PROTOCOL.md",
    "docs/llm/DECISION_RULES.md",
    "docs/llm/TEMPLATES.md",
    "docs/llm/DOC_GUIDELINES.md",
    "docs/llm/templates/acceptance.feature",
    "docs/llm/templates/idea.md",
    "docs/llm/templates/spec.md",
    "docs/llm/templates/plan.md",
    "docs/llm/templates/adr-light.md",
    "docs/llm/templates/adr-standard.md",
    "docs/llm/templates/adr-full.md",
    "docs/llm/templates/roadmap.md",
    "docs/llm/templates/runbook.md",
    "docs/llm/templates/reference.md",
]

EXPECTED_DOC_DIRS = [
    "docs/specs",
    "docs/plans",
    "docs/adr",
    "docs/ideas",
    "docs/roadmap",
]

BOOTSTRAP_ACTION_COUNT = 2 + len(EXPECTED_DOC_DIRS) + len(EXPECTED_DOC_FILES)


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
    assert bootstrap_marker.read_text(encoding="utf-8") == f"{__version__}\n"
