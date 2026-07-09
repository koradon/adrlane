---
title: Add skills install and upgrade CLI for global and local scopes
id: adrlane-m2-issue-003
labels:
- m2
- cli
- skills
milestone: 6
state: open
state_reason: null
number: 25
---

## Goal

Let users install and upgrade adrlane agent skills globally (once per machine) or locally (per repository) without re-running full `init`.

## Tasks

- Add `adrlane skills install --global` writing to `~/.cursor/skills/` and `~/.claude/skills/`.
- Add `adrlane skills install --local` writing to the current repository root (no `--path` flag).
- Add `adrlane skills upgrade --global` and `adrlane skills upgrade --local` to overwrite packaged skills.
- Support repeatable `--agent` flag and `--dry-run` on upgrade.
- Reject `--local` when the current directory is not an adrlane repository (`.adrlane/` or `docs/llm/AGENT_PROTOCOL.md`).
- `install` skips existing skill files; `upgrade` overwrites packaged skills and creates missing ones.
- Add tests for global/local install, upgrade overwrite, validation, and CLI integration.
