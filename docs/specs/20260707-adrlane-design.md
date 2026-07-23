# Adrlane v1 Design Spec

**Status:** Draft
**Owner:** Michal + Agent
**Date:** 2026-07-07
**Project Name:** `adrlane`
**Package Target:** PyPI (`adrlane`)
**Primary Runtime:** Local CLI (Python)

## 1. Problem Statement

Teams using AI coding agents often forget to keep project documentation current while coding.
Architecture decisions, specifications, and implementation notes drift from real code changes.
Agents lack a shared map of where documentation lives, how it is structured, and how to update it consistently.

We need a local-first docs-as-code bootstrap tool that:

- scaffolds a minimal, predictable `/docs` structure in every repository,
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
- Project-type profiles or day-zero scaffolding for CLI, web, API, etc.
- Changelog files in `docs/` — release history lives in Git and release tooling.

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
  Bootstrap `/docs` structure, templates, `docs/llm/*` contract files, and agent skills for selected agents. Run from the target repository root (uses the current working directory).

- `adrlane init --agent <name>` (repeatable)
  Limit or extend which agent adapters are installed (e.g. `cursor`, `claude-code`).

- `adrlane skills install --global` / `--local`
  Install packaged agent skills in the user home directory or the current repository. `install` skips existing files.

- `adrlane skills upgrade --global` / `--local`
  Overwrite packaged agent skills after upgrading the `adrlane` package. Supports `--dry-run`.

- `adrlane upgrade`
  Refresh package-owned bootstrap content after upgrading the `adrlane` package: overwrites `docs/llm/*` contract files, `.adrlane/bootstrap-version`, and local agent skills (equivalent to `skills upgrade --local`). Supports `--dry-run` and `--agent`. Never touches user-owned content — `docs/README.md`, `docs/ideas/README.md`, `docs/roadmap/README.md`, the contents of `docs/{specs,plans,adr,ideas,roadmap}`, or `.adrlane/workspace.yaml`. Requires an existing `.adrlane/` bootstrap (run `init` first).

- `adrlane init --dry-run`
  Show files and folders that would be created without writing them.

- `adrlane doctor` (informational)
  Check whether the repository has the expected documentation structure and agent adapters present. Read-only and non-blocking: always exits `0`.

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

### 7.1 Documentation Model

`adrlane init` creates a **minimal core** and does not predict project shape. The documentation tree **grows with the project** — agents add new top-level sections (for example `docs/runbooks/` or `docs/reference/cli/`) only when real content warrants them.

Release history is tracked in Git and release tooling, not in `docs/`.

#### Day-zero structure

```
docs/
  README.md                 # living map + growth model
  llm/
    AGENT_PROTOCOL.md
    DECISION_RULES.md
    TEMPLATES.md
    DOC_GUIDELINES.md
    templates/
      spec.md
      plan.md
      adr-light.md
      adr-standard.md
      adr-full.md
      runbook.md            # used when agent adds docs/runbooks/
      reference.md          # used when agent adds docs/reference/
  ideas/                    # empty, grows with project
  roadmap/                  # Now / Next / Later horizons
  specs/                    # empty, grows with project
  plans/
  adr/
```

Plus agent adapter files for supported agents.

#### Content types

| Type | Location | Answers |
| --- | --- | --- |
| Idea | `docs/ideas/` | Early, uncommitted concepts (may be promoted or rejected) |
| Spec | `docs/specs/` | **What** the system should do |
| Plan | `docs/plans/` | **How** to implement a spec |
| ADR | `docs/adr/` | **Why** a significant decision was made |
| Roadmap | `docs/roadmap/` | Now / Next / Later horizons for future initiatives |

**Idea → spec → plan workflow:**

1. Write an idea when exploring a potential change before contracts are clear.
2. Promote an accepted idea to a spec when desired behavior and contracts are clear.
3. Create a plan from the spec when implementation spans multiple steps or sessions.
4. Small changes may use a spec alone.
5. Link ideas/specs/plans via a `## Related` section.
6. When a plan finishes, set status to `completed` and optionally rename with a `.completed` suffix.

**ADR tiers** (agent proposes, developer may correct):

| Tier | Template | Use when |
| --- | --- | --- |
| light | `adr-light.md` | Obvious or local decisions (Nygard-style) |
| standard | `adr-standard.md` | Real alternatives existed (MADR minimal) |
| full | `adr-full.md` | Major architectural decisions (MADR full) |

ADRs are numbered sequentially (`0001-short-title.md`). Numbers are never reused; superseded decisions get a new ADR with a link.

#### Metadata

Documents use markdown sections (`## Status`, `## Related`) — not YAML frontmatter. The tool does not parse frontmatter.

#### Growth rules

