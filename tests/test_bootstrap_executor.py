from __future__ import annotations

from pathlib import Path

import pytest
from bootstrap_expectations import BOOTSTRAP_ACTION_COUNT

from adrlane.bootstrap.actions import BootstrapAction
from adrlane.bootstrap.executor import _apply_action, run_bootstrap


def test_apply_action_creates_directory(repo: Path) -> None:
    target = repo / "docs" / "specs"

    outcome = _apply_action(BootstrapAction(path=target, kind="dir"), dry_run=False)

    assert outcome == "created"
    assert target.is_dir()


def test_apply_action_skips_existing_directory(repo: Path) -> None:
    target = repo / "docs" / "specs"
    target.mkdir(parents=True)

    outcome = _apply_action(BootstrapAction(path=target, kind="dir"), dry_run=False)

    assert outcome == "skipped"


def test_apply_action_creates_file_with_content(repo: Path) -> None:
    target = repo / "docs" / "README.md"
    content = "custom readme\n"

    outcome = _apply_action(
        BootstrapAction(path=target, kind="file", content=content),
        dry_run=False,
    )

    assert outcome == "created"
    assert target.read_text(encoding="utf-8") == content


def test_apply_action_creates_empty_file_when_content_is_none(repo: Path) -> None:
    target = repo / "empty.md"

    outcome = _apply_action(
        BootstrapAction(path=target, kind="file", content=None),
        dry_run=False,
    )

    assert outcome == "created"
    assert target.read_text(encoding="utf-8") == ""


def test_apply_action_skips_existing_file(repo: Path) -> None:
    target = repo / "docs" / "README.md"
    target.parent.mkdir(parents=True)
    target.write_text("keep me\n", encoding="utf-8")

    outcome = _apply_action(
        BootstrapAction(path=target, kind="file", content="replace\n"),
        dry_run=False,
    )

    assert outcome == "skipped"
    assert target.read_text(encoding="utf-8") == "keep me\n"


def test_apply_action_dry_run_does_not_create_directory(repo: Path) -> None:
    target = repo / "docs" / "plans"

    outcome = _apply_action(BootstrapAction(path=target, kind="dir"), dry_run=True)

    assert outcome == "created"
    assert not target.exists()


def test_apply_action_dry_run_does_not_create_file(repo: Path) -> None:
    target = repo / "docs" / "README.md"

    outcome = _apply_action(
        BootstrapAction(path=target, kind="file", content="# Docs\n"),
        dry_run=True,
    )

    assert outcome == "created"
    assert not target.exists()


def test_apply_action_unknown_kind_raises(repo: Path) -> None:
    action = BootstrapAction(path=repo / "x", kind="bogus")

    with pytest.raises(ValueError, match="unknown bootstrap action kind"):
        _apply_action(action, dry_run=False)


def test_run_bootstrap_resolves_relative_target(repo: Path) -> None:
    import os

    nested = repo / "nested" / "project"
    nested.mkdir(parents=True)
    old_cwd = os.getcwd()
    try:
        os.chdir(repo)
        result = run_bootstrap(Path("nested/project"))
    finally:
        os.chdir(old_cwd)

    assert (nested / "docs" / "README.md").is_file()
    assert len(result.created) == BOOTSTRAP_ACTION_COUNT
