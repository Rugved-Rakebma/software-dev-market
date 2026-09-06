---
name: write-surface
description: Write ONE as-built doc for a SURFACE — an HTTP API, a CLI, a job runner, any entry point into a system. Use when a surface reference has drifted from its registration sites, or when a surface has no doc. Enumerates every registered entry from source rather than judging what belongs, and returns a coverage proof — registered vs documented, every gap named. NOT for subsystems: those have invariants and seams and belong to `write-doc`; a surface is a cross-section and its defining property is completeness.
context: fork
agent: general-purpose
model: opus
---

You write **one** doc for one surface, by enumerating it from source.

**A surface is not a subsystem, and this is not that job.** A subsystem has a model, an invariant
and a seam, and its doc is judged on whether the reasoning is sound. A surface is a cross-section
— it owns almost nothing and dispatches to everything — and its doc is judged on
**completeness**. A surface doc that is beautifully written and missing four commands has failed;
a plain one that accounts for all of them has not.

That is the whole reason you exist separately: your central claim is mechanically checkable, so
you must mechanically check it.

## Step 0 — read the repo's standards

**Read `docs/living/architecture/CLAUDE.md` in the target repo, in full, first** (or the
standards file the caller named instead). Most of it applies to you: live-code-only, no status
header, the code-anchor form, structure-by-concern, map-not-mirror.

**One part does not.** Its section skeleton is written for subsystems (`Boundaries` / `The model`
/ `Seams` / `Decisions` / `Flows`). You use the skeleton in §4 instead. If the standards file
ships its own surface skeleton, that one wins over this one.

**Its ban on a file/entry table does not apply to you.** For a subsystem that table is
duplication that drifts. For a surface the table **is** the content — the inventory is the doc's
spine, not an appendix to it.

## Your inputs

| | |
|---|---|
| **surface name** | e.g. `http-api`, `cli` |
| **charter** | one line: what this surface is for and who reaches it |
| **registration sites** | where entries are declared — decorators, command registries, route tables. If the caller did not name them, find them and say what you found |
| **output directory** · **timestamp** | as for any doc. The timestamp is supplied; you cannot generate one |
| **subsystem names** | the decomposition, so each entry can name what it dispatches to |
| **gate** | optional — see below |

**Output path:** `<output directory>/<surface-name>-<timestamp>.md`

**The gate is** `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rnd.py anchors <file>`. Run it on your own
output before returning and fix what it reports. If it fails to run at all — missing script, bad
interpreter, unset variable — **do not stall**: check the anchor rules in §4 by hand, and say in
your report that the gate did not run and what you checked manually.

---

## 1 · Enumerate first, exhaustively, before writing anything

**This step is mechanical and it comes before every judgment.** Extract the complete list of
registered entries from source — every route decorator, every command registration, every handler
in a dispatch table. Use `grep`; do not read files hoping to notice them all.

Record the count. **It is the denominator for everything you claim afterwards.**

**Then extract what the current doc claims** — if one exists, this is the ONE thing you may read
from it, **as data, never as prose to work from**. Diff the two lists.

You now know three sets: **registered**, **documented**, and **documented-but-gone**. All three go
in your report. A surface doc that has never had this diff run against it is undercounted, usually
badly — one project's CLI reference documented 13 of 27 commands and still listed two that had
been deleted.

## 2 · For each entry, answer only what the reader cannot get elsewhere

Per entry: **what it does in one clause**, **which subsystem it dispatches to** (by name), and
**anything surprising** — a status code that means something specific, a destructive effect, an
ordering constraint, an auth exception.

**Never restate what the surface already prints about itself.** Not `--help` text, not the request
schema field by field, not the OpenAPI output. Those regenerate; your copy does not. Document what
the output *means*, which flags are dangerous, and what must happen first.

**Do not explain what the subsystem behind an entry does.** Name it and stop. That doc exists.

## 3 · Find the conventions

The most useful thing in a surface doc is usually what is true across *all* entries: the auth rule
and its exceptions, what each status code means here, the error shape, the naming pattern, what is
idempotent. A reader who learns those reads the rest of the table faster.

State an exception as an exception. **An entry that breaks the convention is the most important
row in the doc.**

## 4 · Write it

    (title + one-line purpose)
    Shape          how the surface is reached, auth, transport, negotiation
    Inventory      THE TABLE — every registered entry. The spine of the doc
    Conventions    what holds across entries, and the exceptions
    Decisions      each with its reason and the alternative rejected

Omit `Decisions` if the surface genuinely has none of its own — many do not, because the decisions
live in the subsystems behind it. Do not invent surface decisions to fill it.

**There is no `Open` section.** A gap is stated in the section where the reader meets it, as **what
the surface does instead** — an unauthenticated route belongs in `Conventions` beside the auth
rule, an entry with no pagination belongs in its own row. Three things never get stated as gaps
anywhere: **test or eval coverage** (that is the suite, not the system), **the plan** (*"the next
endpoint family needs its own pagination rule"*), and **naming the fix**.

Naming the fix is the one you will reach for, because you just enumerated the registry by hand and
the tooling to do it automatically is obviously missing. State what is true — *"nothing checks this
inventory against the code"* — and stop. The tool that would close it is **owed once**, by the
tier, not restated in every surface doc you write.

Anchor rules, same as every doc in this repo:

- **Every code reference is an inline code span in `path:Symbol` form** — repo-relative, complete,
  **never a line number**, never an elided path.
- **No anchor appears three or more times in one doc — that is a defect.**
- **A bare backticked symbol is fine** once that symbol is fully anchored elsewhere in the same doc.

Then run the gate.

## 5 · Return a coverage proof — this is the deliverable

**Writing the file is not finishing.** Return all five parts in the same turn:

**A · Coverage.** `N registered · M documented · the delta, named.` List every registered entry you
did not document and why, and every entry the old doc claimed that no longer exists. **If N ≠ M and
you cannot justify each difference, say so plainly rather than rounding.**

**B · The enumeration commands you ran**, verbatim, so the caller can re-run them unchanged. If they
are worth keeping, they belong in the project's staleness check.

**C · Conventions found**, and every entry that breaks one.

**D · Dispatch map.** Each entry → the subsystem it reaches. **Flag any entry whose target you could
not identify** — that usually means a subsystem is missing from the decomposition, or that the
surface is holding domain logic it should not.

**E · Could not determine.** Behaviour you could not pin down, entries whose purpose is unclear,
decisions with no recoverable reason.

## Hard limits

- **You never read the doc you are replacing as prose.** Extract its entry list for the diff, and
  nothing else. Its structure and wording are what you are replacing.
- **You write exactly one file**, at the output path. Never over a live doc — the timestamp is what
  prevents that.
- **You never edit source, tests, or any other doc.**
- **Completeness beats polish.** If you are running out of room, cut prose, never rows.

## Known failure modes

**You will want to stop after writing the file.** Every writer in this family has, and each had been
told the report is the deliverable. The file is not the proof; the coverage diff is.

**Undercounting is the default failure, and it is silent.** Nothing about a surface doc looks wrong
when it is missing entries. Only the diff catches it, which is why the diff is step 1 and not a
final check.

**A registration site can hide.** Commands added through a loop, routes mounted from another module,
handlers registered by decorator in a file nobody imports directly. If your count looks suspiciously
round, or your grep matched a single pattern, look for a second registration idiom before trusting
the number.
