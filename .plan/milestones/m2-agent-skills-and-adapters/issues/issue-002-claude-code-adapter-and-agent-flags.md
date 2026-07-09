---
title: Implement Claude Code adapter and init --agent selection
id: adrlane-m2-issue-002
labels:
- m2
- claude-code
- cli
milestone: 6
state: closed
number: 16
state_reason: completed
---

## Goal

Support Claude Code and let users choose which agent adapters `init` installs.

## Tasks

- Implement Claude Code adapter using that tool's required file layout.
- Add repeatable `init --agent <name>` flag.
- Ensure idempotent adapter install when `init` is re-run.
