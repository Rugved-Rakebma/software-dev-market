---
description: Heavy adversarial validation — plans, roadmaps, proposals. Loads full critic skill (assumption-challenging + antipattern-detection + plan-verification + validation-reports). Use when /rnd:plan's compact verdict isn't enough.
argument-hint: [plan description or @file]
---

## When to Use This vs `/rnd:plan`'s Built-in Critic

`/rnd:plan` (standard/large scope) runs a **compact** critic — `plan-verification.md` only, 1-loop budget on blockers. Cheap pass.

`/rnd:validate` is the **heavy** adversarial pass — loads the full critic skill:
- `assumption-challenging.md` (5 categories of assumption stress-testing)
- `antipattern-detection.md` (25+ failure-pattern catalog)
- `plan-verification.md` (if validating build plans)
- `validation-reports.md` (8-section structured verdict format)

Use this when:
- The plan/proposal is high-stakes and warrants deep adversarial review
- The compact critic in `/rnd:plan` approved but you want a second opinion
- Validating a roadmap, decision, or architecture (not just build plans)
- Cost projections, timeline claims, or scale assumptions need stress-testing

## Prerequisites

1. **Check `.rnd/` exists.** If not: "No R&D project found. Run `/rnd:init` first."
2. **Read `.rnd/state.md`** for project context.

## Context Loading

Read prior context from `.rnd/`:
- `.rnd/decisions/` — locked decisions
- `.rnd/architecture/current.md` — architecture constraints (note scope assessment)
- `.rnd/spec/spec.md` — requirements
- `.rnd/audit/` — audit findings (if exists)

## What to Validate

**$ARGUMENTS**

If `$ARGUMENTS` references a file (e.g., `@.rnd/architecture/current.md`), read that file as the validation target.

## Optional Evidence Gathering

Before the critic validates, optionally spawn an analyst to gather evidence:

- If the target is a **document** (spec, proposal, PRD): Spawn **rnd-analyst** via Agent tool in document-audit mode to surface gaps, assumptions, and risks
- If the target is **code-related** (build plans, implementation): Spawn **rnd-code-analyst** via Agent tool to gather code-level evidence

Provide the analyst's findings to the critic as context.

## Validation

Spawn **rnd-critic** via the Agent tool:
- **description**: "Heavy validation: {target summary}"
- **model**: opus
- **prompt**: Include:
  - The validation target (inline or file content)
  - Prior context (spec, architecture, decisions)
  - Analyst findings (if gathered)
  - **Instruction to load the full critic skill**: `assumption-challenging.md` + `antipattern-detection.md` + `plan-verification.md` (if build plans) + `validation-reports.md`
  - Instruction to produce an 8-section validation report per `validation-reports.md` with **GOOD** / **NEEDS MAJOR WORK** / **BAD** verdict
  - Max 3 revision loops on BLOCKERs (if plan validation)

## After Completion

Present the critic's verdict and report to the user. If the verdict is:
- **GOOD** — suggest proceeding to the next lifecycle step
- **NEEDS MAJOR WORK** — list specific issues to address and which command to use
- **BAD** — recommend stepping back and rethinking the approach

Advisories surface in the report regardless of verdict, but only blockers gate revision.

## Persistence

Update `.rnd/state.md`:
- Add entry to Recent Activity: `{today's date}: Validated {target} via /rnd:validate — verdict: {GOOD|NEEDS MAJOR WORK|BAD}`
- Follow compression protocol: keep under 120 lines, compress oldest Recent Activity entries into History phase summaries when exceeding 15 entries. Never delete entries.
