from __future__ import annotations

EXPECTED_DOC_FILES = [
    "docs/README.md",
    "docs/ideas/README.md",
    "docs/roadmap/README.md",
    "docs/llm/AGENT_PROTOCOL.md",
    "docs/llm/DECISION_RULES.md",
    "docs/llm/TEMPLATES.md",
    "docs/llm/DOC_GUIDELINES.md",
    "docs/llm/templates/acceptance.feature",
    "docs/llm/templates/idea.md",
    "docs/llm/templates/spec.md",
    "docs/llm/templates/plan.md",
    "docs/llm/templates/adr-light.md",
    "docs/llm/templates/adr-standard.md",
    "docs/llm/templates/adr-full.md",
    "docs/llm/templates/roadmap.md",
    "docs/llm/templates/runbook.md",
    "docs/llm/templates/reference.md",
]

EXPECTED_DOC_DIRS = [
    "docs/specs",
    "docs/plans",
    "docs/adr",
    "docs/ideas",
    "docs/roadmap",
]

BOOTSTRAP_ACTION_COUNT = 2 + len(EXPECTED_DOC_DIRS) + len(EXPECTED_DOC_FILES)
WORKSPACE_BOOTSTRAP_ACTION_COUNT = BOOTSTRAP_ACTION_COUNT + 1

REMOVED_LEGACY_PATHS = [
    "docs/changelog",
    "docs/runbooks",
    "docs/adr/_template.md",
    "docs/specs/_template.md",
]
