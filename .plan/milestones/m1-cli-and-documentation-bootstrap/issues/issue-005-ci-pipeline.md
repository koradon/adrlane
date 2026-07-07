---
title: Add CI pipeline for lint and pytest
id: adrlane-m1-issue-005
labels:
- m1
- ci
- github-actions
milestone: 5
state: closed
number: 12
state_reason: completed
---

## Goal

Run automated checks on every push and pull request.

## Tasks

- Add GitHub Actions workflow for CI.
- Run pytest on supported Python versions.
- Add lint/format checks (ruff or equivalent) if adopted by the project.
- Fail CI on test or lint errors.

## Depends On

- issue-003 (pytest test foundation)
- issue-004 (packaging and versioning)
