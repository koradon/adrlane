---
title: Configure Python packaging and versioning strategy
id: adrlane-m1-issue-004
labels:
- m1
- packaging
- versioning
milestone: 'M1: CLI and Documentation Bootstrap'
state: open
number: 9
state_reason: null
---

## Goal

Make `adrlane` installable as a proper Python package with a clear versioning scheme.

## Tasks

- Add `pyproject.toml` with PEP 621 metadata and console entry point (`adrlane`).
- Define versioning approach (e.g. semver, single source of truth for `__version__`).
- Configure build backend (e.g. hatchling or setuptools) and verify local `pip install -e .` works.
- Document global install path (`pipx install adrlane`).

## Depends On

- issue-001 (CLI init scaffold)
