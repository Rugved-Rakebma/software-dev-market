# Lock File Format

Defines the schema and conventions for the per-invocation lock file written by `/rnd:c-run`. The lock is the durable execution graph — generated upfront, approved by the user, executed stage-by-stage, and left as a permanent audit trail.

## Purpose

A `c-run` invocation does many things: build, simplify, merge worktrees, verify, triage, fix-up, finalize. Without a lock, the main session improvises step-by-step and the user has no visibility until something pauses. With a lock:

- The user reads ONE document and approves a full execution graph.
- Parallel/sequential structure is explicit.
- Gates between stages are explicit exit conditions.
- Adaptive stages (triage, fix-up) declare their shape upfront and fill leaves at runtime.
- Resume after interrupt is trivial — read the lock, find the first unchecked leaf, continue.

For abstract wave concepts (parallel within wave, sequential between waves, file ownership rules), see `rnd-build/reference/wave-orchestration.md`. This doc covers the lock file itself.

## File Location

```
.rnd/build/runs/{run-id}.md
```

Flat directory. One file per invocation. Permanent (no GC) — the run-id timestamp keeps them ordered and identifiable.

## Run ID Format

```
{scope-prefix}-YYYYMMDD-HHMM
```

| Invocation | Run ID example |
|---|---|
| `/rnd:c-run wave 4` | `wave-04-20260506-1432` |
| `/rnd:c-run phase 2` | `phase-02-20260506-1432` |
| `/rnd:c-run` (all remaining) | `all-20260506-1432` |

## Frontmatter

```yaml
---
run_id: wave-04-20260506-1432
scope: wave 4                    # human-readable scope
trunk: feature/voice-mode        # branch HEAD was on at Stage 1 — merge target for Stages 3 + 6
plans: [04-01-feed-ingestion, 04-02-feed-cache, 04-03-feed-renderer]
status: running                  # running | complete | failed
created: 2026-05-06 14:32
last-updated: 2026-05-06 14:32
fix_loop_count: 0                # increments after each fix-up + re-verify cycle
fix_loop_max: 2                  # aligns with rnd-build escalation-protocol.md max-2-reattempts
---
```

`trunk` is captured per-run from `git rev-parse --abbrev-ref HEAD` at Stage 1.1. Can be any branch — `c-run` does NOT require you to be on `main`. The trunk is the merge target for every Stage 3 and Stage 6 merge; resume verifies HEAD still matches before continuing (see `worktree-merge.md` Resume Behavior).

### Status enum (3 values, no others)

| Status | Meaning |
|---|---|
| `running` | Lock is in flight. Main session is executing stages. Includes "approved but not yet started" and "paused waiting for user input." |
| `complete` | All stages passed gates. Wave is done. Permanent record. |
| `failed` | Aborted before completion. Either user aborted, fix loop exceeded `fix_loop_max`, or an unrecoverable pre-flight check failed. Permanent record with failure reason in last stage. |

No `paused` or `aborted` separate states. Pauses are still `running` (waiting for user). Aborted runs are `failed`.

## Body Structure

Stages are markdown sections. Leaves are checkboxes. Each stage ends with a `gate:` line.

```markdown
## Stage N — {name} (parallel|sequential)

Optional 1-line description.

- [ ] N.1 {leaf description}
- [ ] N.2 {leaf description}
- gate: {exit condition}
```

### Stage header conventions

| Element | Meaning |
|---|---|
| `## Stage N` | Sequential identifier. Stages run in order. |
| `— {name}` | Human-readable name (Build, Verify, Triage, Finalize, etc.). |
| `(parallel)` | Leaves within this stage run concurrently. |
| `(sequential)` | Leaves within this stage run in order. |
| `[ADAPTIVE]` tag | Some leaves filled in mid-run (after a predecessor stage completes). Lock generator writes a placeholder; main session expands at runtime. |
| `[CONDITIONAL — {when}]` tag | Stage may be skipped. Condition stated in the tag (e.g. `[CONDITIONAL — only if Stage 5 found blockers]`). |

