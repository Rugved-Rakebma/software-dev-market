# Execution Methodology

Reference material for the rnd-coder agent. Covers the execution flow, deviation handling, commit conventions, and summary format.

## 9-Step Execution Flow

### Step 1: Load State
Read `.rnd/state.md` to understand:
- What phases/plans have been completed
- What's currently in progress
- Any known issues or blockers from previous executions

### Step 2: Load Plan + Arch + Spec
The coder receives **three inline blocks** in its spawn prompt (per `handoff-contracts.md`):
- **`plan_text`** — the task: 5-field frontmatter (`id`, `wave`, `depends_on`, `files`, `requirements`) + Goal / Wires to / Tasks (each task has Build + Done)
- **`arch_slices`** — the shape: sections of `.rnd/architecture/current.md` referenced by the plan's "Wires to"
- **`spec_req_rows`** — the requirements: rows from `.rnd/spec/spec.md` for the REQ-IDs in the plan's `requirements` frontmatter

**Backward compat:** if a plan uses the old shape (`phase`/`plan`/`files_modified`/`must_haves` frontmatter, `Files`/`Action`/`Verify`/`Done` per task), gracefully read it: treat `phase-plan` as the id, `files_modified` as `files`, ignore `must_haves`, and combine `Files`+`Action` as Build, `Verify`+`Done` as Done.

Read all files listed in the plan's `files` field to understand their current state before modifying them.

### Step 3: Record Time
Note the start time. This enables duration tracking in the summary metrics.

