# Decision Policy

Defines what `/rnd:c-run`'s main session does at each decision point: when to auto-decide, when to pause for the user. The guiding principle is **decide + log, only escalate when no clear path forward** — aligned with the user's stated direction.

## Coder Status Handling

The four return statuses are defined in `rnd-build/reference/escalation-protocol.md`. This table says how `c-run` reacts to each.

| Status | Action | Why |
|---|---|---|
| `DONE` | Continue. Mark leaf `[x]`. | Plan succeeded fully. |
| `DONE_WITH_CONCERNS` | Continue. Scan concerns for `BACKLOG CANDIDATE` markers; queue for Stage 8 backlog creation. Mark leaf `[x]`. | Coder finished but flagged things — those are observations, not blockers. Defer to triage in Stage 5 if any are about wave-scope work. |
| `BLOCKED` | **PAUSE → user.** Mark leaf `[!]` with the blocker note. | Coder explicitly said it cannot proceed. Auto-resolution is out of scope. |
| `NEEDS_CONTEXT` | **PAUSE → user.** Mark leaf `[!]` with the context request. | Coder needs information not in the spawn prompt. Main session can't synthesize that. |

## Verifier Verdict Aggregation

The three verifiers return different shapes (per `rnd-build/reference/handoff-contracts.md`). `c-run` Stage 5 must handle all three.

| Agent | Returns | Notes |
|---|---|---|
| `rnd-code-spec-checker` | `verdict: PASS \| FAIL` + findings array | Each finding has `severity` (typically `blocker` or `suggestion`). |
| `rnd-code-reviewer` | `verdict: PASS \| CONDITIONAL \| FAIL` + `blockers[]` + `suggestions[]` + `integration_map[]` | Blockers and suggestions are pre-separated. |
| `rnd-code-analyst` | `findings[]` + `summary` (no overall verdict) | Each finding has `severity` (`high`/`medium`/`low`) and `category` (`security`/`debt`/etc.). No PASS/FAIL. |

### Aggregation rule

After collecting all three reports, compute the run-level verdict:

```
if spec_checker.verdict == FAIL:                  run_verdict = FAIL
elif reviewer.verdict == FAIL:                    run_verdict = FAIL
elif reviewer.verdict == CONDITIONAL:             run_verdict = CONDITIONAL
elif any(f.severity == 'high' for f in analyst.findings):  run_verdict = CONDITIONAL
else:                                             run_verdict = PASS
```

Then route by run_verdict:
- `PASS` → skip Stages 6 + 7
- `CONDITIONAL` or `FAIL` → run Stage 6 fix-up

## Finding Triage

After aggregation, every individual finding gets routed. Categories:

| Category | Definition | Routing |
|---|---|---|
| **Blocker** | Severity `blocker` or `high`. Wrong behavior, security issue, broken contract. | **Auto-address** in Stage 6. |
| **Clear-fix suggestion** | Severity `suggestion` or `medium`. Fix is unambiguous, scoped to files already touched in this run, and doesn't introduce new abstractions. | **Auto-address** in Stage 6. |
| **Judgment-call suggestion** | Severity `suggestion`. Multiple valid approaches, scope expansion (touches files outside the wave), or design tradeoff. | **PAUSE → user** with the finding and options. |
| **Nit / out-of-scope** | Severity `low` or marked `BACKLOG CANDIDATE` by the verifier. Polish, future work, unrelated debt. | **Auto-backlog** in Stage 8. No fix-up. |

### Clear-fix vs judgment-call decision rule

A suggestion is **clear-fix** when ALL of these hold:
1. The fix is described concretely in the verifier's finding.
2. The fix touches only files already in the run's changed-files set.
3. The fix doesn't introduce a new pattern or abstraction not already in the codebase.
4. The fix is mechanical (rename, validation add, null-check, error case) — not architectural.

If ANY of these fail, treat as **judgment-call** and pause. Better to ask once than to guess wrong.

### Behavior change vs `/rnd:c-verify`

Today's `/rnd:c-verify` surfaces ALL suggestions to the user. `/rnd:c-run` auto-addresses clear-fix suggestions without asking. This is intentional and aligned with the user's preference: "ONLY involved the user if its not a clear solution or path forward." Document this in the lock's Stage 5 description so the user sees what was auto-decided.

