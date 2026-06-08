# Decision Policy

Defines what `/rnd:c-run`'s main session does at each decision point: when to auto-decide, when to pause for the user. The guiding principle is **decide + log, only escalate when no clear path forward** — aligned with the user's stated direction.

## Coder Status Handling

The four return statuses are defined in `rnd-build/reference/escalation-protocol.md`. This table says how `c-run` reacts to each.

| Status | Action | Why |
|---|---|---|
| `DONE` | Continue. Mark leaf `[x]`. | Plan succeeded fully. |
| `DONE_WITH_ADVISORIES` | Continue. Scan advisories for `BACKLOG CANDIDATE` markers; queue for Stage 8 backlog creation. Mark leaf `[x]`. | Coder finished and flagged advisories — observations, not blockers. Advisories never gate fix-up. |
| `BLOCKED` | **PAUSE → user.** Mark leaf `[!]` with the blocker note. | Coder explicitly said it cannot proceed. Auto-resolution is out of scope. |
| `NEEDS_CONTEXT` | **PAUSE → user.** Mark leaf `[!]` with the context request. | Coder needs information not in the spawn prompt. Main session can't synthesize that. |

## Verifier Verdict Aggregation

`c-run` Stage 5 aggregates two verifier reports (per `rnd-build/reference/handoff-contracts.md`). `rnd-code-analyst` is intentionally NOT part of c-run's verify pipeline — opt in separately via `/rnd:audit` for STRIDE+OWASP review.

| Agent | Returns | Notes |
|---|---|---|
| `rnd-code-spec-checker` | `verdict: PASS \| FAIL` + findings array | FAIL = REQ-blocker present. Each finding tagged BLOCKER or ADVISORY. |
| `rnd-code-reviewer` | `verdict: PASS \| CONDITIONAL \| FAIL` + `blockers[]` + `advisories[]` + `integration_map[]` | PASS = no findings. CONDITIONAL = advisories only. FAIL = blockers present. |

### Proportionality gating

For `proportionality: small`, Stages 4–7 are skipped entirely. No verifier reports collected; no triage; aggregation rule below does not run. Advisories surfaced by Stage 2 coders still route to Stage 8.4 backlog. For `standard` / `large`, the aggregation rule below applies.

### Aggregation rule

After collecting both reports, compute the run-level verdict:

```
if spec_checker.verdict == FAIL:        run_verdict = FAIL          # blockers present
elif reviewer.verdict == FAIL:          run_verdict = FAIL          # blockers present
elif reviewer.verdict == CONDITIONAL:   run_verdict = CONDITIONAL   # advisories only
else:                                   run_verdict = PASS
```

Then route by run_verdict:
- `PASS` → skip Stages 6 + 7
- `CONDITIONAL` → skip Stage 6 fix-up; advisories route directly to Stage 8 backlog
- `FAIL` → run Stage 6 fix-up (blockers only)

## Finding Triage

After aggregation, every individual finding gets routed. Two buckets:

| Category | Definition | Routing |
|---|---|---|
| **BLOCKER** | Wrong behavior, security issue, broken contract, missing REQ. Tagged BLOCKER by the verifier. | **Auto-address** in Stage 6 fix-up. |
| **ADVISORY** | Polish, debt, partial-met optimization, adjacent improvement. Tagged ADVISORY by the verifier (often with `BACKLOG CANDIDATE` marker). | **Auto-backlog** in Stage 8. No fix-up. |

**Special case: judgment-call blockers.** A finding tagged BLOCKER with multiple valid resolutions or scope expansion outside the wave → **PAUSE → user** with the finding and options. The bias is to auto-fix mechanical blockers and pause only when the resolution path is unclear.

### Mechanical-blocker vs judgment-call decision rule

A BLOCKER is **mechanical** (auto-fix in Stage 6) when ALL of these hold:
1. The fix is described concretely in the verifier's finding.
2. The fix touches only files already in the run's changed-files set.
3. The fix doesn't introduce a new pattern or abstraction not already in the codebase.
4. The fix is mechanical (rename, validation add, null-check, error case) — not architectural.

