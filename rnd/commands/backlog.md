---
description: Add, list, close, or sweep backlog items — ids and frontmatter stamped by the CLI, triage always human
argument-hint: add <kind> <title> | list [filters] | close <id> | sweep
---

## Process

Backlog: **$ARGUMENTS**

All operations run through the CLI — never hand-author a backlog file:

| Op | Command |
|---|---|
| add | `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rnd.py backlog new <bug\|debt\|feat\|perf> "<title>" --files <paths...>` — then open the created file and fill the body: what's wrong, how to reproduce, why it matters. Two sentences minimum, no essays. |
| list | `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rnd.py fm --kind <k>` / `--status open` / `--where files=<path>` — present as a table |
| close | `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rnd.py backlog close <ID> --resolution "<what fixed it>"` — only when the user confirms it's actually resolved |
| sweep | read every open item + `git log --oneline -20`; report per item: still valid · likely fixed (name the commit) · duplicate of (name the id) · stale. **Advisory only — mutate nothing.** The user picks which closes to run. |

## Notes

- If the same issue resurfaces, bump `seen` and `last-seen` in its frontmatter (Edit) instead of filing a duplicate — recurrence is the strongest priority signal this system has.
- Auto-creates `.rnd/` on first use; no init required.
- Agents never close items. `BACKLOG CANDIDATE`s arriving from build/verify runs are offered to the user one by one, never bulk-filed.
