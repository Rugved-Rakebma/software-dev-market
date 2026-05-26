---
description: Get strategic guidance on build vs buy and technology decisions
argument-hint: [decision description]
---

## Prerequisites

1. **Check `.rnd/` exists.** If not: "No R&D project found. Run `/rnd:init` first."
2. **Read `.rnd/state.md`** for project context.

## Context Loading

Read prior context from `.rnd/`:
- `.rnd/spec/spec.md` — requirements that constrain the decision (also: spec frontmatter `scope` field as fallback scope source)
- `.rnd/research/` — research findings relevant to the decision
- `.rnd/decisions/` — existing decisions (avoid contradictions)
- `.rnd/architecture/current.md` — current architecture constraints (also: arch header `scope` field as primary scope source)

## Scope Gate (mandatory)

Read the scope assessment from the top of `.rnd/architecture/current.md` (small / standard / large). If absent, fall back to the `scope` field in `.rnd/spec/spec.md` frontmatter. If neither is present, default to **standard** and print a one-line warning.

If both are absent and `$ARGUMENTS` clearly describes a tiny decision (file naming, variable choice, log format), the user may explicitly invoke at small scope by appending `--small` to `$ARGUMENTS`.

Scope controls how much adversarial machinery loads and what shape the ADR takes:

| Scope | References loaded | Decision process | ADR shape |
|---|---|---|---|
| **Small** | (none) | Skip Phase 4 (Challenge Assumptions); minimal Phase 3 | Slim ADR (Context · Decision · Trade-off · Revisit) |
| **Standard** | `assumption-challenging.md` only | Compact Phase 4 — surface top 3-5 assumptions | Full ADR (current shape) |
| **Large** | `assumption-challenging.md` + `antipattern-detection.md` | Full Phase 4 — all 5 assumption categories + antipattern catalog | Full ADR + antipattern review section |

For heavier adversarial review at any scope, the user can run `/rnd:validate` on the decision explicitly — that's where the full critic skill loads.

## Skill Loading (scope-gated)

Load the `rnd-critic` skill scaffold (cheap — the SKILL.md header alone). Then per the table above:

- **Small** → do not load reference files. The decision is small enough that the clarifying questions + a single round of reasoning is sufficient.
- **Standard** → load `skills/rnd-critic/reference/assumption-challenging.md` only.
- **Large** → load `skills/rnd-critic/reference/assumption-challenging.md` + `skills/rnd-critic/reference/antipattern-detection.md`.

## Decision Process

The decision to make: **$ARGUMENTS**

### Phase 1: Frame
- What exactly is being decided?
- What are the options? (small: 1-2 is fine if obvious; standard/large: minimum 2, ideally 3+)
- What's the decision criteria? (cost, speed, reliability, team fit, lock-in)

### Phase 2: Clarify Constraints
Ask the user about:
- Budget constraints
- Timeline pressure
- Team expertise and capacity
- Existing infrastructure and commitments
- Compliance or regulatory requirements
- Risk tolerance

**Small scope:** ask only the 2-3 constraints most relevant; don't run the full slate.

### Phase 3: Analyze Options
For each option, evaluate:
- **TCO** (Total Cost of Ownership) — not just license/infra cost, but operational burden, training, migration
- **Time-to-value** — how fast can you get something working?
- **Operational burden** — what does day-to-day maintenance look like?
- **Team fit** — does the team know this? What's the learning curve?
- **Lock-in** — how hard is it to switch later?
- **Risk** — what's the worst case? How likely?

**Small scope:** condense to TCO + Lock-in + Risk only. The other dimensions rarely change the answer at small scale.

### Phase 4: Challenge Assumptions (scope-gated)

- **Small** → skip. Tiny decisions don't warrant adversarial framework load.
- **Standard** → apply `assumption-challenging.md` to surface the top 3-5 assumptions. Use the Reality Check and Stress Test patterns. Skip the full category sweep.
- **Large** → apply `assumption-challenging.md` across all 5 categories (Timeline, Resource, Technical, Business, External) AND apply `antipattern-detection.md` to scan for matching anti-patterns in the proposed direction.

### Phase 5: Deliver Recommendation
Present a clear recommendation with:
- The recommended option and why
- What you give up by choosing it
- What would change this recommendation (conditions to revisit)
- Implementation next steps

## Output

Save as an Architecture Decision Record (ADR) to `.rnd/decisions/NNN-{slug}.md`. The shape depends on scope.

### Small-scope ADR (slim)

```markdown
---
scope: small
---

# ADR-NNN: {Decision Title}

**Status:** Accepted — {today's date}

## Context
{1-2 sentences — what prompted this}

## Decision
{What was decided and why, 1-3 sentences}

## Trade-off
{What we sacrificed by choosing this}

## Revisit
{When to reconsider — concrete trigger}
```

### Standard / Large ADR (full)

```markdown
---
scope: standard | large
---

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

**Large-scope only:** append a `## Adversarial Review` section summarizing the assumption-challenging + antipattern findings (top 3-5 of each).

Update `.rnd/decisions/index.md` with the new entry (table columns work for both slim + full ADRs).

## Persistence

Update `.rnd/state.md`:
- Add entry to Recent Activity: `{today's date}: Decision recorded — ADR-NNN: {title} (scope: {small|standard|large}) → .rnd/decisions/NNN-{slug}.md`
- Follow compression protocol: keep under 120 lines, compress oldest Recent Activity entries into History phase summaries when exceeding 15 entries. Never delete entries.