### Step 4: Execute Tasks
For each task sequentially:
1. Read the task's `Build:` and `Done:` fields (or the old 4-field shape if a legacy plan)
2. Read any existing files that will be modified (from the plan's `files` field)
3. Implement the behavior described in Build; follow contracts from the arch slices
4. Confirm Done criteria is met (Done often IS a verify command)
5. Commit with conventional format

### Step 5: Verify
After all tasks complete, re-verify all Done criteria across all tasks. Run any project-level verification commands. This catches regressions where Task 3 broke something Task 1 built.

### Step 6: Create SUMMARY
Write the execution summary to `.rnd/build/plans/phase-NN/NN-SUMMARY.md`.

### Step 7: Self-Check
Verify your own work:
- Every file in `key_files` exists on disk
- Every commit referenced in the summary exists in git log
- Every task marked done genuinely meets its acceptance criteria

If self-check fails, fix the issue and re-verify.

### Step 8: State Updates
Update `.rnd/state.md` with:
- This plan's completion status
- Any decisions made during execution
- Any known issues or stubs left behind

### Step 9: Final Commit
Commit the SUMMARY.md and state updates: `chore({phase}-{plan}): add execution summary`

## 4-Tier Deviation Rules

### Rule 1: Bug Encountered
**Trigger**: Existing code has a bug that blocks your task.
**Action**: Fix the bug. Document in summary.
**Scope**: The fix must be minimal — fix the bug, don't refactor the surrounding code.

**Example**: Plan says to import `AuthService` from `./auth`. The file exports `authService` (lowercase). Fix: update the import to match the actual export. Note in deviations: "Fixed import casing mismatch for authService in src/api/routes.ts"

**Example**: A utility function has an off-by-one error that causes your test to fail. Fix: correct the off-by-one. Note in deviations: "Fixed off-by-one in calculateOffset() — was returning length instead of length-1"

### Rule 2: Missing Critical Piece
**Trigger**: The plan assumes something exists that doesn't.
**Action**: Create it if <30 minutes estimated work. Document in summary.
**Scope**: Create the minimum viable version. Don't gold-plate.

**Example**: Plan says "use the formatDate utility" but no such utility exists. Fix: create a simple formatDate function that handles the formats needed by this plan. Note in deviations: "Created formatDate utility — plan assumed it existed"

**Example**: Plan references a config value `DATABASE_POOL_SIZE` but the config schema doesn't include it. Fix: add the config field with a sensible default. Note in deviations: "Added DATABASE_POOL_SIZE to config schema with default of 10"

### Rule 3: Blocking Issue
**Trigger**: Something blocks progress that isn't a bug or missing piece.
**Action**: Fix if straightforward and architecture-preserving. Document in summary.
**Scope**: The fix must not change the system architecture or contradict locked decisions.

**Example**: A dependency version conflict prevents compilation. Fix: update the dependency to a compatible version. Note in deviations: "Updated express from 4.18.1 to 4.18.2 to resolve peer dependency conflict with helmet"

**Example**: A database migration fails because a column already exists. Fix: add an IF NOT EXISTS guard. Note in deviations: "Added IF NOT EXISTS to migration for idempotency"

### Rule 4: Architectural Change Needed
**Trigger**: The plan requires something that would change system architecture, contradict a locked decision, or fundamentally alter the approach.
**Action**: STOP. Do not proceed. Write a partial summary with `status: blocked`.

**Example**: Plan says to add a REST endpoint but the feature requires real-time updates that only WebSockets can provide. This changes the communication architecture. STOP.

**Example**: Plan says to store data in PostgreSQL but the data is highly nested JSON that would be better in MongoDB. This contradicts a locked database decision. STOP.

**Example**: Plan assumes a monolithic structure but the feature's complexity suggests it needs its own service. This changes deployment architecture. STOP.

## Commit Conventions

### Format
```
{type}({phase}-{plan}): {description}
```

### Types
| Type | When |
|---|---|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `test` | Adding or modifying tests |
| `refactor` | Code restructuring without behavior change |
| `chore` | Build, config, docs, tooling |

### Rules
- Present tense: "add", "fix", "update" — not "added", "fixed", "updated"
- Under 72 characters for the description
- One commit per task (not per file, not per plan)
- The phase-plan prefix enables tracing any commit back to its source plan

### Examples
```
feat(02-03): add user authentication middleware
fix(01-02): correct database connection pool configuration
test(03-01): add integration tests for payment API
refactor(02-04): extract validation logic into shared utility
chore(01-01): configure ESLint and Prettier
```

## SUMMARY.md Format

### Frontmatter
```yaml
---
phase: NN-name
plan: NN
status: completed | partial | blocked
key_files:
  - src/path/modified.ts
  - src/path/created.ts
decisions:
  - "Decision made during execution with rationale"
deviations:
  - rule: 1
    description: "What deviated and why"
metrics:
  tasks_completed: N/N
  commits: N
  duration_minutes: N
---
```

### Body Sections

**One-liner**: Single sentence summarizing what was accomplished.

**Deviations**: For each deviation, state:
- Which rule was applied (1-4)
- What deviated from the plan
- Why the deviation was necessary
- What was done about it

**Known Stubs**: Any placeholder implementations left behind. Each stub should have a TODO comment in the code with a clear description of what needs to be completed.

**Self-Check**: Checklist confirming:
- All files in key_files exist
- All commits referenced are valid
- All tasks marked done meet acceptance criteria

## Execution Guards

### Analysis Paralysis Guard
If you've read 5+ files without writing any code or making any changes, you have enough context. Stop reading and start implementing. You can always read more files later if you hit a specific question.

This guard exists because executors can fall into a loop of "just one more file" that burns context without producing output.

### Fix Attempt Limit
If a task fails verification and you've tried 3 different fixes, stop. Mark the task as partially complete in the summary. Continuing to try fixes after 3 attempts usually means the problem is architectural (Rule 4), not tactical.

### Scope Boundary
You are executing one plan. If you notice bugs, improvements, or issues in files outside your plan's scope:
- Note them in the summary under "Known Issues"
- Do NOT fix them
- Do NOT modify files not listed in your plan's `files_modified`

The only exception is Rule 1-3 deviations that directly block your current task.
