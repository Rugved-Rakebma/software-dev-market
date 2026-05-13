---
description: Plan implementation using Claude's native plan mode, then decompose into structured build plans
argument-hint: [optional: specific phase or scope to plan]
---

## Prerequisites

1. **Check `.rnd/` exists.** If not: "No R&D project found. Run `/rnd:init` first."
2. **Read `.rnd/state.md`** for project context.
3. **Check `.rnd/spec/spec.md` exists.** If not: "No spec found. Run `/rnd:spec` first."
4. **Check `.rnd/architecture/current.md` exists.** If not: "No architecture found. Run `/rnd:design` first."

## When to Use This vs `/rnd:plan`

- **`/rnd:plan`** — planning purely from spec + architecture (no need to explore the codebase)
- **`/rnd:claude-plan`** — existing codebases where you need Claude's native planning intelligence to explore current code structure before decomposing

Both produce the same output format: slim plan files at `.rnd/build/plans/`. Both observe the same scope gate.

## Step 1 — Native Plan Mode (Interactive)

Read `.rnd/spec/spec.md` and `.rnd/architecture/current.md` for context.

Call `EnterPlanMode` to enter Claude's native plan mode. In plan mode:
- Explore the actual codebase to understand existing code structure
- Consider how new features integrate with existing code
- Create a comprehensive implementation plan
- Account for existing patterns, conventions, and constraints

The user reviews, refines, and approves the plan interactively.

On approval, save the comprehensive plan to `.rnd/build/master-plan.md` as the reference artifact.

## Step 2 — Scope Gate

Read the scope assessment from the top of `.rnd/architecture/current.md` (small / standard / large). If absent, default to **standard** and print a one-line warning.

Apply the same critic policy as `/rnd:plan`:

| Scope | Critic | Loop budget |
|---|---|---|
| **Small** | Skip | — |
| **Standard / large** | Compact `plan-verification.md` only | Max 1 revision loop on BLOCKERs |

## Step 3 — Decomposition (Batch)

Spawn **rnd-planner** via the Agent tool:
- **description**: "Decompose master plan into structured build plans"
- **model**: opus
- **prompt**: Include:
  - Full `master-plan.md` content (inline) — this is the primary input
  - Spec requirements (inline) — for REQ-ID mapping
  - Architecture constraints (inline) including the scope assessment
  - Locked decisions (inline)
  - Instruction: mechanical decomposition, not creative planning. The creative planning already happened in Step 1.
  - Produce slim plan files per `skills/rnd-build/templates/plan-template.md` (5-field frontmatter + Goal / Wires to / Tasks with Build + Done) — no code, no signatures, reference-rich

## Step 4 — Validation (skip for small scope)

**Small scope:** skip validation.

**Standard / large scope:** spawn **rnd-critic** via the Agent tool with the compact `plan-verification.md` only. Max 1 revision loop on BLOCKERs:
1. **APPROVED** or **APPROVED_WITH_ADVISORIES** → done
2. **NEEDS_REVISION** → re-spawn planner with blocker list → re-validate
3. After 1 loop → escalate remaining blockers to user

## After Completion

Tell the user:
- Master plan preserved at `.rnd/build/master-plan.md`
- Structured plans at `.rnd/build/plans/`
- Next step: `/rnd:c-build` (or `/rnd:c-run` for end-to-end)
- Optional: `/rnd:validate` for the heavy adversarial pass

## Persistence

Update `.rnd/state.md`:
- Add entry to Recent Activity: `{today's date}: Build plans created via /rnd:claude-plan → .rnd/build/plans/ ({N} plans, {M} waves, scope: {small|standard|large})`
- Follow compression protocol: keep under 120 lines, compress oldest Recent Activity entries into History phase summaries when exceeding 15 entries. Never delete entries.
