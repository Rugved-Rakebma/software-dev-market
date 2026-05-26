---
description: Manage backlog items — add, list, close, promote, or sweep discovered issues
argument-hint: [add <description> | close <id> | promote <id> | sweep | (none for list)]
---

## Prerequisites

1. **Check `.rnd/` exists.** If not: "No R&D project found. Run `/rnd:init` first."
2. Create `.rnd/backlog/` and `.rnd/backlog/closed/` if they don't exist.

## Route by Arguments

### No Arguments — List

List all open backlog items from `.rnd/backlog/` (exclude `closed/` subdirectory).

Group by priority (critical first), then by category. Mark items aged > 30 days as **stale**:

```
## Open Backlog Items ({N} total, {K} stale)

### Critical ({N})
- BUG-001: Auth token not refreshing on 401 response (discovered 2026-04-14, **18 days**)

### High ({N})
- SEC-003: API endpoints missing rate limiting (discovered 2026-04-15) **STALE 32d**

### Medium ({N})
- DEBT-002: Duplicated validation logic in auth + profile (discovered 2026-04-14)
- UX-003: Loading state missing on dashboard (discovered 2026-04-15)

### Low ({N})
(none)
```

If stale count > 0, suggest: "Run `/rnd:backlog sweep` to review aging items."

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
discovered-during: {command that found it, e.g. "/rnd:c-run wave-04-20260520-1430"}
discovered-by: {agent that found it, e.g. "rnd-code-reviewer"}
related-files:
  - {file paths}
seen-count: 1
last-seen: {today's date}
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

`seen-count` and `last-seen` support dedup-on-recurrence. When `/rnd:c-run` detects a duplicate finding for an existing open item, it increments `seen-count` and updates `last-seen` instead of creating a new file.

### `close [id]` — Close Item

1. Find the item file matching the ID in `.rnd/backlog/`
2. Ask for resolution: `fixed` | `wont-fix` | `duplicate` | `deferred` | `fixed-incidental`
3. Update frontmatter: `status: closed`, `closed: {today's date}`, `resolution: {type}`
4. Move the file to `.rnd/backlog/closed/`

**`fixed-incidental`** = closed by `/rnd:c-run` auto-close when a wave's diff demonstrably resolved the root cause (see Promote Policy + sweep heuristics below).

### `promote [id]` — Promote to Blocker / Full Lifecycle

1. Find the item file matching the ID
2. Update frontmatter: `status: in-progress`
3. Present the item's description to the user
4. Recommend: "Run `/rnd:spec` with this description to create a specification, then follow the standard lifecycle." (or fold into the current wave's blockers if it matches an active finding)

#### Promote Policy

Promote when **any** of these hold:

| Trigger | Threshold | Why |
|---|---|---|
| **Critical priority** + aged | > 7 days | Critical items that linger are silently breaking trust — escalate or close |
| **High priority** + aged | > 30 days | A high item nobody touches is mis-prioritized; either it's actually critical or it should be downgraded |
| **Recurring symptom** | `seen-count >= 3` across distinct waves | A finding that keeps reappearing points to an upstream root cause — fold into a blocker |
| **Matches active blocker** | An open item's `related-files` overlap with a current wave's FAIL findings | The advisory and the blocker are the same problem — promote and address together |
| **Manually escalated** | User runs `promote <id>` | Explicit override |

The policy is human-actionable, not auto-promoting. `/rnd:backlog sweep` surfaces candidates; user runs `promote` to commit.

### `sweep` — Triage Existing Backlog

Read all open items from `.rnd/backlog/`. Apply heuristics. Produce an **advisory report** — no destructive auto-mutation. The user manually `close`s or `promote`s based on findings.

```
━━━ Backlog Sweep ━━━

Open: {N total}  |  Stale (>30d): {K}  |  Critical aged (>7d): {M}

## Aging — review or close
- SEC-003 (high, 32d): API endpoints missing rate limiting
  related-files: src/api/*.ts
  Suggestion: promote (high+aged) OR close as wont-fix

- DEBT-007 (medium, 45d): Duplicated validation logic in auth + profile
  related-files: src/auth/validate.ts, src/profile/validate.ts
  Suggestion: close (likely resolved by wave-05 refactor) OR re-confirm

## Recurring — promotion candidates
- UX-003 (medium, seen 3 times across wave-04 / wave-05 / wave-06)
  related-files: src/components/Dashboard.tsx
  Suggestion: promote — recurring symptom points at upstream cause

## Dedup candidates
- BUG-012 + BUG-019 — similar description, same related-files
  BUG-012: "Token refresh fails on 401"
  BUG-019: "Auth token not refreshing on expired session"
  Suggestion: close one as duplicate

## Resolution candidates — root cause may be fixed
- BUG-008 (medium, 12d): "Null pointer when user.profile is undefined"
  related-files: src/profile/loader.ts  ← modified in wave-06
  Original line had no null check; current line {N} has `if (!user?.profile) return null`
  Suggestion: close as fixed-incidental (confirm before closing)
```

#### Sweep Heuristics

| Category | Rule |
|---|---|
| **Aging** | `discovered` date > 30 days ago AND status: open |
| **Critical aged** | priority: critical AND > 7 days |
| **Recurring** | `seen-count >= 3` |
| **Dedup candidates** | Two open items where (same category) AND (related-files overlap) AND (description tokens overlap ≥ 50%) |
| **Resolution candidates** | Open item where `related-files` were modified in the last 3 runs (`.rnd/build/runs/*.md status: complete`) AND a quick check of the original issue pattern no longer matches the current code |

The sweep itself never closes, promotes, or modifies items. It only surfaces. The user is the final triage step.

## Persistence

For add/close/promote operations, update `.rnd/state.md`:
- Add entry to Recent Activity: `{today's date}: Backlog {action} — {id}: {title}`
- Follow compression protocol: keep under 120 lines, compress oldest Recent Activity entries into History phase summaries when exceeding 15 entries. Never delete entries.

For `sweep`, do not modify state.md — the sweep is an advisory read.
