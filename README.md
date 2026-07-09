# adrlane

Documentation-as-code bootstrap for AI agents.

`adrlane init` scaffolds a minimal `docs/` layout and an agent-facing contract so AI tools know where to read and write project documentation. The agent decides when to update docs — there is no sync pipeline or enforcement.

## Documentation model

`init` creates a **minimal core** that grows with the project:

| Path | Purpose |
| --- | --- |
| `docs/specs/` | What the system should do |
| `docs/plans/` | How to implement a spec |
| `docs/adr/` | Why significant decisions were made |
| `docs/ideas/` | Early concepts that may be promoted to specs |
| `docs/roadmap/` | Now / Next / Later horizons for future initiatives |
| `docs/llm/` | Agent contract and templates |

Templates live in `docs/llm/templates/`. Documents use markdown sections (`## Status`, `## Related`) — not YAML frontmatter.

When the project gains new documentation needs (CLI reference, runbooks, API docs), the **agent adds** new folders under `docs/` and updates `docs/README.md`. `init` does not predict project type or scaffold empty sections.

By default, `init` also installs five agent skills for Cursor and Claude Code:

- `adrlane-dev-context` — ambient: read specs before coding, propose ADRs after significant decisions
- `adrlane-write-idea`, `adrlane-write-spec`, `adrlane-write-plan`, `adrlane-write-adr` — explicit documentation tasks

Use `--agent cursor` or `--agent claude-code` (repeatable) to limit which adapters are installed.

For a single global install across all projects:

```bash
adrlane skills install --global
```

Update global or per-repo skills after upgrading `adrlane`:

```bash
adrlane skills upgrade --global
cd my-repo && adrlane skills upgrade --local
```

`skills install --local` must be run from an adrlane repository root.

Release history stays in Git and release tooling — not in `docs/`.

## Requirements

- [uv](https://docs.astral.sh/uv/)

## Development

```bash
uv sync
uv run adrlane --help
uv run adrlane init --path /path/to/target-repo
uv run adrlane init --path /path/to/target-repo --agent cursor
uv run adrlane skills install --global
uv run adrlane skills upgrade --local
uv run adrlane init --path /path/to/target-repo --dry-run
```

Run tests:

```bash
uv run pytest
```

### Pre-commit Hooks

This project uses pre-commit to run code quality checks before commits. Install
the hooks:

```bash
uv run pre-commit install
```

The hooks will automatically run on `git commit`. They check for:
- Code formatting and linting (ruff)
- Trailing whitespace and end-of-file fixes
- YAML, JSON, and TOML syntax
- Merge conflicts and debug statements

Run hooks manually on all files:

```bash
uv run pre-commit run --all-files
```

## Global install

```bash
uv tool install -e .
adrlane init --path /path/to/target-repo
```

## Dependency management

```bash
uv add <package>          # runtime dependency
uv add --dev <package>    # dev dependency
uv lock                   # refresh lockfile after manual pyproject edits
```

## License

AGPL-3.0-or-later. See [LICENSE](LICENSE).
