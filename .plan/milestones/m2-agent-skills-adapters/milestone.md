---
title: 'M2: Agent Skills and Adapters'
id: adrlane-m2-agent-skills-adapters
description: Install agent-specific skills that teach agents how to use the docs contract.
state: open
number: 6
---

## Scope

- Ship Cursor and Claude Code adapters as part of `init`.
- Keep `docs/llm/*` as canonical source; skills are concise entry points.
- Support `init --agent` to select which adapters to install.

## Acceptance Criteria

- At least one supported agent adapter is installed and references `docs/llm/*`.
- Agents can locate, read, and update documentation using the scaffolded structure.
- Adapter install is idempotent and does not overwrite user customizations blindly.
