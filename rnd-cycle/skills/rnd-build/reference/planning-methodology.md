# Planning Methodology

Reference material for the rnd-planner agent. Covers how to decompose project phases into executable build plans.

## Plans-Are-Prompts Principle

Plans are not documentation for humans. They are prompts consumed by rnd-coder agents running in fresh context windows. This distinction drives every planning decision:

| Human Documentation | Plan-as-Prompt |
|---|---|
| Assumes reader has project context | Must be self-contained |
| Can be vague ("implement authentication") | Must be precise ("create JWT middleware that validates tokens from the Authorization header") |
| Organized for reference/scanning | Organized for sequential execution |
| Can reference other docs | Must embed all needed context inline |

The executor loads the plan into a fresh 200K context window. It knows nothing about the project except what the plan tells it. If context is missing from the plan, the executor will either guess wrong or fail.

## Task Breakdown Rules

Every task in a plan must have four fields:

### Files
Exact file paths that will be created or modified. No wildcards, no "and related files." The executor needs to know exactly which files to touch.

### Action
Specific implementation instructions. Not "implement the API" but "create a POST endpoint at /api/auth/login that accepts { email, password } in the request body, validates against the users table, returns a JWT token with 24h expiry, and returns 401 for invalid credentials."

Include:
- What to build
- What patterns to follow (reference existing code if applicable)
- What libraries/utilities to use
- Expected function signatures or API contracts

### Verify
A command or check the executor can run to confirm the task is done. Must complete in <10 seconds and be read-only (no side effects).

Examples:
- `just typecheck` (runs TypeScript compiler)
- `just test -- --filter auth` (runs specific test suite)
- "File exists at src/middleware/auth.ts and exports `authMiddleware` function"
- `just lint -- src/api/auth.ts` (lints specific file)

### Done
Binary acceptance criteria. Unambiguous pass/fail — no "mostly works" or "looks good."

Examples:
- "POST /api/auth/login returns 200 with JWT for valid credentials and 401 for invalid credentials"
- "UserService class exists with login(), logout(), and getCurrentUser() methods"
- "All existing tests pass and 3 new tests added for auth middleware"

## Scope Estimation

Target ~50% context window utilization per plan (~100K tokens of work).

### Context Budget Breakdown
| Activity | Tokens |
|---|---|
| Plan loading + project context | ~10K |
| File reads (existing code) | ~20K |
| Implementation (code written) | ~30K |
| Verification + debugging | ~20K |
| Summary creation | ~5K |
| Safety buffer | ~15K |
| **Total** | **~100K** |

### Quality Degradation Curve
- **0-50% context**: High quality. Executor follows instructions precisely, verifies thoroughly.
- **50-75% context**: Quality degrades. Executor may skip verification steps, produce less clean code.
- **75-90% context**: Significant degradation. Executor may hallucinate imports, skip edge cases.
- **90%+ context**: Unreliable. Executor may produce broken code, false completion claims.

### Sizing Heuristic
- 2-3 tasks per plan
- Each task: 15-60 minutes of estimated implementation work
- If a task would take >60 minutes, split it into subtasks across plans

## Dependency Graph Construction

### Step 1: List All Plans
Enumerate every plan for the phase with its inputs and outputs.

### Step 2: Identify Productions
For each plan, what does it produce?
- New files (types, services, components, configs)
- New exports (functions, classes, constants)
- New API endpoints
- New database tables/migrations
- New test fixtures

### Step 3: Identify Consumptions
For each plan, what does it consume?
- Imports from other plans' files
- API calls to other plans' endpoints
- Database queries against other plans' tables
- Type references from other plans' type definitions

### Step 4: Draw Edges
If Plan B consumes what Plan A produces, draw an edge: A → B (B depends on A).

### Step 5: Detect Cycles
If the graph has cycles (A → B → C → A), restructure:
- Extract the shared dependency into its own plan
- Merge the cyclically-dependent plans into one
- Introduce an interface plan that defines contracts without implementation

## Wave Assignment Algorithm

```
FUNCTION assignWaves(plans):
  FOR each plan P:
    IF P has no dependencies:
      P.wave = 1
    ELSE:
      P.wave = MAX(dependency.wave for all dependencies) + 1
  RETURN plans sorted by wave
```

Properties:
- Plans in the same wave have no dependencies on each other → can execute in parallel
- Plans in wave N+1 depend only on plans in waves 1..N → sequential after prior waves complete
- Fewer waves = faster total execution time

## Vertical Slices vs Horizontal Layers

### Horizontal Layers (avoid)
```
Plan 1: All database tables
Plan 2: All API endpoints
Plan 3: All UI components
```
Problems:
- Can't test anything until all 3 plans complete
- Each plan touches many unrelated concerns
- Integration issues discovered late

### Vertical Slices (prefer)
```
Plan 1: User auth (DB + API + UI for login/signup)
Plan 2: User profile (DB + API + UI for profile management)
Plan 3: Dashboard (DB + API + UI for dashboard data)
```
Benefits:
- Each plan delivers a testable increment
- Integration verified within the plan
- Failures are contained to one feature

### When Horizontal Is Acceptable
- Shared infrastructure (database migrations, config setup) — Wave 1 horizontal plan, then vertical slices in Wave 2+
- Cross-cutting concerns (auth middleware, error handling) that many features depend on

## Interface-First Ordering

Within a plan, order tasks so contracts come before implementations:

1. **Task 1**: Define types, interfaces, API contracts
2. **Task 2**: Implement against the contracts
3. **Task 3**: Wire up and verify integration

This ensures the executor has stable interfaces to code against, reducing back-and-forth modifications.

## File Ownership

No two plans in the same wave may modify the same file. This is a hard constraint for parallel execution.

### Checking File Ownership
Before assigning plans to waves, build a file ownership map:

```
Plan 01 (Wave 1): src/types/user.ts, src/services/user.ts
Plan 02 (Wave 1): src/types/post.ts, src/services/post.ts
Plan 03 (Wave 1): src/services/user.ts  ← CONFLICT with Plan 01
```

Resolution: Move Plan 03 to Wave 2 (after Plan 01 completes), or restructure so Plan 01 and Plan 03 don't both modify `src/services/user.ts`.

### Shared Files
Some files are naturally shared (index files, route registrations, config). Strategies:
- Defer shared file modifications to a "wiring" plan in a later wave
- Have one plan own the shared file and other plans document what they need added
- Use append-only patterns where each plan adds to the file without modifying existing content
