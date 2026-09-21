# Architecture overview skill

## Status

accepted

## Summary

`adrlane init` installs a 7th packaged skill, `adrlane-write-architecture-overview`, alongside the existing six. It lets an agent create or refresh a single whole-system overview document, `docs/architecture.md`, in **any** repository bootstrapped with `adrlane` — not just this one. Until now, producing that kind of document was something an agent had to improvise from scratch each time; this makes it a repeatable, packaged capability like the other `adrlane-write-*` skills.

## User stories

- As a developer opening an unfamiliar adrlane-bootstrapped repo, I want to ask my agent to explain the architecture and get a consistent, complete document back, so that I don't depend on the agent improvising a different structure every time.
- As an agent working in a bootstrapped repo, I want a documented convention for *where* the architecture overview lives and *how* to refresh it, so I don't have to guess the file name or rewrite the whole thing on every change.
- As a maintainer of `adrlane` itself, I want adding this capability to require no new CLI code, so it stays consistent with how every other skill is packaged and installed.

## Requirements

- A new packaged skill directory: `src/adrlane/bootstrap/templates/agents/skills/adrlane-write-architecture-overview/SKILL.md`. `bootstrap/agents_loader.py` already installs every subfolder under `templates/agents/skills/` automatically, for every agent adapter (`cursor`, `claude-code`) — no change to `agents/registry.py`, `bootstrap/plan.py`, or the CLI was needed.
- A new packaged starter template: `docs/llm/templates/architecture.md`, following the same "framework file" convention as the other templates under `docs/llm/templates/` (created by `init`, refreshed by `upgrade`).
- The output file is always `docs/architecture.md` — a single, fixed-name, top-level file. Not a folder, not date-prefixed, not an instance of the existing generic "Reference" doc type (`docs/reference/`): an architecture overview is one canonical document per repository, not one of many growing topic pages.
- `docs/llm/DECISION_RULES.md`, `docs/llm/AGENT_PROTOCOL.md`, and `docs/llm/TEMPLATES.md` document the new type (when to create/refresh it, its location, its template, and its `current` / `stale` status values), matching how Idea/Spec/Plan/ADR/Roadmap are already documented.
- Trigger model: **on-demand and proactive**. A developer or agent can ask directly ("generate an architecture overview", "explain this codebase"). `adrlane-dev-context` also proposes refreshing it after a change that alters module boundaries, execution flow, or requirements to run — the same moment it already proposes an ADR.
- Refresh semantics: when `docs/architecture.md` already exists, the skill patches only the sections that are stale. It never does a full rewrite of an existing file as its default behavior.
- The skill must generate as many Mermaid diagrams as the target project actually needs to be well visualized (module map, data/request flow, deployment topology, etc.) — no fixed count, and no diagram added just to have one.
- The skill's instructions must stay tech-stack agnostic: they describe *what to investigate* (entry points, manifest/lockfile, module boundaries) rather than assuming any specific language or framework, since `adrlane` bootstraps projects of any stack.
- The skill adds a row for `docs/architecture.md` to `docs/README.md`'s structure table the first time it creates the file, per the existing "extending the documentation tree" convention.

## Behavior

1. Agent triggers the skill (asked directly, or proactively after a qualifying change).
2. Skill reads `docs/llm/DECISION_RULES.md` (Architecture overview section) and `docs/llm/AGENT_PROTOCOL.md`.
3. If `docs/architecture.md` does not exist: copy `docs/llm/templates/architecture.md`, then fill it in from the actual project (not assumptions).
4. If `docs/architecture.md` already exists: re-read it, identify which sections no longer match the code, and patch only those.
5. Cover at minimum: purpose, requirements to run, execution flow, subsystems, data/storage model, modes/entry points, design principles — plus as many diagrams as needed.
6. Use `## Status` (`current` / `stale`) and `## Related` sections; no YAML frontmatter, consistent with every other adrlane doc type.
7. On first creation only, add a row to `docs/README.md`.

## Acceptance scenarios (BDD)

No Gherkin feature file — this spec describes agent-guided document generation, not a deterministic system behavior with fixed inputs/outputs. Acceptance evidence instead comes from:

- `tests/agent_expectations.py` — `AGENT_SKILL_NAMES` includes `adrlane-write-architecture-overview`; existing parametrized tests (`test_agents.py`, `test_cli_init_agents.py`, `test_cli_skills.py`, `test_cli_upgrade.py`, `test_cli_doctor.py`) verify it installs, upgrades, and reports correctly for both agent adapters, for free, since they iterate this list.
- `tests/bootstrap_expectations.py` — `EXPECTED_DOC_FILES` includes `docs/llm/templates/architecture.md`; existing bootstrap/upgrade/doctor tests verify it is created, non-empty, and refreshed like every other framework template.

## Related

- Spec: `docs/specs/20260707-adrlane-design.md`
- Doc: `docs/architecture.md` (the document type this spec defines, dogfooded in this repo)
- ADR: `docs/adr/0002-agent-agnostic-contract-with-thin-adapters.md` (why skills are thin, packaged adapters)
- ADR: `docs/adr/0005-dedicated-upgrade-command-for-package-owned-content.md` (why templates refresh via `upgrade`, not `init`)

## Open Questions

- None outstanding — scope, naming, trigger model, refresh semantics, and diagram requirement were settled during planning before implementation.
