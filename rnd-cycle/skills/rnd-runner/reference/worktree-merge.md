# Worktree Merge

Defines the git mechanics for `/rnd:c-run` Stage 3 (build merges) and Stage 6 (fix-up merges). `rnd-coder` runs with `isolation: worktree` (declared at `agents/rnd-coder.md`), which means each coder spawn produces an isolated git worktree on its own branch. Those branches need to reach the **trunk** — the branch HEAD was on when `/rnd:c-run` was invoked. The trunk can be any branch (not required to be `main`); it is captured at Stage 1 and recorded in the lock's `trunk:` frontmatter.

## Strategy: `git merge --no-ff`

Use **non-fast-forward merges per branch**. Reasoning:

- Preserves the per-task commits the coder produced inside the worktree (audit trail).
- Makes the wave's parallel/sequential structure visible in `git log --graph` — each plan is a fan that re-converges at its merge commit.
- The wrapping wave checkpoint commit at the end of the stage is a single squashable artifact for changelog purposes if you want one.

```bash
git merge --no-ff feature/run-{run-id}-{plan-name} -m "build({scope}): merge plan {plan-name}"
```

Do NOT use:
- `--squash` (loses task-level commits)
- `--ff-only` (fails when there's any divergence; we always have divergence)
- `--rebase` (rewrites history; defeats the audit trail purpose)

## Order: Dependency First

Plans within a wave are independent by planner contract (file ownership rules in `rnd-build/reference/wave-orchestration.md`). But plans across sub-waves within one `c-run` invocation may depend on each other.

When merging:

1. Read the lock's `plans:` frontmatter and the dependency notes in Stage 2 leaves.
2. Topological sort: plans whose outputs others depend on merge first.
3. Within the same dependency level, alphabetical or plan-id order is fine.

Example: lock has plans `[04-01-feed-ingestion, 04-02-feed-cache, 04-03-feed-renderer]` and Stage 2 says `04-03 depends on 04-02`. Merge order:

```
1. 04-02-feed-cache    (no deps)
2. 04-01-feed-ingestion (no deps)
3. 04-03-feed-renderer  (depends on 04-02)
```

If two plans have a true cycle, that's a planner bug — escalate, don't try to resolve.

## Conflict Policy: ESCALATE

If `git merge` returns conflicts:

1. **Do not attempt to auto-resolve.**
2. Run `git merge --abort` immediately to leave the working tree clean.
3. PAUSE → user with:
   - The two branches involved
   - The conflicting files
   - The implication: planner's file-ownership allocation was wrong (Stage 2 plans claimed disjoint files but the actual changes overlap)

The reason is structural: the planner is supposed to enforce that no two same-wave plans modify the same file (`rnd-build/reference/planning-methodology.md` "File ownership rules"). A merge conflict means that contract was violated. Auto-resolving would silently paper over a planner gap.

User options when paused:
- Choose which branch's version wins (manual resolve)
- Abort the run, fix the planner (re-plan the wave)
- Defer the conflicting plan to a later wave

## Cleanup: Remove Worktree + Delete Branch

After each successful merge:

```bash
# Remove the worktree (deletes the isolated working directory)
git worktree remove {worktree-path}

# Delete the branch (it's been merged into the trunk)
git branch -d feature/run-{run-id}-{plan-name}
```

Order matters: remove the worktree BEFORE deleting the branch (otherwise `git worktree remove` may complain about the branch being checked out elsewhere).

If `git worktree remove` fails (uncommitted state in the worktree, which shouldn't happen but might): use `git worktree remove --force`. If the branch has unmerged commits (also shouldn't happen post-merge): use `git branch -D` and capture in the lock why.

Run `git worktree prune` once at the end of Stage 3 to clean up any stale worktree refs.

## Wave Checkpoint Commit

After all per-plan merges in Stage 3, the wave gets ONE summarizing commit:

```bash
git commit --allow-empty -m "build({scope}): merge plans {first}..{last}, {N} plans across {M} sub-waves"
```

The `--allow-empty` is needed because the merges themselves already changed the tree; the checkpoint commit is just a marker. If you prefer, use a tag instead:

```bash
git tag run-{run-id}-build "build merges for {scope}"
```

Tags are cheaper if the user doesn't want extra empty commits cluttering the log. Either is fine — pick one and stick with it per project. Default is the empty commit (visible in `git log`).

## Stage 6 Fix-up Merges

Same rules apply. Differences:

- Fix branches are named `fix/run-{run-id}-{block-id}` (e.g. `fix/run-wave-04-20260506-1432-block-1`).
- Order is fix-id ascending (fixes don't generally have inter-dependencies; if they do, the dependency is in the planner's reasoning).
- Wave checkpoint commit message: `"fix({scope}): address verify blockers ({N} fixes)"`.

## Pre-Flight Check (Stage 1)

Before any worktree spawn, Stage 1 captures the **trunk** for this run and verifies state:

```bash
# Capture HEAD as the run's trunk. Recorded in lock frontmatter for resume safety.
TRUNK=$(git rev-parse --abbrev-ref HEAD)

# Is the working tree clean?
git status --porcelain              # → empty

# Are there any leftover worktrees from a prior aborted run?
git worktree list                   # → only the trunk; no feature/run-* or fix/run-* paths
```

If any check fails:
- Dirty tree → PAUSE: `"uncommitted changes on ${TRUNK}; commit or stash before c-run"`
- Stale worktrees → present them; ask user to confirm cleanup or abort

The trunk can be **any branch** — `/rnd:c-run` no longer requires you to be on `main`. Whatever branch HEAD is on at Stage 1 becomes the merge target for every Stage 3 / Stage 6 merge in this run, and gets recorded in the lock's `trunk:` frontmatter.

## Resume Behavior

If a `c-run` is interrupted mid-merge (Stage 3 partially complete), resuming requires care:

0. **Verify trunk hasn't moved.** Read the lock's `trunk:` frontmatter and compare to `git rev-parse --abbrev-ref HEAD`. If they differ, the user has switched branches between sessions — PAUSE and surface the discrepancy. Continuing would merge into the wrong branch.
1. Read the lock — see which Stage 3 leaves are `[x]` and which are `[ ]` or `[~]`.
2. Check git state: which branches still exist? `git branch | grep feature/run-{run-id}`.
3. For branches whose lock leaf is `[x]`: should already be merged + deleted; verify with `git branch --merged {trunk}` (trunk = lock frontmatter value).
4. For branches whose lock leaf is `[ ]`: the merge hasn't started; resume from there.
5. For branches whose lock leaf is `[~]`: a merge was in progress when interrupted. Check `git status` for `MERGE_HEAD` — if present, the merge is half-done. PAUSE → user to either complete the in-flight merge manually or `git merge --abort` and retry.

The resume contract: lock leaf state must match git state, AND current HEAD must match the recorded trunk. If either diverges, escalate.

## Scope of Git Operations — Local Only

Every git operation in this document is **local**. `/rnd:c-run` never:

- Runs `git push` or any remote-affecting command
- Touches any branch except the trunk (captured at Stage 1) and the per-run `feature/run-*` / `fix/run-*` worktree branches (which it creates and deletes within the same run)
- Touches your other feature branches, shared/release branches, or any remote refs

This is intentional. The runner stops at the local trunk so you have room to manually test the merged result before deciding whether to push. **Pushing is always the user's call, never `c-run`'s.**

If a future change to this skill or to any agent ever introduces a `git push`, `git remote`, or any remote-affecting command, that's a violation of this contract and must be removed.

## See Also

- `lock-format.md` — where Stage 3 and Stage 6 are defined in the lock
- `decision-policy.md` — pause format for conflict and pre-flight failures
- `rnd-build/reference/planning-methodology.md` — file ownership rules the planner enforces (the contract that conflicts violate)
- `rnd-build/reference/wave-orchestration.md` — abstract wave concept; this doc is the git-mechanics layer
- `agents/rnd-coder.md` — `isolation: worktree` declaration that makes this all work
