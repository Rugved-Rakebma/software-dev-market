---
description: Automated end-to-end wave runner — generates a lock, executes 8 stages with gates, auto-triages verify findings, merges worktrees, finalizes. Pauses only when no clear path forward.
argument-hint: [wave N | phase N | all]
---

## When to Use `/rnd:c-run`

Use `c-run` when verify is automatable (tests, golden outputs, spec-checkable behavior) AND you want autonomous completion. The verify-triage-fix loop earns its wall-time only when verify answers your real failure-mode question.

Use **`/rnd:c-build`** instead when:
- The project is UI / feel-based / animation-driven — the questions that matter ("does the eye animation feel right?", "does the layout work in-hand?") only surface on a real device, not from a verifier
- The code is throwaway or prototype — heavy compliance is the wrong investment
- The wave has 1–2 plans — manual worktree merging is cheaper than ceremony

`c-run` automatically lightens itself for `scope: small` projects (verify pipeline skipped — see Proportionality below). But `c-build` is still the right call when verify itself isn't the question you're asking.

## Prerequisites

1. **Check `.rnd/` exists.** If not: "No R&D project found. Run `/rnd:init` first."
2. **Read `.rnd/state.md`** for project context.
3. **Check `.rnd/build/plans/` exists with plans matching `$ARGUMENTS` scope.** If not: "No build plans found for {scope}. Run `/rnd:plan` first."
4. **Verify clean working tree** (no uncommitted changes). The current branch becomes the run's **trunk** — `c-run` branches worktrees off it and merges back to it. Any branch is fine (you do NOT need to be on `main`). If dirty: surface to user.
5. **Local-only guarantee**: `c-run` operates entirely on the local trunk and its per-run worktree branches. It never runs `git push`, never touches any other branch, never modifies remote state. After the run completes, you have room to manually test the trunk and decide whether to push. See `reference/worktree-merge.md` "Scope of Git Operations" for the full contract.
6. **Read project proportionality** from `.rnd/spec/spec.md` frontmatter `scope: small|standard|large`. Default to `small` if absent. Recorded in the lock as `proportionality:` and drives whether Stages 4–7 (verify pipeline) execute or are pre-marked skipped. See "Proportionality Gating" below.

## Resume Check

Scan `.rnd/build/runs/` for any file with frontmatter `status: running` whose `scope:` matches `$ARGUMENTS`. If found:

- A previous `c-run` invocation was interrupted.
- Read the lock, identify the first leaf that is not `[x]`.
- Present to the user: completed stages (✓), in-progress leaf, pending stages.
- Offer: **resume** (continue from the first incomplete leaf) or **abort** (flip prior lock to `status: failed` and start a new run).

See `skills/rnd-runner/reference/lock-format.md` for resume semantics and `skills/rnd-runner/reference/worktree-merge.md` for handling in-flight merges on resume.

## Skill Loading

Load the `rnd-runner` skill. The three reference documents drive every decision in this command:

- `reference/lock-format.md` — schema for the lock file generated in Phase 1
- `reference/decision-policy.md` — what to auto-decide vs pause for in Stages 5–8
- `reference/worktree-merge.md` — git mechanics for Stages 3 + 6

Cross-references into `rnd-build` are used (not duplicated):
- `rnd-build/reference/escalation-protocol.md` — coder status enum
- `rnd-build/reference/handoff-contracts.md` — exact agent input/output shapes
- `rnd-build/reference/reporting-format.md` — how to parse coder reports for `BACKLOG CANDIDATE` markers

## Scope

Parse `$ARGUMENTS`:

| Input | Scope | Run-id prefix |
|---|---|---|
| `wave N` | Single wave N | `wave-{NN}-{YYYYMMDD-HHMM}` |
| `phase N` | All waves in phase N | `phase-{NN}-{YYYYMMDD-HHMM}` |
| (empty) or `all` | All remaining unbuilt waves | `all-{YYYYMMDD-HHMM}` |

If parse fails: "Usage: `/rnd:c-run wave N` | `/rnd:c-run phase N` | `/rnd:c-run` (all remaining)"

## Phase 0 — Backlog Pre-flight Context

Before generating the lock, scan `.rnd/backlog/` for open items whose `related-files` overlap with the upcoming wave's plan `files`. Capture these as sub-lines under leaf 1.4 in the lock — they're not built or fixed by this run, but Stage 8.5 will re-evaluate them for auto-close after Stage 7 passes.

**Interruption note:** Phase 0 produces no persisted artifact until Stage 1.4 records its results. If interrupted before the lock is written (Phase 1), there is no lock to resume — re-invoke `/rnd:c-run` to restart from scratch. The Resume Check only fires once a lock with `status: running` exists.

## Phase 1 — Generate Lock

