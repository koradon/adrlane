---
title: Add adrlane-write-architecture-overview skill
number: 35
state: closed
assignees: []
state_reason: completed
---

Adds a 7th packaged agent skill, `adrlane-write-architecture-overview`, so any repo bootstrapped
with `adrlane init` can create/refresh a single whole-system overview at `docs/architecture.md`
(previously something an agent had to improvise from scratch each time).

Key decisions:

- Fixed filename `docs/architecture.md`, not `docs/reference/*` and not date-prefixed.
- Trigger: on-demand or proactive, after changes to module boundaries/execution flow/requirements
  to run (same moment `adrlane-dev-context` already proposes an ADR).
- Refresh patches only stale sections, never a full rewrite by default.
- Includes as many Mermaid diagrams as the project needs — no fixed count.
- Tech-stack agnostic instructions (describes where to look, not language-specific commands).
- No CLI code change needed — `bootstrap/agents_loader.py` already auto-discovers every skill
  folder under `templates/agents/skills/`.

Done:

- New skill: `src/adrlane/bootstrap/templates/agents/skills/adrlane-write-architecture-overview/SKILL.md`
- New template: `docs/llm/templates/architecture.md`
- Updated `DECISION_RULES.md`, `AGENT_PROTOCOL.md`, `TEMPLATES.md`, `adrlane-dev-context`
- Updated `tests/agent_expectations.py` and `tests/bootstrap_expectations.py` (single source of
  truth for skill/template counts); `pytest` and `ruff` pass
- Dogfooded via `adrlane upgrade` in this repo; renamed `docs/architecture_overview.md` →
  `docs/architecture.md` with real diagrams
- Spec: `docs/specs/20260921-architecture-overview-skill.md`

Not yet done: changes are in the working tree, not committed/pushed to git.
