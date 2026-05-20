---
description: Decompose architecture into slim executable build plans with wave assignments
argument-hint: [optional: specific phase to plan]
---

## Prerequisites

1. **Check `.rnd/` exists.** If not: "No R&D project found. Run `/rnd:init` first."
2. **Read `.rnd/state.md`** for project context.
3. **Check `.rnd/spec/spec.md` exists.** If not: "No spec found. Run `/rnd:spec` first."
4. **Check `.rnd/architecture/current.md` exists.** If not: "No architecture found. Run `/rnd:design` first."

## Context Loading

Read full context for the planner:
- `.rnd/spec/spec.md` — all requirements with REQ-IDs
- `.rnd/architecture/current.md` — architecture (note the scope assessment in the header)
- `.rnd/decisions/` — locked decisions (constraints)
- `.rnd/audit/` — audit findings (if exists)

If `$ARGUMENTS` specifies a phase, scope planning to that phase only.

## Scope Gate (mandatory)

Read the scope assessment from the top of `.rnd/architecture/current.md` (small / standard / large). If absent, fall back to the `scope` field in `.rnd/spec/spec.md` frontmatter. If neither is present, default to **standard** and print a one-line warning.

The scope controls critic policy:

| Scope | Critic | Loop budget |
|---|---|---|
| **Small** (single dev, <1KLOC, 1–2 components) | **Skip** | — |
| **Standard** (2–5 devs, 1–10KLOC) | Compact `plan-verification.md` only | Max 1 revision loop on BLOCKERs |
| **Large** (multi-team, >10KLOC, greenfield) | Compact `plan-verification.md` only | Max 1 revision loop on BLOCKERs |

For heavier adversarial review at any scope, the user can run `/rnd:validate` explicitly — that's where the full critic skill loads.

## Phase 1 — Plan Decomposition

Spawn **rnd-planner** via the Agent tool:
- **description**: "Plan decomposition for {phase or project}"
- **model**: opus
- **prompt**: Include:
  - Full spec content (inline)
  - Full architecture content (inline) including the scope assessment
  - All locked decisions (inline)
  - Audit findings if they exist (inline)
  - Instruction to produce `.rnd/build/plans/phase-NN/NN-PLAN.md` files using the slim template at `skills/rnd-build/templates/plan-template.md`
  - Reminder: plans are reference-rich prompts (point at arch + spec, never restate); no code, no signatures
  - Plans separate the *task* (plan) from the *shape* (arch) from the *requirements* (spec) — the coder receives all three at build time

When the planner returns, present the plan overview to the user:
- Number of phases
- Plans per phase
- Wave structure (which plans are parallel, which are sequential)
- Requirements coverage (which REQ-IDs are covered by which plans)
- Estimated scope

## Phase 2 — Plan Validation (skip for small scope)

**Small scope:** skip this phase entirely. Tell the user "Plans saved. Run `/rnd:validate` if you want adversarial review before `/rnd:c-build`."

**Standard / large scope:**

Spawn **rnd-critic** via the Agent tool:
- **description**: "Validate build plans"
- **model**: opus
- **prompt**: Include:
  - All plan files produced by the planner (inline)
  - Spec requirements for coverage checking
  - Reference to `skills/rnd-critic/reference/plan-verification.md` (and ONLY that reference — do not load the heavy adversarial set)
  - Instruction to classify each issue as BLOCKER or ADVISORY and return one of `APPROVED` / `APPROVED_WITH_ADVISORIES` / `NEEDS_REVISION`

**Validation loop (max 1 iteration):**
1. If critic returns **APPROVED** or **APPROVED_WITH_ADVISORIES** → done; surface any advisories to the user
2. If critic returns **NEEDS_REVISION** (blockers present) → re-spawn `rnd-planner` with the critic's blocker list, then re-spawn `rnd-critic` to recheck
3. After 1 revision, if still NEEDS_REVISION → present remaining blockers to the user for manual resolution

Advisories never trigger a revision loop. Only blockers do.

## After Completion

Tell the user:
- Plans are ready at `.rnd/build/plans/`
- Next step: `/rnd:c-build` to execute the plans as code (or `/rnd:c-run` for end-to-end with verify + triage)
- Optional: `/rnd:validate` for the heavy adversarial pass (loads the full critic skill: assumption-challenging + antipattern-detection + plan-verification + validation-reports)

## Persistence

Update `.rnd/state.md`:
- Add entry to Recent Activity: `{today's date}: Build plans created via /rnd:plan → .rnd/build/plans/ ({N} plans, {M} waves, scope: {small|standard|large})`
- Follow compression protocol: keep under 120 lines, compress oldest Recent Activity entries into History phase summaries when exceeding 15 entries. Never delete entries.
