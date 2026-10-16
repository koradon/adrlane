---
title: Refresh adrlane and planhub agent skills for Antigravity
labels:
- agents
assignees:
- koradon
state: closed
number: 45
state_reason: completed
---

## Goal

Refresh this repository's agent scaffolding and skills to adrlane 0.5.2 and planhub 0.4.2 so that Antigravity (`agy`) and all supported harnesses (Claude Code, Cursor, Codex, and Antigravity) have identical skills.

## Context

adrlane 0.5.2 and planhub 0.4.2 both support Antigravity (`agy`), installing skills into `.agents/skills/<name>/SKILL.md`.

## Tasks

- Refresh adrlane scaffolding and contract files using `adrlane upgrade`.
- Refresh planhub skills using `planhub init`.
- Ensure `.agents/skills/planhub-plan-artifacts/SKILL.md` is present alongside adrlane skills.
- Verify `.adrlane/bootstrap-version` is updated to 0.5.2.
- Verify `adrlane doctor` passes.