If ANY of these fail, treat as **judgment-call** and pause. Better to ask once than to guess wrong.

ADVISORIES never trigger fix-up regardless. They always route to backlog.

### Behavior change vs `/rnd:c-verify`

Today's `/rnd:c-verify` surfaces ALL findings to the user. `/rnd:c-run` auto-addresses mechanical blockers without asking and auto-backlogs advisories. This is intentional and aligned with the user's preference: "ONLY involve the user if its not a clear solution or path forward." Document this in the lock's Stage 5 description so the user sees what was auto-decided.

## Pause Triggers — Full List

The main session pauses (status stays `running`, lock is updated, user is asked for direction) when:

| Trigger | Stage | What user sees |
|---|---|---|
| Pre-flight check fails (dirty tree, missing plan, missing prior context) | 1 | The failed check + suggested resolution |
| Coder returns `BLOCKED` | 2 or 6 | The blocker note + the plan + what was attempted |
| Coder returns `NEEDS_CONTEXT` | 2 or 6 | The context request + what would unblock |
| Merge conflict during worktree merge | 3 | Files in conflict + the two branches involved (planner gap — escalate, don't auto-resolve) |
| Triage finds a judgment-call blocker | 5 | The finding + the multiple valid approaches |
| Re-verify FAIL with `fix_loop_count >= fix_loop_max` | 7 | Both fix-loop reports + what was tried each time |

**Not a pause trigger:** mechanical blockers (auto-fix), advisories (auto-backlog), `DONE_WITH_ADVISORIES` (continue + queue for backlog), all-PASS verify (skip to finalize), `CONDITIONAL` verify (skip fix-up, route advisories to backlog).

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

`fix_loop_max: 2` in the lock frontmatter. This aligns with `rnd-build/reference/escalation-protocol.md` ("Max 2 re-attempts per review gate failure"). **The loop only fires on blockers** — advisories never trigger a loop.

After Stage 7 re-verify:
- PASS → continue to Stage 8.
- CONDITIONAL (advisories only, no blockers) → continue to Stage 8 (advisories become backlog).
- FAIL + `fix_loop_count < fix_loop_max` → loop back to Stage 5 (re-triage blockers, then Stage 6 again).
- FAIL + `fix_loop_count >= fix_loop_max` → PAUSE.

Increment `fix_loop_count` at Stage 6.4 (after fix coders complete, before re-verify).

## Backlog Routing

Backlog is an active queue, not a write-only log. Three policies govern how `/rnd:c-run` interacts with it: **pre-flight scan** (Stage 1), **auto-close on fix** (Stage 8), and **dedup-aware create with origin tagging** (Stage 8.4).

### Pre-flight scan (Stage 1)

Before building, scan `.rnd/backlog/` for open items whose `related-files` overlap with the upcoming wave's plan `files`. Surface them in the pre-flight summary:

```
Backlog context for this wave:
- BUG-008 (medium, 12d): "Null pointer when user.profile is undefined" — src/profile/loader.ts
- UX-003 (medium, seen 3x): "Loading state missing on Dashboard" — src/components/Dashboard.tsx
```

The wave's coders are not told to fix these — but the human reviewing the lock now knows that relevant items exist. After Stage 7 passes, the auto-close check below will re-evaluate them.

### Stage 8.4 — Create with dedup + origin tags

For each `BACKLOG CANDIDATE` marker scanned from:

| Source | Where to look |
|---|---|
| Coder advisories | Each coder report's Advisories section (Stage 2 + Stage 6) |
| Spec-checker findings | Findings tagged ADVISORY |
| Reviewer advisories | `advisories[]` array (all are backlog candidates) |

(Analyst findings are not a c-run source — `rnd-code-analyst` runs via `/rnd:audit`, which writes its own findings into the audit report directly.)

**Step 1 — Dedup check.** Before creating a new file, scan existing open items in `.rnd/backlog/`. A match exists when ALL of:
- Same `category`
- `related-files` overlap (at least one file in common)
- Description tokens overlap ≥ 50% (simple token match — stop-word stripped)

On match: **do not create a new file**. Update the existing item:
- `seen-count` += 1 (treat missing field as 0, so first dedup sets it to 1, then 2 on next match)
- `last-seen` = today's date (set if missing)
- Append a one-line note to the item's Context section: `- Seen again in run {run-id} by {agent}.`

**Backward compatibility:** pre-existing backlog items created before this policy was introduced may lack `seen-count`, `last-seen`, `discovered-during`, and `discovered-by`. The runner treats missing fields as defaults (`seen-count` → 0 pre-increment; `last-seen` → item's `discovered` date; origin tags → leave absent). Never error on missing optional fields.

**Step 2 — Origin tagging (required on auto-create).** When creating a new item, the runner populates these fields from its own context — agents do not need to emit them:
- `discovered-during: /rnd:c-run {run-id}`
- `discovered-by: {agent-name}` (e.g. `rnd-code-reviewer`)
- `seen-count: 1`
- `last-seen: {today}`

Origin tags are **required** on auto-create. If the runner cannot determine `discovered-by` from the source, log this as a triage bug and pause (the agent emitting the BACKLOG CANDIDATE marker should be identifiable from the source).

**Step 3 — Category/priority defaults.** Auto-create when category and priority are clear from the marker. Pause to ask the user only when ambiguous.

Default category mapping if not specified by the verifier:
- Security findings → `SEC`
- Reviewer blockers not auto-fixed → `BUG`
- Reviewer suggestions (deferred) → `DEBT`
- Analyst debt findings → `DEBT`
- Spec-checker missing-feature findings → `FEAT` (unless explicitly bug)

### Stage 8.5 — Auto-close on fix

After the new advisories are created/merged, check the open items surfaced in Stage 1.4's pre-flight scan. The auto-close test is **signal-based**, not code-pattern-based — the runner can't reliably grep for arbitrary patterns described in prose.

**Auto-close criteria (must ALL hold):**
1. The item's `related-files` overlap with this run's diff files (the wave actually touched the relevant code).
2. **No new finding** in this run matches the item's signature — i.e. the dedup check in 8.4 did NOT find a match for any new advisory against this item. (If the symptom recurred, 8.4 would have bumped `seen-count` and we'd see it; absence is the signal.)

When both hold: auto-close with `resolution: fixed-incidental`. Log under Stage 8 leaves:
```markdown
- [x] 8.5 backlog auto-close
       closed-by-fix: BUG-008 (profile loader modified in wave-06, no recurrence in verify)
       no-change: SEC-003 (related-files not touched this run)
```

When criterion 1 holds but criterion 2 doesn't (the item's symptom recurred), leave open and let 8.4's seen-count bump capture the recurrence. When neither holds, leave open. The next `/rnd:backlog sweep` will surface candidates manually.

