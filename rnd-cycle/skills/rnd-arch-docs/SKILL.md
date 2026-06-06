---
name: rnd-arch-docs
description: Authoring comprehensive architecture documentation for an existing codebase. Templates, principles, and protocols for the Prime → Plan → Investigate → Synthesize flow. Loaded by /rnd:arch-docs and the rnd-domain-investigator agent.
user-invocable: false
---

# R&D Arch Docs

Reference material for **deriving comprehensive arch docs from an existing codebase**. Loaded by `/rnd:arch-docs` (orchestrator) and `rnd-domain-investigator` (agent).

Distinct from `rnd-architect` (skill) and `/rnd:design` (command):

| | `/rnd:design` + `rnd-architect` | `/rnd:arch-docs` + `rnd-arch-docs` |
|---|---|---|
| Mode | Design-time (new effort) | Bootstrap-time (existing code) |
| Output | Single `.rnd/architecture/current.md` | Multi-doc set under `/docs/arch/` |
| Source of truth | Spec + intent | Code (cited file:line) |
| Audience | The design under discussion | All future readers (Claude + humans) |

These coexist — they are different operations for different needs.

## When to Use This Skill

Loaded automatically by:
- `/rnd:arch-docs` — the orchestrator runs all five phases
- `rnd-domain-investigator` — the agent reads the investigation schema and principles

Not for general arch work. Use `rnd-architect` for design-time architecture.

## The Five-Phase Flow

```
0. PRIME       → .rnd/arch-docs/codebase-survey.md
1. PLAN        → .rnd/arch-docs/plan.md + todos     (PAUSE for user review)
2. INVESTIGATE → .rnd/arch-docs/investigations/{domain}.md (parallel agents)
3. SYNTHESIZE  → /docs/arch/{domain}.md             (sequential, per investigation)
4. OVERVIEW    → /docs/arch/system-overview.md      (last, ties domain docs)
```

Working state in `.rnd/arch-docs/`. Final docs in `/docs/arch/` (checked into the repo as the maintained truth source).

## Reference Documents

### `reference/principles.md`
The dos and don'ts. No code blocks in arch docs. File references with `file:line`. ASCII diagrams. Tables over prose for structured data. Stay at the abstraction level where decisions get made.

### `reference/prime-protocol.md`
What to read in Phase 0 (README, package manifests, configs, entry points, tree). What `codebase-survey.md` contains. Output format.

### `reference/plan-format.md`
What `plan.md` contains (codebase summary, domain list with rationale, in/out scope). How domains are justified (must reference observable code structure, not vibes).

### `reference/investigation-schema.md`
The evidence report schema returned by `rnd-domain-investigator`. Scope, Key Files, Flows, Boundaries, Contracts, Notable Decisions, Open Questions — all citation-required.

## Templates

### `templates/domain.md`
Per-domain doc shape. Purpose, Boundaries, Key Files, Flows, Contracts, Notable Decisions, See Also. ~80-200 lines per domain.

### `templates/system-overview.md`
System overview shape. Stack, Domains table, High-Level Shape (ASCII), Entry Points, Cross-Cutting Concerns. ~60-120 lines.

## Output Locations

| Path | Owner | Lifecycle |
|---|---|---|
| `.rnd/arch-docs/codebase-survey.md` | Phase 0 (orchestrator) | Overwritten on re-run |
| `.rnd/arch-docs/plan.md` | Phase 1 (orchestrator) | Overwritten on re-run |
| `.rnd/arch-docs/investigations/{domain}.md` | Phase 2 (investigator agent) | One per domain, overwritten on re-run |
| `/docs/arch/{domain}.md` | Phase 3 (orchestrator) | Final artifact, checked in |
| `/docs/arch/system-overview.md` | Phase 4 (orchestrator) | Final artifact, checked in |

## Posture Rules

- **Code is the authority.** Every claim cites file:line. Aspirational "what we intend" is out of scope for v1.
- **Domains over directories.** A domain is a coherent area of responsibility, not necessarily a folder. The plan justifies its cut.
- **Skip what isn't earned.** A template section that has nothing to say should be omitted, not padded.
- **Mark uncertainties.** `(uncertain: only investigated entry path)` is better than confident wrong.
