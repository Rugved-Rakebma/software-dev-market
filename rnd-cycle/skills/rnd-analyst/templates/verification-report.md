---
scope: [what was verified — feature name, phase, or milestone]
verified: YYYY-MM-DDTHH:MM:SSZ
status: passed | gaps_found | human_needed
score: N/M
gaps:
  - truth: "Observable truth that failed"
    status: failed
    reason: "Brief explanation"
    artifacts:
      - path: "src/path/to/file"
        issue: "What is wrong"
    missing:
      - "Specific thing to add/fix"
human_verification:
  - test: "What to do"
    expected: "What should happen"
    why_human: "Why this cannot be verified programmatically"
---

# Verification Report: [Scope Name]

**Goal:** [The stated goal or outcome being verified]
**Verified:** [timestamp]
**Status:** [passed | gaps_found | human_needed]
**Score:** [N/M] observable truths verified

## Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | [What must be true for the goal to be achieved] | VERIFIED / FAILED | [File paths and observations] |
| 2 | [Truth statement] | VERIFIED / FAILED | [Evidence] |

## Required Artifacts

| Artifact | Expected | L1: Exists | L2: Substantive | L3: Wired | L4: Data Flows | Status |
|----------|----------|------------|-----------------|-----------|----------------|--------|
| `[path]` | [What it should contain] | FOUND/MISSING | REAL/STUB | WIRED/ORPHANED | FLOWING/STATIC | [Final status] |

## Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `[source file]` | `[target file/route]` | [How connected — import, fetch, etc.] | WIRED/PARTIAL/NOT_WIRED | [Specific observations] |

## Data-Flow Trace

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `[component]` | [state variable name] | `[API route or data source]` | Yes/No | FLOWING/STATIC/DISCONNECTED |

## Requirements Coverage

| Requirement | Description | Status | Evidence |
|-------------|-------------|--------|----------|
| [REQ-ID] | [Brief description] | SATISFIED/BLOCKED/NEEDS_HUMAN | [File paths showing implementation] |

**Orphaned Requirements:** [Requirements expected for this scope that have no implementation evidence]

## Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `[path]` | [line #] | [What was found — TODO, stub, debug log, etc.] | Blocker/Warning/Info | [Effect on goal] |

## Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| [What was tested] | [Command run] | [Output observed] | PASS/FAIL/SKIP |

## Human Verification Required

### 1. [Test Name]

**Test:** [Step-by-step instructions for what to do]
**Expected:** [What should happen when the test is performed]
**Why human:** [Why this cannot be verified programmatically]

## Gaps Summary

[Narrative summary of what is missing and why. Group related gaps by root cause. Identify the minimum set of fixes needed to move from gaps_found to passed.]

---
*Verified: [timestamp]*
*Verifier: rnd-analyst (verification mode)*
