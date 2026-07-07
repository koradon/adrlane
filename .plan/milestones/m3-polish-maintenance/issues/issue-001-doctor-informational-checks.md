---
title: Add informational doctor command
id: adrlane-m3-issue-001
labels:
- m3
- cli
- doctor
milestone: 'M3: Polish and Maintenance'
state: open
number: 17
state_reason: null
---

## Goal

Provide a non-blocking health check for documentation structure and agent adapters.

## Tasks

- Implement `adrlane doctor` as informational only.
- Verify expected `docs/` layout and `docs/llm/*` files exist.
- Report missing or outdated agent adapters.
