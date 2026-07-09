---
title: Set up pytest test suite and first CLI tests
id: adrlane-m1-issue-003
labels:
- m1
- testing
- pytest
milestone: 5
state: closed
number: 11
state_reason: completed
---

## Goal

Establish pytest as the test framework and cover initial CLI and init behavior.

## Tasks

- Add pytest and test dependencies via uv dev group (`[dependency-groups].dev`).
- Create `tests/` layout and fixtures for invoking the CLI in isolated temp directories.
- Write first tests for `adrlane init` (success path, `--dry-run`, idempotent re-run).
- Wire `pytest` into local dev workflow and document how to run tests.

## Depends On

- issue-001 (CLI init scaffold)
