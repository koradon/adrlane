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
This causes onboarding friction, poor handoffs, and avoidable rework.

We need a local-first docs-as-code tool that:

- keeps documentation inside `/docs`,
- supports autonomous AI-assisted updates,
- works with hybrid model providers (local + remote),
- stays agent-agnostic (Cursor, Claude, ChatGPT, local LLMs),
- and integrates with normal Git workflows.

## 2. Product Goals

### 2.1 Primary Goals

- Provide a `pip install adrlane` CLI for local docs automation.
- Automatically create/update docs artifacts based on code changes.
- Keep edits constrained to docs scope and visible in `git diff`.
- Encode universal LLM-facing rules so different agents behave consistently.
- Support both manual execution and Git hook execution.

### 2.2 Non-Goals (v1)

- Full docs website generator.
- Real-time daemon watching all file system events.
- External SaaS dependency for core functionality.
- Complex multi-repo orchestration.

## 3. Target User (v1)

- Solo developer working locally in one repository.
- Wants high autonomy with safe review via Git.
- Uses one or more AI agents during coding.

## 4. High-Level Architecture

`adrlane` has five core subsystems:

1. **CLI Layer**  
   Entry point commands (`init`, `sync`, `doctor`, `hook`).
2. **Policy Engine**  
   Rule evaluation for "what docs action is required".
3. **Change Analyzer**  
   Inspects Git state and maps code changes to doc intents.
4. **AI Orchestrator**  
   Routes tasks to selected providers/models and applies edits.
5. **Quality Gate**  
   Validates docs changes (scope, templates, lint, required artifacts).

## 5. Core UX and CLI

### 5.1 Commands

- `adrlane init`  
  Bootstrap `/docs` structure, templates, and `adrlane.yml`.

- `adrlane sync`  
  Analyze current repo state and apply docs updates automatically.

- `adrlane sync --from <git-ref>`  
  Limit analysis to changes since a ref.

- `adrlane sync --dry-run`  
  Show intended actions without writing files.

- `adrlane doctor`  
  Validate config, providers, template integrity, and hook setup.

- `adrlane hook install --pre-commit`  
  Install pre-commit integration.

- `adrlane hook install --post-commit`  
  Install post-commit integration.

- `adrlane hook uninstall`

### 5.2 Exit Behavior

- `0`: success, no blocking issues
- `1`: blocking validation or runtime failure
- `2`: partial success with warnings (non-blocking policy failures)

## 6. Repository Contract (Docs-as-Code Standard)

`adrlane init` creates:

- `docs/README.md`
- `docs/adr/`
- `docs/specs/`
- `docs/runbooks/`
- `docs/changelog/`
- `docs/llm/AGENT_PROTOCOL.md`
- `docs/llm/DECISION_RULES.md`
- `docs/llm/TEMPLATES.md`
- `docs/llm/QUALITY_GATES.md`
- `adrlane.yml`

### 6.1 Universal LLM Contract

`docs/llm/AGENT_PROTOCOL.md` defines:

- allowed write scope (`/docs/**` only in doc update mode),
- mandatory artifact conventions (ADR naming, spec naming),
- required metadata headers,
- update semantics (create vs append vs patch),
- conflict policy (never delete unrelated docs),
- language/style consistency rules.

This file is intentionally model-agnostic and plain Markdown so any agent can follow it.

## 7. Policy Engine

### 7.1 Intent Types

`adrlane` classifies changes into intents:

- `adr_required`
- `spec_update_required`
- `runbook_required`
- `changelog_update_required`
- `doc_refactor_recommended`

### 7.2 Example Rules

- If files in `src/architecture/**` change and no ADR changed, emit `adr_required`.
- If public API signatures changed and no spec changed, emit `spec_update_required`.
- If deployment scripts changed and no runbook changed, emit `runbook_required`.
- If release-impacting changes exist, emit `changelog_update_required`.

