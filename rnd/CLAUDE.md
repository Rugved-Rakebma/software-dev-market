# rnd v3 — Development Guide

Minimal R&D plugin. Governing rule: **persist only what code and git cannot
reconstruct.** Two frontmatter schemas (design record, backlog item), both
owned and validated by one CLI. No state files, no session tracking, no locks,
no "current" documents.

## Architecture

| Layer | Contents | Job |
|---|---|---|
| `commands/` (5) | design · build · verify · backlog · docs | thin orchestrators — master context is sacred; they resolve, spawn, relay |
| `agents/` (4) | dev-manager · coder · code-reviewer · qa-lead | the dev-team; manager runs the whole fix loop one level below the master session and reports once |
| `skills/` (3) | map · write-doc · write-surface | `context: fork` — each body becomes an isolated subagent's prompt; used by `/rnd:docs derive` |
| `scripts/rnd.py` | one stdlib-only CLI (~1,400 lines) | every schema, every gate |
| `hooks/` | PostToolUse Edit\|Write → `drift.sh` | edits to source that living docs cite → structured align-only instruction (exit 2 feedback) |
| `templates/standards/` | 5 CLAUDE.md canon files | universal doc standards; repos fill `<!-- rnd:binding NAME -->` regions only |

## The dev-team loop (what /rnd:build does)

```
master ── intent ──▶ dev-manager (background, named)
   investigate → scope → compose team → spawn coder (self-plans)
   → spawn reviewer fresh → relay BLOCKERs only, ≤2 rounds → qa runs checks
   → ONE report up (escalations: disputed BLOCKER, budget out, BLOCKED/NEEDS_CONTEXT)
```

Contracts: inline context bundles (agents never read `.rnd/`) · coder
four-status enum (DONE / DONE_WITH_ADVISORIES / BLOCKED / NEEDS_CONTEXT) ·
reviewer BLOCKER/ADVISORY with `path:Symbol` anchors, advisories never loop ·
qa PASS/FAIL with the exact command + output · report-don't-fix
(`BACKLOG CANDIDATE`) · humans commit all triage.

## What a consuming repo holds

```
.rnd/            config.toml (bindings — the ONLY per-repo customization) + backlog/
docs/living/     architecture/ operations/ [doctrine/] — NO frontmatter; anchors are the index
docs/design/     dated records WITH frontmatter — born live, frozen by git mv into v#-{slug}/
```

## CLI

```
python3 scripts/rnd.py fm [--kind K] [--status S] [--where k=v] [--json]
python3 scripts/rnd.py anchors [--audit|--fix|--dry-run|--suggest] [roots]
python3 scripts/rnd.py affected <files...>          # the hook's engine, <200ms
python3 scripts/rnd.py docs-check                   # [[surfaces]] bindings diff
python3 scripts/rnd.py standards [--write]          # canon vs repo, bindings preserved
python3 scripts/rnd.py backlog new <kind> "<title>" [--files ..] | close <ID> --resolution ".."
python3 scripts/rnd.py record new "<title>" [--kind design|decision]
python3 scripts/rnd.py init
```

Exit codes: 0 clean · 1 findings/drift · 2 argparse · 3 usage/config.
`--audit`, `--fix`, `--dry-run` always exit 0 (advisory modes).

## Schemas (the only two)

| | keys | enums |
|---|---|---|
| design record | kind · date · status · refs · [supersedes] | kind: design\|decision · status: live\|superseded |
| backlog item | id · kind · status · opened · files · seen · last-seen · [closed · resolution] | kind: bug\|debt\|feat\|perf · status: open\|closed |

One date format: `YYYY-MM-DD`. Ids: `KIND-NNN`, sequenced by the CLI. Never
hand-author either file type — `rnd backlog new` / `rnd record new`.

## Anchor gate internals

Ported from a field-proven checker (manifested-reality-agent's
`arch_check.py`), multi-language:
- anchors live ONLY in inline code spans; fenced blocks are illustrative
- banned shapes (line anchors) are tested before the anchor shape
- Python symbols via `ast` (names + `Owner.member`, nested defs, constants at
  module/class level only); Kotlin/TS/JS/Swift/Go/Rust via tuned per-language
  regex with brace-depth container tracking (~95% by design — a miss degrades
  to a file-existence check, never a false pass)
- `--audit` catches anchors that resolve but contradict the identifier beside
  them ("green is necessary, never sufficient")
- skips: `CLAUDE.md` (quotes banned forms to ban them) · `docs/design/`
  (frozen — rewriting erases provenance) · `doctrine/` (cites sources)
- same anchor 3+ times in one doc = defect (reported by the default check)

## Standards canon mechanics

`templates/standards/*.md` map to `docs/CLAUDE.md` + `docs/living/**/CLAUDE.md`.
`rnd standards` splits both sides on `<!-- rnd:binding NAME -->` /
`<!-- /rnd:binding -->` markers; canon segments must match byte-for-byte,
binding contents are the repo's own. `--write` regenerates while preserving
existing binding contents by name. Doctrine is generated only when
`[doctrine] authority` is set in config. **Shared-rule edits belong in this
plugin's templates, then `standards --write` in each repo.**

## Testing

```bash
python3 scripts/rnd.py --help                     # all 8 subcommands
python3 /tmp/rnd_smoke.py                         # round-trip in a scratch repo (if present)
# Fixture with planted defects: see the verification section of the build plan.
# Read-only parity check against a real deployment:
#   cd any repo with docs/living/ && python3 <plugin>/scripts/rnd.py anchors
```

## Design lineage

v2 (`../rnd-cycle/`, kept as reference) was condemned by audit: 23 artifact
types / 0 parsers, 7 incompatible status enums, prose workflow engine (c-run)
never once run, docs derived from intent instead of source. v3 inverts each:
parser first, one enum per key, orchestration in agents not prose, docs from
source with mechanical gates. Carried forward: adversarial verification,
BLOCKER/ADVISORY, four-status escalation, inline bundling, report-don't-fix,
binary `Done:` checks, seen/last-seen recurrence.
