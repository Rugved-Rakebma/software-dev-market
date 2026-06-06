# System Overview

> {One-line system description — what this project is}

**Status**: bootstrap-derived | **Last reviewed**: {date} | **Plan**: `.rnd/arch-docs/plan.md`

## Stack

| Layer | Choice | Notes |
|---|---|---|
| Language | {primary, secondary} | |
| Framework | {} | |
| Persistence | {db, ORM} | {schema location} |
| Build | {tool} | |
| Runtime | {how it runs} | |

## Domains

| Domain | Purpose | Doc |
|---|---|---|
| **{domain-1}** | {one line} | [{domain-1}](./{domain-1}.md) |
| **{domain-2}** | {one line} | [{domain-2}](./{domain-2}.md) |
| **{domain-3}** | {one line} | [{domain-3}](./{domain-3}.md) |

## High-Level Shape

```
{ASCII diagram showing domains and their primary connections}

  ┌──────────────┐       ┌──────────────┐
  │   {domain}   │──────▶│   {domain}   │
  └──────────────┘       └──────────────┘
         │                       │
         ▼                       ▼
  ┌──────────────┐       ┌──────────────┐
  │   {domain}   │       │   {domain}   │
  └──────────────┘       └──────────────┘
```

Show **primary** flows only. If every domain talks to every other, the diagram has nothing to say.

## Entry Points

| Entry | Purpose | File |
|---|---|---|
| {server / CLI / worker} | {what it does} | {file:line} |

## Cross-Cutting Concerns

> Things that touch multiple domains but don't warrant their own doc.

### Logging
- {how / where} ({file path})

### Errors
- {propagation model — exceptions vs. result types vs. error middleware}
- {where they bubble to}

### Config
- {source: env vars / config file / both}
- {loading point: {file:line}}

### Observability
- {metrics, tracing — only include if present}

## Build & Deploy

> Brief — link to runbooks for detail.

- **Build**: {how to build locally} ({where to look})
- **Deploy**: {target environment, how it ships}
- **CI**: {workflow file path}

## See Also

- Per-domain docs (Domains table above)
- `.rnd/arch-docs/codebase-survey.md` — Phase 0 survey this was built from
- `.rnd/arch-docs/plan.md` — Phase 1 plan that drove the doc set

---

> **Authoring notes** (delete this block when filling out)
>
> - Length target: 60-150 lines for most projects
> - **No code blocks.** File:line refs for everything concrete.
> - The diagram should make the system's shape obvious in 10 seconds.
> - Cross-Cutting Concerns are typically 1-3 lines each — link out for detail.
> - Written *after* all per-domain docs are done, so it can reference them honestly.
