---
name: rnd-build
description: Planning methodology, wave orchestration, execution methodology, and build coordination reference material. Used by rnd-planner (planning) and rnd-coder (execution).
user-invocable: false
---

# R&D Build

The rnd-build skill is the consolidated knowledge base that powers the build pipeline. It contains reference documents covering specification, planning, execution, orchestration, testing, and agent coordination — plus templates for plan and summary files. Used by `rnd-planner` (planning) and `rnd-coder` (execution).

## Reference Documents

### 1. Spec Methodology (`reference/spec-methodology.md`)
**Use when**: Turning ideas into structured specifications with testable requirements.

Includes:
- Problem framing techniques (problem-first, not solution-first)
- Interview process for requirement extraction
- REQ-{CAT}-{NN} identifier format and conventions
- Scope classification decision tree (v1/v2/out-of-scope)
- Gap identification checklist (15 common gaps)
- Success criteria writing guide (binary-testable outcomes)
- Open questions format that routes to /rnd:research

### 2. Planning Methodology (`reference/planning-methodology.md`)
**Use when**: Breaking project phases into executable build plans.

Includes:
- Plans-are-prompts principle (plans are consumed by rnd-coder agents, not humans)
- Task breakdown rules (Files/Action/Verify/Done, 2-3 tasks per plan)
- Scope estimation (~50% context window target, quality degradation curve)
- Dependency graph construction (productions, consumptions, edges)
- Wave assignment algorithm (independent plans parallel, dependent sequential)
- Vertical slices vs horizontal layers (prefer vertical)
- Interface-first ordering (contracts before implementations)
- File ownership rules (no two same-wave plans modify the same file)

### 3. Execution Methodology (`reference/execution-methodology.md`)
**Use when**: Executing a build plan — implementing tasks, committing, and producing summaries.

Includes:
- 9-step execution flow (load state -> execute -> verify -> summarize -> self-check)
- 4-tier deviation rules with examples (bug fix, missing piece, blocking issue, architectural change)
- Commit conventions: `{type}({phase}-{plan}): {description}`
- Summary format (frontmatter + one-liner + deviations + stubs + self-check)
- Execution guards (analysis paralysis, fix attempt limit, scope boundary)

### 4. Wave Orchestration (`reference/wave-orchestration.md`)
**Use when**: Orchestrating parallel execution of multiple plans in waves.

Includes:
- Wave concept (parallel within wave, sequential between waves)
- Task spawning pattern (one rnd-coder per plan, all same-wave in parallel)
- Result collection (read status report from each coder)
- Wave completion gate (all coders done, no blockers)
- Error handling (coder failure, blocking issues, merge conflicts)

### 5. Test Methodology (`reference/test-methodology.md`)
**Use when**: Generating tests driven by spec requirements.

Includes:
- Requirement-driven test generation (each REQ-ID maps to 1+ test cases)
- Test categories (unit, integration, e2e) with characteristics and examples
- Test classification by requirement type (data->integration, UI->e2e, API->integration, auth->security)
- Verification command format (runnable in <10s, read-only)
- Debug loop (check implementation first, 3 iterations max, escalate if stuck)

### 6. Handoff Contracts (`reference/handoff-contracts.md`)
**Use when**: Understanding what each agent sends and receives in the build and verify flows.

Includes:
- Input/output contract for every agent-to-agent handoff
- Main session -> rnd-coder contract
- Main session -> code-simplifier contract
- Main session -> rnd-code-spec-checker contract
- Main session -> rnd-code-reviewer contract
- Main session -> rnd-code-analyst contract

### 7. Escalation Protocol (`reference/escalation-protocol.md`)
**Use when**: Deciding whether to continue, stop, or escalate during build execution.

Includes:
- Status definitions: DONE, DONE_WITH_CONCERNS, BLOCKED, NEEDS_CONTEXT
- Retry limits (max 2 re-attempts per review gate failure)
- Escalation triggers (architectural decisions, code beyond context, uncertainty about correctness)

### 8. Reporting Format (`reference/reporting-format.md`)
**Use when**: Producing standardized status reports from code agents.

Includes:
- Standardized status report template for all code agents
- Evidence requirements (file:line citations for every claim)
- Tasks completed, files changed, commits, test results, concerns sections

## Templates

### Plan Template (`templates/plan-template.md`)
**Use when**: Creating a new build plan. Copy and fill in the template.

### Summary Template (`templates/summary-template.md`)
**Use when**: Creating an execution summary after plan completion. Copy and fill in the template.

### Spec Template (`templates/spec-template.md`)
**Use when**: Creating a new project specification.

## Quick Reference

### Requirement ID Format
| Category | Prefix | Example |
|----------|--------|---------|
| Authentication | AUTH | REQ-AUTH-01 |
| User Interface | UI | REQ-UI-03 |
| Data / Storage | DATA | REQ-DATA-02 |
| API / Integration | API | REQ-API-01 |
| Performance | PERF | REQ-PERF-01 |
| Security | SEC | REQ-SEC-01 |
| Infrastructure | INFRA | REQ-INFRA-01 |
| Business Logic | BIZ | REQ-BIZ-01 |

### Scope Classification
| Scope | Criteria | Action |
|-------|----------|--------|
| v1 — Must Have | Blocks core value proposition | Implement first |
| v2 — Planned | Enhances but not required for launch | Defer with rationale |
| Out of Scope | Not aligned with vision or premature | Exclude with reason |

### Escalation Status Quick Reference
| Status | Meaning | Action |
|--------|---------|--------|
| **DONE** | All tasks implemented, tests pass | Continue to next plan/wave |
| **DONE_WITH_CONCERNS** | Completed but doubts about correctness | Review concerns, decide if blocking |
| **BLOCKED** | Cannot proceed | Surface to user, pause |
| **NEEDS_CONTEXT** | Missing information, risks quality | Surface to user, decide if blocking |

### Gap Checklist (Quick)
| # | Gap Area | Ask |
|---|----------|-----|
| 1 | Auth | Who can access what? |
| 2 | Error handling | What happens when things fail? |
| 3 | Edge cases | What are the boundary conditions? |
| 4 | Data migration | Is there existing data to move? |
| 5 | Monitoring | How will you know it's healthy? |
| 6 | Rollback | How do you undo a bad deploy? |
| 7 | Rate limiting | What prevents abuse? |
| 8 | Permissions | What's the authorization model? |
| 9 | Offline | Does it need to work without network? |
| 10 | Accessibility | Is a11y required? To what standard? |
| 11 | i18n | Does it need multiple languages? |
| 12 | Audit trail | Do actions need to be logged? |
| 13 | Backup/recovery | What's the data loss tolerance? |
| 14 | Deployment | Blue/green? Rolling? Canary? |
| 15 | Multi-tenancy | Shared or isolated resources? |

## Usage Flow

```
Idea / Problem
    |
    v
[spec-methodology] -> Frame problem, extract requirements
    |
    v
Structured spec with REQ IDs (.rnd/spec/spec.md)
    |
    v
[planning-methodology] -> Break phase into plans
    |
    v
[plan-verification] -> rnd-critic validates 7 dimensions (in rnd-critic skill)
    |
    v
[wave-orchestration] -> Group plans into parallel waves
    |
    v
[execution-methodology] -> rnd-coder implements each plan
    |
    v
[test-methodology] -> Requirement-driven test generation
    |
    v
Completed phase with reports in .rnd/build/plans/
```
