---
title: Define upgrade refresh strategy and onboarding documentation
id: adrlane-m3-issue-002
labels:
- m3
- docs
- maintenance
milestone: 7
state: closed
number: 18
state_reason: completed
---

## Goal

Make package upgrades and first-time onboarding clear for users and agents.

## Tasks

- Define how `init` handles new templates/skills from upgraded `adrlane` versions.
- Document global install (`uv tool install`) and per-repo `init` workflow in README.
- Document agent workflow: agent decides when to update docs using installed skills.
- Document upgrade path: `uv tool upgrade adrlane` → `adrlane upgrade` (+ optional `skills upgrade --global`).
