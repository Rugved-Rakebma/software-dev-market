---
description: Show all R&D commands, agents, skills, and the full project lifecycle flow
argument-hint:
---

Print this reference card:

```
━━━ R&D System v2 — Reference Card ━━━

## Lifecycle Flow

/rnd:init → /rnd:spec → /rnd:research → /rnd:decide → /rnd:design
         → /rnd:plan → /rnd:validate → /rnd:c-build → /rnd:c-verify
                                              ↕
                                        /rnd:c-debug

## Commands

### Setup
| Command       | What It Does                                  |
|---------------|-----------------------------------------------|
| /rnd:init     | Create .rnd/ skeleton, configure hooks         |

### Non-Code (planning & strategy)
| Command           | What It Does                                  |
|-------------------|-----------------------------------------------|
| /rnd:spec         | Turn idea into structured requirements        |
| /rnd:research     | Deep landscape research with citations        |
| /rnd:decide       | Technology decisions (ADRs)                   |
| /rnd:design       | Architecture + roadmap                        |
| /rnd:plan         | Decompose into build plans (from spec)        |
| /rnd:validate     | Stress-test any plan or proposal              |

### Code (build & verify)
| Command        | What It Does                                   |
|----------------|------------------------------------------------|
| /rnd:c-build   | Execute plans as code (coders + simplifier)    |
| /rnd:c-verify  | Full validation (spec + quality + security)    |
| /rnd:c-debug   | Scientific debugging with session persistence  |

### Meta
| Command        | What It Does                                   |
|----------------|------------------------------------------------|
| /rnd:audit     | Deep analysis of code or documents             |
| /rnd:backlog   | Manage discovered issues (add/list/close/promote/sweep) |
| /rnd:status    | Show project state and next steps              |
| /rnd:help      | This reference card                            |

## Agents (10)

### Non-Code Domain
| Agent          | Role                                           |
|----------------|------------------------------------------------|
| rnd-architect  | System design, tech stack, roadmaps            |
| rnd-critic     | Adversarial validation, assumption challenging |
| rnd-planner    | Plan decomposition, wave assignment            |
| rnd-analyst    | Document investigation and audit               |
| rnd-researcher | Autonomous 8-phase research pipeline           |

### Code Domain
| Agent                 | Role                                      |
|-----------------------|-------------------------------------------|
| rnd-coder             | Plan implementation, commits per task     |
| rnd-code-spec-checker | Adversarial spec compliance verification  |
| rnd-code-reviewer     | Quality review + integration wiring       |
| rnd-code-debugger     | Scientific debugging with session state   |
| rnd-code-analyst      | Codebase audit, security, verification    |

## Skills (5)
| Skill         | Purpose                                        |
|---------------|------------------------------------------------|
| rnd-architect | Architecture patterns, tech selection, roadmaps|
| rnd-critic    | Assumption challenging, anti-pattern detection  |
| rnd-analyst   | Audit methodology, verification, code review   |
| rnd-build     | Planning, execution, wave orchestration        |
| rnd-research  | 8-phase research pipeline, citation tracking   |

## .rnd/ State Directory
```
.rnd/
├── state.md              # Project status + activity log
├── spec/                 # Specifications
├── research/             # Research summaries
├── decisions/            # ADRs (Architecture Decision Records)
│   └── index.md
├── architecture/         # Architecture documents
│   └── history/
├── audit/                # Audit reports
├── build/                # Build plans and progress
│   └── plans/
├── debug/                # Debug sessions + knowledge base
├── verifications/        # Verification reports
└── backlog/              # Tracked issues
    └── closed/
```

## Design Principles
1. Main session is the only orchestrator (no nested spawning)
2. Code and non-code are separate domains
3. Commands do one thing
4. Interactive commands load skills, batch commands spawn agents
5. State compounds, never truncates (compression, not deletion)
6. Backlog over scope creep (agents report, don't fix out-of-scope issues)
```
