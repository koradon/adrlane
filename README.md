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

By default, `init` installs five skills for Cursor and Claude Code:

| Skill | Role |
| --- | --- |
| `adrlane-dev-context` | Ambient — read specs before coding; propose ADRs after significant decisions |
| `adrlane-write-idea` | Write or update ideas |
| `adrlane-write-spec` | Write or update specs (and Gherkin `.feature` files) |
| `adrlane-write-plan` | Write or update implementation plans |
| `adrlane-write-adr` | Document architectural decisions |

**Project-local** (default via `init`): `.cursor/skills/` and `.claude/skills/` in the repository.

**Global** (optional via `skills install --global`): same skills in your home directory, shared across all projects.

Skills are thin adapters; the canonical contract lives in `docs/llm/AGENT_PROTOCOL.md` and `docs/llm/DECISION_RULES.md`.

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