Rules are configurable in `adrlane.yml`.

## 8. AI Orchestration

### 8.1 Provider Model

Hybrid support:

- local providers (LM Studio, Ollama, OpenAI-compatible local gateways),
- remote providers (OpenAI-compatible APIs).

### 8.2 Routing

Task-to-model mapping example:

- `adr_required` -> reasoning-heavy model
- `changelog_update_required` -> cheaper fast model
- fallback chain per task class

### 8.3 Determinism and Safety

- deterministic prompt templates for each artifact type,
- file-scoped write plan before execution,
- hard path guard (cannot write outside `/docs` in v1),
- operation log for reproducibility.

## 9. Git Integration

### 9.1 Modes

- On-demand: user runs `adrlane sync`.
- Hooked:
  - pre-commit mode for mandatory docs gating,
  - post-commit mode for non-blocking autonomous updates.

### 9.2 Review Flow

- Tool writes docs changes automatically.
- User verifies via `git status` and `git diff`.
- Normal commit process remains unchanged.

## 10. Config (`adrlane.yml`) Draft Shape

```yaml
version: 1
docs_root: docs
mode:
  auto_write: true
  dry_run_default: false
providers:
  default: local
  local:
    type: openai_compatible
    base_url: http://localhost:1234/v1
    api_key_env: LMSTUDIO_API_KEY
  remote:
    type: openai_compatible
    base_url: https://api.openai.com/v1
    api_key_env: OPENAI_API_KEY
routing:
  adr_required: remote
  spec_update_required: remote
  runbook_required: local
  changelog_update_required: local
policies:
  require_adr_on_arch_change: true
  require_runbook_on_deploy_change: true
  enforce_templates: true
hooks:
  pre_commit: false
  post_commit: true
```

## 11. Quality Gates

Before writing success state:

- all writes stay under `/docs`,
- required templates are respected,
- mandatory metadata headers exist,
- markdown lint passes (if enabled),
- operation log stored under `.adrlane/logs/`.

## 12. Observability and Artifacts

- machine-readable run report (JSON),
- human summary in CLI output,
- optional debug prompt trace (sanitized),
- per-run correlation id.

## 13. Security and Privacy

- no silent network calls without configured provider,
- redact secrets from logs,
- strict environment-variable based credential loading,
- local-first behavior by default where feasible.

## 14. Packaging and Distribution

- Python package built with modern PEP 621 metadata.
- Install via `pip install adrlane`.
- Console entry point: `adrlane`.
- Optional extras:
  - `adrlane[local]` for local provider helpers,
  - `adrlane[dev]` for test/lint tooling.

## 15. v1 Milestones

### M1: Bootstrap and Config

- CLI scaffolding (`init`, `doctor`),
- config schema validation,
- docs skeleton generation.

### M2: Change Analyzer + Policies

- Git diff parsing,
- intent detection,
- rule engine with configurable toggles.

### M3: AI Write Path

- provider adapters,
- prompt templates,
- constrained doc writes.

### M4: Hooks + Quality Gates

- pre/post commit install,
- quality checks and run reports,
- hardening and UX polish.

## 16. Acceptance Criteria (v1)

- User can run `adrlane init` in empty repo and get full docs contract.
- User can run `adrlane sync` after code change and receive meaningful docs updates.
- Auto-written docs appear only in `/docs` and are reviewable via Git.
- At least one local provider and one remote provider path work end-to-end.
- Policy engine blocks or warns based on configured rule severity.
- Hook mode functions reliably for solo local workflow.

## 17. Open Questions

- Should v1 include automatic ADR supersession links?
- Should `post-commit` mode auto-stage docs or leave unstaged?
- How strict should template enforcement be for legacy docs imports?

## 18. Suggested Next Step

After creating the new repository:

1. copy this spec,
2. lock `adrlane.yml` schema,
3. create implementation plan per milestone,
4. implement M1 first with tests.
