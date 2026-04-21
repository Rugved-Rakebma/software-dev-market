# rnd — R&D Lifecycle for Claude Code

Turn Claude Code into a structured R&D system — from idea to shipped code with 10 specialized agents, persistent state, and zero context loss between sessions.

```
claude plugin install rnd@software-dev-market
```

---

## The Problem

Claude Code is powerful but stateless. Every session starts cold. Complex projects need structure — specs, decisions, plans, verification — and without lifecycle discipline, AI coding is fast but fragile. Context gets lost, scope creeps, nothing gets verified, and there's no audit trail.

This plugin adds the missing lifecycle.

---

## Quick Start

```
/rnd:init my-project          # Create .rnd/ state, configure hooks
/rnd:spec Build a task API    # Turn the idea into structured requirements
/rnd:status                   # See where you are and what's next
```

Every new session auto-loads your project state. Run `/rnd:help` anytime for the full reference.

---

## The Lifecycle

### Initial Build — Idea to Shipped Code

The first time through, you follow the full pipeline. Each step produces an artifact that feeds the next.

```
/rnd:init       → .rnd/ skeleton + session hooks
     ↓
/rnd:spec       → .rnd/spec/spec.md (requirements with REQ-IDs)
     ↓
/rnd:research   → .rnd/research/ (citation-backed landscape analysis)
     ↓
/rnd:decide     → .rnd/decisions/ (ADRs — locked technology choices)
     ↓
/rnd:design     → .rnd/architecture/current.md (system architecture + roadmap)
     ↓
/rnd:plan       → .rnd/build/plans/ (executable plans with wave assignments)
     ↓
/rnd:validate   → stress-test plans before committing to code
     ↓
/rnd:c-build    → working code (one agent per plan, parallel within waves)
     ↓
/rnd:c-verify   → .rnd/verifications/ (spec compliance + quality + security)
```

You don't have to run every step. Skip `/rnd:research` if you already know the landscape. Skip `/rnd:validate` if the plans are simple. The lifecycle is a guide, not a straitjacket.

### Iteration — Build/Verify/Fix Cycle

After the initial build, most work is a tight loop:

```
/rnd:c-build    → implement changes
     ↓
/rnd:c-verify   → check spec compliance, code quality, security
     ↓
  PASS? → done
  FAIL? → fix issues, run /rnd:c-build again
     ↓
/rnd:c-debug    → if a specific bug needs investigation
     ↓
/rnd:c-build    → apply the fix
     ↓
/rnd:c-verify   → verify the fix didn't break anything
```

The verify step spawns three independent agents in parallel — a spec-checker, a code reviewer, and a security analyst. If any of them return FAIL, you get specific file:line issues to fix.

### Bug Hunting

When something breaks and you don't know why:

```
/rnd:c-debug "API returns 500 intermittently on form submit"
```

The debugger uses scientific method — hypothesis testing with persistent session state at `.rnd/debug/`. If the investigation spans multiple sessions, it picks up where it left off. Related bugs found during investigation get reported as backlog candidates, not fixed out of scope.

### Backlog — Tracking What You Find Along the Way

During build, verify, and debug cycles, agents constantly discover issues outside their current scope — minor bugs, tech debt, missing edge cases, security concerns. In v1 these were either fixed immediately (scope creep) or lost after the session.

Now agents report findings as `BACKLOG CANDIDATE` items. The main session collects them and offers to create tracked items:

```
/rnd:backlog                  # list all open items by priority
/rnd:backlog add "description"  # create a new item interactively
/rnd:backlog close BUG-003    # close with resolution
/rnd:backlog promote FEAT-002 # promote to full lifecycle (/rnd:spec)
```

Items are categorized (BUG, DEBT, UX, PERF, SEC, FEAT), prioritized (critical/high/medium/low), and tracked with file references and discovery context. Small items get fixed in a future build wave. Large items get promoted to their own spec and follow the full lifecycle.

### Evolving the Architecture

When requirements change or you need to add major features:

```
/rnd:spec "Add real-time collaboration"   # extend the spec
/rnd:design                               # revise architecture (old version archived)
/rnd:plan                                 # generate new build plans
/rnd:validate                             # stress-test before building
/rnd:c-build                              # execute
/rnd:c-verify                             # verify
```

Previous architecture is automatically archived to `.rnd/architecture/history/`. Decisions remain locked unless explicitly revisited. The state never loses history — old entries compress into phase summaries instead of being deleted.

---

## Commands

### Setup
| Command | What It Does |
|---------|-------------|
| `/rnd:init` | Create `.rnd/` skeleton, configure status line and session hooks |

### Non-Code — Planning and Strategy
| Command | What It Does |
|---------|-------------|
| `/rnd:spec` | Turn an idea into structured requirements with REQ-IDs |
| `/rnd:research` | Deep landscape research with source scoring and citations |
| `/rnd:decide` | Technology decisions — produces Architecture Decision Records |
| `/rnd:design` | System architecture with roadmap and technology justification |
| `/rnd:plan` | Decompose architecture into executable build plans with waves |
| `/rnd:claude-plan` | Plan using native plan mode (codebase-aware), then decompose |
| `/rnd:validate` | Adversarial stress-test of any plan, proposal, or roadmap |

### Code — Build and Verify
| Command | What It Does |
|---------|-------------|
| `/rnd:c-build` | Execute build plans — one coder agent per plan, parallel within waves |
| `/rnd:c-verify` | Full validation — spec compliance + code quality + security audit |
| `/rnd:c-debug` | Scientific debugging with hypothesis tracking and session persistence |

