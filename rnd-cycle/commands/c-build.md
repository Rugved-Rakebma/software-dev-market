---
description: Execute build plans as code — spawn coders per plan, simplify after each. No reviews.
argument-hint: [optional: specific phase or wave to build]
---

## Prerequisites

1. **Check `.rnd/` exists.** If not: "No R&D project found. Run `/rnd:init` first."
2. **Read `.rnd/state.md`** for project context.
3. **Check `.rnd/build/plans/` exists and has plan files.** If not: "No build plans found. Run `/rnd:plan` first."

## Resume Check

Check for `.rnd/build/progress.md` with frontmatter `status: in-progress`. If found, a previous build session was interrupted:
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
- **prompt**: Include three inline blocks:
  - **`plan_text`** — full plan text. The coder NEVER reads plan files itself.
  - **`arch_slices`** — sections of `.rnd/architecture/current.md` referenced by the plan's `## Wires to` section. Parse the plan's Wires to bullets (e.g. "arch §5.1"); read those sections from the arch doc; embed inline. **Fallback:** if the plan has no `## Wires to` section, embed the full arch doc.
  - **`spec_req_rows`** — rows from `.rnd/spec/spec.md` corresponding to the REQ-IDs in the plan's `requirements` frontmatter. Parse the frontmatter, look up each REQ row in the spec, embed inline.
  - Plus: project context from `.rnd/state.md`, prior wave summaries (status reports from completed waves), references to `skills/rnd-build/reference/execution-methodology.md` and `skills/rnd-build/reference/escalation-protocol.md`.

This three-block bundling implements the **Plan = task / Arch = shape / Spec = reqs** separation: plans stay slim because the coder receives the shape and requirements alongside the task.

**2. Collect coder's status report:**
- **DONE** or **DONE_WITH_ADVISORIES** → continue (advisories route to backlog in step 4)
- **BLOCKED** or **NEEDS_CONTEXT** → surface to user, pause execution, wait for resolution

**3. Spawn code-simplifier via the Agent tool:**
- **description**: "Simplify: {plan name} files"
- Target the files changed by the coder (from the coder's report)

### Wave Gate

All plans in the wave must complete before proceeding to the next wave.

### Progress Tracking

Maintain a single rolling progress file at `.rnd/build/progress.md`. On the first wave, create it with frontmatter `status: in-progress`. After each wave completes, update the same file in place:

```markdown
---
status: in-progress
started: {timestamp}
last-updated: {timestamp}
---

# Build Progress — {project name}

## Completed
- {plan name} — wave {N}, {status}
- {plan name} — wave {N}, {status}

## In Progress
- {plan name} — wave {N}, {current state}

## Pending
- {plan name} — wave {N+1}
- {plan name} — wave {N+1}

## Deferred
- {plan name} — {reason}

## Key Decisions Made This Session
- {decision}: {rationale}

## Backlog Candidates Found
- {items discovered but not yet created}
```

`## Completed` and `## Deferred` list one bullet per plan (not per wave) so the statusline can compute pending count.

### Context Preservation

If context usage exceeds **50%**, write a full progress snapshot to `.rnd/build/progress.md` before continuing. This protects against auto-compaction losing working state.

## After All Waves

1. **Finalize `.rnd/build/progress.md`** — flip frontmatter `status: in-progress` → `status: complete`, update `last-updated`, and ensure all plans appear under `## Completed` or `## Deferred` (no remaining `## In Progress` or `## Pending` entries).
2. **Collect BACKLOG CANDIDATE items** from all coder Advisories sections. If any found, offer to create backlog items: "Found {N} backlog candidates during build. Run `/rnd:backlog add` to create items, or I can create them now."
3. **Recommend**: "Build complete. Run `/rnd:c-verify` for full code validation."

## Persistence

Update `.rnd/state.md`:
- Add entry to Recent Activity: `{today's date}: Built {phase} via /rnd:c-build — {N} plans, {M} waves, status: {DONE|DONE_WITH_ADVISORIES}`
- Follow compression protocol: keep under 120 lines, compress oldest Recent Activity entries into History phase summaries when exceeding 15 entries. Never delete entries.
