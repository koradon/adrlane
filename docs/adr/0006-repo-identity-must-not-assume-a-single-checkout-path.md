# Repo identity must not assume a single checkout path

## Status

accepted

## Context and Problem Statement

Captain's Log — a global `commit-msg` hook that logs every commit on the machine into a
separate dedicated log repo — broke in two related ways once repos started being accessed
through pooled/worktree checkouts (e.g. treehouse's worktree pools under `~/.treehouse/`)
instead of a single canonical clone path per repo:

1. **Cross-repo git subprocess calls silently target the wrong repo.** Git sets `GIT_DIR` and
   `GIT_INDEX_FILE` in a hook's environment for the whole duration of the hook, pointing at the
   *invoking* worktree's private gitdir/index. `git -C <other-repo>` only changes the directory
   used to search for a repo — it does **not** override an already-set `GIT_DIR`/`GIT_INDEX_FILE`.
   So every `git -C <log-repo> ...` call the hook made was actually reading/writing the
   *invoking* worktree's refs and index, not the log repo's — reproduced live: it marked a
   tracked file in the invoking worktree as deleted purely from an "add" targeting a
   completely different repo, and in real usage it clobbered real commits (`fatal: cannot lock
   ref 'HEAD'`) in `planhub`/`facts-service` worktrees.
2. **Path-based repo grouping breaks for checkouts that live elsewhere.** Project/repo grouping
   matched a repo to its parent project by filesystem ancestry (`configured-root in
   repo-path.parents`). That works for a canonical clone nested under an umbrella project
   directory, but a pooled worktree of the same repo lives under `~/.treehouse/...` with no
   shared path ancestor at all — so it silently fell back to being treated as its own
   standalone project instead of grouping with its siblings.

Both bugs share a root cause: tooling assumed a repo has exactly one stable checkout location,
and that assumption is false the moment worktree pooling (treehouse or plain `git worktree`)
enters the picture.

## Considered Options

- Leave repo-identifying tools as-is and treat pooled worktrees as an unsupported edge case.
- Fix only the specific symptom encountered (e.g. hardcode around one repo's path).
- Fix at the mechanism level: never let inherited git env vars leak into a cross-repo git call,
  and never assume repo identity/grouping can be derived from a single fixed path.

## Decision Outcome

Chosen option: "Fix at the mechanism level", because pooled/worktree checkouts are now a normal
part of this environment (treehouse dispatches many agents into pooled worktrees across many
repos), so any tool that shells out to git across a repo boundary, or that identifies/groups a
repo by name, will keep hitting this class of bug otherwise.

The concrete fixes landed in Captain's Log (`captains-log` repo):

- Every git subprocess call that targets a repo other than "whichever repo the process happened
  to be invoked from" now runs with `GIT_DIR`, `GIT_INDEX_FILE`, `GIT_WORK_TREE`, and
  `GIT_COMMON_DIR` stripped from its environment.
- Repo-to-project grouping now also matches a repo by name against the nested git repos found
  directly under a configured project's root, so a repo checked out elsewhere (a pooled
  worktree) still groups with its canonical siblings.

### Consequences

- Good, because any tool in this environment that shells out to git against a different repo
  than it was invoked from, or that groups/identifies repos, now has a documented convention to
  follow: strip inherited `GIT_*` env vars before cross-repo git calls, and don't assume repo
  identity is derivable from one fixed filesystem path.
- Bad, because it adds a small amount of defensive plumbing (an explicit `env=` on every git
  subprocess call, a directory scan for grouping) that wouldn't be necessary in a world without
  worktree pooling.
- Bad, because the name-based grouping fallback is a heuristic (directory-name match), not a
  guarantee — two unrelated repos with the same directory name nested under different roots
  could theoretically collide.
