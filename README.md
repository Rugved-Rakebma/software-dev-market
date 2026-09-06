# rnd — Minimal R&D System for Claude Code

Dev-team orchestration, living docs with anchor gates, dated design records,
and a backlog — governed by one rule: **persist only what code and git cannot
reconstruct.**

```
/plugin marketplace add Rugved-Rakebma/software-dev-market
/plugin install rnd@software-dev-market
```

---

## The problem

Lifecycle tooling for AI coding tends to grow ceremony: state files nothing
reads back, specs that confine the product months later, docs that describe
intent instead of code, artifacts written because a stage demanded them.
The previous version of this plugin (v2, kept in `rnd-cycle/` as reference)
had all of it — 23 artifact types and not one parser.

v3 keeps five things and deletes everything else.

## What it does

| Command | What happens |
|---|---|
| `/rnd:build <intent>` | A **dev-manager** agent investigates, composes a team (coder · code-reviewer · qa-lead), runs the fix loop one level below your session, and reports one settled outcome. You stay in your master session. |
| `/rnd:verify` | One adversarial reviewer on the current diff — BLOCKER/ADVISORY with `path:Symbol` anchors. |
| `/rnd:design <topic>` | Explore + attack in conversation. A dated record is written **only** when a real alternative was rejected. |
| `/rnd:backlog` | Add / list / close / sweep. Ids and frontmatter stamped by the CLI; triage is always human. |
| `/rnd:docs` | Scaffold the living-docs tiers, derive architecture/surface docs from source (forked subagents), or audit the whole set. |

## The spine: one CLI

`scripts/rnd.py` — stdlib-only, owns every schema and every gate:

```
rnd fm            # query records + backlog by frontmatter
rnd anchors       # every path:Symbol in living docs resolves (multi-language)
rnd affected      # which docs cite these files — powers the drift hook
rnd docs-check    # surface docs vs the real surface
rnd standards     # doc standards vs plugin canon (binding regions per repo)
rnd backlog/record/init
```

A PostToolUse hook closes the classic hole: editing source that living docs
cite triggers a same-commit, align-only instruction — docs stay true where
the edit happens.

## What a consuming repo holds

```
.rnd/            config.toml + backlog/          ← the entire plugin state
docs/living/     architecture · operations · [doctrine]   (no frontmatter; anchors are the index)
docs/design/     dated records (frozen by git mv, never rewritten)
```

No state.md. No sessions. No locks. No "current" documents. Plans are
ephemeral; git history is the record; decisions capture only what a diff
can't — the alternative you rejected.

## Docs

Development guide: [`rnd/CLAUDE.md`](rnd/CLAUDE.md).