Construct the lock file at `.rnd/build/runs/{run-id}.md` per `reference/lock-format.md`:

1. **Frontmatter**: `run_id`, `scope` (the run target — `wave N` / `phase N` / `all`), `proportionality` (read from `.rnd/spec/spec.md` `scope:` field, default `small`), `trunk` (capture current HEAD via `git rev-parse --abbrev-ref HEAD` — recorded so Stages 3+6 know where to merge and resume can verify HEAD hasn't moved), `plans` (read from `.rnd/build/plans/` matching scope), `status: running`, `created`, `last-updated`, `fix_loop_count: 0`, `fix_loop_max: 2`.

2. **Body**: write all 8 stages from the standard skeleton. For each stage:
   - Stage 1 (Pre-flight): static checks + backlog scan (surface items whose related-files overlap with this wave's plan files)
   - Stage 2 (Build + Simplify): one leaf per plan, with the plan name and the worktree branch name `feature/run-{run-id}-{plan-name}`
   - Stage 3 (Merge): one merge leaf per plan, ordered by plan dependencies (read each plan's frontmatter for deps); plus delete + checkpoint commit leaves
   - Stage 4 (Verify): two fixed leaves (spec-checker, reviewer). Analyst is NOT spawned — opt-in via `/rnd:audit` post-run.
   - Stage 5 (Triage): tagged `[ADAPTIVE]`; placeholder leaves for "collect verdicts," "categorize findings," "record triage decision"
   - Stage 6 (Fix-up): tagged `[CONDITIONAL — only if Stage 5 categorized to-fix items, ADAPTIVE]`; placeholder leaves
   - Stage 7 (Re-verify): tagged `[CONDITIONAL — only if Stage 6 ran]`; two fixed leaves (spec-checker, reviewer)
   - Stage 8 (Finalize): six static leaves (progress, state, verifications, backlog dedup+create with origin tags, backlog auto-close-on-fix, mark complete)

3. **Proportionality Gating** (B): if `proportionality: small`, pre-mark ALL leaves in Stages 4, 5, 6, 7 as `[x] skipped — verify not load-bearing at small scope`. Set each stage's gate to `gate: skipped`. Execution jumps from Stage 3 directly to Stage 8. No verifier agents spawn. Stage 8.3 (verification report) is also skipped.

4. **Gates**: write a `gate:` line at the end of every stage per `reference/lock-format.md`.

## Phase 2 — Present + Approve

Show the lock file to the user. Tight presentation:

```
━━━ Run Plan — {run-id} ━━━

Scope: {scope}
Plans: {N}
Stages: 8 (Stages 6+7 conditional)
Worktrees: {N} (one per plan)
Estimated subagent spawns: {N coders + N simplifiers + 3 verifiers + ~N fix-up coders}

Lock saved to: .rnd/build/runs/{run-id}.md

Approve and execute? (yes / edit / abort)
```

- **yes**: continue to Phase 3.
- **edit**: tell the user the lock is at `{path}` and to edit it manually, then re-invoke `/rnd:c-run` (resume check picks it up).
- **abort**: flip lock to `status: failed`, reason "user aborted before execution."

### Task list setup (stage-level granularity)

On approval, create **8 stage-level Tasks** via `TaskCreate` — one per stage:
1. Pre-flight
2. Build + Simplify
3. Merge worktrees
4. Verify
5. Triage
6. Fix-up
7. Re-verify
8. Finalize

The lock file is the leaf-level execution graph; Tasks track stage-level progress for live visibility. Mark Task 1 `in_progress` immediately after creation. Do NOT create one Task per leaf — that floods the panel.

For adaptive stages (5/6/7), append dynamic sub-Tasks via `TaskCreate` as findings materialize (e.g. `Triage: 4 findings → 2 auto-fix, 1 backlog, 1 paused`, `Fix-up: cluster 1 — auth race`). These sub-Tasks complete alongside their parent stage.

On any pause, the current stage Task stays `in_progress`, and its `subject` is updated via `TaskUpdate` to name the blocker (e.g. `Stage 5 — paused on judgment-call: dashboard loading state`). When the user resolves and the run resumes, restore the stage's neutral subject.

## Phase 3 — Execute Stages

Iterate stages 1 through 8 in order. For each stage, iterate leaves per the stage's parallel/sequential annotation.

### Stage transitions (Tasks)

When entering a stage: `TaskUpdate` the corresponding stage Task to `in_progress`.
When the stage's gate passes: `TaskUpdate` to `completed`.
On pause: see "Task list setup" above.

### Per-leaf execution (lock only)

1. Mark leaf `[~]` in the lock.
2. Execute the leaf:
   - In-session work: do it directly (file read, git op, decision recording).
   - `▶` subagent spawn: use the **Agent tool** with the spec from the leaf's sub-lines.
3. Collect the result. On success: mark `[x]` in lock. On failure: mark `[!]` with note, route per `reference/decision-policy.md`.
4. Update lock frontmatter `last-updated`.

Per-leaf transitions update only the lock. The Task tracker remains stage-level.

### Per-stage gate

After all leaves in a stage are complete, evaluate the `gate:` line:
- Gate satisfied → `TaskUpdate` stage Task to `completed`, proceed to next stage.
- Gate not satisfied → consult `reference/decision-policy.md`. Either auto-decide (e.g. CONDITIONAL verdict → fix-up) or PAUSE.

### Stage-specific subagent spawns

#### Stage 2 — Build + Simplify (per plan, parallel)

For each plan in the wave:

**Spawn rnd-coder via the Agent tool:**
- **description**: "Build: {plan name}"
- **model**: opus
- **prompt**: Include three inline blocks per `rnd-build/reference/handoff-contracts.md`:
  - **`plan_text`** — full plan inline (coder NEVER reads plan files)
  - **`arch_slices`** — sections of `.rnd/architecture/current.md` referenced by the plan's `## Wires to` section (parse the bullets, fetch those sections). Fallback: full arch if Wires to absent.
  - **`spec_req_rows`** — rows from `.rnd/spec/spec.md` for the REQ-IDs in the plan's `requirements` frontmatter.
  - Plus: project context from `.rnd/state.md`, prior wave summaries, references to `rnd-build/reference/execution-methodology.md` and `rnd-build/reference/escalation-protocol.md`.

The coder runs in worktree isolation (declared in `agents/rnd-coder.md`); the spawn returns the worktree path and branch.

**Then spawn code-simplifier via the Agent tool** (same conversation, same worktree):
- **description**: "Simplify: {plan name} files"
- **prompt**: Target the files changed by the coder (from coder's report)

Per `reference/decision-policy.md`:
- `DONE` / `DONE_WITH_ADVISORIES` → continue, queue advisories for Stage 8 backlog
- `BLOCKED` / `NEEDS_CONTEXT` → PAUSE

#### Stage 3 — Merge worktrees (sequential)

Follow `reference/worktree-merge.md`:
1. Checkout the trunk (lock frontmatter's `trunk:` value), verify clean.
2. For each plan in dependency order: `git merge --no-ff {branch} -m "build({scope}): merge plan {name}"`.
3. On conflict: `git merge --abort`, PAUSE per `decision-policy.md` (planner gap).
4. After all merges: `git worktree remove {path}` + `git branch -d {branch}` per plan.
5. Wave checkpoint commit: `git commit --allow-empty -m "build({scope}): merge plans {first}..{last}"`.

#### Stage 4 — Verify (parallel)

**Skipped entirely** if `proportionality: small` (Stages 4–7 pre-marked `[x] skipped` in Phase 1; execution jumps to Stage 8).

Otherwise, **two** Agent tool spawns in parallel:

**rnd-code-spec-checker** — see `commands/c-verify.md` for the established prompt structure.
**rnd-code-reviewer** — same.

Both receive the files-changed list from Stage 2 + Stage 3 (effectively `git diff {trunk}~{N}..{trunk} --name-only` where `{trunk}` is the lock's trunk and N = number of merge commits).

**`rnd-code-analyst` is intentionally NOT part of c-run's default verify.** STRIDE+OWASP audit is heavyweight and only load-bearing for production-bound services. For security/audit review, run `/rnd:audit` on this run's diff after c-run completes — see After Completion below.

#### Stage 5 — Triage (in-session, ADAPTIVE)

Aggregate the three reports per `reference/decision-policy.md`:

1. Compute run verdict from the verdict-aggregation table (PASS / CONDITIONAL / FAIL).
2. For each finding, tag BLOCKER or ADVISORY (verifier already split these).
3. Record decisions as sub-lines under leaf 5.3.
4. **ADVISORY findings** → route to Stage 8 backlog. Never trigger Stage 6.
5. **BLOCKER findings (mechanical)** → expand Stage 6 with leaves per cluster.
6. **BLOCKER findings (judgment-call: multi-approach or scope expansion)** → PAUSE for user.
7. If run verdict is PASS or CONDITIONAL → mark Stage 6 + 7 skipped (`[x]` with note "skipped — no blockers"). CONDITIONAL means advisories present but no blockers; advisories still route to Stage 8 backlog.

#### Stage 6 — Fix-up (CONDITIONAL on FAIL verdict, ADAPTIVE)

Stage 6 runs ONLY on FAIL verdict (blockers present). On CONDITIONAL (advisories only), this stage is skipped — advisories already routed to Stage 8 backlog in triage.

Cluster blockers by file proximity (findings touching the same file or adjacent files = one cluster, one fix coder).

For each cluster:
- Spawn `rnd-coder` per the Stage 2 pattern (plan + arch slice + spec slice bundle), prompt scoped to the cluster's blockers.
- Worktree: `fix/run-{run-id}-block-{N}`.
- Same status routing as Stage 2.

After all fix coders complete:
- Merge per `reference/worktree-merge.md` (sequential, no-ff).
- Commit: `git commit --allow-empty -m "fix({scope}): address verify blockers ({N} fixes)"`.
- Increment `fix_loop_count` in lock frontmatter.

#### Stage 7 — Re-verify (CONDITIONAL)

Spawn `rnd-code-spec-checker` and `rnd-code-reviewer` (skip analyst — re-running audit on the same files is redundant unless the user requests it).

Gate per `reference/decision-policy.md`:
- PASS → Stage 8.
- CONDITIONAL (advisories only, no remaining blockers) → Stage 8 (advisories become backlog).
- FAIL + `fix_loop_count < fix_loop_max` → loop back to Stage 5 (re-triage blockers, then Stage 6 again).
- FAIL + `fix_loop_count >= fix_loop_max` → PAUSE.

#### Stage 8 — Finalize (sequential)

1. **Update `.rnd/build/progress.md`**: move plans built in this run from `## Pending` / `## In Progress` into `## Completed` (per-plan bullets, per the c-build schema). Set frontmatter `status: complete`. Same file format as `/rnd:c-build`.
2. **Update `.rnd/state.md`** Recent Activity:
   - `{today's date}: Run {run-id} via /rnd:c-run — {scope}, {N} plans, run verdict: {PASS|CONDITIONAL|FAIL}, fix loops: {fix_loop_count}`
   - Follow compression protocol: keep under 120 lines, compress oldest Recent Activity entries into History phase summaries when exceeding 15 entries. Never delete entries.
3. **Write `.rnd/verifications/{scope}-{date}.md`** — consolidated verdict report from Stages 4 + 7 (use the same template as `/rnd:c-verify`). **Skipped if `proportionality: small`** (no verify ran, no report to write).
4. **Backlog dedup + create**: scan all sources per `reference/decision-policy.md` Backlog Routing → Stage 8.4:
   - Coder concerns from Stages 2 + 6
   - Verifier findings flagged BACKLOG CANDIDATE or routed as nit
   - Analyst findings (all)
   - For each candidate: dedup against existing open items first (same category + overlapping related-files + description token overlap ≥ 50%). On match → increment `seen-count` + update `last-seen` on the existing item. On miss → auto-create per `commands/backlog.md` format with required origin tags (`discovered-during: /rnd:c-run {run-id}`, `discovered-by: {agent-name}`).
   - For ambiguous category/priority: pause once at the end with a list, ask the user to bulk-decide.
5. **Backlog auto-close on fix**: re-evaluate the open items surfaced in Stage 1.4's pre-flight scan. Signal-based test (NOT code-pattern grep): an item closes when (a) its `related-files` overlap with this run's diff AND (b) the dedup check in 8.4 found no new finding matching the item's signature. Close with `resolution: fixed-incidental`, move to `.rnd/backlog/closed/`. Items where the symptom recurred (8.4 matched and bumped `seen-count`) stay open. Log decisions as sub-lines per `reference/decision-policy.md` Stage 8.5.
6. **Mark this run.md frontmatter `status: complete`**.

## After Completion

Print a tight summary:

```
━━━ Run Complete — {run-id} ━━━

Verdict: {PASS|CONDITIONAL|FAIL}
Plans built: {N}
Fix loops: {fix_loop_count}/{fix_loop_max}
Backlog items created: {N}

Artifacts:
  Lock: .rnd/build/runs/{run-id}.md (status: complete)
  Progress: .rnd/build/progress.md (per-plan entries appended to ## Completed)
  Verification: .rnd/verifications/{scope}-{date}.md     ← omitted if proportionality: small
  Backlog: {paths if any created}

Next:
  - For security/audit review, run `/rnd:audit` on this run's diff.
  - Review the verification report (if present), then `/rnd:c-run` next wave.
```

## On Failure or Abort

If the run is aborted (user aborts at a pause, fix loop exceeded, pre-flight unrecoverable):

1. Set lock frontmatter `status: failed`.
2. Append a `## Failure` section at the bottom of the lock with:
   - Stage where it failed
   - Reason (paste the failed gate or the user's abort note)
   - Git state at time of failure (current branch, any in-flight merge, leftover worktrees)
3. Update `.rnd/state.md` Recent Activity: `{date}: Run {run-id} failed at Stage {N} — {reason}`.
4. Do NOT delete worktrees or branches on failure — leave them for the user to inspect or for resume.
