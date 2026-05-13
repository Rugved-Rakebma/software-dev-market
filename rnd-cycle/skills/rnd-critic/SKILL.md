---
name: rnd-critic
description: Assumption challenging frameworks, anti-pattern detection catalogs, and validation report structures. Loaded by main session during /rnd:decide, and by the rnd-critic agent during /rnd:validate and /rnd:plan validation loops.
user-invocable: false
---

# R&D Critic

The validation and strategic analysis knowledge base for the `rnd-critic` agent. Four complementary frameworks for adversarial validation of plans, proposals, decisions, and roadmaps.

## When to Use Which References

The critic is invoked from multiple commands with different budgets. Load only what each command needs:

| Caller | References to load | Loop budget | Purpose |
|---|---|---|---|
| `/rnd:plan` (standard/large scope) | `plan-verification.md` only | Max **1** revision loop on BLOCKERs only | Cheap pass — catch real plan bugs before build |
| `/rnd:plan` (small scope) | (skip the critic entirely) | — | Small projects don't warrant the ceremony; user can run `/rnd:validate` manually |
| `/rnd:validate` | All four references | Max **3** revision loops | Heavy adversarial pass — full 8-section validation report |
| `/rnd:decide` | `assumption-challenging.md` + `antipattern-detection.md` | N/A (not a build plan) | Reason about decisions/tradeoffs |

**Do not load `validation-reports.md` for `/rnd:plan`** — it's the heavy 8-section format used by `/rnd:validate`. `/rnd:plan` uses the compact verdict format defined in `plan-verification.md`.

**Do not load `antipattern-detection.md` or `assumption-challenging.md` for `/rnd:plan`** — they're 800+ and 500+ lines respectively, written for strategic adversarial review, not lightweight plan checking.

## Reference Documents

### 1. Assumption Challenging
**File**: `reference/assumption-challenging.md`
**Use when**: You need to systematically surface and stress-test implicit assumptions in plans, proposals, roadmaps, or architecture decisions.
**Provides**:
- 5 assumption categories (Timeline, Resource, Technical, Business, External)
- Step-by-step identification and assessment process
- Challenge patterns (Reality Check, History Test, Stress Test, Dependency Audit, Inverse Test)
- Wishful thinking indicators
- Ready-to-use challenge questions organized by category and intensity level
- Output format template for assumption analysis

### 2. Anti-Pattern Detection
**File**: `reference/antipattern-detection.md`
**Use when**: You need to detect common failure patterns in proposals, architectures, team structures, or project plans before they become problems.
**Provides**:
- 25+ anti-patterns across 5 categories (Architecture, Timeline, Team, Process, Technology)
- Detection signals and red flag phrases
- Severity framework (Critical / High / Medium / Low)
- Detailed catalog with examples, consequences, and remediation for each pattern
- Common pattern combinations (Startup Death Spiral, Enterprise Trap, Tech Debt Avalanche, Microservices Mistake)
- Output format template for anti-pattern analysis

### 3. Validation Reports
**File**: `reference/validation-reports.md`
**Use when**: After completing validation analysis and you need to produce a structured final deliverable with a clear verdict.
**Provides**:
- 8-section report structure (Verdict, Strengths, Flaws, Blindspots, Reframe, Bulletproof Criteria, Path Forward, Questions)
- Verdict criteria and decision tree for GOOD / NEEDS MAJOR WORK / BAD
- Full report template with all sections
- Confidence level framework
- Tone calibration by verdict severity
- Edge case handling (mixed signals, insufficient information, scope mismatch)
- Calibration examples for each verdict type

### 4. Plan Verification
**File**: `reference/plan-verification.md`
**Use when**: Validating build plan quality before execution during `/rnd:plan` (standard/large scope only).
**Provides**:
- 7 verification dimensions classified as **BLOCKER** (gates revision) or **ADVISORY** (reported only)
  - BLOCKER: requirement coverage, task completeness, dependency correctness, context compliance
  - ADVISORY: scope sanity, verification derivation, wires-to completeness
- Verdict triplet: `APPROVED` / `APPROVED_WITH_ADVISORIES` / `NEEDS_REVISION`
- Only `NEEDS_REVISION` (blockers present) triggers a revision loop
- Loop budget: 1 in `/rnd:plan`, 3 in `/rnd:validate`
- Compact verification report format with requirement coverage matrix

## Quick Reference

### Validation Workflow

The workflow branches by caller:

```
                         Proposal / Plan arrives
                                  |
                                  v
              Which command is invoking the critic?
                                  |
       +--------------------------+--------------------------+
       |                          |                          |
       v                          v                          v
  /rnd:plan small           /rnd:plan std/lg           /rnd:validate
       |                          |                          |
   (skip critic)         [plan-verification]    [assumption-challenging]
                                  |                          |
                          Compact verdict        [antipattern-detection]
                          1-loop budget                      |
                          BLOCKERs only             [plan-verification]
                                                             |
                                                    [validation-reports]
                                                    8-section report
                                                    3-loop budget
```

### Assumption Categories
| Category | Risk if Wrong | Validation Difficulty |
|----------|---------------|----------------------|
| Timeline | Project delay | Medium |
| Resource | Execution failure | Medium |
| Technical | System failure | High |
| Business | Wasted investment | High |
| External | Plans disrupted | Variable |

### Critical Anti-Patterns
| Pattern | Category | Severity |
|---------|----------|----------|
| Hero Culture | Team | Critical |
| Timeline Fantasy | Timeline | Critical |
| Premature Microservices | Architecture | High |
| Not Invented Here | Technology | High |
| MVP Maximalism | Timeline | High |

### Verdict Decision Summary
| Verdict | Meaning | Action |
|---------|---------|--------|
| **GOOD** | Ready for implementation | Proceed with minor notes |
| **NEEDS MAJOR WORK** | Sound foundation, significant gaps | Revise and re-validate |
| **BAD** | Fundamentally flawed | Stop and rethink |
