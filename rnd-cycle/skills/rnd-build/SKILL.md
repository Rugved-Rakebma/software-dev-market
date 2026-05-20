---
name: rnd-build
description: Planning methodology, wave orchestration, execution methodology, and build coordination reference material. Used by rnd-planner (planning) and rnd-coder (execution).
user-invocable: false
---

# R&D Build

The rnd-build skill is the consolidated knowledge base for the build pipeline. It contains reference documents covering specification, planning, execution, orchestration, testing, and agent coordination — plus templates for plan and summary files. Used by `rnd-planner` (planning) and `rnd-coder` (execution).

## Plan = Task / Arch = Shape / Spec = Reqs

Three artifacts, three roles. The build pipeline depends on this separation:

- **Plan** (`.rnd/build/plans/`) — the *task*: what to build, what files to touch, how to verify it's done
- **Arch** (`.rnd/architecture/current.md`) — the *shape*: contracts, mechanisms, data flow
- **Spec** (`.rnd/spec/spec.md`) — the *requirements*: REQ-IDs and acceptance criteria

The coder receives all three in its priming prompt. Plans do not re-embed contracts or requirements — they point at them.

## When to Use This Skill

Match references to scope:

| Scope | Use these references |
|---|---|
| **Small** refactor (<1KLOC, single dev, 1–2 components) | `planning-methodology`, `escalation-protocol`, `reporting-format` only |
| **Standard** feature add (1–10KLOC) | Above + `handoff-contracts`, `execution-methodology`, `wave-orchestration` |
| **Large** / greenfield / multi-team | All references as relevant |

`spec-methodology` and `test-methodology` load only when their commands fire (`/rnd:spec` and verification respectively).

## Reference Documents

### 1. Spec Methodology (`reference/spec-methodology.md`)
**Use when**: Turning ideas into structured specifications with testable requirements.

Includes:
- The three-artifact triangle (spec owns requirements only; no tech, no team, no roadmap)
- Scope assessment (small / standard / large) captured in spec frontmatter as a fallback hint
- Problem framing (problem-first, not solution-first)
- Scope-gated interview rounds for requirement extraction
- Canonical REQ row format: `| ID | Category | Requirement | Acceptance |`
- Version classification (v1 / v2 / out-of-scope)
- Scope-gated gap checklist (core 7 / +standard 5 / +large 3)
- Open questions with HIGH/MEDIUM/LOW impact triage

### 2. Planning Methodology (`reference/planning-methodology.md`)
**Use when**: Breaking project phases into executable build plans.

Includes:
- Plans-are-prompts principle (consumed by rnd-coder agents, not humans)
- Plan = Task / Arch = Shape / Spec = Reqs separation
- No-code-in-plans rule (with ❌/✅ contrast example)
- Plan anatomy (5 flat frontmatter fields + Goal / Wires to / Tasks)
- Task anatomy: `Build:` + `Done:` only (2-3 tasks per plan)
- Scope estimation (~50% context window target)
- Dependency graph construction + wave assignment
- Vertical slices over horizontal layers
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
- Status definitions: DONE, DONE_WITH_ADVISORIES, BLOCKED, NEEDS_CONTEXT
- BLOCKER vs ADVISORY routing (blockers gate fix-up; advisories route to backlog)
- Retry limits (max 2 re-attempts on blockers; advisories never trigger retry)
- Escalation triggers (architectural decisions, code beyond context, uncertainty about correctness)

### 8. Reporting Format (`reference/reporting-format.md`)
**Use when**: Producing standardized status reports from code agents.

Includes:
- Standardized status report template for all code agents
- Evidence requirements (file:line citations for every claim)
- Tasks completed, files changed, commits, test results, advisories sections

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
| **DONE_WITH_ADVISORIES** | Completed; advisories surfaced (not blocking) | Continue; advisories route to backlog |
| **BLOCKED** | Cannot proceed | Surface to user, pause |
| **NEEDS_CONTEXT** | Missing information, risks quality | Surface to user, decide if blocking |

### Gap Checklist (scope-gated)

Set reviewed depends on spec scope. Default to **small** unless the conversation proves otherwise.

| # | Gap Area | Tier |
|---|----------|------|
| 1 | Auth | core (all) |
| 2 | Error handling | core (all) |
| 3 | Edge cases | core (all) |
| 4 | Data migration | core (all) |
| 5 | Monitoring | core (all) |
| 6 | Rollback | core (all) |
| 7 | Permissions | core (all) |
| 8 | Rate limiting | +standard |
| 9 | External dependencies | +standard |
| 10 | Audit trail | +standard |
| 11 | Deployment strategy | +standard |
| 12 | Backup/recovery | +standard |
| 13 | Multi-tenancy | +large |
| 14 | Accessibility | +large |
| 15 | i18n | +large |

## Usage Flow

```
Idea / Problem
    |
    v
[spec-methodology] -> Frame problem, extract requirements
    |
    v
Spec with REQ IDs (.rnd/spec/spec.md)
    |
    v
Arch with contracts (.rnd/architecture/current.md)  — produced by /rnd:design
    |
    v
[planning-methodology] -> Break phase into slim plans (point at arch + spec, no code)
    |
    v
Assess scope from arch header (small / standard / large)
    +-- Small    -> skip critic; proceed to execution
    +-- Standard -> plan-verification critic with 1-loop budget on BLOCKERs only
    +-- Large    -> plan-verification critic; /rnd:validate available for heavier review
    |
    v
[wave-orchestration] -> Group plans into parallel waves
    |
    v
[execution-methodology] -> rnd-coder implements (receives plan + arch slice + spec slice)
    |
    v
[test-methodology] -> Requirement-driven test generation
    |
    v
Completed phase with reports in .rnd/build/plans/
```
