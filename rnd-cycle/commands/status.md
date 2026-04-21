---
description: Show current R&D project state — decisions, architecture, research, build progress, backlog
argument-hint:
---

## Prerequisites

1. **Check `.rnd/` exists.** If not: "No R&D project found. Run `/rnd:init` first."

## Process

1. **Read `.rnd/state.md`** and display it formatted.

2. **Inventory all artifacts:**

   - **Spec**: Check `.rnd/spec/spec.md` — if exists, show requirement count and date
   - **Research**: List all files in `.rnd/research/` with dates and topics
   - **Decisions**: Read `.rnd/decisions/index.md` — show full decision log table
   - **Architecture**: Check `.rnd/architecture/current.md` — if exists, show date and summary. Check `history/` for previous versions.
   - **Audit**: List all files in `.rnd/audit/` with dates
   - **Build Plans**: Check `.rnd/build/plans/` — show phase/plan/wave counts
   - **Build Progress**: Check `.rnd/build/progress.md` — show completion status
   - **Verifications**: List all files in `.rnd/verifications/` with dates and verdicts
   - **Debug Sessions**: List active sessions in `.rnd/debug/` with status

3. **Backlog Summary:**

   If `.rnd/backlog/` exists and has items:
   - Total open items
   - Count by priority (critical / high / medium / low)
   - Count by category (BUG / DEBT / UX / PERF / SEC / FEAT)
   - Oldest open item and its age in days
   - Surface any critical-priority items explicitly

4. **Present as a clean summary:**

```
━━━ R&D Status: {project name} ━━━

## Current Status
{from state.md}

## Artifacts
| Artifact      | Status           | Details                    |
|---------------|------------------|----------------------------|
| Spec          | ✅ exists         | {N} requirements           |
| Research      | ✅ {N} reports    | Latest: {topic}            |
| Decisions     | ✅ {N} ADRs       | Latest: ADR-{N}            |
| Architecture  | ✅ current        | {date}                     |
| Build Plans   | ✅ {N} plans      | {M} waves                  |
| Build         | ⏳ wave 2/4       | ...                        |
| Verifications | ✅ {N} reports    | Latest: {verdict}          |
| Backlog       | ⚠️  {N} open      | {M} critical, {K} high     |

## Recent Activity
{last 5 entries from state.md}

## Backlog Highlights
{critical items if any}

## Suggested Next Steps
{based on what's missing or incomplete}
```

5. **Suggest next steps** based on gaps:
   - No spec → "Run `/rnd:spec` to define requirements"
   - Spec but no architecture → "Run `/rnd:design` to create architecture"
   - Architecture but no plans → "Run `/rnd:plan` to create build plans"
   - Plans but no build → "Run `/rnd:c-build` to execute plans"
   - Build but no verification → "Run `/rnd:c-verify` for validation"
   - Critical backlog items → "Address critical backlog items before proceeding"
