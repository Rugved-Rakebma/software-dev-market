---
description: Design system architecture — boundaries, contracts, decisions. Not implementation.
argument-hint: [system or feature description]
---

## Prerequisites

1. **Check `.rnd/` exists.** If not: "No R&D project found. Run `/rnd:init` first."
2. **Read `.rnd/state.md`** for project context.
3. **Read `.rnd/spec/spec.md`** — required. Architecture designs against a spec. If absent, say "Run `/rnd:spec` first" and stop.

## Context Loading

Read prior context from `.rnd/`:
- `.rnd/spec/spec.md` — requirements the architecture must satisfy
- `.rnd/decisions/` — locked technology decisions (constraints)
- `.rnd/audit/` — audit findings about existing codebase (if exists)
- `.rnd/research/` — research findings relevant to design choices

## Skill Loading

Load `rnd-architect` skill **only when references are relevant**. Skip the skill entirely for small refactors. Never apply enterprise references (Kubernetes, microservices, multi-region) to projects that don't operate at that scale.

## What an Architecture Doc Is

It describes the **shape** of the system — components, how they work together, and the decisions that shape them. It operates at the **structural level**: mechanisms, contracts, data flow, sequencing. It stops at the **codebase boundary**: no syntax, type-annotated signatures, decorators, or function bodies.

In short: it describes the **system's how**, not the **code's how**.

It answers:
- What are the parts? What is each responsible for?
- How do they connect (data + control flow)?
- What are the contracts at each seam (input/output shape, invariants, side effects)?
- What mechanisms does the system use (concurrency model, caching, error handling, state management)?
- What significant choices shape this system, and why?
- What can go wrong with this shape?

It is **NOT** implementation, **NOT** requirements, **NOT** a build plan.

## Scope Assessment (mandatory first step)

Before writing, assess scope from the spec and state it explicitly at the top of the doc:

| Signal | Small | Standard | Large |
|---|---|---|---|
| LOC delta | <1KLOC | 1–10KLOC | >10KLOC |
| Team | single dev | 2–5 devs | multi-team |
| Components changed | 1–2 | 3–5 | >5 |
| External deps added | 0 | 1–2 | >2 |
| Greenfield? | no | partial | yes |

**Default to small unless the spec proves otherwise.** Length proportional to scope: small ~50–150 lines, standard ~150–300 lines, large 300+.

## Required Sections (always include)

1. **Header** — title, date, status, link to upstream spec, scope assessment
2. **Component Diagram** — boxes + arrows showing what exists and what talks to what (ASCII fine)
3. **Module Layout** — where each component lives in the repo (file tree or pointer)
4. **Data Flow** — per-request/event path through the components
5. **Boundary Contracts** — for each seam: purpose, input shape, output shape, side effects, invariants. *Prose + tables. Never signatures.*
6. **Data Models** — entity name → role → key fields (table). *Never class bodies.*
7. **Decisions Log** — per significant choice: what / why / trade-off / rejected alternatives
8. **Out of Scope** — what this design explicitly does not address

## Conditional Sections (include only if warranted)

- **Non-functional Budgets** — latency targets per stage, throughput, scale assumptions
- **Failure Model** — what can fail, how the shape responds at the boundary level
- **Tech Stack** — chosen tech / role / why / rejected (only if introducing or changing tech)
- **Cross-cutting Models** — concurrency, error handling, persistence, caching approach
- **Phasing** — high-level v1/v2/v3 sequencing. *What lands when, not task lists.*
- **Architectural Risks** — weaknesses inherent to the shape itself, not implementation bugs

## Optional Sections (add only if earned)

- **External Integrations** — services, protocols, auth, rate limits
- **Deployment Topology** — what runs where (processes, containers, regions)
- **Observability** — instrumentation approach, signal flow
- **Security Posture** — threat model, trust boundaries
- **Glossary** — vocabulary used throughout, defined once

## Forbidden Content

Never include:

| Content | Belongs in |
|---|---|
| Class bodies, Pydantic schemas, type-annotated signatures | the codebase |
| `@decorators`, async function bodies, code snippets | the codebase |
| Bash commands (`git mv`, `sed`, `os.environ.get(...)`, etc.) | the build plan |
| Build task lists with effort estimates | `.rnd/build/plans/*.md` |
| Acceptance criteria, success metrics, verification commands | `.rnd/spec/spec.md` |
| Test fixtures, eval cases | the build plan or codebase |

**If you start writing code, stop. Convert it to prose + table describing the contract.**

### Concrete contrast

❌ Implementation in arch doc:
```python
async def retrieve_sources(
    query: str,
    depth: Literal["shallow","balanced","deep"] = "balanced",
) -> SourceBundle: ...
```

✅ Arch description:
> **`retrieve_sources`** — takes a natural-language query and a depth knob (`shallow` / `balanced` / `deep`, controlling 1–2 / 5–8 / 15–20 returned units), returns a `SourceBundle` with bodies and per-unit rationale. Side effect: reads the vault filesystem.

## Posture Rules

- Every section earns its place. Skip sections that don't apply.
- Diagrams + tables over prose where shape > narrative.
- Describes **what** parts exist, **how** they work together (mechanisms, contracts, data flow, sequencing), and **why** these choices. Stops at the codebase boundary: no syntax, signatures, decorators, or function bodies.
- If the input is already a clear plan (e.g. spec with locked decisions and phase summaries), pass it through. Do not inflate into more sections than the input warrants.
- No marketing language ("highly scalable", "production-grade") unless load-bearing.

## Saving

If `.rnd/architecture/current.md` already exists, archive it:
- Copy to `.rnd/architecture/history/{date}-current.md`

Save the new architecture to `.rnd/architecture/current.md`.

After saving:
- **Small scope** → recommend `/rnd:plan` directly. Skip validation (adds ceremony without value at this size).
- **Standard or larger** → "Architecture saved. Run `/rnd:validate` to stress-test the shape before planning."

## Persistence

Update `.rnd/state.md`:
- Add entry to Recent Activity: `{today's date}: Architecture designed via /rnd:design → .rnd/architecture/current.md`
- Follow compression protocol: keep under 120 lines, compress oldest Recent Activity entries into History phase summaries when exceeding 15 entries. Never delete entries.
