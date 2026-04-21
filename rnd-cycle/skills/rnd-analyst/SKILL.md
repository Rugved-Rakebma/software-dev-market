---
name: rnd-analyst
description: Audit methodology, investigation techniques, and report templates. Used by both rnd-analyst (document mode) and rnd-code-analyst (code mode) agents.
user-invocable: false
---

# R&D Analyst

The rnd-analyst skill is the consolidated knowledge base that powers investigation capabilities. It contains five reference documents covering investigation methodology and six templates for structured output. Used by both `rnd-analyst` (document mode) and `rnd-code-analyst` (code mode) agents.

## Reference Documents

### 1. Audit Methodology (`reference/audit-methodology.md`)
**Use when**: Performing codebase audits or document audits and need the confidence classification framework, calibration tiers, and evidence format.

Includes:
- Two modes: codebase audit vs document audit
- Confidence classification (Confident/Likely/Unclear) with definitions
- Calibration tiers (full_maturity, standard, minimal_decisive)
- Evidence format: Assumption -> Evidence -> If Wrong -> Confidence
- "Needs External Research" section format
- Document audit gap categories and assessment criteria

### 2. Codebase Mapping (`reference/codebase-mapping.md`)
**Use when**: Running codebase-audit mode and need exploration patterns, output templates, and writing guidelines.

Includes:
- 4-track parallel analysis model (tech/arch/quality/concerns)
- Exploration patterns using Grep/Glob/Read for each track
- Full template content for STACK, ARCHITECTURE, STRUCTURE, CONVENTIONS, TESTING, CONCERNS
- "Prescriptive not descriptive" writing guide
- File path citation requirements
- Forbidden files list

### 3. Verification Methodology (`reference/verification-methodology.md`)
**Use when**: Running verification mode and need the 4-level verification framework, stub detection patterns, and report structure.

Includes:
- Goal-backward verification principle
- 4-level verification (EXISTS -> SUBSTANTIVE -> WIRED -> DATA FLOWS)
- Stub detection patterns (React, API routes, wiring red flags)
- Re-verification mode for previously-failed items
- Requirements coverage checking
- Anti-pattern scanning patterns
- Behavioral spot-checks
- Human verification flagging criteria
- Overall status determination

### 4. Security Review (`reference/security-review.md`)
**Use when**: Running security-review mode and need STRIDE framework, OWASP patterns, and severity classification.

Includes:
- STRIDE threat model framework with examples and mitigations
- OWASP Top 10 checklist with Grep patterns
- Secrets scanning patterns
- Auth verification methodology
- Input validation checks
- Security headers checklist
- Severity-ranked output format (Critical/High/Medium/Low)

### 5. Code Review (`reference/code-review.md`)
**Use when**: Running code-review mode and need severity tiers, integration wiring checks, and anti-pattern catalog.

Includes:
- Line-by-line review methodology
- Severity tiers (Blocker/Suggestion/Nit) with definitions
- Review comment format
- Integration wiring checks (export/import map, API consumers, auth protection, E2E flows)
- Requirements Integration Map format
- Anti-pattern catalog (orphaned exports, unused imports, form-without-handler, API-without-consumer, state-without-render)

## Templates

### 1. Codebase Audit — Stack (`templates/audit-stack.md`)
**Use when**: Producing tech track output from codebase-audit mode.
Sections: Languages, Runtime, Frameworks, Key Dependencies, Configuration, Platform Requirements.

### 2. Codebase Audit — Architecture (`templates/audit-architecture.md`)
**Use when**: Producing arch track output from codebase-audit mode.
Sections: Pattern Overview, Layers, Data Flow, Key Abstractions, Entry Points, Error Handling, Cross-Cutting Concerns.

### 3. Codebase Audit — Conventions (`templates/audit-conventions.md`)
**Use when**: Producing quality track output from codebase-audit mode.
Sections: Naming Patterns, Code Style, Import Organization, Error Handling, Logging, Comments, Function Design, Module Design.

### 4. Codebase Audit — Concerns (`templates/audit-concerns.md`)
**Use when**: Producing concerns track output from codebase-audit mode.
Sections: Tech Debt, Known Bugs, Security Considerations, Performance Bottlenecks, Fragile Areas, Scaling Limits, Dependencies at Risk, Missing Critical Features, Test Coverage Gaps.

### 5. Document Audit (`templates/audit-document.md`)
**Use when**: Producing output from document-audit mode.
Sections: Document Summary, Gaps, Assumptions, Risks, Ambiguities, Implementability Assessment, Recommendations.

### 6. Verification Report (`templates/verification-report.md`)
**Use when**: Producing output from verification mode.
Sections: YAML frontmatter with gaps/human_verification, Observable Truths, Required Artifacts, Key Link Verification, Data-Flow Trace, Requirements Coverage, Anti-Patterns Found, Behavioral Spot-Checks, Human Verification Required, Gaps Summary.

## Quick Reference

### Mode Selection
| Mode | Trigger | Output |
|------|---------|--------|
| codebase-audit | Map/analyze/understand a codebase | Stack + Architecture + Conventions + Concerns |
| document-audit | Analyze spec/PRD/proposal | Gap analysis + Assumptions + Risks |
| verification | Verify implementation completeness | Verification report with pass/fail |
| code-review | Review code changes or PRs | Severity-ranked findings + wiring check |
| security-review | Check for vulnerabilities/threats | STRIDE + OWASP findings by severity |

### Confidence Tiers
| Tier | Definition | When to Use |
|------|-----------|-------------|
| Confident | Clear from code/evidence | Pattern explicit, unambiguous |
| Likely | Reasonable inference | Pattern implied, consistent |
| Unclear | Could go multiple ways | Evidence thin, contradictory, absent |

### Verification Levels
| Level | Check | Pass | Fail |
|-------|-------|------|------|
| 1: EXISTS | File at expected path | FOUND | MISSING |
| 2: SUBSTANTIVE | Real content, not stub | REAL | STUB |
| 3: WIRED | Imported AND used | WIRED | ORPHANED |
| 4: DATA FLOWS | Real data, not static | FLOWING | DISCONNECTED |

### Review Severity
| Tier | Scope | Examples |
|------|-------|---------|
| Blocker | Security, data loss, crashes | SQL injection, race condition, auth bypass |
| Suggestion | Quality, maintainability | Missing validation, unclear naming, no tests |
| Nit | Style, preferences | Naming alternatives, docs, approach options |

## Usage Flow

```
Investigation Request
    |
    v
[Determine mode from context]
    |
    +---> codebase-audit ---> [codebase-mapping] ---> 4-track analysis
    |
    +---> document-audit ---> [audit-methodology] ---> gap/risk analysis
    |
    +---> verification -----> [verification-methodology] ---> 4-level checks
    |
    +---> code-review ------> [code-review] ---> quality + wiring checks
    |
    +---> security-review --> [security-review] ---> STRIDE + OWASP scan
    |
    v
Structured output using appropriate template
```
