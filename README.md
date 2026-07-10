# adrlane

Documentation-as-code bootstrap for AI agents.

`adrlane` scaffolds a minimal `docs/` layout and agent skills so AI tools know where to read and write project documentation. The agent decides when to update docs — there is no sync pipeline or enforcement.

## Install

### Global CLI (recommended)

Install `adrlane` once on your machine with [uv](https://docs.astral.sh/uv/):

```bash
uv tool install adrlane
```

From a local checkout:

```bash
uv tool install -e .
```

Verify:

```bash
adrlane --help
```

### Development checkout

Clone the repository and install dependencies:

```bash
git clone https://github.com/koradon/adrlane.git
cd adrlane
uv sync
uv run adrlane --help
```

## Quick start

Run these commands from your **project repository root**:

```bash
cd /path/to/your-project

# 1. Scaffold docs and install project-local agent skills
adrlane init

# Multi-repo workspace (project root is not a single git repo):
adrlane init --workspace   # adds .adrlane/workspace.yaml for doc routing
# Then run `adrlane init` in each sub-repository for service-level docs.

# 2. Optional: install skills globally (one copy for all projects)
adrlane skills install --global
```

Preview changes without writing files:

```bash
adrlane init --dry-run
```

Limit which agent adapters `init` installs:

```bash
adrlane init --agent cursor
adrlane init --agent cursor --agent claude-code
```

After upgrading the `adrlane` package, refresh skills:

```bash
adrlane skills upgrade --global
adrlane skills upgrade --local   # run from a bootstrapped repo
```

## Commands

| Command | Description |
| --- | --- |
| `adrlane init` | Bootstrap `docs/` and install agent skills in the current repository |
| `adrlane init --dry-run` | Show planned bootstrap actions without writing files |
| `adrlane init --agent <name>` | Limit adapters (`cursor`, `claude-code`; repeatable) |
| `adrlane init --workspace` | Bootstrap with multi-repo doc routing config |
| `adrlane skills install --global` | Install skills in `~/.cursor/skills/` and `~/.claude/skills/` |
| `adrlane skills install --local` | Install skills in the current repository (skips existing files) |
| `adrlane skills upgrade --global` | Overwrite global skills with the current package version |
| `adrlane skills upgrade --local` | Overwrite local skills in the current repository |

`init` and `skills --local` always use the **current working directory** — there is no `--path` flag. Change into the target repository first.

## What `init` creates

`init` scaffolds a **minimal core** that grows with the project:

| Path | Purpose |
| --- | --- |
| `docs/specs/` | What the system should do |
| `docs/plans/` | How to implement a spec |
| `docs/adr/` | Why significant decisions were made |
| `docs/ideas/` | Early concepts that may be promoted to specs |
| `docs/roadmap/` | Now / Next / Later horizons |
| `docs/llm/` | Agent contract, decision rules, and templates |

Templates live in `docs/llm/templates/`. Documents use markdown sections (`## Status`, `## Related`) — not YAML frontmatter.

When the project gains new documentation needs (runbooks, API reference, CLI docs), the **agent adds** new folders under `docs/` and updates `docs/README.md`. `init` does not predict project type.

Release history stays in Git and release tooling — not in `docs/`.

## Agent skills

By default, `init` installs six skills for Cursor and Claude Code:

| Skill | Role |
| --- | --- |
| `adrlane-dev-context` | Ambient — read specs before coding; propose ADRs after significant decisions |
| `adrlane-write-idea` | Write or update ideas |
| `adrlane-write-spec` | Write or update specs (and Gherkin `.feature` files) |
| `adrlane-write-plan` | Write or update implementation plans |
| `adrlane-write-adr` | Document architectural decisions |
| `adrlane-workspace-routing` | Route docs to project or sub-repo trees (when `.adrlane/workspace.yaml` exists) |

**Project-local** (default via `init`): `.cursor/skills/` and `.claude/skills/` in the repository.

**Global** (optional via `skills install --global`): same skills in your home directory, shared across all projects.

Skills are thin adapters; the canonical contract lives in `docs/llm/AGENT_PROTOCOL.md` and `docs/llm/DECISION_RULES.md`.

## Multi-repo workspace

Use this when the Cursor workspace root is **not** a single git repository — for example a folder that contains several independent repos plus shared project docs.

### Setup

```bash
cd /path/to/project-root

# Project-level docs + routing config + skills
adrlane init --workspace

# Service-level docs in each repository
cd repository1 && adrlane init
cd ../repository2 && adrlane init
```

Open the **project root** in Cursor so routing applies. Optionally install skills globally once: `adrlane skills install --global`.

### Layouts

**Flat** — repositories are direct children of the project root. No `repo_roots` needed:

```
project/
  docs/                 ← cross-cutting ADRs, specs, roadmap
  repository1/docs/     ← service-specific docs
  repository2/docs/
```

**Grouped** — repositories live under category folders. Uncomment and edit `repo_roots` in `.adrlane/workspace.yaml`:

```
project/
  docs/
  services/order-service/docs/
  frontends/checkout-fe/docs/
```

```yaml
project_docs: docs
repo_roots:
  - services
  - frontends
```

### How routing works

The `adrlane-workspace-routing` skill (active when `.adrlane/workspace.yaml` exists) sends documentation to:

| Scope | Location | Examples |
| --- | --- | --- |
| Project | `docs/` at project root | Platform ADRs, cross-service conventions |
| Service | `<repo>/docs/` | API specs, service-internal decisions |

The other `adrlane-write-*` skills follow the resolved path automatically. Link project and service docs in `## Related`.

## Contributing

Run tests:

```bash
uv run pytest
```

Install pre-commit hooks:

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

Dependency management:

```bash
uv add <package>          # runtime dependency
uv add --dev <package>    # dev dependency
uv lock                   # refresh lockfile after manual pyproject edits
```

## License

AGPL-3.0-or-later. See [LICENSE](LICENSE).
