# Antigravity (`agy`) adapter uses a distinct global skill prefix

## Status

accepted

## Context and Problem Statement

adrlane's `cursor`, `claude-code`, and `codex` adapters (ADR 0002, ADR 0008) all
install into a single `skill_prefix` string that is appended to the install
target — `Path.cwd()` for `--local`, `Path.home()` for `--global` (ADR 0003). That
worked for `codex` because `.codex/skills` happens to be a valid skill root under
*both* the repository and the home directory (`$CODEX_HOME/skills` defaults to
`~/.codex/skills`).

Antigravity CLI (`agy`), which replaced the retired Gemini CLI, does not share
that property. It reads workspace skills only from
`<workspace>/.agents/skills/<name>/SKILL.md`, and global skills only from
`~/.gemini/config/skills/<name>/SKILL.md`. Verified against the installed `agy`
CLI 1.4.0 in a scratch workspace outside this repository: probe skills were
planted at once in `<workspace>/.agents/skills`, `<workspace>/.codex/skills`,
and `<workspace>/.claude/skills`, then `agy -p "... list every skill ..."
--mode plan` was asked to enumerate. Only the `.agents/skills` probe appeared;
the `.codex/skills` and `.claude/skills` probes never did. The same run's skill
list also included skills already installed at the real `~/.gemini/config/skills`
(this machine's existing global skills), confirming that path as a live global
root without needing to write a new probe into it. `.agents/skills` relative to
`home()` is not `.gemini/config/skills`, so the existing single-`skill_prefix`
model cannot represent `agy` without either special-casing it outside the
adapter model or extending the model itself.

## Considered Options

- **Extend `AgentAdapter` with an optional `global_skill_prefix`.** Keep the thin
  per-adapter data shape from ADR 0002, but let an adapter declare a different
  relative path for the `--global` scope. Adapters that don't set it (all
  existing ones) keep today's behavior unchanged.
- **Special-case `agy` in `resolve_skills_target` or `run_skills`.** Branch on
  agent name outside the adapter registry to resolve `~/.gemini/config/skills`
  directly, leaving `AgentAdapter` single-prefix.
- **Give up on a shared global root and only support `agy --local`.** Skip the
  `--global` scope for this adapter.

## Decision Outcome

Chosen option: "Extend `AgentAdapter` with an optional `global_skill_prefix`",
because it keeps the agent-specific knowledge inside the one adapter entry that
already owns it (ADR 0002's thin-adapter contract), instead of leaking an
agent-name branch into the scope-resolution code that every adapter shares.
`AGENT_ADAPTERS["agy"]` sets `skill_prefix=".agents/skills"` for `--local` and
`global_skill_prefix=".gemini/config/skills"` for `--global`; `agent_bootstrap_actions`
picks the right one once it knows which scope it is building for. Existing
adapters leave `global_skill_prefix` unset and are unaffected.

The special-casing option was rejected because it would have put the first
agent-specific `if` statement into shared scope-resolution code, which ADR 0002
and ADR 0008 both avoided. Dropping `--global` support was rejected because the
captain's intent is parity across all four agent harnesses, and `--local` only
would make `agy` a second-class adapter.

### Consequences

- Good, because the thin-adapter model survives with one new optional field
  rather than a structural rework.
- Good, because `cursor`, `claude-code`, and `codex` adapter behavior is provably
  unchanged — they never set `global_skill_prefix`.
- Good, because `agy --local` and `agy --global` both resolve to real Antigravity
  skill roots with no agent-name branching outside the registry entry.
- Bad, because `.agents/skills` and `.gemini/config/skills` are behaviors of the
  Antigravity CLI verified by direct testing rather than from a stable published
  contract; a future release could change either root and silently break the
  adapter, same risk ADR 0008 already accepted for Codex.
- Neutral, because `.agents/skills` is also the undocumented root Codex scans
  (ADR 0008); the two adapters coincidentally agree on the local path while
  needing different global ones.

## Related

- Decision context: `docs/adr/0002-agent-agnostic-contract-with-thin-adapters.md`
- Install scopes: `docs/adr/0003-global-and-local-skills-install-scope.md`
- Precedent adapter: `docs/adr/0008-codex-adapter-installs-into-repo-local-dot-codex-skills.md`
