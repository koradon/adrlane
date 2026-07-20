# Dedicated `adrlane upgrade` command for package-owned content

## Status

accepted

## Context and Problem Statement

`adrlane init` is intentionally idempotent: re-running it never overwrites an
existing file, so it never destroys documentation content a developer or agent
has written. That guarantee has a side effect: `docs/llm/*` contract files and
`.adrlane/bootstrap-version` also never update after the first `init`, even
after the `adrlane` package ships new contract wording or templates. `adrlane
skills upgrade` already solves this for agent skill files, but there was no
equivalent for the rest of the package-owned bootstrap content. This was a
known gap, flagged as an open question in the design spec (§12).

## Considered Options

- **Add `--upgrade` flag to `init`.** `adrlane init --upgrade` overwrites all
  packaged files; plain `init` stays additive. Keeps one command, but mixes two
  different safety contracts (idempotent vs. overwriting) behind one verb
  distinguished only by a flag.
- **Make plain `init` always overwrite package-owned files.** Simplest surface,
  but breaks the documented "`init` never destroys content" guarantee and
  would silently rewrite `docs/llm/*` on every re-run, including cases where a
  developer intentionally hand-edited a contract file.
- **New `adrlane upgrade` command**, mirroring `adrlane skills upgrade` at the
  top level. `init` keeps its current additive/idempotent contract untouched;
  `upgrade` is a separate verb whose entire job is to overwrite package-owned
  content and is safe to run repeatedly after bumping the package.

## Decision Outcome

Chosen option: "New `adrlane upgrade` command".

`adrlane upgrade` (`src/adrlane/upgrade.py::run_upgrade`) overwrites:

- `docs/llm/*` contract files and templates (`framework_bootstrap_actions`,
  a filtered view of the packaged doc templates restricted to the `llm/`
  prefix),
- `.adrlane/bootstrap-version`,
- local agent skill files, by delegating to the existing
  `run_skills(..., upgrade=True)` used by `skills upgrade --local`.

It never touches user-owned content: `docs/README.md`, `docs/ideas/README.md`,
`docs/roadmap/README.md` (living docs the growth model expects agents to
edit), the contents of `docs/{specs,plans,adr,ideas,roadmap}`, or
`.adrlane/workspace.yaml`. It requires an existing `.adrlane/` bootstrap
(`is_adrlane_repository`) and supports `--dry-run` and `--agent`, matching the
existing `init`/`skills upgrade` conventions.

`init` is unchanged: still purely additive, still never overwrites an
existing file.

### Consequences

- Good, because `init`'s "never destroys content" guarantee stays true and
  unambiguous — there is no flag that silently changes its behavior.
- Good, because one command (`adrlane upgrade`) is the answer to "how do I
  pick up new contract/template/skill content after bumping the package,"
  matching the existing `skills upgrade` mental model.
- Good, because the framework/user-owned split is enforced by a single
  filter (`framework_bootstrap_actions`'s `llm/` prefix check) rather than
  scattered exclusion lists.
- Bad, because there are now three related verbs (`init`, `skills upgrade`,
  `upgrade`) instead of one, which a new user has to learn.
- Bad, because `upgrade` and `skills upgrade --local` overlap for the skills
  portion; running both is harmless but redundant.

## Related

- Design spec: `20260707-adrlane-design.md` (§5.1 Commands, §12 Open Questions)
- Precedent: `docs/adr/0003-global-and-local-skills-install-scope.md`
- Bootstrap idempotency: `docs/adr/0002-agent-agnostic-contract-with-thin-adapters.md`
