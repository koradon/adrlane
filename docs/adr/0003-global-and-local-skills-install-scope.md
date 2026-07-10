# Global and local scopes for skills installation

## Status

accepted

## Context and Problem Statement

`adrlane init` installs agent skills into a repository, but developers also want
skills available without initialising every checkout, and a way to refresh skills
after upgrading the `adrlane` package. We needed to decide where installed skills
live and how they are kept current across many repositories.

## Considered Options

- **Two explicit scopes — `--global` and `--local`.** `install`/`upgrade`
  commands take a required, mutually exclusive scope. Global writes to the user
  home directory (agent skill prefixes under `~`); local writes to the current
  repository and requires it to be an adrlane repository.
- **Repository-only.** Skills exist solely inside each repo, installed by `init`;
  no shared/global copy.
- **Auto-detect scope.** Infer global vs local from the working directory instead
  of an explicit flag.

## Decision Outcome

Chosen option: "Two explicit scopes — `--global` and `--local`".

`adrlane skills install|upgrade` requires exactly one of `--local` or `--global`
(`_parse_scope` rejects zero or both). `resolve_skills_target` maps global to
`Path.home()` and local to the current working directory; local additionally
validates that the target is an adrlane repository (`.adrlane/` or
`docs/llm/AGENT_PROTOCOL.md` present). `install` skips existing files; `upgrade`
overwrites packaged skill files and supports `--dry-run`. Both scopes and both
verbs share a single `run_skills` code path.

### Consequences

- Good, because a developer can install skills once globally for all repos, or
  scope them to a single repo, using the same command surface.
- Good, because `upgrade` gives a clear, explicit way to pull new skill content
  after bumping the package, with `--dry-run` to preview.
- Good, because requiring an explicit scope avoids surprising writes to the home
  directory or the wrong repository.
- Bad, because global and local copies can drift; a repo may lag the global set
  until `upgrade --local` is run.
- Bad, because the required-flag design costs a little ergonomics (no implicit
  default scope).

## Related

- Decision context: `docs/adr/0002-agent-agnostic-contract-with-thin-adapters.md`
- Milestone: `.plan/milestones/m2-agent-skills-and-adapters/issues/issue-003-global-and-local-skills-cli.md`
- Design spec: `2026-07-07-adrlane-design.md` (§5.1 Commands)
