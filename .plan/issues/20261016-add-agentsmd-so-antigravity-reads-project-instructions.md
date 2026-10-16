---
title: Add AGENTS.md so Antigravity reads project instructions
number: 47
state: open
assignees:
- koradon
state_reason: null
---

## Goal

Add an `AGENTS.md` to this repository so that Antigravity (the `agy` CLI) and other AGENTS.md-reading agents work with project instructions instead of none.

## Context

Antigravity reads project instructions only from `AGENTS.md` or `GEMINI.md`, never from `CLAUDE.md`. This repository had no `AGENTS.md`, so an `agy` worker here previously had no project rules at all.

## Tasks

- Create `AGENTS.md` using the firstmate convention (`fm-ensure-agents-md.sh`) with `CLAUDE.md` as a two-line `@AGENTS.md` pointer.
- Document verified project facts only: what the project is, install/test/lint commands (taken from CI and run to confirm), and pointers to `docs/llm/AGENT_PROTOCOL.md` and `.plan/`.
