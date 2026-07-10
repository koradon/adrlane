# Agent-agnostic documentation contract with thin per-agent adapters

## Status

accepted

## Context and Problem Statement

adrlane must teach several AI coding agents (Cursor, Claude Code, and others in
future) how to read and write project documentation consistently. Each agent
discovers skills from a different location (`.cursor/skills`, `.claude/skills`, …)
and may evolve its own conventions. We needed a way to support multiple agents
without duplicating the actual guidance or coupling the tool to any single agent.

## Considered Options

- **Agent-agnostic contract + thin per-agent adapters.** Keep the canonical
  guidance in plain Markdown under `docs/llm/` (`AGENT_PROTOCOL.md`,
  `DECISION_RULES.md`) and register each supported agent as a small adapter that
  only knows its install prefix. The same skill content is installed into each
  agent's location.
- **Single hardcoded agent.** Support only one agent (e.g. Claude Code) and its
  skill layout directly.
- **Per-agent skill content.** Maintain a separate, independently authored set of
  skills for each agent.

## Decision Outcome

Chosen option: "Agent-agnostic contract + thin per-agent adapters".

The source of truth is the plain-Markdown contract under `docs/llm/`. Agents are
modelled as `AgentAdapter` records in a registry (`agents/registry.py`) whose only
per-agent knowledge is a `skill_prefix`. Skill installation (`agents/skills.py`,
`adrlane skills install/upgrade`) resolves the target location from the adapter and
writes the shared skill files there, so adding a new agent is a registry entry plus
a prefix — not a new body of guidance. Skills remain thin adapters that point back
at the contract, keeping behavior identical across agents.

### Consequences

- Good, because supporting a new agent is a one-line registry change; guidance is
  authored once and stays consistent across agents.
- Good, because the contract lives in the repo as reviewable Markdown, independent
  of any agent, matching the project's local-first, no-enforcement stance.
- Good, because `install` (skip existing) and `upgrade` (overwrite) share one code
  path across all agents and both local and global scopes.
- Bad, because a shared skill body cannot exploit agent-specific capabilities;
  adapters are deliberately limited to path prefixes today.
- Bad, because if an agent ever needs genuinely different skill content, the
  "thin adapter" assumption will have to be revisited.

## Related

- Design spec: `2026-07-07-adrlane-design.md` (§4 High-Level Architecture — Agent Adapters)
- Milestone: `.plan/milestones/m2-agent-skills-and-adapters/milestone.md`
- Agent contract: `docs/llm/AGENT_PROTOCOL.md`