### Meta
| Command | What It Does |
|---------|-------------|
| `/rnd:audit` | Deep analysis of codebases or documents (routes by target type) |
| `/rnd:backlog` | Manage discovered issues — add, list, close, promote |
| `/rnd:status` | Project state, artifact inventory, backlog summary, next steps |
| `/rnd:help` | Full reference card |

---

## Why 10 Agents

Most AI coding tools use one agent that does everything. This plugin uses 10 specialists because **separation of concerns produces better results**.

The coder doesn't review its own work — that's a conflict of interest. The spec-checker doesn't trust the coder's report — it reads the actual code independently. The critic is adversarial by design — it exists to find flaws, not to encourage.

### Non-Code Domain

These agents never touch code. They think, plan, research, and challenge.

| Agent | Role | Spawned By |
|-------|------|-----------|
| **rnd-architect** | System design, tech stack selection, roadmaps | `/rnd:spec`, `/rnd:design` |
| **rnd-critic** | Adversarial validation — GOOD / NEEDS MAJOR WORK / BAD verdicts | `/rnd:validate`, `/rnd:plan` |
| **rnd-planner** | Decomposes architecture into executable plans with wave assignments | `/rnd:plan` |
| **rnd-analyst** | Evidence-based document investigation (specs, proposals, PRDs) | `/rnd:audit` |
| **rnd-researcher** | Autonomous 8-phase research pipeline with citation tracking | `/rnd:research` |

### Code Domain

These agents read and write code. They implement, review, and debug.

| Agent | Role | Spawned By |
|-------|------|-----------|
| **rnd-coder** | Implements a single plan (2-3 tasks), commits per task, reports status | `/rnd:c-build` |
| **rnd-code-spec-checker** | Adversarial — reads code independently, does NOT trust the coder | `/rnd:c-verify` |
| **rnd-code-reviewer** | Two-layer review: tactical quality + integration wiring verification | `/rnd:c-verify` |
| **rnd-code-analyst** | Codebase audit, 4-level verification, security review (STRIDE + OWASP) | `/rnd:c-verify`, `/rnd:audit` |
| **rnd-code-debugger** | Scientific-method debugging with 8 techniques and persistent sessions | `/rnd:c-debug` |

Code and non-code agents never cross domains. The architect designs but never implements. The coder implements but never designs. This boundary prevents the most common failure mode in AI-assisted development: an agent making architectural decisions while trying to fix a bug.

---

## How State Works

Everything persists in the `.rnd/` directory at the project root. New sessions auto-load context via the session-start hook — the agent knows where you left off without being told.

```
.rnd/
├── state.md                    # Current status + activity log (compresses, never deletes)
├── spec/
│   └── spec.md                 # Requirements with REQ-{CAT}-{NN} identifiers
├── research/
│   └── {topic}.md              # Research summaries with citations
├── decisions/
│   ├── index.md                # Decision log table
│   └── NNN-{slug}.md           # Individual ADRs (locked constraints)
├── architecture/
│   ├── current.md              # Active architecture design
│   └── history/
│       └── {date}-current.md   # Previous versions (auto-archived on redesign)
├── audit/
│   └── {date}-{target}.md      # Audit reports (codebase or document)
├── build/
│   ├── plans/
│   │   └── phase-NN/
│   │       └── NN-PLAN.md      # Executable plans with YAML frontmatter
│   ├── progress.md             # Build completion status
│   └── master-plan.md          # Native plan mode output (if using /rnd:claude-plan)
├── debug/
│   ├── {issue}/
│   │   └── session.md          # Hypothesis tracking, experiment results
│   └── knowledge-base.md       # Resolved patterns for future reference
├── verifications/
│   └── {date}-verification.md  # Consolidated reports (spec + quality + security)
├── backlog/
│   ├── BUG-001-{slug}.md       # Open issues with YAML frontmatter
│   ├── DEBT-002-{slug}.md
│   └── closed/
│       └── BUG-003-{slug}.md   # Resolved items (moved here, never deleted)
└── live-progress.md            # Build session checkpoint (deleted when build completes)
```

### State Compression

`state.md` uses progressive compression — recent entries stay detailed, older entries compress into phase summaries. Nothing is ever deleted. A project with 10 completed phases uses ~30 lines, not 300.

### Session Continuity

The session-start hook fires on every new Claude Code session. If `.rnd/` exists, it outputs a context summary with progressive disclosure — interrupted builds first (most urgent), then current status, backlog highlights, artifact inventory, and locked decisions. Full file contents load on demand when specific commands run.

### Backlog Discipline

Agents never fix issues outside their current task scope. They report findings as `BACKLOG CANDIDATE` with category, priority, file path, and description. The main session creates formal backlog items from these candidates. This prevents scope creep during build cycles while ensuring nothing discovered is lost.

---

## Design Principles

1. **Main session is the only orchestrator.** No nested agent spawning. Commands dispatch agents directly.
2. **Code and non-code are separate domains.** Agents never cross the boundary.
3. **Commands do one thing.** No overloaded commands spanning multiple domains.
4. **Interactive commands load skills. Batch commands spawn agents.** User conversation stays in the main session. Autonomous work gets delegated.
5. **State compounds, never truncates.** Progressive compression — recent stays detailed, old compresses. Nothing is deleted.
6. **Backlog over scope creep.** Agents report findings, never fix out-of-scope issues.

---

## Install

```
claude plugin install rnd@software-dev-market
```

Then in any project:

```
/rnd:init my-project
```
