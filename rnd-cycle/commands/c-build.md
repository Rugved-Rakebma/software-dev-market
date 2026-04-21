---
description: Execute build plans as code — spawn coders per plan, simplify after each. No reviews.
argument-hint: [optional: specific phase or wave to build]
---

## Prerequisites

1. **Check `.rnd/` exists.** If not: "No R&D project found. Run `/rnd:init` first."
2. **Read `.rnd/state.md`** for project context.
3. **Check `.rnd/build/plans/` exists and has plan files.** If not: "No build plans found. Run `/rnd:plan` first."

## Resume Check

Check for `.rnd/live-progress.md`. If it exists, a previous build session was interrupted:
- Read the progress file to understand what was completed
- Present the state to the user: completed waves, in-progress wave, pending waves
- Offer to resume from where the previous session left off

## Scope

If `$ARGUMENTS` specifies a phase or wave, scope execution to that subset only. Otherwise, execute all plans.

## Execution Flow

### Per Wave (sequential)

Waves execute sequentially — wave 2 starts only after wave 1 is fully complete.

### Per Plan in Wave (parallel)

All plans within a wave execute in parallel.

For each plan:

**1. Spawn rnd-coder via the Agent tool:**
- **description**: "Build: {plan name}"
- **model**: opus
- **prompt**: Include:
  - **Full plan text inline** — the coder NEVER reads plan files itself
  - Project context from `.rnd/state.md`
  - Prior wave summaries (status reports from completed waves)
  - Relevant spec requirements and architecture constraints
  - Reference to `skills/rnd-build/reference/execution-methodology.md` and `skills/rnd-build/reference/escalation-protocol.md`

**2. Collect coder's status report:**
- **DONE** or **DONE_WITH_CONCERNS** → continue
- **BLOCKED** or **NEEDS_CONTEXT** → surface to user, pause execution, wait for resolution

**3. Spawn code-simplifier via the Agent tool:**
- **description**: "Simplify: {plan name} files"
- Target the files changed by the coder (from the coder's report)

### Wave Gate

All plans in the wave must complete before proceeding to the next wave.

### Progress Tracking

After each wave completes, update `.rnd/live-progress.md`:

```markdown
# Live Progress — {project name}

## Session
- Started: {timestamp}
- Last updated: {timestamp}

## Completed
- Wave 1: {plans completed}, {status}
- Wave 2: {plans completed}, {status}

## In Progress
- Wave N: {plan name} — {current state}

## Pending
- Wave N+1: {plans remaining}

## Key Decisions Made This Session
- {decision}: {rationale}

## Backlog Candidates Found
- {items discovered but not yet created}
```

### Context Preservation

If context usage exceeds **50%**, write a full progress snapshot to `.rnd/live-progress.md` before continuing. This protects against auto-compaction losing working state.

## After All Waves

1. **Create/update `.rnd/build/progress.md`** with final build status
2. **Collect BACKLOG CANDIDATE items** from all coder Concerns sections. If any found, offer to create backlog items: "Found {N} backlog candidates during build. Run `/rnd:backlog add` to create items, or I can create them now."
3. **Delete `.rnd/live-progress.md`** — build is complete, progress captured in progress.md
4. **Recommend**: "Build complete. Run `/rnd:c-verify` for full code validation."

## Persistence

Update `.rnd/state.md`:
- Add entry to Recent Activity: `{today's date}: Built {phase} via /rnd:c-build — {N} plans, {M} waves, status: {DONE|DONE_WITH_CONCERNS}`
- Follow compression protocol: keep under 120 lines, compress oldest Recent Activity entries into History phase summaries when exceeding 15 entries. Never delete entries.
