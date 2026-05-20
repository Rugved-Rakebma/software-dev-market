---
description: Turn an idea into a structured specification with requirements and acceptance criteria
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

Load the `rnd-build` skill. Reference `skills/rnd-build/reference/spec-methodology.md` for:
- The three-artifact triangle (Spec owns requirements only; arch owns shape; plan owns task)
- Problem framing + requirement extraction
- REQ-{CAT}-{NN} identifier format
- Version classification (v1 / v2 / out-of-scope)
- Scope-gated gap checklist (core 5–7 / standard 8–12 / large 13–15)
- Open questions routing

Reference `skills/rnd-build/templates/spec-template.md` for the output shape.

## Specification Process

The idea to specify: **$ARGUMENTS**

### Phase 1: Clarify

Ask targeted questions to understand:
- What problem does this solve? (problem-first, not solution-first)
- Who are the users? What are their goals?
- What does success look like?

Through the conversation, **assess scope** (small / standard / large) using the signals in `spec-methodology.md`. The scope you settle on controls how heavy the rest of the process is and is captured in the spec frontmatter as a fallback hint for downstream commands.

### Phase 2: Extract Requirements

For each requirement:
- Assign a REQ-{CAT}-{NN} identifier (AUTH, UI, DATA, API, PERF, SEC, INFRA, BIZ, NOTIFY, REPORT, ADMIN)
- Write a clear, behavior-only description (no code, no signatures)
- Classify version: v1 (must-have), v2 (planned), or out-of-scope
- Define **binary-testable** acceptance — the spec-checker will read this row verbatim

### Phase 3: Gap Review (scope-gated)

Review the gap set for the chosen scope (small / standard / large) per `spec-methodology.md` §4. For each gap, either capture as a REQ row or route as an Open Question.

### Phase 4: Present for Validation

Present the spec for user review in this order:
1. Scope assessment (small / standard / large, with one-line justification)
2. Problem statement
3. Users
4. Requirements (v1 / v2 / out-of-scope tables)
5. Open Questions (with HIGH/MEDIUM/LOW triage)

Iterate with the user until they approve.

## Output

Save the approved specification to `.rnd/spec/spec.md` using the slim template. The frontmatter `scope` field captures the assessment as a fallback hint for `/rnd:design`, `/rnd:plan`, and `/rnd:decide` until arch is written.

**What the spec does NOT include** (these belong elsewhere):
- Tech stack, mechanisms, system shape → `/rnd:design`
- Team, timeline, task breakdowns → `/rnd:plan`
- Cost projections, roadmaps → `/rnd:design` (proportionally, per scope)
- Validation assumptions about implementation → tracked by `/rnd:plan` / `rnd-critic`

## Persistence

Update `.rnd/state.md`:
- Add entry to Recent Activity: `{today's date}: Specification created via /rnd:spec → .rnd/spec/spec.md (scope: {small|standard|large})`
- Follow compression protocol: keep under 120 lines, compress oldest Recent Activity entries into History phase summaries when exceeding 15 entries. Never delete entries.
