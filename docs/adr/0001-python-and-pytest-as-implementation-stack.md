# Python and pytest as the implementation and testing stack

## Status

accepted

## Context and Problem Statement

adrlane is a local-first CLI distributed to developer machines. We needed to pick
an implementation language and a test framework that make the tool easy to install
globally, quick to iterate on, and approachable for contributors, without adding a
heavy toolchain.

## Considered Options

- **Python + pytest**, packaged with uv/hatchling, CLI built on Typer.
- **A compiled language (Go / Rust).** Single static binary, no runtime needed.
- **Node.js/TypeScript.** Ships via npm/npx, strong CLI ecosystem.

## Decision Outcome

Chosen option: "Python + pytest".

The project targets Python `>=3.10` (developed on 3.12), builds with hatchling, and
is installed via `uv tool install adrlane`. The CLI is built on Typer. Tests use
pytest (`>=8.0`) with `pytest-cov`, configured under `[tool.pytest.ini_options]`
(`testpaths = ["tests"]`, `-q`); ruff provides linting and formatting. This matches
the uv-centric workflow the design assumes and keeps the barrier to contribution
low, since the tool's job — scaffolding Markdown and files — needs no compiled
performance.

### Consequences

- Good, because uv makes global install and isolated tool environments trivial, and
  Python + Typer keeps the CLI small and readable.
- Good, because pytest is ubiquitous and low-ceremony, so contributors can add tests
  without learning a bespoke harness.
- Good, because the wide `>=3.10` support (classifiers through 3.14) broadens where
  adrlane can be installed.
- Bad, because distribution requires a Python runtime and uv, unlike a single static
  binary from a compiled language.
- Bad, because Python's runtime performance is worse than Go/Rust — acceptable here
  given the tool does light filesystem work.

## Related

- Config: `pyproject.toml`
- Design spec: `20260707-adrlane-design.md` (Primary Runtime: Local CLI (Python))
