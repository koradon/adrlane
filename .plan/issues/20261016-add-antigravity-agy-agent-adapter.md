---
title: Add Antigravity (agy) agent adapter
number: 43
labels:
- agents
assignees:
- koradon
state: open
state_reason: null
---

## Goal

Give Antigravity (the `agy` CLI, which replaced the retired Gemini CLI) the same
adrlane skills that `cursor`, `claude-code`, and `codex` already get, so every
supported agent harness has as-close-to-identical capabilities.

## Background

Antigravity discovers workspace skills only from
`<workspace>/.agents/skills/<name>/SKILL.md` and global skills only from
`~/.gemini/config/skills/<name>/SKILL.md`. It does not read `.claude/skills`,
`.cursor/skills`, or `.codex/skills`, so today adrlane's skills are invisible to it.

Unlike the codex adapter (ADR 0008), a single relative `skill_prefix` cannot serve
both scopes for Antigravity: the repo-local root (`.agents/skills`) and the global
root (`.gemini/config/skills`) are unrelated paths, not the same suffix under both
`cwd()` and `home()`.

## Tasks

- Add an `agy` entry to `AGENT_ADAPTERS` in `src/adrlane/agents/registry.py`,
  following the codex adapter precedent (PR #40, ADR 0008).
- Support a per-adapter global-scope skill prefix distinct from the local one.
- Wire `agy` through `adrlane init`, `adrlane upgrade`, `adrlane skills install`,
  `adrlane skills upgrade` (including default-agent-set behavior when `--agent` is
  omitted), and `adrlane doctor`.
- Update CLI help text, `README.md`, and `docs/architecture.md`.
- Add tests mirroring the codex adapter's test coverage.
- Record the scope-prefix decision in an ADR.
- Verify against the real `agy` CLI that installed skills actually load.

## Related

- PR precedent: `feat(agents): add codex adapter installing into .codex/skills` (#40)
- ADR: `docs/adr/0008-codex-adapter-installs-into-repo-local-dot-codex-skills.md`
