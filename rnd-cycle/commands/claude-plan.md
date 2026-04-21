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

- **`/rnd:plan`** — greenfield projects, no existing code to explore, planning purely from spec + architecture
- **`/rnd:claude-plan`** — existing codebases, need to understand current code structure before planning, want Claude's native planning intelligence to explore the actual codebase

Both produce the same output format: `.rnd/build/plans/` files for `rnd-coder`.

## Step 1 — Native Plan Mode (Interactive)

Read `.rnd/spec/spec.md` and `.rnd/architecture/current.md` for context.

Call `EnterPlanMode` to enter Claude's native plan mode. In plan mode:
- Explore the actual codebase to understand existing code structure
- Consider how new features integrate with existing code
- Create a comprehensive implementation plan
- Account for existing patterns, conventions, and constraints

The user reviews, refines, and approves the plan interactively.

On approval, save the comprehensive plan to `.rnd/build/master-plan.md` as the reference artifact.

## Step 2 — Decomposition (Batch)

Spawn **rnd-planner** via the Agent tool:
- **description**: "Decompose master plan into structured build plans"
- **model**: opus
- **prompt**: Include:
  - Full `master-plan.md` content (inline) — this is the primary input
  - Spec requirements (inline) — for REQ-ID mapping
  - Architecture constraints (inline)
  - Locked decisions (inline)
  - Instruction: mechanical decomposition, not creative planning. The creative planning already happened in Step 1.
  - Produce `.rnd/build/plans/phase-NN/NN-PLAN.md` files with YAML frontmatter, wave assignments, dependencies, file ownership

## Step 3 — Validation (Batch)

Spawn **rnd-critic** via the Agent tool:
- **description**: "Validate decomposed build plans"
- **model**: opus
- **prompt**: Include all plan files + spec requirements + the 7 verification dimensions reference

Validation loop (max 3 iterations):
1. If **APPROVED** → done
2. If **NEEDS REVISION** → re-spawn planner with feedback → re-validate
3. After 3 loops → escalate remaining issues to user

## After Completion

Tell the user:
- Master plan preserved at `.rnd/build/master-plan.md`
- Structured plans at `.rnd/build/plans/`
- Next step: `/rnd:c-build` to execute

## Persistence

Update `.rnd/state.md`:
- Add entry to Recent Activity: `{today's date}: Build plans created via /rnd:claude-plan → .rnd/build/plans/ ({N} plans, {M} waves)`
- Follow compression protocol: keep under 120 lines, compress oldest Recent Activity entries into History phase summaries when exceeding 15 entries. Never delete entries.
