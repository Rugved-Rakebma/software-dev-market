# Wave Orchestration

Reference material for orchestrating parallel plan execution using waves. Covers the wave concept, task spawning patterns, result collection, and completion gates.

## Wave Concept

A **wave** is a group of plans that can execute in parallel because they have no dependencies on each other. Waves execute sequentially — all plans in Wave N must complete before Wave N+1 begins.

```
Wave 1: [Plan 01] [Plan 02] [Plan 03]  ← parallel
            ↓         ↓         ↓
         (all complete)
            ↓
Wave 2: [Plan 04] [Plan 05]            ← parallel, depends on Wave 1
            ↓         ↓
         (all complete)
            ↓
Wave 3: [Plan 06]                       ← depends on Wave 2
```

### Why Waves?
- **Speed**: Independent plans run simultaneously instead of sequentially
- **Safety**: Plans in the same wave can't conflict (file ownership constraint)
- **Quality gates**: Review happens between waves, catching issues before they propagate

## Task Spawning Pattern

For each wave, the orchestrator spawns rnd-coder instances:

### Step 1: Gather Wave Plans
Collect all plans assigned to the current wave number from `.rnd/build/plans/phase-NN/`.

### Step 2: Spawn Executors
For each plan in the wave, create a Task with the rnd-coder agent:
- **Input**: Plan file path, project root path
- **Context**: Each executor gets a fresh 200K context window
- **Parallelism**: All tasks in the same wave are launched in a single message with multiple Task calls

### Step 3: Wait for Completion
All executor tasks in the wave must complete before proceeding. Each executor will:
- Execute its plan's tasks
- Produce a SUMMARY.md
- Commit all work

### Step 4: Collect Results
After all executors complete, read each executor's SUMMARY.md:
- `.rnd/build/plans/phase-NN/NN-SUMMARY.md` for each plan in the wave

## Result Collection

After a wave completes, the orchestrator collects and analyzes results:

### Summary Review
For each SUMMARY.md, check:
- **status**: `completed`, `partial`, or `blocked`
- **deviations**: Any Rule 1-3 deviations that need awareness
- **decisions**: Any decisions made during execution that affect future plans
- **metrics**: Task completion rate, duration

### Status Handling
| Status | Action |
|---|---|
| `completed` | Proceed — plan fully executed |
| `partial` | Review incomplete tasks — decide if blocking for next wave |
| `blocked` | Stop — Rule 4 triggered, needs human decision |

### Decision Propagation
Decisions made by executors during this wave may affect plans in future waves. Update `.rnd/state.md` with new decisions before spawning the next wave.

## Wave Completion Gate

Before proceeding to the next wave, ALL of these must pass:

### Gate 1: All Executors Done
Every executor in the wave has completed (status: completed or partial with non-blocking incomplete tasks).

### Gate 2: Review Pass
rnd-reviewer runs both layers:
- **Layer 1 (Code Review)**: No blockers in any executor's output
- **Layer 2 (Integration Wiring)**: Exports from this wave's plans are properly wired

### Gate 3: Spot Check
rnd-analyst performs a spot check:
- Requirements covered by this wave's plans are actually implemented
- Architecture constraints are respected
- No locked decisions were violated

### Gate 4: No Blockers
No executor reported `status: blocked` (Rule 4 deviation).

### Gate Failure Handling
If any gate fails:
1. Identify the specific failure
2. Determine if it's fixable without human input
3. If fixable: create a patch plan, execute it, re-verify
4. If not fixable: surface to user with clear description of the issue

## Error Handling

### Executor Fails Mid-Task
If an executor crashes or times out:
- Check what was committed (partial work may be usable)
- Read the partial SUMMARY.md if one was created
- Decide: retry the plan, or create a continuation plan for remaining tasks

### Blocking Issue (Rule 4)
If an executor reports `status: blocked`:
- Read the blocker description from the SUMMARY.md
- Surface to user immediately — do not proceed with next wave
- The user's decision becomes a new entry in `.rnd/decisions/`
- After decision, either revise the blocked plan or create a new plan

### Merge Conflicts
If multiple executors somehow modify the same file (shouldn't happen with file ownership):
- Stop the wave
- Identify the file ownership violation
- Revise the plans to fix ownership boundaries
- Re-execute the conflicting plans sequentially

## Wave Execution Checklist

```
[ ] All plans for this wave identified
[ ] File ownership verified — no conflicts within wave
[ ] All dependency plans (prior waves) completed
[ ] Executor tasks spawned in parallel
[ ] All executors completed
[ ] All SUMMARY.md files collected and reviewed
[ ] rnd-reviewer Layer 1 + Layer 2 passed
[ ] rnd-analyst spot check passed
[ ] No blocked status from any executor
[ ] State updated with decisions from this wave
[ ] Ready to proceed to next wave
```
