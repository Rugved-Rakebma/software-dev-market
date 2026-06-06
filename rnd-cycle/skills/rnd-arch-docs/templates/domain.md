# {Domain Name}

> {One-line purpose — what this domain owns}

**Status**: bootstrap-derived | **Last reviewed**: {date} | **Investigation**: `.rnd/arch-docs/investigations/{domain}.md`

## Boundaries

**Owns**:
- {responsibility} ({primary file path})
- {responsibility}

**Does NOT own**:
- {non-responsibility} → [{other-domain}](./{other-domain}.md)
- {non-responsibility} → [{other-domain}](./{other-domain}.md)

**Talks to**:
- [{other-domain}](./{other-domain}.md) — {nature of interaction}
- [{other-domain}](./{other-domain}.md) — {nature of interaction}

## Key Files

| File | Role |
|---|---|
| {path:line} | {one-line role} |
| {path:line} | {one-line role} |
| {path:line} | {one-line role} |

> Reference, don't restate. To understand *how* a file works, open it. This table tells you which files to open first.

## Flows

### {Flow name}
```
{ASCII diagram OR numbered steps}

1. {step} ({file:line})
2. {step} ({file:line})
3. {step} ({file:line})
```

### {Flow name}
```
{etc}
```

## Contracts

**Provides** (other domains consume these):

| Contract | Where | Notes |
|---|---|---|
| {name / shape} | {file:line} | {1-line context} |

**Consumes** (this domain depends on these):

| From domain | What | Where called |
|---|---|---|
| [{domain}](./{domain}.md) | {function / interface} | {file:line} |

## Notable Decisions

- **{decision}** — {what's chosen, what's not}. Evidence: {file:line}. Trade-off: {what this costs vs. alternative}.
- **{decision}** — {what's chosen}. Evidence: {file:line}.

## Open Questions

> Things that are unclear from code alone. These are honest gaps, not TODOs.

- {question}
- {question — uncertain because only investigated entry path}

## See Also

- [system-overview](./system-overview.md) — where this domain sits in the whole
- [{related-domain}](./{related-domain}.md) — {relationship}

---

> **Authoring notes** (delete this block when filling out)
>
> - Length target: 80-200 lines depending on domain size
> - **No code blocks.** Every claim cites file:line.
> - Skip sections you can't fill meaningfully — better empty than padded.
> - ASCII diagrams encouraged for flows. Tables for structured data.
> - Source of truth: `.rnd/arch-docs/investigations/{domain}.md` (the investigator's evidence report)
> - Principles: `skills/rnd-arch-docs/reference/principles.md`
