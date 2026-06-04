# rnd — Project Lifecycle for Claude Code

10 specialized agents, persistent state, zero context loss between sessions.

```
/plugin marketplace add Rugved-Rakebma/software-dev-market
/plugin install rnd@software-dev-market
```

---

## The Problem

Claude Code is powerful but stateless. Every session starts cold. Without lifecycle discipline, AI coding is fast but fragile — context gets lost, scope creeps, nothing gets verified, no audit trail.

This plugin adds the missing lifecycle.

---

## Quick Start

```
/rnd:init my-project          # Create .rnd/ state, configure status line
/rnd:spec Build a task API    # Turn the idea into structured requirements
/rnd:status                   # See where you are and what's next
```

Every new session auto-loads your project state via the plugin's SessionStart hook.

---

## The 8 Cycles

### 1. Greenfield — Idea to first working code

```
  init → spec → research → decide → design → plan → validate → build → verify
   │      │        │          │        │        │        │         │        │
   │    [main]  [rnd-       [main]  [main]  [rnd-    [rnd-     [rnd-    [rnd-code-
   │   session  researcher] session session  planner] critic]   coder]   spec-checker]
   │      +                   +       +        +                  +     [rnd-code-
   │   rnd-architect        rnd-   rnd-     rnd-              [code-    reviewer]
   │     skill             critic  architect critic            simpli- [rnd-code-
   │                        skill   skill                      fier]    analyst]
   │
  [main session — creates .rnd/ skeleton]
```

You don't have to run every step. Skip research if you know the landscape. Skip validate if the plans are simple. The lifecycle is a guide, not a straitjacket.

### 2. Build/Verify Loop — Tight iteration during active development

```
         ┌──────────────────────────────────────┐
         │                                      │
         ▼                                      │
       build ────────► verify ────► PASS ✓      │
         │                │                     │
    [rnd-coder]     [rnd-code-spec-checker]     │
    [code-simplifier] [rnd-code-reviewer]       │
         │            [rnd-code-analyst]         │
         │                │                     │
         │              FAIL                    │
         │                │                     │
         │          file:line issues             │
         │                │                     │
         └────────────────┘ (build fixes them)  │
                                                │
         max iterations → escalate to user ─────┘
```

### 3. Debug — Something's broken, find root cause

```
  bug report
      │
      ▼
    debug ─────────► root cause found
      │                    │
  [rnd-code-              │
   debugger]              ▼
      │              build (fix) ──► verify
      │                  │              │
      │             [rnd-coder]    [rnd-code-
      │             [code-          spec-checker]
      │              simplifier]   [rnd-code-
      │                             reviewer]
      ▼                            [rnd-code-
  .rnd/debug/                       analyst]
  session.md
  knowledge-base.md   (related bugs → BACKLOG CANDIDATE)
```

Debug sessions persist across conversations. If an investigation spans multiple sessions, the debugger picks up where it left off.

### 4. Backlog Drain — Processing accumulated issues

```
  /rnd:backlog (review)
        │
        ├── small items (BUG, NIT, DEBT)
        │       │
        │       ▼
        │     build ──► verify
        │       │          │
        │  [rnd-coder]  [rnd-code-spec-checker]
        │  [code-       [rnd-code-reviewer]
        │   simplifier] [rnd-code-analyst]
        │
        └── large items (FEAT, major DEBT)
                │
                ▼
          /rnd:backlog promote
                │
                ▼
          ┌─ GREENFIELD CYCLE (from spec) ─┐
```

Agents never fix issues outside their current scope. They report `BACKLOG CANDIDATE` items — categorized (BUG, DEBT, UX, PERF, SEC, FEAT), prioritized, with file references. Nothing discovered is lost.

### 5. Feature Evolution — Adding to an existing system

```
  current.md ──► history/                (auto-archived)
                    │
  spec (extend) ──► design (revise) ──► plan ──► validate ──► build ──► verify
       │                │                 │          │           │          │
     [main]          [main]          [rnd-      [rnd-      [rnd-      [rnd-code-
    session          session          planner]   critic]    coder]      spec-checker]
       +                +               +                  [code-     [rnd-code-
    rnd-architect    rnd-architect    rnd-                   simpli-    reviewer]
      skill            skill          critic                fier]     [rnd-code-
                                                                       analyst]

  .rnd/decisions/ remain LOCKED (constraints for new design)
```

Previous architecture is automatically archived. Decisions stay locked unless explicitly revisited. State never loses history — old entries compress into phase summaries.

### 6. Research Spike — Exploring before committing

