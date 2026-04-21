---
description: Get strategic guidance on build vs buy and technology decisions
argument-hint: [decision description]
---

## Prerequisites

1. **Check `.rnd/` exists.** If not: "No R&D project found. Run `/rnd:init` first."
2. **Read `.rnd/state.md`** for project context.

## Context Loading

Read prior context from `.rnd/`:
- `.rnd/spec/spec.md` — requirements that constrain the decision
- `.rnd/research/` — research findings relevant to the decision
- `.rnd/decisions/` — existing decisions (avoid contradictions)
- `.rnd/architecture/current.md` — current architecture constraints

## Skill Loading

Load the `rnd-critic` skill for assumption-challenging frameworks. Reference:
- `skills/rnd-critic/reference/assumption-challenging.md` — for surfacing hidden assumptions
- `skills/rnd-critic/reference/antipattern-detection.md` — for detecting decision anti-patterns

## Decision Process

The decision to make: **$ARGUMENTS**

### Phase 1: Frame
- What exactly is being decided?
- What are the options? (minimum 2, ideally 3+)
- What's the decision criteria? (cost, speed, reliability, team fit, lock-in)

### Phase 2: Clarify Constraints
Ask the user about:
- Budget constraints
- Timeline pressure
- Team expertise and capacity
- Existing infrastructure and commitments
- Compliance or regulatory requirements
- Risk tolerance

### Phase 3: Analyze Options
For each option, evaluate:
- **TCO** (Total Cost of Ownership) — not just license/infra cost, but operational burden, training, migration
- **Time-to-value** — how fast can you get something working?
- **Operational burden** — what does day-to-day maintenance look like?
- **Team fit** — does the team know this? What's the learning curve?
- **Lock-in** — how hard is it to switch later?
- **Risk** — what's the worst case? How likely?

### Phase 4: Challenge Assumptions
Apply the rnd-critic skill's assumption-challenging framework:
- Surface implicit assumptions in each option
- Test assumptions against evidence
- Identify wishful thinking

### Phase 5: Deliver Recommendation
Present a clear recommendation with:
- The recommended option and why
- What you give up by choosing it
- What would change this recommendation (conditions to revisit)
- Implementation next steps

## Output

Save as an Architecture Decision Record (ADR) to `.rnd/decisions/NNN-{slug}.md`:

```markdown
# ADR-NNN: {Decision Title}

## Status
Accepted — {today's date}

## Context
{What prompted this decision}

## Decision
{What was decided and why}

## Options Considered
### Option A: {name}
- Pros: ...
- Cons: ...

### Option B: {name}
- Pros: ...
- Cons: ...

## Consequences
{What changes as a result of this decision}

## Revisit Conditions
{When should this decision be reconsidered}
```

Update `.rnd/decisions/index.md` with the new entry.

## Persistence

Update `.rnd/state.md`:
- Add entry to Recent Activity: `{today's date}: Decision recorded — ADR-NNN: {title} → .rnd/decisions/NNN-{slug}.md`
- Follow compression protocol: keep under 120 lines, compress oldest Recent Activity entries into History phase summaries when exceeding 15 entries. Never delete entries.
