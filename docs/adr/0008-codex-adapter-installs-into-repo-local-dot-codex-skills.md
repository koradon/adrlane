# Codex adapter installs into repo-local `.codex/skills`

## Status

accepted

## Context and Problem Statement

adrlane shipped two agent adapters, `cursor` and `claude-code`, both of which install
skills into a repo-local prefix (`.cursor/skills`, `.claude/skills`). Codex CLI had no
adapter, so agents running on Codex saw none of the `adrlane-*` skills.

Adding a Codex adapter was not obviously a one-line change, because it was unclear
whether Codex reads skills from inside the repository at all. The existing adapter model
assumes a repo-local `skill_prefix`; if Codex only read a user-level directory, the
adapter abstraction itself would have needed reworking. Two signals suggested it might:
`$CODEX_HOME/skills` is the documented install target of Codex's own `skill-installer`,
and an unrelated tool's installer script in the wider toolchain treats Codex as
"not automated", telling users to paste skill content into `AGENTS.md` by hand.

## Considered Options

- **Repo-local `.codex/skills`.** Same shape as the existing adapters: a
  `skill_prefix` under the target directory.
- **User-level `$CODEX_HOME/skills`.** Install outside the repository, into the
  directory Codex's own `skill-installer` writes to.
- **Managed section in `AGENTS.md`.** Generate skill content into the repo's
  `AGENTS.md` between start/end markers so it can be refreshed without clobbering
  hand-written text.

## Decision Outcome

Chosen option: "Repo-local `.codex/skills`".

We resolved the uncertainty empirically rather than by reading documentation. Four probe
skills were planted at once — in `<repo>/.codex/skills`, `<repo>/.agents/skills`,
`<repo>/.claude/skills`, and `$CODEX_HOME/skills` — and Codex CLI `0.156.1` was asked to
enumerate its available skills and then use one. Codex listed the probes from
`.codex/skills`, `.agents/skills`, and `$CODEX_HOME/skills`, printed a `### Skill roots`
table mapping each alias to its absolute path, and read a repo-local probe's `SKILL.md`
to return a value embedded in it. The `.claude/skills` probe did not appear — confirming
that adrlane's existing adapters really were invisible to Codex.

So `<repo>/.codex/skills` is a first-class Codex skill root, and
`AGENT_ADAPTERS["codex"]` uses it as its `skill_prefix` exactly like the other two
adapters. The `AGENTS.md` fallback is unnecessary, and user-level installation was
rejected because it puts skills outside version control and outside review.

One convenient property falls out of this choice: Codex also scans
`$CODEX_HOME/skills`, whose default is `~/.codex/skills`. Because
`resolve_skills_target` maps the global scope to `Path.home()` (ADR-0003), the single
`.codex/skills` prefix lands on a real Codex skill root under both `--local` and
`--global` — no scope-dependent special-casing.

### Consequences

- Good, because Codex support cost one registry entry and changed no shared code path;
  the thin-adapter model of ADR-0002 held without modification.
- Good, because Codex skills are versioned and reviewable in the repo, like the Cursor
  and Claude Code ones.
- Good, because `--local` and `--global` both work for Codex with no extra machinery.
- Bad, because `.codex/skills` is a behaviour of the Codex CLI that we verified by
  experiment rather than from a published contract; a future Codex release could drop
  the repo-local root and silently break the adapter.
- Neutral, because the undocumented `.agents/skills` root also works. We did not adopt
  it: it is not Codex-specific, and nothing in the current tooling writes there.

## Related

- Decision context: `docs/adr/0002-agent-agnostic-contract-with-thin-adapters.md`
- Install scopes: `docs/adr/0003-global-and-local-skills-install-scope.md`