## Pause Triggers — Full List

The main session pauses (status stays `running`, lock is updated, user is asked for direction) when:

| Trigger | Stage | What user sees |
|---|---|---|
| Pre-flight check fails (dirty tree, missing plan, missing prior context) | 1 | The failed check + suggested resolution |
| Coder returns `BLOCKED` | 2 or 6 | The blocker note + the plan + what was attempted |
| Coder returns `NEEDS_CONTEXT` | 2 or 6 | The context request + what would unblock |
| Merge conflict during worktree merge | 3 | Files in conflict + the two branches involved (planner gap — escalate, don't auto-resolve) |
| Triage finds a judgment-call suggestion | 5 | The finding + the multiple valid approaches |
| Re-verify FAIL with `fix_loop_count >= fix_loop_max` | 7 | Both fix-loop reports + what was tried each time |

**Not a pause trigger:** clear-fix suggestions, nits, blockers (auto-fix), `DONE_WITH_CONCERNS` (continue + queue for backlog), all-PASS verify (skip to finalize).

### Pause format

When pausing, the main session presents:

```
PAUSE — Stage {N}.{M} — {trigger reason}

Context:
{what was happening}

Finding / Issue:
{the specific finding or error}

Options:
1. {option a}
2. {option b}
3. abort run

Your call?
```

Keep it tight. The user reads, picks. The main session continues the lock with their answer recorded as a sub-line under the leaf.

## Loop Limits

`fix_loop_max: 2` in the lock frontmatter. This aligns with `rnd-build/reference/escalation-protocol.md` ("Max 2 re-attempts per review gate failure").

After Stage 7 re-verify:
- PASS → continue to Stage 8.
- CONDITIONAL with no blockers → continue to Stage 8 (remaining suggestions become backlog).
- FAIL + `fix_loop_count < fix_loop_max` → loop back to Stage 5 (re-triage with new findings, then Stage 6 again).
- FAIL + `fix_loop_count >= fix_loop_max` → PAUSE.

Increment `fix_loop_count` at Stage 6.4 (after fix coders complete, before re-verify).

## Backlog Routing

At Stage 8, scan all sources for `BACKLOG CANDIDATE` markers:

| Source | Where to look |
|---|---|
| Coder concerns | Each coder report's Concerns section (Stage 2 + Stage 6) |
| Spec-checker findings | Findings with severity `suggestion` not auto-addressed |
| Reviewer suggestions | `suggestions[]` array marked `BACKLOG CANDIDATE` or routed as nit |
| Analyst findings | All findings (analyst doesn't auto-route; treat each as backlog candidate) |

For each candidate, create a backlog item per `commands/backlog.md` format:
- Auto-create when category and priority are clear from the marker (e.g. `BUG / medium / src/auth/token.ts:45 / token refresh edge case`).
- Pause to ask the user only when category or priority is ambiguous.

Default category mapping if not specified by the verifier:
- Security findings → `SEC`
- Reviewer blockers not auto-fixed → `BUG`
- Reviewer suggestions (deferred) → `DEBT`
- Analyst debt findings → `DEBT`
- Spec-checker missing-feature findings → `FEAT` (unless explicitly bug)

## Decision Logging

Every auto-decision in Stages 5–8 gets logged in the lock as a sub-line under the relevant leaf:

```markdown
- [x] 5.3 record triage decision
       auto-fix: BLOCK-1 (auth edge case), BLOCK-2 (cache TTL)
       auto-backlog: 4 nits → DEBT items in Stage 8.4
       paused-for-user: 1 judgment-call suggestion (Dashboard loading state)
```

This is the audit trail. Future readers (or future c-run resumes) can see exactly what was auto-decided and why.

## See Also

- `lock-format.md` — where the gates referenced here live in the lock
- `worktree-merge.md` — conflict policy for merge gates
- `rnd-build/reference/escalation-protocol.md` — canonical status definitions
- `rnd-build/reference/handoff-contracts.md` — canonical agent return shapes
- `commands/backlog.md` — backlog item file format
