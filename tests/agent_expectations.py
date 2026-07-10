from __future__ import annotations

AGENT_SKILL_NAMES = (
    "adrlane-dev-context",
    "adrlane-write-idea",
    "adrlane-write-spec",
    "adrlane-write-plan",
    "adrlane-write-adr",
    "adrlane-workspace-routing",
)

AGENT_SKILL_PREFIX = {
    "cursor": ".cursor/skills",
    "claude-code": ".claude/skills",
}


def agent_skill_path(agent: str, skill_name: str) -> str:
    return f"{AGENT_SKILL_PREFIX[agent]}/{skill_name}/SKILL.md"


def agent_skill_paths(agent: str) -> list[str]:
    return [agent_skill_path(agent, name) for name in AGENT_SKILL_NAMES]


# Representative paths used in tests that only need one skill per agent.
AGENT_SKILL_FILES = {
    "cursor": agent_skill_path("cursor", "adrlane-dev-context"),
    "claude-code": agent_skill_path("claude-code", "adrlane-dev-context"),
}

SKILLS_PER_AGENT = len(AGENT_SKILL_NAMES)
AGENT_ACTION_COUNT = SKILLS_PER_AGENT * len(AGENT_SKILL_PREFIX)
