from __future__ import annotations

from pathlib import Path

import pytest

from adrlane.bootstrap.actions import BootstrapAction


def test_bootstrap_action_describe_directory() -> None:
    action = BootstrapAction(path=Path("/repo/docs/specs"), kind="dir")

    assert action.describe() == "create directory: /repo/docs/specs"


def test_bootstrap_action_describe_file() -> None:
    action = BootstrapAction(
        path=Path("/repo/docs/README.md"),
        kind="file",
        content="# Docs\n",
    )

    assert action.describe() == "create file: /repo/docs/README.md"


def test_bootstrap_action_describe_unknown_kind_raises() -> None:
    action = BootstrapAction(path=Path("/repo/x"), kind="unknown")

    with pytest.raises(ValueError, match="unknown bootstrap action kind"):
        action.describe()
