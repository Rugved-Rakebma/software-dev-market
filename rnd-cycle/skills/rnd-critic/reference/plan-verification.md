# Plan Verification

Reference for validating build plans. Used by rnd-critic to check plan quality across 7 dimensions, classified as BLOCKER (gates revision) or ADVISORY (reported only).

## Verification Loop

```
rnd-planner produces plans
        |
rnd-critic checks 7 dimensions
        |
    Issues found?
    +-- No blockers          -> APPROVED (with or without advisories)
    +-- Blockers present     -> NEEDS_REVISION
                                    |
                                rnd-planner revises
                                    |
                                Recheck
                                    |
                                Still blockers?
                                +-- Yes -> escalate to user
```

**Loop budget by command:**
- `/rnd:plan` — max **1** revision loop on blockers only (advisories never trigger revision)
- `/rnd:validate` — max **3** revision loops (heavier adversarial pass)

Advisories never gate. They are reported alongside the verdict for the user / planner to consider.

## 7 Verification Dimensions

| # | Dimension | Severity | Gates? |
|---|---|---|---|
| 1 | Requirement Coverage | **BLOCKER** | Yes — every REQ must be claimed |
| 2 | Task Completeness | **BLOCKER** | Yes — missing Build/Done breaks coder |
| 3 | Dependency Correctness | **BLOCKER** | Yes — cycles break wave execution |
| 4 | Scope Sanity | ADVISORY | No — plan executable but maybe oversized |
| 5 | Verification Derivation | ADVISORY | No — Done can be tightened post-hoc |
| 6 | Wires-to Completeness | ADVISORY | No — coder gets fallback (full arch) |
| 7 | Context Compliance | **BLOCKER** | Yes — contradicting locked decisions invalidates the plan |

### Dimension 1: Requirement Coverage [BLOCKER]

Every REQ-ID from `.rnd/spec/spec.md` must appear in at least one plan's `requirements` frontmatter field.

**Check:** Extract all REQ-{CAT}-{NN} from the spec. For each, verify it appears in ≥1 plan.

**Issue format:**
```
dimension: requirement-coverage
severity: BLOCKER
description: REQ-AUTH-03 (password reset flow) not covered by any plan
fix_hint: Add a plan or extend an existing plan to cover password reset
```

### Dimension 2: Task Completeness [BLOCKER]

Every task in every plan must have both `Build:` and `Done:`.

**Check:** Parse each plan's tasks. Verify both fields are present and non-empty. Verify Build does not contain code/signatures. Verify Done is binary-verifiable.

**Issue format:**
```
dimension: task-completeness
severity: BLOCKER
description: Plan 03, Task 2 missing Done field
fix_hint: Add a binary verification — e.g., `just typecheck` exits 0
```

Common failures: Build contains pseudocode or signatures; Done says "works correctly" (vague); Files field uses wildcards.

### Dimension 3: Dependency Correctness [BLOCKER]

No circular dependencies. All `depends_on` references point to existing plan IDs.

**Check:**
1. Build adjacency list from `depends_on` fields
2. Run cycle detection (DFS with back-edge detection)
3. Verify every referenced plan ID exists

**Issue format:**
```
dimension: dependency-correctness
severity: BLOCKER
description: Circular dependency: 03-vault -> 05-prompts -> 03-vault
fix_hint: Extract shared dep into a new plan, merge cyclic plans, or introduce an interface plan
```

### Dimension 4: Scope Sanity [ADVISORY]

2-3 tasks per plan. Each task ~15-60 minutes.

**Check:** Count tasks per plan. Flag plans with 1 task (too granular) or 4+ tasks (too large).

**Issue format:**
```
dimension: scope-sanity
severity: ADVISORY
description: Plan 04 has 5 tasks — likely exceeds ~50% context budget
fix_hint: Split into Plan 04a (Tasks 1-3) and Plan 04b (Tasks 4-5)
```

### Dimension 5: Verification Derivation [ADVISORY]

Each `Done:` should trace to a spec REQ or arch acceptance criterion. Truths that can't trace are likely fabricated.

**Check:** For each task's Done, verify it maps to a specific REQ-ID or arch constraint.

**Issue format:**
```
dimension: verification-derivation
severity: ADVISORY
description: Plan 01 Task 2 Done "system handles 10K concurrent users" not traceable to any spec requirement
fix_hint: Either add a performance REQ to the spec or relax this Done
```

### Dimension 6: Wires-to Completeness [ADVISORY]

If the plan references contracts that live in the arch doc, those arch sections should appear in the `## Wires to` section so c-build can bundle the right slices into the coder's prompt.

**Check:** For each plan, scan task bodies for arch references ("arch §X", "per arch …"). Verify each appears in `## Wires to`.

**Issue format:**
```
dimension: wires-to-completeness
severity: ADVISORY
description: Plan 02 Task 1 references "arch §5.1" but it's not in ## Wires to
fix_hint: Add `arch §5.1 — retrieve_sources contract` to Wires to
```

### Dimension 7: Context Compliance [BLOCKER]

Locked decisions from `.rnd/decisions/` are honored, not re-evaluated.

**Check:** Read all files in `.rnd/decisions/`. For each locked decision, verify no plan contradicts it or re-evaluates the decision.

**Issue format:**
```
dimension: context-compliance
severity: BLOCKER
description: Plan 03 Task 1 says "evaluate PostgreSQL vs MongoDB" but DEC-002 locks PostgreSQL
fix_hint: Remove the evaluation — use PostgreSQL as specified in DEC-002
```

## Verdict

| Verdict | Condition |
|---|---|
| `APPROVED` | No blockers, no advisories |
| `APPROVED_WITH_ADVISORIES` | No blockers, advisories present |
| `NEEDS_REVISION` | One or more blockers present |

Only `NEEDS_REVISION` triggers a revision loop. `APPROVED_WITH_ADVISORIES` proceeds — advisories are surfaced in the verdict report.

## Verification Report Format

```
## Plan Verification Report

### Verdict: APPROVED | APPROVED_WITH_ADVISORIES | NEEDS_REVISION

### Summary
- Plans checked: N
- Blockers: N
- Advisories: N

### Blockers
[List all BLOCKER-severity issues, each with dimension/description/fix_hint]

### Advisories
[List all ADVISORY-severity issues]

### Requirement Coverage Matrix
| REQ-ID | Description | Covered By |
|--------|-------------|------------|
| REQ-AUTH-01 | User login | 02-auth |
| REQ-AUTH-02 | Password reset | (MISSING) |

### Dependency Graph
[Text rep of plan dependency graph with wave assignments]
```