```
  question
      │
      ▼
   research ──► decide (ADR)
      │              │
  [rnd-           [main session
   researcher]     + rnd-critic skill]
      │              │
      ▼              ▼
  .rnd/research/  .rnd/decisions/
      │              │
      └──────┬───────┘
             │
             ▼
    back to triggering cycle
    (design, plan, or spec)
```

### 7. Audit / Onboard — Understanding before acting

```
  existing codebase              existing document
        │                              │
        ▼                              ▼
   /rnd:audit                     /rnd:audit
   (code mode)                   (doc mode)
        │                              │
  [rnd-code-analyst]           [rnd-analyst]
   (up to 4 parallel:              │
    tech/arch/quality/             ▼
    concerns)                 .rnd/audit/
        │
        ▼
   .rnd/audit/
        │
        ├──► feeds /rnd:spec (gaps → new requirements)
        ├──► feeds /rnd:design (architecture concerns)
        └──► feeds /rnd:backlog (issues discovered)
```

### 8. Plan Revision — Plans fail validation

```
         ┌──────────────────────────┐
         │                          │
         ▼                          │
       plan ────► validate          │
         │            │             │
    [rnd-planner] [rnd-critic]      │
         │            │             │
         │          GOOD ──► build  │
         │            │             │
         │       NEEDS WORK         │
         │            │             │
         │       feedback           │
         │            │             │
         └────────────┘             │
                                    │
         max 3 loops → escalate ────┘
```

---

## Commands

### Setup
| Command | What It Does |
|---------|-------------|
| `/rnd:init` | Create `.rnd/` skeleton, configure status line |

### Non-Code — Planning and Strategy
| Command | What It Does |
|---------|-------------|
| `/rnd:spec` | Turn an idea into structured requirements with REQ-IDs |
| `/rnd:research` | Deep landscape research with source scoring and citations |
| `/rnd:decide` | Technology decisions — produces Architecture Decision Records |
| `/rnd:design` | System architecture with roadmap and technology justification |
| `/rnd:plan` | Decompose architecture into executable build plans with waves |
| `/rnd:validate` | Adversarial stress-test of any plan, proposal, or roadmap |

### Code — Build and Verify
| Command | What It Does |
|---------|-------------|
| `/rnd:c-build` | Execute build plans — one coder per plan, parallel within waves |
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

## Agents

### Non-Code Domain

| Agent | Role |
|-------|------|
| **rnd-architect** | System design, tech stack selection, roadmaps |
| **rnd-critic** | Adversarial validation — GOOD / NEEDS MAJOR WORK / BAD verdicts |
| **rnd-planner** | Decomposes architecture into executable plans with wave assignments |
| **rnd-analyst** | Evidence-based document investigation (specs, proposals, PRDs) |
| **rnd-researcher** | Autonomous 8-phase research pipeline with citation tracking |

### Code Domain

| Agent | Role |
|-------|------|
| **rnd-coder** | Implements a single plan (2-3 tasks), commits per task, isolated worktree |
| **rnd-code-spec-checker** | Adversarial — reads code independently, does NOT trust the coder |
| **rnd-code-reviewer** | Two-layer review: tactical quality + integration wiring verification |
| **rnd-code-analyst** | Codebase audit, 4-level verification, security review (STRIDE + OWASP) |
| **rnd-code-debugger** | Scientific-method debugging with 8 techniques and persistent sessions |

Code and non-code agents never cross domains.

---

## State

Everything persists in `.rnd/` at the project root. New sessions auto-load context via the SessionStart hook.

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
│   └── history/                # Previous versions (auto-archived on redesign)
├── audit/
│   └── {date}-{target}.md      # Audit reports (codebase or document)
├── build/
│   ├── plans/phase-NN/         # Executable plans with YAML frontmatter
│   └── progress.md             # Build completion status
├── debug/
│   ├── {issue}/session.md      # Hypothesis tracking, experiment results
│   └── knowledge-base.md       # Resolved patterns for future reference
├── verifications/              # Consolidated reports (spec + quality + security)
├── backlog/
│   ├── {CAT}-{NNN}-{slug}.md  # Open issues with YAML frontmatter
│   └── closed/                 # Resolved items (moved here, never deleted)
└── live-progress.md            # Build session checkpoint (deleted when build completes)
```

`state.md` uses progressive compression — recent entries stay detailed, older entries become phase summaries. Nothing is ever deleted.

---

## Install

```
/plugin marketplace add Rugved-Rakebma/software-dev-market
/plugin install rnd@software-dev-market
```

Then in any project:

```
/rnd:init my-project
```
