# adrlane

Documentation-as-code bootstrap for AI agents.

## Requirements

- [uv](https://docs.astral.sh/uv/)

## Development

```bash
uv sync
uv run adrlane --help
uv run adrlane init --path /path/to/target-repo
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
