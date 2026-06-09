# software-dev-market — Plugin Marketplace

Personal Claude Code plugin marketplace. Currently ships one plugin: `rnd`.

## Structure

```
software-dev-market/
├── .claude-plugin/marketplace.json    # Marketplace manifest
├── rnd-cycle/                         # "rnd" plugin (namespace = plugin name, not dir name)
│   ├── .claude-plugin/plugin.json     # Plugin manifest (v2.7.1)
│   ├── agents/          (11 files)    # 5 non-code + 6 code domain
│   ├── commands/        (16 files)    # Setup, non-code, code, meta
│   ├── skills/          (7 dirs)      # Knowledge bases for agents
│   ├── hooks/hooks.json               # SessionStart + UserPromptSubmit + Stop
│   └── scripts/         (4 files)     # statusline, session-start, command-tracker, session-stop
└── README.md
```

## Key Architecture Decisions

- **Plugin name `rnd`** → commands register as `/rnd:*` (not `/rnd-cycle:*`)
- **`${CLAUDE_PLUGIN_ROOT}`** for paths inside plugin-owned files (hooks.json, skills)
- **Glob `ls -d ... | tail -1`** for paths in settings.local.json (statusline) — `${CLAUDE_PLUGIN_ROOT}` doesn't work in user-space config files
- **Auto-discovery** — plugin.json has NO `commands`, `agents`, `skills` fields. System discovers from directory names.
- **hooks.json** registers SessionStart (context loading), UserPromptSubmit (command tracking), Stop (session end)

## Spec & Dev Repo

The full v2 spec lives at `~/Code/rnd-lifecycle/rnd-v2.md`. That repo is the dev/spec workspace. This repo is the distribution artifact. Content is copied, not symlinked.

## Open Items

- **Init v1→v2 migration**: `/rnd:init` should migrate state.md headers (`Current Phase` → `Current Status`) on existing projects. Not yet implemented.
- **Line 3 statusline** (phase detection): Deferred. Needs a standardized `phase:` field in state.md to be reliable across build cycles.
- **Decision count**: Statusline counts decision FILES (correct), not individual decisions within files. By design — bash can't parse markdown tables every 10 seconds.
- **Worktree isolation silent-bypass (root cause unknown)**: Claude Code's harness was observed silently bypassing `isolation: worktree` for parallel `rnd-coder` spawns — agents ran in the shared working tree, no error surfaced, commits collided. Circuit breaker added in c-build / c-run (Stage 2 gate via `git worktree list` count delta) catches this loudly. Open question: v2.7.0's SessionStart git auto-init may have flipped the prior *hard* failure ("Cannot create agent worktree: not in a git repository") into this *silent* one — verification pending on a true cold-session test. If confirmed, decide whether to gate the auto-init or accept it (circuit breaker makes the safety question moot from the user's standpoint).
- **Case B worktree bypass detection**: Current circuit breaker catches Case A (worktree never created). Does NOT catch Case B (worktree created but agents use parent cwd via cwd-inheritance bug). Case B requires cross-tree file-diff detection. Not observed; defer until it bites.

## Version History

- **2.0.0** — Initial release (agents, commands, skills, scripts, hooks)
- **2.1.0** — Added 📚 research count to statusline, removed last-cmd timestamp, version bump to force cache refresh
- **2.2.0** — `/rnd:c-run` + `rnd-runner` skill for end-to-end wave automation (lock-driven 8-stage runner)
- **2.4.0** — `/rnd:decide` scope-gate completes the alignment cycle
- **2.5.0** — Alignment cycle close: proportionality across spec / arch / plan / decide / backlog
- **2.7.0** — `/rnd:arch-docs` for bootstrapping arch docs from existing code; `/rnd:claude-plan` removed; git auto-init in SessionStart hook + `/rnd:init` (closes the cold-session worktree-isolation trap); c-run unblocked (trunk-from-HEAD instead of forced `main`, explicit local-only guarantee); c-run proportional defaults (`rnd-code-analyst` dropped from default Stage 4 — opt in via `/rnd:audit`; verify pipeline scope-gated via new `proportionality:` lock field — `scope: small` skips Stages 4–7; "When to use c-run" routing block added)
- **2.7.1** — Worktree isolation circuit breaker in c-build / c-run Stage 2. Detects when Claude Code's harness silently bypasses `isolation: worktree` (observed in a real run — agents shared cwd, commits collided, no error surfaced). Per-wave check via `git worktree list` count delta; loud PAUSE with diagnostic before simplifier or merge runs.
