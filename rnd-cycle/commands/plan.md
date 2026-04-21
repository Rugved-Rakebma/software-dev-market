---
description: Decompose architecture into executable build plans with wave assignments
argument-hint: [optional: specific phase to plan]
---

## Prerequisites

1. **Check `.rnd/` exists.** If not: "No R&D project found. Run `/rnd:init` first."
2. **Read `.rnd/state.md`** for project context.
3. **Check `.rnd/spec/spec.md` exists.** If not: "No spec found. Run `/rnd:spec` first."
4. **Check `.rnd/architecture/current.md` exists.** If not: "No architecture found. Run `/rnd:design` first."

## Context Loading

Read and prepare full context for the planner:
- `.rnd/spec/spec.md` — all requirements with REQ-IDs
- `.rnd/architecture/current.md` — architecture design
- `.rnd/decisions/` — locked decisions (constraints)
- `.rnd/audit/` — audit findings (if exists)

If `$ARGUMENTS` specifies a phase, scope planning to that phase only.

## Phase 1 — Plan Decomposition

Spawn **rnd-planner** via the Agent tool:
- **description**: "Plan decomposition for {phase or project}"
- **model**: opus
- **prompt**: Include:
  - Full spec content (inline)
  - Full architecture content (inline)
  - All locked decisions (inline)
  - Audit findings if they exist (inline)
  - Instruction to produce `.rnd/build/plans/phase-NN/NN-PLAN.md` files
  - Reference to `skills/rnd-build/reference/planning-methodology.md` for plan structure
  - Reminder: plans are prompts for rnd-coder agents, not documentation for humans

When the planner returns, present the plan overview to the user:
- Number of phases
- Plans per phase
- Wave structure (which plans are parallel, which are sequential)
- Requirements coverage (which REQ-IDs are covered by which plans)
- Estimated scope

## Phase 2 — Plan Validation (max 3 loops)

Spawn **rnd-critic** via the Agent tool:
- **description**: "Validate build plans"
- **model**: opus
- **prompt**: Include:
  - All plan files produced by the planner (inline)
  - Spec requirements for coverage checking
  - Reference to `skills/rnd-critic/reference/plan-verification.md` for the 7 verification dimensions
  - Instruction to return APPROVED or NEEDS REVISION with specific issues

**Validation loop:**
1. If critic returns **APPROVED** → done, plans are ready
2. If critic returns **NEEDS REVISION** → re-spawn `rnd-planner` with the critic's feedback, then re-spawn `rnd-critic` to recheck
3. Maximum 3 loops. After 3 revisions with remaining issues, present the issues to the user for manual resolution

## After Completion

Tell the user:
- Plans are ready at `.rnd/build/plans/`
- Next step: `/rnd:c-build` to execute the plans as code
- Optional: `/rnd:validate` for additional stress-testing of the plans

## Persistence

Update `.rnd/state.md`:
- Add entry to Recent Activity: `{today's date}: Build plans created via /rnd:plan → .rnd/build/plans/ ({N} plans, {M} waves)`
- Follow compression protocol: keep under 120 lines, compress oldest Recent Activity entries into History phase summaries when exceeding 15 entries. Never delete entries.