### Leaf conventions

```markdown
- [ ] N.M ▶ spawn rnd-coder (foreground): plan {name}
       worktree: feature/run-{run-id}-{plan-name}
       expects: DONE | DONE_WITH_ADVISORIES

- [ ] N.M update .rnd/build/progress.md (status: complete)
```

| Element | Meaning |
|---|---|
| `[ ]` | Not started. |
| `[~]` | In progress. |
| `[x]` | Complete. |
| `[!]` | Failed (with failure note appended on next line). |
| `▶` prefix | This leaf spawns a subagent via the Agent tool. |
| No `▶` | In-session work (file read, git op, decision, write). |
| Indented sub-lines | Parameters for the leaf — agent name, worktree branch, expected return, etc. |

### Gates

```markdown
- gate: all reports collected, no BLOCKED
- gate: clean tree on {trunk}, all branches deleted
- gate: PASS verdict from spec-checker AND no FAIL from reviewer
```

A gate is the exit condition for a stage. The main session blocks at the gate until the condition is met. Gate failures route to PAUSE per `decision-policy.md`.

## Standard Skeleton — Code Wave Run

Eight stages. Apply to every `/rnd:c-run` invocation. Stages 6 and 7 are conditional (skipped if Stage 5's triage found nothing requiring fix-up).

```markdown
## Stage 1 — Pre-flight (sequential)
- [ ] 1.1 capture trunk (current HEAD) and verify clean working tree — record trunk in lock frontmatter
- [ ] 1.2 confirm plans for {scope} exist in .rnd/build/plans/
- [ ] 1.3 read prior wave summary for context handoff
- [ ] 1.4 backlog pre-flight scan: surface open .rnd/backlog/ items whose related-files overlap with this wave's plan files. Recorded as sub-lines under this leaf for Stage 8.5 to re-evaluate. See decision-policy.md Backlog Routing.
- gate: all checks pass

## Stage 2 — Build + Simplify (parallel per plan)
Each plan: spawn rnd-coder in worktree, then code-simplifier on its files (same worktree).
- [ ] 2.1 ▶ spawn rnd-coder + code-simplifier: plan {04-01}
       worktree: feature/run-{run-id}-04-01
- [ ] 2.2 ▶ spawn rnd-coder + code-simplifier: plan {04-02}
       worktree: feature/run-{run-id}-04-02
- [ ] 2.3 ▶ spawn rnd-coder + code-simplifier: plan {04-03}
       worktree: feature/run-{run-id}-04-03
- gate: all coders return DONE | DONE_WITH_ADVISORIES (no BLOCKED, no NEEDS_CONTEXT)

## Stage 3 — Merge worktrees (sequential, dependency order)
- [ ] 3.1 git checkout {trunk}; verify clean
- [ ] 3.2 merge feature/run-{run-id}-04-02 → {trunk} (no-ff) — cache types first
- [ ] 3.3 merge feature/run-{run-id}-04-01 → {trunk} (no-ff)
- [ ] 3.4 merge feature/run-{run-id}-04-03 → {trunk} (no-ff)
- [ ] 3.5 delete worktrees and branches
- [ ] 3.6 commit checkpoint: "build({scope}): merge plans 04-01..03"
- gate: clean tree on {trunk}, no orphan branches/worktrees

## Stage 4 — Verify (parallel)
Scope: files touched in Stage 2.
- [ ] 4.1 ▶ spawn rnd-code-spec-checker
- [ ] 4.2 ▶ spawn rnd-code-reviewer
- [ ] 4.3 ▶ spawn rnd-code-analyst
- gate: all three reports collected

## Stage 5 — Triage (in-session, ADAPTIVE)
Aggregate the three return shapes (each agent returns differently — see decision-policy.md).
- [ ] 5.1 collect verdicts and findings from all three agents
- [ ] 5.2 categorize findings: BLOCKER (mechanical) / BLOCKER (judgment-call) / ADVISORY
- [ ] 5.3 record triage decision: mechanical blockers → Stage 6 auto-fix; advisories → Stage 8 backlog; judgment-call blockers → PAUSE for user
- gate: triage decision recorded; if any judgment-call blocker or hit a pause trigger → PAUSE

## Stage 6 — Fix-up [CONDITIONAL — only if Stage 5 categorized any to-fix items, ADAPTIVE]
Leaves filled at runtime based on Stage 5 categorization.
- [ ] 6.1 ▶ spawn rnd-coder per blocker cluster (worktree per cluster)
- [ ] 6.2 merge fix branches sequentially (no-ff)
- [ ] 6.3 commit: "fix({scope}): address verify blockers"
- [ ] 6.4 fix_loop_count++
- gate: all fix coders DONE | DONE_WITH_ADVISORIES, clean tree

## Stage 7 — Re-verify [CONDITIONAL — only if Stage 6 ran]
- [ ] 7.1 ▶ spawn rnd-code-spec-checker (scope: files from Stage 6)
- [ ] 7.2 ▶ spawn rnd-code-reviewer (scope: files from Stage 6)
- gate: PASS or CONDITIONAL with no remaining blockers
       FAIL + fix_loop_count < fix_loop_max → loop back to Stage 5
       FAIL + fix_loop_count >= fix_loop_max → PAUSE → user

## Stage 8 — Finalize (sequential)
- [ ] 8.1 update .rnd/build/progress.md: move plans built in this run from ## Pending/## In Progress into ## Completed (per-plan bullets); set frontmatter status: complete
- [ ] 8.2 update .rnd/state.md Recent Activity (compression protocol — see commands/c-build.md)
- [ ] 8.3 write .rnd/verifications/{scope}-{date}.md (consolidated verdict)
- [ ] 8.4 backlog dedup + create: scan ALL streams for BACKLOG CANDIDATE markers; dedup against existing open items (same category + file overlap + ≥50% token overlap) — on match, bump seen-count + last-seen on the existing file; on miss, create per commands/backlog.md with required origin tags (discovered-during / discovered-by). See decision-policy.md Stage 8.4.
- [ ] 8.5 backlog auto-close on fix: re-evaluate items surfaced in Stage 1's pre-flight scan. Close with resolution: fixed-incidental when (a) related-files modified in this run AND (b) no new finding in this run matches the item's signature. See decision-policy.md Stage 8.5.
- [ ] 8.6 set this run.md frontmatter status: complete
- gate: none, done
```

Simpler waves (1 plan, no dependencies, clean verify) collapse to ~6 stages with single leaves each. Complex waves with 2 fix loops fan out to ~10 effective stages. Same shape, different leaf counts.

## Resume Semantics

If the lock has `status: running` when `/rnd:c-run` is invoked again with the same scope, a previous invocation was interrupted.

Main session reads the lock, finds the first unchecked or `[~]` leaf, and offers resume:

```
Found prior run: wave-04-20260506-1432 (status: running)
  Stage 2 — Build + Simplify: complete
  Stage 3 — Merge worktrees: in progress (3.2 [~])
  Stages 4-8: pending

Resume from Stage 3.2? (yes/abort)
```

On `abort`: flip `status: failed` with reason "user aborted, replaced by run {new-run-id}".

On `yes`: continue from the first incomplete leaf. Worktrees and branches from the prior session are still on disk — Stage 3 picks up the merge.

The lock file itself is the resume point. No separate progress file needed for in-flight detection.

## See Also

- `decision-policy.md` — what to do when gates fail or findings appear
- `worktree-merge.md` — git mechanics for Stage 3 + Stage 6 merges
- `rnd-build/reference/wave-orchestration.md` — abstract wave concepts (parallel/sequential, file ownership)
- `rnd-build/reference/escalation-protocol.md` — coder status enum referenced in gates
- `rnd-build/reference/handoff-contracts.md` — exact agent input/output shapes
