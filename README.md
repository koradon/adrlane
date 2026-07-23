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

1. Install the CLI globally (see [Install](#install)).
2. From your **project repository root**, scaffold docs and project-local skills:

```bash
cd /path/to/your-project
adrlane init
```

3. Optional: install skills once for all projects on this machine:

```bash
adrlane skills install --global
```

4. Work with your agent as usual. When docs should change, the agent uses the installed skills (see [Agent workflow](#agent-workflow)).

Multi-repo workspace (project root is not a single git repo):

```bash
adrlane init --workspace   # adds .adrlane/workspace.yaml for doc routing
# Then run `adrlane init` in each sub-repository for service-level docs.
```

Preview without writing files:

```bash
adrlane init --dry-run
```

Limit which agent adapters `init` installs:

```bash
adrlane init --agent cursor
adrlane init --agent cursor --agent claude-code
```

`init` and `skills --local` always use the **current working directory** — there is no `--path` flag.

## Upgrading

`init` is additive: it never overwrites an existing file. After you upgrade the `adrlane` package, re-running `init` will not refresh stale `docs/llm/*` contracts or skills. Use `upgrade` for that.

```bash
# 1. Upgrade the installed CLI
uv tool upgrade adrlane

# 2. In each bootstrapped repository: refresh package-owned content
cd /path/to/your-project
adrlane upgrade

# 3. If you use global skills, refresh those too
adrlane skills upgrade --global
```

`adrlane upgrade` overwrites:

- `docs/llm/*` contract files and templates
- `.adrlane/bootstrap-version`
- local agent skill files (same as `skills upgrade --local`)

It never touches user-owned content: `docs/README.md`, `docs/ideas/README.md`, `docs/roadmap/README.md`, the contents of `docs/{specs,plans,adr,ideas,roadmap}`, or `.adrlane/workspace.yaml`.

Preview: `adrlane upgrade --dry-run`. Details: [ADR 0005](docs/adr/0005-dedicated-upgrade-command-for-package-owned-content.md).

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
| `adrlane upgrade` | Refresh `docs/llm/*` contract files, `.adrlane/bootstrap-version`, and local agent skills after upgrading the `adrlane` package |
| `adrlane upgrade --dry-run` | Show planned upgrade actions without writing files |
| `adrlane upgrade --agent <name>` | Limit which agent adapters get their skills refreshed (repeatable) |

## Agent workflow

`adrlane` does not detect documentation gaps, schedule updates, or write docs on its own. The **agent** decides when documentation needs updating during normal development.

Typical loop:

1. Developer installs `adrlane` and runs `adrlane init` once per repository.
2. Developer works with Cursor or Claude Code as usual.
3. When the agent judges that behavior, decisions, or structure should be recorded, it uses the installed skills and `docs/llm/*` to create or patch files under `docs/`.
4. Developer reviews with `git diff` and commits normally.

Skills are thin adapters; the contract is `docs/llm/AGENT_PROTOCOL.md` and `docs/llm/DECISION_RULES.md`.

## Documentation model

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
