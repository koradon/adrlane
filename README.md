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
