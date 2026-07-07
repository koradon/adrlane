---
title: Set up PyPI release workflow
id: adrlane-m1-issue-006
labels:
- m1
- pypi
- release
milestone: 5
state: closed
number: 14
state_reason: completed
---

## Goal

Publish `adrlane` to PyPI with a repeatable, versioned release process.

## Tasks

- Configure build and publish steps (GitHub Actions release workflow or documented manual flow).
- Use PyPI trusted publishing or secure token-based auth.
- Tag releases aligned with the versioning strategy from issue-004.
- Verify `pipx install adrlane` works from PyPI after first release.

## Depends On

- issue-004 (packaging and versioning)
- issue-005 (CI pipeline)
