---
description: Design system architecture with roadmap and technology recommendations
argument-hint: [system or feature description]
---

## Prerequisites

1. **Check `.rnd/` exists.** If not: "No R&D project found. Run `/rnd:init` first."
2. **Read `.rnd/state.md`** for project context.

## Context Loading

Read prior context from `.rnd/`:
- `.rnd/spec/spec.md` — requirements that the architecture must satisfy
- `.rnd/decisions/` — locked technology decisions (constraints)
- `.rnd/audit/` — audit findings about existing codebase (if exists)
- `.rnd/research/` — research findings relevant to design choices

## Skill Loading

Load the `rnd-architect` skill for design methodology. Reference:
- `skills/rnd-architect/reference/architecture-patterns.md` — pattern selection
- `skills/rnd-architect/reference/tech-stack-selection.md` — technology evaluation
- `skills/rnd-architect/reference/scalability-planning.md` — growth planning
- `skills/rnd-architect/reference/roadmap-generation.md` — phased implementation
- `skills/rnd-architect/reference/ml-cv-systems.md` — ML/CV architecture (if applicable)

## Design Process

The system to design: **$ARGUMENTS**

### Phase 1: Clarify Requirements
- Confirm scope from spec requirements
- Identify non-functional requirements (latency, throughput, uptime, cost)
- Understand integration points with existing systems

### Phase 2: Understand Constraints
- Team size, expertise, availability
- Budget for infrastructure and tooling
- Timeline and phasing expectations
- Compliance, security, data residency requirements

### Phase 3: Design Architecture
- Component diagram with clear boundaries and responsibilities
- Data flow: ingestion → processing → storage → serving
- Integration points and API contracts
- Scalability and fault tolerance mechanisms

### Phase 4: Select Technology
For every choice, provide:
- What and why (concrete justification)
- Trade-offs (what you give up)
- Alternatives considered and why rejected
- Cost at target scale

### Phase 5: Create Roadmap
Break into phases using the roadmap-generation methodology:
- Phase 1 — MVP: core flows, simple architecture, basic monitoring
- Phase 2 — Scale: optimization, caching, refined architecture
- Phase 3 — Advanced: multi-region, advanced features, operational excellence

Each phase: Epic → User Stories → Technical Tasks with acceptance criteria.

## Output Sections

1. **Executive Summary** — business value, approach, timeline, budget
2. **System Architecture** — component diagram, data flow, integration points
3. **Technology Stack** — justified choices with trade-offs
4. **Implementation Roadmap** — phased with deliverables and dependencies
5. **Risk Assessment** — technical debt, bottlenecks, team gaps
6. **Code Examples** — API contracts, integration patterns
7. **Deployment Strategy** — IaC, containers, monitoring, disaster recovery

## Saving

If `.rnd/architecture/current.md` already exists, archive it:
- Copy to `.rnd/architecture/history/{date}-current.md`

Save the new architecture to `.rnd/architecture/current.md`.

After saving, recommend: "Architecture complete. Run `/rnd:validate` to stress-test this design before planning."

## Persistence

Update `.rnd/state.md`:
- Add entry to Recent Activity: `{today's date}: Architecture designed via /rnd:design → .rnd/architecture/current.md`
- Follow compression protocol: keep under 120 lines, compress oldest Recent Activity entries into History phase summaries when exceeding 15 entries. Never delete entries.
