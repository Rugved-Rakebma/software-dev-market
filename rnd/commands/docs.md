---
description: Living docs — scaffold the tiers, derive architecture/surface docs from source, or audit the whole set
argument-hint: scaffold | derive [subsystem...] | audit
---

## Process

Docs mode: **$ARGUMENTS**

### scaffold

1. `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rnd.py standards --write` — generates `docs/CLAUDE.md` + `docs/living/{,architecture/,operations/}CLAUDE.md` (+ doctrine if an authority is bound in `.rnd/config.toml`).
2. Walk the user through each **binding region** (`<!-- rnd:binding ... -->`) — anchor gate command, surface enumeration commands, frozen-tier names, project command list. Fill them together; a template with brackets left in reads as the standard.
3. Migrate what already exists: existing docs move (`git mv`) into their tier, frozen material gets its `FROZEN <date>` banner, indexes get deleted with a "do not recreate" note. Never rewrite a frozen body.
4. Add the same-commit obligation to the **repo root** CLAUDE.md (the tier files don't load when code is edited — the root file is the only place that helps).

### derive

1. **Map** — invoke the `map` skill (forks into its own context; reads no docs). Present its decomposition: candidates + evidence, disagreements with the file tree, borderline calls.
2. **Gate** — the user approves/edits the subsystem list. No doc is written before this.
3. **Write** — per approved subsystem (≤3 at once), invoke `write-doc` with a packet: domain, charter, sibling names, timestamp, the standards file path, and (if replacing an old doc) a rationale packet — every decision-bearing sentence from the old doc, heading-stripped, shuffled flat, labeled UNVERIFIED CLAIMS. For surfaces (HTTP API, CLI), invoke `write-surface` instead.
4. **Verify each report** — spot-check 2-3 claims-manifest rows against source; read the writer's could-not-determine section; then land: `git mv <name>-<timestamp>.md <name>.md`, run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rnd.py anchors`, repair inbound name references, delete the old doc only when fully covered.

### audit

1. `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rnd.py anchors` — hard gate, must be green.
2. `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rnd.py anchors --audit` — anchors that resolve but contradict their prose; triage each with the user.
3. `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rnd.py docs-check` — surface diff per binding.
4. `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rnd.py standards` — canon drift.
5. Report findings in one table; fixes are same-commit edits, deletions preferred over additions.

## Notes

- Standards are CANON — edits to shared rules belong in the plugin's templates, then `standards --write` everywhere. Only binding regions are per-repo.
- Green gate ≠ true docs: the gate proves anchors resolve, nothing more. That is why `--audit` and review exist.
