---
description: Initialize R&D project — create .rnd/ skeleton, configure status line, set up backlog
argument-hint: [project name]
---

## Step 0 — Check if Already Initialized

If `.rnd/` already exists, DO NOT overwrite any files. Instead:
- Skip skeleton creation
- Verify status line + session hook are configured (add if missing)
- Show artifact inventory (what exists, what's missing)
- Show the onboarding report with current project state
- This makes init safe to re-run — it's additive, never destructive

## Step 1 — Create `.rnd/` Skeleton

Only if `.rnd/` doesn't exist. Create:

```
.rnd/
├── state.md
├── spec/
├── research/
├── decisions/
│   └── index.md
├── architecture/
│   └── history/
├── audit/
├── build/
│   └── plans/
├── debug/
├── verifications/
└── backlog/
    └── closed/
```

## Step 2 — Initialize State Files

**`.rnd/state.md`:**
```markdown
# Project: {name from $ARGUMENTS, or detected from package.json/directory name}

## Current Status
Initialized. No spec, architecture, or build plans yet.

## Recent Activity
- {today's date}: Project initialized via /rnd:init

## History
(none)
```

**`.rnd/decisions/index.md`:**
```markdown
# Decision Log

| # | Date | Decision | File |
|---|------|----------|------|
```

## Step 3 — Configure Status Line

The session-start hook is registered automatically via the plugin's `hooks/hooks.json` — no manual configuration needed.

Configure the status line by creating or updating `.claude/settings.local.json` in the project directory:

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash ~/.claude/plugins/cache/software-dev-market/rnd/*/scripts/rnd-statusline.sh",
    "refreshInterval": 10
  }
}
```

The `*` glob matches whatever version is cached, so the path survives plugin updates.

If the file already exists, merge this setting — don't overwrite existing settings.

## Step 4 — Onboarding Report

Print:

```
━━━ R&D Initialized: {project name} ━━━

✅ .rnd/ directory created
✅ Status line configured
✅ Session start hook registered via plugin (automatic)

## Lifecycle

/rnd:init ✅ → /rnd:spec → /rnd:research → /rnd:decide → /rnd:design
           → /rnd:plan → /rnd:validate → /rnd:c-build → /rnd:c-verify

## Next Step
Run /rnd:spec to define what you're building.

## Quick Reference
| Command        | What It Does                          |
|----------------|---------------------------------------|
| /rnd:spec      | Turn idea into structured requirements|
| /rnd:research  | Deep landscape research               |
| /rnd:decide    | Technology decisions (ADRs)           |
| /rnd:design    | Architecture + roadmap                |
| /rnd:plan      | Decompose into build plans            |
| /rnd:validate  | Stress-test any plan                  |
| /rnd:c-build   | Execute plans as code                 |
| /rnd:c-verify  | Full code validation                  |
| /rnd:c-debug   | Scientific debugging                  |
| /rnd:backlog   | Track issues for later                |
| /rnd:status    | See project state                     |
| /rnd:help      | Full reference card                   |

Every new session auto-loads your project state.
Run /rnd:help anytime for the full reference.
```
