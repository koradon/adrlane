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
- Configure build backend (hatchling) and verify local `uv sync` + `uv run adrlane` works.
- Commit and maintain `uv.lock`.
- Document global install path (`uv tool install adrlane`).

## Depends On

- issue-001 (CLI init scaffold)
