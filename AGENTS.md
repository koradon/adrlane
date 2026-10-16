# Project agent memory

This file is the project's committed home for project-intrinsic agent knowledge: build, test, release, architecture, and sharp-edge notes that should travel with the code.

- Correct entries that work proves wrong; add new ones only by deliberate maintainer choice, never as routine task output.

## What this is

`adrlane` is a documentation-as-code bootstrap for AI agents: it scaffolds a minimal `docs/` layout and agent skills so AI tools know where to read and write project documentation.

## Commands

- Install dependencies: `uv sync --dev`
- Run tests: `uv run pytest --cov=adrlane`
- Lint: `uv run ruff check .`
- Format check: `uv run ruff format --check .`

## Conventions

- Documentation-as-code contract: `docs/llm/AGENT_PROTOCOL.md`.
- Planning (issues/milestones), synced with Planhub: `.plan/`.

## Maintaining this file

Keep this file for knowledge useful to almost every future agent session in this project.
Do not repeat what the codebase already shows; point to the authoritative file or command instead.
Prefer rewriting or pruning existing entries over appending new ones.
When updating this file, preserve this bar for all agents and keep entries concise.
