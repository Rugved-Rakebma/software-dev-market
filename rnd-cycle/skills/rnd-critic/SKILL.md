---
name: rnd-critic
description: Assumption challenging frameworks, anti-pattern detection catalogs, and validation report structures. Loaded by main session during /rnd:decide, and by the rnd-critic agent during /rnd:validate and /rnd:plan validation loops.
user-invocable: false
---

# R&D Critic

The validation and strategic analysis knowledge base for the `rnd-critic` agent. This skill consolidates four complementary frameworks into a single reference for adversarial validation of plans, proposals, decisions, and roadmaps. Loaded by the main session during `/rnd:decide`, and by the `rnd-critic` agent during `/rnd:validate` and `/rnd:plan` validation loops.

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
**Use when**: Validating build plan quality before execution during `/rnd:plan` validation loops.
**Provides**:
- 7 verification dimensions (requirement coverage, task completeness, dependency correctness, key links, scope sanity, verification derivation, context compliance)
- Verification loop (planner produces -> critic checks -> planner revises, max 3 loops)
- Issue format (dimension, severity, description, fix hint)
- Verification report format with requirement coverage matrix

## Quick Reference

### Validation Workflow

```
Proposal/Plan arrives
     |
     v
[assumption-challenging] -> Surface and categorize assumptions
     |                      Assess evidence, risk, and validity
     |
     v
[antipattern-detection] -> Scan for failure patterns
     |                     Verify matches and assess severity
     |
     v
[plan-verification]     -> Validate 7 dimensions (if build plans)
     |
     v
[validation-reports]    -> Determine verdict using decision tree
                          Generate structured 8-section report
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
