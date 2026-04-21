---
description: Scientific-method debugging with persistent session state
argument-hint: [bug description or issue]
---

## Prerequisites

1. **Check `.rnd/` exists.** If not: "No R&D project found. Run `/rnd:init` first."
2. **Read `.rnd/state.md`** for project context.

## Bug Description

**$ARGUMENTS**

## Context Loading

- `.rnd/debug/knowledge-base.md` — if exists, prior debugging patterns and resolutions
- `.rnd/debug/{issue-name}/session.md` — if resuming a prior debug session for this issue
- `.rnd/state.md` — project context

## Execution

Spawn **rnd-code-debugger** via the Agent tool:
- **description**: "Debug: {bug summary}"
- **model**: opus
- **prompt**: Include:
  - Bug description from `$ARGUMENTS`
  - Project context from `.rnd/state.md`
  - Knowledge base content (if `.rnd/debug/knowledge-base.md` exists)
  - Existing debug session file (if resuming — include full session history so the debugger can continue from where it left off)
  - Reference to `skills/rnd-build/reference/escalation-protocol.md` for status definitions
  - Instruction: maintain debug session at `.rnd/debug/{issue-slug}/session.md`
  - Instruction: update knowledge base at `.rnd/debug/knowledge-base.md` after resolution

The debugger works autonomously: investigate → hypothesize → test → fix → verify.

## After Completion

When the debugger returns:
1. Present the root cause and fix to the user
2. If the debugger reports `BACKLOG CANDIDATE` items (related bugs found during investigation), offer to create backlog items via `/rnd:backlog add`
3. If the debugger reports `BLOCKED`, present what's blocking and ask the user for guidance

## Persistence

Update `.rnd/state.md`:
- Add entry to Recent Activity: `{today's date}: Debug session — {issue} via /rnd:c-debug — status: {resolved|blocked|investigating}`
- Follow compression protocol: keep under 120 lines, compress oldest Recent Activity entries into History phase summaries when exceeding 15 entries. Never delete entries.
