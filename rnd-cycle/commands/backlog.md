---
description: Manage backlog items — add, list, close, or promote discovered issues
argument-hint: [add <description> | close <id> | promote <id> | (none for list)]
---

## Prerequisites

1. **Check `.rnd/` exists.** If not: "No R&D project found. Run `/rnd:init` first."
2. Create `.rnd/backlog/` and `.rnd/backlog/closed/` if they don't exist.

## Route by Arguments

### No Arguments — List

List all open backlog items from `.rnd/backlog/` (exclude `closed/` subdirectory).

Group by priority (critical first), then by category:

```
## Open Backlog Items ({N} total)

### Critical ({N})
- BUG-001: Auth token not refreshing on 401 response (discovered 2026-04-14)

### High ({N})
- SEC-003: API endpoints missing rate limiting (discovered 2026-04-15)

### Medium ({N})
- DEBT-002: Duplicated validation logic in auth + profile (discovered 2026-04-14)
- UX-003: Loading state missing on dashboard (discovered 2026-04-15)

### Low ({N})
(none)
```

### `add [description]` — Create New Item

Interactively gather:
1. **Category**: BUG | DEBT | UX | PERF | SEC | FEAT
2. **Priority**: critical | high | medium | low
3. **Related files**: file paths involved
4. **Description**: what was found (use `$ARGUMENTS` after "add" as starting point)
5. **Impact**: why it matters
6. **Suggested fix**: if known

**ID generation**: Scan `.rnd/backlog/` for the highest number in the chosen category, increment by 1. Format: `{CATEGORY}-{NNN}`.

**File name**: `.rnd/backlog/{CATEGORY}-{NNN}-{slug}.md`

**File content**:
```yaml
---
id: {CATEGORY}-{NNN}
title: {title}
status: open
priority: {priority}
category: {CATEGORY}
discovered: {today's date}
discovered-during: {command that found it, if known}
discovered-by: {agent that found it, if known}
related-files:
  - {file paths}
closed: null
resolution: null
---

## Description
{what was found}

## Context
{where/when discovered}

## Impact
{why it matters}

## Suggested Fix
{if known}
```

### `close [id]` — Close Item

1. Find the item file matching the ID in `.rnd/backlog/`
2. Ask for resolution: `fixed` | `wont-fix` | `duplicate` | `deferred`
3. Update frontmatter: `status: closed`, `closed: {today's date}`, `resolution: {type}`
4. Move the file to `.rnd/backlog/closed/`

### `promote [id]` — Promote to Full Lifecycle

1. Find the item file matching the ID
2. Update frontmatter: `status: in-progress`
3. Present the item's description to the user
4. Recommend: "Run `/rnd:spec` with this description to create a specification, then follow the standard lifecycle."

## Persistence

For add/close/promote operations, update `.rnd/state.md`:
- Add entry to Recent Activity: `{today's date}: Backlog {action} — {id}: {title}`
- Follow compression protocol: keep under 120 lines, compress oldest Recent Activity entries into History phase summaries when exceeding 15 entries. Never delete entries.