**Why this is conservative.** We never claim "the bug is gone" — only "files moved and no new finding flagged this". A user-invoked sweep is the safety net for items where the runner's signal isn't strong enough.

### Sweep (advisory, user-invoked)

`/rnd:backlog sweep` runs the full triage report — aging, recurring symptoms, dedup candidates, resolution candidates — and surfaces them for the user to manually close or promote. The sweep itself never mutates state. See `commands/backlog.md` for sweep heuristics + promote policy.

## Decision Logging

Every auto-decision in Stages 5–8 gets logged in the lock as a sub-line under the relevant leaf:

```markdown
- [x] 5.3 record triage decision
       auto-fix: BLOCK-1 (auth edge case), BLOCK-2 (cache TTL)
       auto-backlog: 4 nits → DEBT items in Stage 8.4
       paused-for-user: 1 judgment-call blocker (Dashboard loading state — multiple valid approaches)
```

This is the audit trail. Future readers (or future c-run resumes) can see exactly what was auto-decided and why.

## See Also

- `lock-format.md` — where the gates referenced here live in the lock
- `worktree-merge.md` — conflict policy for merge gates
- `rnd-build/reference/escalation-protocol.md` — canonical status definitions
- `rnd-build/reference/handoff-contracts.md` — canonical agent return shapes
- `commands/backlog.md` — backlog item file format