When the project gains a new documentation need:

1. Agent adds a top-level folder under `docs/` if content does not fit specs/plans/adr/ideas/roadmap.
2. Agent copies and adapts a template from `docs/llm/templates/`.
3. Agent updates `docs/README.md`.

Do not create empty folders "for later."

### 7.2 Universal LLM Contract

`docs/llm/AGENT_PROTOCOL.md` is the canonical, agent-agnostic source of truth. It defines:

- where each documentation type lives,
- how specs and plans relate,
- how to search for existing context before writing,
- where to append or create new documentation,
- artifact naming conventions,
- how to extend the documentation tree,
- update semantics (create vs patch),
- conflict policy (never delete unrelated docs),
- language and style consistency rules.

Agent-specific skills/rules are adapters: they teach the agent how to find and follow `docs/llm/*`.

### 7.3 Agent Decision Model

The agent decides whether documentation needs updating during normal development work.
`adrlane` does not detect gaps, schedule updates, or write documentation on behalf of the user.

## 8. Agent Skills and Adapters

### 8.1 Purpose

Skills give each supported agent a project-local, tool-native entry point into the documentation system.
An agent skill should answer:

- where documentation lives in this repository,
- which file to read first,
- how to update specs, plans, and ADRs,
- which templates and guidelines to follow,
- how to extend the documentation tree when needed.

### 8.2 Supported Agents (v1 target)

Initial targets (subject to prioritization):

- Cursor
- Claude Code

Additional adapters (e.g. OpenCode) can follow the same pattern without changing the core contract.

### 8.3 Skill Content Strategy

- Canonical rules live in `docs/llm/*`.
- Agent skills are concise adapters that reference those files.
- Skills are copied/generated during `init`, not fetched from a remote service.
- v1 installs five skills per supported agent:
  - **ambient:** `adrlane-dev-context` — read specs before coding; propose ADRs when a significant decision settles in conversation.
  - **explicit:** `adrlane-write-idea`, `adrlane-write-spec`, `adrlane-write-plan`, `adrlane-write-adr`.

## 9. Developer Workflow

1. Install `adrlane` globally.
2. Run `adrlane init` in a repository.
3. Work with an agent as usual.
4. When the agent judges that documentation should be updated, it uses the installed skills and `docs/llm/*` contract to make consistent edits under `docs/`.
5. Developer reviews changes via `git diff` and commits normally.

## 10. v1 Milestones

### M1: CLI and Documentation Bootstrap

- CLI scaffolding (`init`, `doctor`).
- Documentation skeleton and `docs/llm/*` contract files.
- Centralized templates in `docs/llm/templates/`.
- Pytest test suite for CLI and bootstrap behavior.
- Python packaging (PEP 621), versioning, CI pipeline, and PyPI release workflow.

### M2: Agent Skills and Adapters (done)

- Five shared skills installed per agent adapter: `adrlane-dev-context` (ambient) plus `adrlane-write-idea`, `adrlane-write-spec`, `adrlane-write-plan`, `adrlane-write-adr` (explicit).
- Cursor paths: `.cursor/skills/<skill-name>/SKILL.md`.
- Claude Code paths: `.claude/skills/<skill-name>/SKILL.md`.
- `init --agent` selection (repeatable); defaults to both supported agents.
- Idempotent adapter install when `init` is re-run.

### M3: Polish and Maintenance

- `doctor` informational checks. (done)
- `init --dry-run` and refresh/migrate strategy for upgraded package versions (done: `adrlane upgrade`).
- README and onboarding docs.

## 11. Acceptance Criteria (v1)

- User can install `adrlane` globally and run it from any repository.
- User can run `adrlane init` in an empty repo and get the documentation contract and minimal folder structure.
- At least one supported agent adapter is installed and points to `docs/llm/*`.
- Agents can locate, read, and update documentation consistently using the scaffolded structure.
- Re-running `init` does not destroy existing documentation content.

## 12. Open Questions

- Do we need a minimal repository manifest file (e.g. `.adrlane/bootstrap-version`), or is `docs/llm/*` sufficient?
- ~~How should `init` handle upgrades when `adrlane` ships new templates or skills?~~ Resolved: `init` stays purely additive/idempotent; `adrlane upgrade` refreshes package-owned content (see [ADR 0005](../adr/0005-dedicated-upgrade-command-for-package-owned-content.md)).
- ~~Should `doctor` ship in v1 or wait until after the first adapter set is stable?~~ Resolved: shipped in v1 as an informational, non-blocking check.

## 13. Suggested Next Step

1. Implement M3 (`doctor`, upgrade/migrate strategy).
2. Expand test coverage for CLI `--agent` edge cases if needed.
3. Publish first PyPI release when CI and packaging are green.
