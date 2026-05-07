---
name: rnd-runner
description: End-to-end run orchestration for code waves — lock file format, stage execution, decision policy for triage and escalation, worktree merge mechanics. Loaded by main session via /rnd:c-run.
user-invocable: false
---

# R&D Runner

The rnd-runner skill is the methodology behind `/rnd:c-run` — the automated end-to-end runner that takes a wave from build through merge through verify through triage through optional fix-up to finalize, producing a per-invocation lock file as the durable execution graph and audit trail.

This skill is loaded by the **main session** when `/rnd:c-run` is invoked. It is not consumed by subagents.

## Reference Documents

### 1. Lock Format (`reference/lock-format.md`)
**Use when**: Generating, reading, updating, or resuming a `c-run` lock file.

Includes:
- File location and run-id naming convention
- Frontmatter spec (status enum: `running` / `complete` / `failed`)
- Stage header conventions (parallel/sequential, ADAPTIVE, CONDITIONAL tags)
- Leaf states (`[ ]` / `[~]` / `[x]` / `[!]`) and the `▶` subagent-spawn marker
- Gate semantics
- Standard 8-stage skeleton for code wave runs
- Resume semantics

### 2. Decision Policy (`reference/decision-policy.md`)
**Use when**: Deciding whether to auto-address, auto-backlog, continue, or pause for the user. Covers Stage 5 triage and all pause triggers.

Includes:
- Coder status handling (`DONE` / `DONE_WITH_CONCERNS` / `BLOCKED` / `NEEDS_CONTEXT`)
- Verifier verdict aggregation across the three different return shapes
- Finding triage: blocker / clear-fix suggestion / judgment-call suggestion / nit
- The "clear-fix vs judgment-call" decision rule
- Full pause-trigger list with pause format
- Loop limits (`fix_loop_max: 2`)
- Backlog routing rules
- Decision logging format (sub-lines under leaves)

### 3. Worktree Merge (`reference/worktree-merge.md`)
**Use when**: Stage 3 (build merges) or Stage 6 (fix-up merges). Pre-flight checks in Stage 1.

Includes:
- `git merge --no-ff` strategy and rationale
- Merge ordering (dependency-first topo sort)
- Conflict policy (escalate, do not auto-resolve)
- Cleanup: `git worktree remove` + `git branch -d`
- Wave checkpoint commit format
- Pre-flight check commands
- Resume behavior for interrupted merges

## Quick Reference

### Status Enum (lock frontmatter)
| Status | Meaning |
|---|---|
| `running` | In flight or paused for user. Not yet finalized. |
| `complete` | All stages passed. Permanent record. |
| `failed` | Aborted before completion. Permanent record with reason. |

### Coder Status Routing
| Status | Action |
|---|---|
| `DONE` | Continue |
| `DONE_WITH_CONCERNS` | Continue; queue concerns for backlog |
| `BLOCKED` | PAUSE → user |
| `NEEDS_CONTEXT` | PAUSE → user |

### Verifier Aggregation
| Spec-checker | Reviewer | Analyst | Run verdict |
|---|---|---|---|
| FAIL | * | * | FAIL |
| * | FAIL | * | FAIL |
| PASS | CONDITIONAL | * | CONDITIONAL |
| PASS | PASS | any high-severity finding | CONDITIONAL |
| PASS | PASS | no high findings | PASS |

### Finding Triage
| Category | Routing |
|---|---|
| Blocker | Auto-address (Stage 6) |
| Clear-fix suggestion | Auto-address (Stage 6) |
| Judgment-call suggestion | PAUSE → user |
| Nit / out-of-scope | Auto-backlog (Stage 8) |

### Standard Stage Skeleton
| # | Stage | Type |
|---|---|---|
| 1 | Pre-flight | sequential, in-session |
| 2 | Build + Simplify | parallel per plan |
| 3 | Merge worktrees | sequential |
| 4 | Verify | parallel |
| 5 | Triage | in-session, ADAPTIVE |
| 6 | Fix-up | CONDITIONAL, ADAPTIVE |
| 7 | Re-verify | CONDITIONAL |
| 8 | Finalize | sequential |

## Boundary with `rnd-build`

Clean separation, no overlap:

| Skill | Owns |
|---|---|
| `rnd-build` | Agent contracts, reporting formats, escalation protocol, abstract gate definitions, wave-orchestration concepts. Loaded by `rnd-coder` and `rnd-planner`. |
| `rnd-runner` | Lock file format, executable stage sequencing, adaptive triage, worktree merge mechanics. Loaded by main session via `/rnd:c-run`. |

`rnd-runner` reference docs cross-reference `rnd-build` (use, don't redefine). No reverse references.

## Usage Flow

```
/rnd:c-run wave 4
    |
    v
[lock-format] -> Generate run.md with 8 stages, status: running
    |
    v
User reviews + approves the lock
    |
    v
Stage 1 (Pre-flight)  -> in-session checks
Stage 2 (Build+Simp)  -> parallel rnd-coder + code-simplifier per plan, in worktrees
Stage 3 (Merge)       -> [worktree-merge] sequential no-ff merges, escalate conflicts
Stage 4 (Verify)      -> parallel 3 verifiers
Stage 5 (Triage)      -> [decision-policy] aggregate, categorize, route findings
Stage 6 (Fix-up)      -> conditional, ADAPTIVE; spawn coders for fixes
Stage 7 (Re-verify)   -> conditional; max 2 loops
Stage 8 (Finalize)    -> progress.md, state.md, verifications/, backlog/
    |
    v
status: complete; lock left as audit trail
```

## See Also

- `rnd-build/reference/wave-orchestration.md` — abstract wave concepts
- `rnd-build/reference/escalation-protocol.md` — canonical status definitions
- `rnd-build/reference/handoff-contracts.md` — canonical agent return shapes
- `commands/c-run.md` — the entry command that loads this skill
- `commands/c-build.md` — standalone primitive that `c-run` composes
- `commands/c-verify.md` — standalone primitive that `c-run` composes
- `commands/backlog.md` — backlog item file format used in Stage 8
