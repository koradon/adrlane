from __future__ import annotations

import re
from collections.abc import Sequence

from typer.testing import CliRunner, Result

from adrlane.cli.main import app

_ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*m")


def invoke_cli(runner: CliRunner, args: Sequence[str]) -> Result:
    """Invoke the CLI with colors disabled for stable CI output."""
    return runner.invoke(app, list(args), color=False)


def plain_output(result: Result) -> str:
    return _ANSI_ESCAPE.sub("", f"{result.stdout}{result.stderr}")
