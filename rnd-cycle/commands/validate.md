---
description: Validate plans, roadmaps, or proposals with ruthless honesty
argument-hint: [plan description or @file]
---

## Prerequisites

1. **Check `.rnd/` exists.** If not: "No R&D project found. Run `/rnd:init` first."
2. **Read `.rnd/state.md`** for project context.

## Context Loading

Read prior context from `.rnd/`:
- `.rnd/decisions/` — locked decisions
- `.rnd/architecture/current.md` — architecture constraints
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
- **description**: "Validate: {target summary}"
- **model**: opus
- **prompt**: Include:
  - The validation target (inline or file content)
  - Prior context (spec, architecture, decisions)
  - Analyst findings (if gathered)
  - Reference to `skills/rnd-critic/` for validation methodology
  - Instruction to produce an 8-section validation report with GOOD / NEEDS MAJOR WORK / BAD verdict

## After Completion

Present the critic's verdict and report to the user. If the verdict is:
- **GOOD** — suggest proceeding to the next lifecycle step
- **NEEDS MAJOR WORK** — list specific issues to address and which command to use
- **BAD** — recommend stepping back and rethinking the approach

## Persistence

Update `.rnd/state.md`:
- Add entry to Recent Activity: `{today's date}: Validated {target} via /rnd:validate — verdict: {GOOD|NEEDS MAJOR WORK|BAD}`
- Follow compression protocol: keep under 120 lines, compress oldest Recent Activity entries into History phase summaries when exceeding 15 entries. Never delete entries.
