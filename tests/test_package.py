from __future__ import annotations

import re

import adrlane
from adrlane.bootstrap import bootstrap_plan, run_bootstrap


def test_package_exports_version() -> None:
    assert isinstance(adrlane.__version__, str)
    assert adrlane.__version__


def test_version_string_is_pep440_like() -> None:
    pattern = re.compile(r"^\d+\.\d+\.\d+([+.].*)?$")
    assert pattern.match(adrlane.__version__)


def test_bootstrap_public_api_exports() -> None:
    assert callable(bootstrap_plan)
    assert callable(run_bootstrap)
