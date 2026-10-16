from __future__ import annotations

AGENT_SKILL_NAMES = (
    "adrlane-dev-context",
    "adrlane-write-idea",
    "adrlane-write-spec",
    "adrlane-write-plan",
    "adrlane-write-adr",
    "adrlane-write-architecture-overview",
    "adrlane-workspace-routing",
)

AGENT_SKILL_PREFIX = {
    "cursor": ".cursor/skills",
    "claude-code": ".claude/skills",
    "codex": ".codex/skills",
    "agy": ".agents/skills",
}

# agy's global (--global) skill root differs from its local one (ADR 0009).
GLOBAL_AGENT_SKILL_PREFIX = {
    **AGENT_SKILL_PREFIX,
    "agy": ".gemini/config/skills",
}


def agent_skill_path(agent: str, skill_name: str) -> str:
    return f"{AGENT_SKILL_PREFIX[agent]}/{skill_name}/SKILL.md"


def agent_skill_paths(agent: str) -> list[str]:
    return [agent_skill_path(agent, name) for name in AGENT_SKILL_NAMES]


def global_agent_skill_path(agent: str, skill_name: str) -> str:
    return f"{GLOBAL_AGENT_SKILL_PREFIX[agent]}/{skill_name}/SKILL.md"


# Representative paths used in tests that only need one skill per agent.
AGENT_SKILL_FILES = {
    "cursor": agent_skill_path("cursor", "adrlane-dev-context"),
    "claude-code": agent_skill_path("claude-code", "adrlane-dev-context"),
    "codex": agent_skill_path("codex", "adrlane-dev-context"),
    "agy": agent_skill_path("agy", "adrlane-dev-context"),
}

SKILLS_PER_AGENT = len(AGENT_SKILL_NAMES)
AGENT_ACTION_COUNT = SKILLS_PER_AGENT * len(AGENT_SKILL_PREFIX)
