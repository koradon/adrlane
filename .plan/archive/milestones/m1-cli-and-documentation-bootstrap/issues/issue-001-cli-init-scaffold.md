---
title: Scaffold adrlane CLI with init command
id: adrlane-m1-issue-001
labels:
- m1
- cli
milestone: 5
state: closed
number: 10
state_reason: completed
---

## Goal

Create the first usable CLI surface for global install and per-repository bootstrap.

## Tasks

- Implement package entry point and `adrlane init` command.
- Support `--dry-run` to preview bootstrap output.
- Ensure idempotent behavior when `init` is re-run.
