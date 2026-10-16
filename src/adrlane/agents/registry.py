from __future__ import annotations

from dataclasses import dataclass

SUPPORTED_AGENTS = ("cursor", "claude-code", "codex", "agy")
DEFAULT_AGENTS = SUPPORTED_AGENTS

SUPPORTED_AGENTS_HELP = ", ".join(SUPPORTED_AGENTS)


@dataclass(frozen=True)
class AgentAdapter:
    name: str
    skill_prefix: str
    # Only set when an agent's global (--global) skill root is not simply
    # `skill_prefix` under the home directory. See ADR 0009.
    global_skill_prefix: str | None = None


def skill_prefix_for(adapter: AgentAdapter, *, global_scope: bool = False) -> str:
    """Return the install-relative skill prefix for an adapter and scope."""
    if global_scope and adapter.global_skill_prefix is not None:
        return adapter.global_skill_prefix
    return adapter.skill_prefix


AGENT_ADAPTERS: dict[str, AgentAdapter] = {
    "cursor": AgentAdapter(name="cursor", skill_prefix=".cursor/skills"),
    "claude-code": AgentAdapter(name="claude-code", skill_prefix=".claude/skills"),
    # Codex CLI scans `<repo>/.codex/skills` as a project-local skill root and
    # `$CODEX_HOME/skills` (default `~/.codex/skills`) as the user-level one, so the
    # same prefix serves both the --local and --global scopes.
    "codex": AgentAdapter(name="codex", skill_prefix=".codex/skills"),
    # Antigravity CLI (agy) scans `<workspace>/.agents/skills` as its repo-local
    # skill root, but a *different*, unrelated global root: `~/.gemini/config/skills`.
    # Unlike codex, one relative prefix cannot serve both scopes. See ADR 0009.
    "agy": AgentAdapter(
        name="agy",
        skill_prefix=".agents/skills",
        global_skill_prefix=".gemini/config/skills",
    ),
}


def validate_agent_names(agent_names: list[str]) -> list[str]:
    unknown = sorted({name for name in agent_names if name not in AGENT_ADAPTERS})
    if unknown:
        unknown_list = ", ".join(unknown)
        raise ValueError(
            f"Unknown agent(s): {unknown_list}. Supported agents: {SUPPORTED_AGENTS_HELP}."
        )
    return agent_names


def normalize_agent_selection(selected: list[str] | None) -> tuple[str, ...]:
    if selected is None:
        return DEFAULT_AGENTS
    if not selected:
        return ()
    deduped: list[str] = []
    seen: set[str] = set()
    for name in selected:
        validate_agent_names([name])
        if name in seen:
            continue
        seen.add(name)
        deduped.append(name)
    return tuple(deduped)
