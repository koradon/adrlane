---
title: 'M1: CLI and Documentation Bootstrap'
id: adrlane-m1-cli-docs-bootstrap
description: Deliver CLI, docs bootstrap, pytest suite, packaging, CI, versioning,
  and PyPI release workflow.
state: open
number: 5
---

## Scope

- Build `adrlane` CLI with `init` as the primary command.
- Scaffold `docs/` folder structure and entry templates.
- Ship canonical `docs/llm/*` contract files for agent-agnostic documentation rules.
- Establish pytest-based test suite for CLI and bootstrap behavior.
- Set up Python packaging (PEP 621), versioning, CI, and PyPI publishing workflow.

## Acceptance Criteria

- `adrlane init` creates the full documentation tree and contract files in an empty repo.
- Re-running `init` is idempotent and does not destroy existing documentation content.
- Package installs globally and exposes the `adrlane` console entry point.
- Pytest suite covers core CLI and init behavior.
- CI runs tests on every push/PR.
- Versioning and PyPI release process are documented and repeatable.

## Issue Order

1. CLI init scaffold
2. Docs structure and `docs/llm` contract
3. Pytest test foundation
4. Packaging and versioning
5. CI pipeline
6. PyPI release workflow
