# Doc filename and lifecycle conventions

## Status

accepted

## Context and Problem Statement

As `docs/ideas/`, `docs/specs/`, and `docs/plans/` accumulate files, it becomes harder to
tell at a glance what is done versus still waiting for implementation, and hard to sort
files chronologically. Separately, `docs/specs/` was mixing prose spec files 1:1 with
Gherkin `.feature` files, which made the folder hard to scan as the number of specs grew.

## Considered Options

- Lifecycle tracking: dedicated `completed/` and `waiting/` folders per doc type, versus
  the existing `## Status` field inside each document (already used by every template).
- Chronological ordering: a `YYYYMMDD-` filename prefix for ideas/specs/plans, versus no
  prefix (relying on file mtime or git history).
- ADR ordering: switch ADRs from sequential numbering to the same date prefix, for visual
  consistency with other doc types, versus keeping sequential numbers.
- Acceptance (BDD) files: keep as a sibling file directly in `docs/specs/`, versus moving
  to a `docs/specs/features/` subfolder.

## Decision Outcome

- Keep lifecycle status in the `## Status` field inside each document (`draft`,
  `accepted`, `completed`, `rejected`, `superseded`, ...) as the single source of truth.
  We do not introduce `completed/`/`waiting/` folders: moving files on every status
  change creates churn (broken relative links in `## Related`, noisy git history) and a
  second source of truth that can drift from the in-document status.
- Prefix Idea, Spec, and Plan filenames with `YYYYMMDD-` so a plain directory listing
  sorts chronologically without extra tooling.
- Keep ADRs on sequential numbering (`NNNN-`). It is a stable citation ID
  (`ADR-0003`) consistent with the MADR/adr-tools convention, and a date prefix would
  still need a counter to disambiguate same-day ADRs — it doesn't remove the need for a
  number, it just makes the number longer.
- Move Gherkin acceptance files from `docs/specs/<spec-slug>.feature` to
  `docs/specs/features/<spec-slug>.feature`, decoupling BDD scenario files from prose
  specs.

### Consequences

- Good, because lifecycle state has exactly one place to check (the `## Status` field),
  with no risk of folder location and status drifting apart.
- Good, because ideas/specs/plans sort chronologically by filename alone.
- Good, because `docs/specs/` now lists only prose specs; acceptance scenarios live
  under `docs/specs/features/`.
- Bad, because seeing "what's done vs waiting" at a glance requires opening files or
  grepping for `## Status` rather than reading a folder listing.
- Bad, because the existing spec file needed a one-time rename
  (`2026-07-07-adrlane-design.md` → `20260707-adrlane-design.md`); any project with
  existing docs adopting this convention needs the same one-time migration.

## More Information

- Naming patterns: `docs/llm/TEMPLATES.md`
- Related spec: `docs/specs/20260707-adrlane-design.md`
