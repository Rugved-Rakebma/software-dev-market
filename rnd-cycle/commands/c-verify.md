---
description: Full code validation — spec compliance, code quality, integration wiring, codebase audit
argument-hint: [optional: specific scope to verify]
---

## Prerequisites

1. **Check `.rnd/` exists.** If not: "No R&D project found. Run `/rnd:init` first."
2. **Read `.rnd/state.md`** for project context.

## Context Loading

- `.rnd/spec/spec.md` — requirements with REQ-IDs for spec compliance checking
- `.rnd/architecture/current.md` — architecture context for integration verification
- `.rnd/build/` — build summaries and plan files for understanding what was built
- Determine files changed during the build (from build summaries or git diff)

If `$ARGUMENTS` specifies a scope, limit verification to that scope.

## Verification — Spawn 3 Agents in Parallel

### Agent 1: Spec Compliance

Spawn **rnd-code-spec-checker** via the Agent tool:
- **description**: "Spec compliance check"
- **model**: opus
- **prompt**: Include:
  - Spec requirements from `.rnd/spec/spec.md` (filtered to relevant scope)
  - List of files changed during the build
  - Coder's status report(s) from `.rnd/build/` — provided for context only
  - Explicit instruction: "DO NOT trust the coder's report. Read the actual code independently."
  - Reference to `skills/rnd-analyst/reference/verification-methodology.md`

### Agent 2: Code Quality + Integration

Spawn **rnd-code-reviewer** via the Agent tool:
- **description**: "Code review + integration wiring"
- **model**: opus
- **prompt**: Include:
  - List of files changed during the build
  - Architecture context from `.rnd/architecture/current.md`
  - Reference to `skills/rnd-analyst/reference/code-review.md`
  - Instruction to perform Layer 1 (tactical quality) and Layer 2 (integration wiring) review
  - Instruction to produce Requirements Integration Map

### Agent 3: Codebase Audit + Security

Spawn **rnd-code-analyst** via the Agent tool:
- **description**: "Codebase audit + security review"
- **model**: opus
- **prompt**: Include:
  - Scope: files changed during the build
  - Mode: audit + security
  - Reference to `skills/rnd-analyst/reference/security-review.md` and `skills/rnd-analyst/reference/codebase-mapping.md`

## Aggregate Results

After all 3 agents return, aggregate into a consolidated verification report:

```markdown
# Verification Report — {date}

## Verdicts
| Agent | Verdict | Blockers | Suggestions |
|-------|---------|----------|-------------|
| Spec Checker | PASS/FAIL | N | N |
| Code Reviewer | PASS/CONDITIONAL/FAIL | N | N |
| Code Analyst | {summary} | N | N |

## Overall: PASS / CONDITIONAL / FAIL

## Blockers (must fix)
{aggregated blockers from all agents}

## Suggestions (should fix)
{aggregated suggestions}

## Backlog Candidates
{aggregated BACKLOG CANDIDATE items from all agents}
```

Save to `.rnd/verifications/{date}-verification.md`.

## After Completion

If any agent returns **FAIL**:
- List specific issues that need fixing
- Suggest: "Fix the blockers, then run `/rnd:c-build` to rebuild affected plans, then `/rnd:c-verify` again."

If all pass:
- Congratulate: "All verification checks passed."

## Backlog Collection

Scan all agent outputs for `BACKLOG CANDIDATE` items. If found, offer to create backlog items via `/rnd:backlog add`.

## Persistence

Update `.rnd/state.md`:
- Add entry to Recent Activity: `{today's date}: Verified via /rnd:c-verify — overall: {PASS|CONDITIONAL|FAIL} → .rnd/verifications/{filename}`
- Follow compression protocol: keep under 120 lines, compress oldest Recent Activity entries into History phase summaries when exceeding 15 entries. Never delete entries.
