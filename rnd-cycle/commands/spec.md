---
description: Turn an idea into a structured specification with requirements and success criteria
argument-hint: [idea or feature description]
---

## Prerequisites

1. **Check `.rnd/` exists.** If not: "No R&D project found. Run `/rnd:init` first."
2. **Read `.rnd/state.md`** for project context.

## Context Loading

Read prior context from `.rnd/`:
- `.rnd/decisions/` — locked decisions are constraints on the spec
- `.rnd/research/` — prior research informs requirements
- `.rnd/spec/spec.md` — if an existing spec exists, this is an update/extension

## Skill Loading

Load the `rnd-architect` skill for specification methodology. Reference `skills/rnd-build/reference/spec-methodology.md` for:
- Problem framing techniques
- Requirement extraction process
- REQ-{CAT}-{NN} identifier format
- Scope classification (v1/v2/out-of-scope)
- Gap identification checklist
- Success criteria writing guide

## Specification Process

The idea to specify: **$ARGUMENTS**

### Phase 1: Clarify
Ask targeted questions to understand:
- What problem does this solve? (problem-first, not solution-first)
- Who are the users? What are their goals?
- What are the constraints? (budget, timeline, team, existing infrastructure)
- What does success look like?

### Phase 2: Extract Requirements
For each requirement:
- Assign a REQ-{CAT}-{NN} identifier (AUTH, UI, DATA, API, PERF, SEC, INFRA, BIZ)
- Write a clear, testable description
- Classify scope: v1 (must-have), v2 (planned), or out-of-scope
- Define acceptance criteria (binary pass/fail)

### Phase 3: Define Success Criteria
- Each requirement maps to at least one acceptance test
- Tests must be binary (pass/fail, not "looks good")
- Include both functional and non-functional criteria

### Phase 4: Present for Validation
Present the spec in digestible sections for user review:
1. Problem statement
2. Requirements table (grouped by category)
3. Success criteria
4. Scope decisions (what's in, what's deferred, what's out)
5. Open questions (route to `/rnd:research` if needed)

Iterate with the user until they approve.

## Output

Save the approved specification to `.rnd/spec/spec.md`.

## Persistence

Update `.rnd/state.md`:
- Add entry to Recent Activity: `{today's date}: Specification created via /rnd:spec → .rnd/spec/spec.md`
- Follow compression protocol: keep under 120 lines, compress oldest Recent Activity entries into History phase summaries when exceeding 15 entries. Never delete entries.
