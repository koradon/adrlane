# Adrlane v1 Design Spec

**Status:** Draft  
**Owner:** Michal + Agent  
**Date:** 2026-07-07  
**Project Name:** `adrlane`  
**Package Target:** PyPI (`adrlane`)  
**Primary Runtime:** Local CLI (Python)

## 1. Problem Statement

Teams using AI coding agents often forget to keep project documentation current while coding.
Architecture decisions, runbooks, and implementation notes drift from real code changes.
Agents lack a shared map of where documentation lives, how it is structured, and how to update it consistently.

We need a local-first docs-as-code bootstrap tool that:

- scaffolds a predictable `/docs` structure in every repository,
- ships agent-facing instructions and skills so different agents work the same way,
- stays agent-agnostic (Cursor, Claude Code, OpenCode, and other LLM agents),
- leaves update decisions to the agent and developer — no automation pipeline, no enforcement.

## 2. Product Goals

### 2.1 Primary Goals

- Provide a globally installable CLI (`uv tool install adrlane` after PyPI release).
- Bootstrap repository documentation layout and templates via `adrlane init`.
- Install agent-specific skills/rules so agents know where to read and write documentation.
- Encode a universal, plain-Markdown documentation contract under `docs/llm/`.
- Keep all documentation inside the repository and reviewable via normal Git workflows.

### 2.2 Non-Goals (v1 and beyond)

- Automated documentation sync or rewrite pipelines.
- Policy engines, intent detection, or required-docs rules.
- Git hooks for docs gating or post-commit automation.
- LLM provider orchestration, routing, or auto-write execution.
- Blocking or warning gates on commits/CI.
- Full docs website generator.
- External SaaS dependency for core functionality.
- Complex multi-repo orchestration.

## 3. Target User (v1)

- Solo developer working locally in one repository.
- Uses one or more AI agents during coding.
- Wants agents to understand project documentation structure without manual onboarding each time.

## 4. High-Level Architecture

`adrlane` has three core subsystems:

1. **CLI Layer**  
   Entry point commands (`init`, optional `doctor`).

2. **Documentation Bootstrap**  
   Creates folder structure, templates, and canonical agent instructions in `docs/`.

3. **Agent Adapters**  
   Installs skills/rules for supported agents (e.g. Cursor, Claude Code) that point agents at the documentation contract.

## 5. Core UX and CLI

### 5.1 Commands

- `adrlane init`  
  Bootstrap `/docs` structure, templates, `docs/llm/*` contract files, and agent skills for selected agents.

- `adrlane init --agent <name>` (repeatable)  
  Limit or extend which agent adapters are installed (e.g. `cursor`, `claude-code`).

- `adrlane init --dry-run`  
  Show files and folders that would be created without writing them.

- `adrlane doctor` (optional, informational)  
  Check whether the repository has the expected documentation structure and agent adapters present.

### 5.2 Exit Behavior

- `0`: success
- `1`: runtime or validation failure

## 6. Installation and Distribution

### 6.1 Install

Development (project contributors):

```bash
uv sync
uv run adrlane init
```

Global install on a developer machine (local checkout or after PyPI release):

```bash
uv tool install adrlane
# or from a local checkout:
uv tool install -e .
```

### 6.2 Per-Repository Bootstrap

Inside a target repository:

```bash
adrlane init
```

`init` is idempotent: re-running should not destroy existing documentation content.

### 6.3 Packaging

- Python package built with modern PEP 621 metadata.
- `uv` as the package manager (`uv.lock`, `uv sync`, `uv run`).
- Console entry point: `adrlane`.
- Dev dependencies in `[dependency-groups].dev` (pytest).
- Agent skill templates ship inside the package and are copied into the repository on `init`.

## 7. Repository Contract (Docs-as-Code Standard)

`adrlane init` creates:

- `docs/README.md` — map of the documentation tree
- `docs/adr/` — architecture decision records
- `docs/specs/` — feature and API specifications
- `docs/runbooks/` — operational procedures
- `docs/changelog/` — release and change notes
- `docs/llm/AGENT_PROTOCOL.md` — how agents should read and update docs
- `docs/llm/DECISION_RULES.md` — when and why to create or update each doc type
- `docs/llm/TEMPLATES.md` — required sections and naming conventions
- `docs/llm/DOC_GUIDELINES.md` — style, metadata, and consistency guidelines

Plus agent adapter files for supported agents, for example:

- Cursor skills under `.cursor/skills/` (or project rules, depending on final format)
- Claude Code instructions under the path required by that tool

Exact adapter paths are defined per agent and may evolve independently of the core `docs/llm/` contract.

### 7.1 Universal LLM Contract

`docs/llm/AGENT_PROTOCOL.md` is the canonical, agent-agnostic source of truth. It defines:

- where each documentation type lives,
- how to search for existing context before writing,
- where to append or create new documentation,
- artifact naming conventions (ADR, spec, runbook),
- required metadata headers,
- update semantics (create vs append vs patch),
- conflict policy (never delete unrelated docs),
- language and style consistency rules.

Agent-specific skills/rules are adapters: they teach the agent how to find and follow `docs/llm/*`.

### 7.2 Agent Decision Model

The agent decides whether documentation needs updating during normal development work.
`adrlane` does not detect gaps, schedule updates, or write documentation on behalf of the user.

## 8. Agent Skills and Adapters

### 8.1 Purpose

Skills give each supported agent a project-local, tool-native entry point into the documentation system.
An agent skill should answer:

- where documentation lives in this repository,
- which file to read first,
- how to update ADRs, specs, runbooks, and changelog entries,
- which templates and guidelines to follow.

### 8.2 Supported Agents (v1 target)

Initial targets (subject to prioritization):

- Cursor
- Claude Code

Additional adapters (e.g. OpenCode) can follow the same pattern without changing the core contract.

### 8.3 Skill Content Strategy

- Canonical rules live in `docs/llm/*`.
- Agent skills are concise adapters that reference those files.
- Skills are copied/generated during `init`, not fetched from a remote service.

## 9. Developer Workflow

1. Install `adrlane` globally.
2. Run `adrlane init` in a repository.
3. Work with an agent as usual.
4. When the agent judges that documentation should be updated, it uses the installed skills and `docs/llm/*` contract to make consistent edits under `docs/`.
5. Developer reviews changes via `git diff` and commits normally.

## 10. v1 Milestones

### M1: CLI and Documentation Bootstrap

- CLI scaffolding (`init`, optional `doctor`).
- Documentation skeleton and `docs/llm/*` contract files.
- Templates for ADR, spec, runbook, and changelog entries.
- Pytest test suite for CLI and bootstrap behavior.
- Python packaging (PEP 621), versioning, CI pipeline, and PyPI release workflow.

### M2: Agent Skills and Adapters

- Cursor skill/rule adapter.
- Claude Code adapter.
- `init --agent` selection and idempotent install behavior.

### M3: Polish and Maintenance

- `doctor` informational checks.
- `init --dry-run` and refresh/migrate strategy for upgraded package versions.
- README and onboarding docs.

## 11. Acceptance Criteria (v1)

- User can install `adrlane` globally and run it from any repository.
- User can run `adrlane init` in an empty repo and get the full documentation contract and folder structure.
- At least one supported agent adapter is installed and points to `docs/llm/*`.
- Agents can locate, read, and update documentation consistently using the scaffolded structure.
- Re-running `init` does not destroy existing documentation content.

## 12. Open Questions

- Which two agent adapters are must-have for the first release?
- Should `init` install all supported adapters by default, or only those selected via flags?
- Do we need a minimal repository manifest file (e.g. `.adrlane/version`), or is `docs/llm/*` sufficient?
- How should `init` handle upgrades when `adrlane` ships new templates or skills?
- Should `doctor` ship in v1 or wait until after the first adapter set is stable?

## 13. Suggested Next Step

1. Lock the `docs/llm/*` contract and template set.
2. Define the first agent adapter format (Cursor first, or Claude Code first).
3. Implement M1 (`init` + docs bootstrap).
4. Implement M2 (agent skills).
