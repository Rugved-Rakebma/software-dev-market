---
description: Initialize R&D project — create .rnd/ skeleton, configure status line, set up backlog
argument-hint: [project name]
---

## Step 0 — Verify Git Repository

**FIRST**: run `git rev-parse --git-dir 2>/dev/null` via Bash.

If it **fails** (project is not a git repo):

1. Run `git init -b main` (use `main`, never `master`)
2. Run `git commit --allow-empty -m "Initial commit"` (creates a HEAD so worktrees can branch from it)
3. **STOP — do NOT proceed to any later step.** Print:

   ```
   ━━━ Git Initialized ━━━

   This directory was not a git repository. /rnd:c-build spawns worktree-
   isolated agents which require a git repo. I just ran:

     git init -b main
     git commit --allow-empty -m "Initial commit"

   ⚠️  You must restart Claude Code before continuing.

   The current session cached "no git repo" at startup and won't refresh
   mid-session, even though .git/ now exists. Without a restart, every
   /rnd:c-build coder spawn will still fail with "not in a git repository".

   Restart:
     1. /exit
     2. claude
     3. /rnd:init   (will skip this step automatically and continue)
   ```

4. Exit the command. Do not create `.rnd/`, do not run later steps.

If `git rev-parse --git-dir` succeeds, continue to Step 1.

> **Why this exists**: Claude Code caches `is_git_repo` at session start. On a brand-new project, the user opens `claude` *before* running `/rnd:init`, so the cache is `false`. The SessionStart hook (`scripts/rnd-session-start.sh`) auto-inits git for already-managed projects (those with `.rnd/`), but on a *first* `/rnd:init` there's no `.rnd/` yet, so the hook is silent. This step closes that gap. One restart, then never again.

## Step 1 — Check if Already Initialized

If `.rnd/` already exists, DO NOT overwrite any files. Instead:
- Skip skeleton creation
- Verify status line + session hook are configured (add if missing)
- Show artifact inventory (what exists, what's missing)
- Show the onboarding report with current project state
- This makes init safe to re-run — it's additive, never destructive

## Step 2 — Create `.rnd/` Skeleton

Only if `.rnd/` doesn't exist. Create:

```
.rnd/
├── state.md
├── spec/                  # spec.md uses frontmatter `scope: small|standard|large` — see spec-template.md
├── research/
├── decisions/
│   └── index.md
├── architecture/
│   └── history/
├── audit/
├── build/
│   ├── plans/
│   └── runs/              # /rnd:c-run lock files (per-invocation, permanent)
├── debug/
├── verifications/
└── backlog/               # items follow commands/backlog.md schema (id, category, priority, discovered, discovered-during, discovered-by, related-files, seen-count, last-seen)
    └── closed/
```

The backlog directory holds frontmatter-yaml items; the schema is defined in `commands/backlog.md` and auto-populated by `/rnd:c-run` Stage 8.4. Manual items can be created via `/rnd:backlog add` (interactively prompts for the required fields).

## Step 3 — Initialize State Files

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

## Step 4 — Configure Status Line

The session-start hook is registered automatically via the plugin's `hooks/hooks.json` — no manual configuration needed.

Configure the status line by creating or updating `.claude/settings.local.json` in the project directory:

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash \"$(ls -d ~/.claude/plugins/cache/software-dev-market/rnd/*/scripts/rnd-statusline.sh | tail -1)\"",
    "refreshInterval": 10
  }
}
```

The `ls | tail -1` pattern picks the latest version if multiple are cached, preventing glob expansion issues.

If the file already exists, merge this setting — don't overwrite existing settings.

## Step 5 — Onboarding Report

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
