from __future__ import annotations

from dataclasses import dataclass

SUPPORTED_AGENTS = ("cursor", "claude-code")
DEFAULT_AGENTS = SUPPORTED_AGENTS


@dataclass(frozen=True)
class AgentAdapter:
    name: str
    skill_prefix: str


AGENT_ADAPTERS: dict[str, AgentAdapter] = {
    "cursor": AgentAdapter(name="cursor", skill_prefix=".cursor/skills"),
    "claude-code": AgentAdapter(name="claude-code", skill_prefix=".claude/skills"),
}


def validate_agent_names(agent_names: list[str]) -> list[str]:
    unknown = sorted({name for name in agent_names if name not in AGENT_ADAPTERS})
    if unknown:
        supported = ", ".join(SUPPORTED_AGENTS)
        unknown_list = ", ".join(unknown)
        raise ValueError(f"Unknown agent(s): {unknown_list}. Supported agents: {supported}.")
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
