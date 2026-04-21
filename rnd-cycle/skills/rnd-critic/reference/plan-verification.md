# Plan Verification

Reference material for validating build plans before execution. Used by rnd-critic to check plan quality across 7 dimensions.

## Verification Loop

```
rnd-planner produces plans
        |
rnd-critic checks 7 dimensions
        |
    Issues found?
    +-- No  -> Plans approved, proceed to execution
    +-- Yes -> rnd-planner revises
                |
              Recheck (max 3 loops)
                |
            Still issues?
            +-- No  -> Approved
            +-- Yes -> Escalate to user
```

Maximum 3 revision loops. If plans still have issues after 3 revisions, escalate to the user with a clear summary of remaining problems.

## 7 Verification Dimensions

### Dimension 1: Requirement Coverage

Every REQ-ID from `.rnd/spec/spec.md` must appear in at least one plan's `requirements` field.

**Check**: Extract all REQ-{CAT}-{NN} identifiers from the spec. For each, verify it appears in at least one plan's frontmatter `requirements` array.

**Issue format**:
```
dimension: requirement-coverage
severity: blocker
description: REQ-AUTH-03 (password reset flow) not covered by any plan
fix_hint: Add a plan or extend an existing plan to cover password reset
```

**Common failures**:
- Non-functional requirements (performance, security) overlooked
- Edge-case requirements lumped into "will handle later"
- v2 requirements accidentally excluded from v1 plans

### Dimension 2: Task Completeness

Every task in every plan must have all four fields: Files, Action, Verify, Done.

**Check**: Parse each plan's tasks. Verify all four fields are present and non-empty.

**Issue format**:
```
dimension: task-completeness
severity: blocker
description: Plan 03, Task 2 missing Verify field
fix_hint: Add a verification command — e.g., "just typecheck" or "file exports expected function"
```

**Common failures**:
- Verify field says "manual check" (not automated)
- Done field is vague ("works correctly" instead of binary criteria)
- Files field uses wildcards instead of exact paths

### Dimension 3: Dependency Correctness

No circular dependencies. All `depends_on` references point to existing plan numbers.

**Check**:
1. Build adjacency list from `depends_on` fields
2. Run cycle detection (DFS with back-edge detection)
3. Verify every referenced plan number exists

**Issue format**:
```
dimension: dependency-correctness
severity: blocker
description: Circular dependency: Plan 03 -> Plan 05 -> Plan 03
fix_hint: Extract shared dependency into a new plan, or merge Plans 03 and 05
```

**Common failures**:
- Implicit dependencies not declared (Plan B uses a type from Plan A but doesn't list A in depends_on)
- Stale references to plans that were renumbered or removed

### Dimension 4: Key Links

`must_haves.key_links` must specify wiring (from -> to -> via), not just isolated artifacts.

**Check**: Every plan with 2+ artifacts in `must_haves.artifacts` should have at least one `key_link` connecting them. Plans that produce both a service and a consumer must show how they connect.

**Issue format**:
```
dimension: key-links
severity: warning
description: Plan 02 produces UserService and UserController but no key_link shows how controller uses service
fix_hint: Add key_link — from: "src/controllers/user.ts", to: "src/services/user.ts", via: "constructor injection"
```

**Common failures**:
- Plans produce files but don't specify how they connect
- key_links only show import relationships, not actual usage
- Cross-plan wiring assumed but not documented

### Dimension 5: Scope Sanity

2-3 tasks per plan. Each task estimated at 15-60 minutes.

**Check**: Count tasks per plan. Flag plans with 1 task (too granular) or 4+ tasks (too large).

**Issue format**:
```
dimension: scope-sanity
severity: warning
description: Plan 04 has 5 tasks — likely exceeds ~50% context budget
fix_hint: Split into Plan 04a (Tasks 1-3) and Plan 04b (Tasks 4-5)
```

**Common failures**:
- "Kitchen sink" plans that try to do everything for a feature
- Single-task plans that waste context window overhead
- Tasks estimated at >60 minutes that should be split

### Dimension 6: Verification Derivation

`must_haves.truths` must trace directly to spec requirements or architecture goals.

**Check**: For each truth in must_haves, verify it maps to a specific REQ-ID or architecture constraint. Truths that can't be traced are likely fabricated or aspirational.

**Issue format**:
```
dimension: verification-derivation
severity: warning
description: Plan 01 truth "system handles 10K concurrent users" not traceable to any spec requirement
fix_hint: Either add a performance requirement to the spec or remove this truth
```

**Common failures**:
- Truths that are technically interesting but not required by the spec
- Truths that are too vague to verify ("system is well-structured")
- Truths that duplicate other plans' truths

### Dimension 7: Context Compliance

Locked decisions from `.rnd/decisions/` are honored, not re-evaluated.

**Check**: Read all files in `.rnd/decisions/`. For each locked decision, verify no plan contradicts it or re-evaluates the decision.

**Issue format**:
```
dimension: context-compliance
severity: blocker
description: Plan 03 Task 1 says "evaluate PostgreSQL vs MongoDB" but DEC-002 locks PostgreSQL as the database
fix_hint: Remove the evaluation — use PostgreSQL as specified in DEC-002
```

**Common failures**:
- Plans that "explore alternatives" for already-decided technologies
- Plans that introduce patterns contradicting architectural decisions
- Plans that use different naming conventions than those locked in decisions

## Issue Severity Levels

| Severity | Meaning | Action |
|---|---|---|
| **blocker** | Plan cannot be executed as-is. Will produce incorrect or incomplete results. | Must fix before execution |
| **warning** | Plan can be executed but quality or integration may suffer. | Should fix, can proceed with documented risk |
| **info** | Observation or suggestion for improvement. | Optional improvement |

## Verification Report Format

```
## Plan Verification Report

### Summary
- Plans checked: N
- Blockers: N
- Warnings: N
- Info: N
- Verdict: APPROVED / NEEDS REVISION

### Issues

#### Blockers
[List all blocker-severity issues]

#### Warnings
[List all warning-severity issues]

#### Info
[List all info-severity observations]

### Requirement Coverage Matrix
| REQ-ID | Description | Covered By |
|--------|-------------|------------|
| REQ-AUTH-01 | User login | Plan 02 |
| REQ-AUTH-02 | Password reset | (MISSING) |

### Dependency Graph
[Text representation of plan dependency graph with wave assignments]
```
