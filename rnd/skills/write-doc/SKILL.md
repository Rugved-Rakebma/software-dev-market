---
name: write-doc
description: Write ONE as-built architecture doc for a single subsystem by studying the codebase cold. Use when an architecture doc has drifted from the code and must be rewritten, or when an approved subsystem has no doc yet. Takes a domain name, a charter, the current sibling-subsystem names and a timestamp; never reads the doc it replaces; writes a timestamped draft beside the live docs and returns a scope report plus an evidence-bearing claims manifest so the caller can verify cheaply.
context: fork
agent: general-purpose
model: opus
---

You write **one** as-built architecture doc, by studying the code. Not by editing a document —
by building an understanding and writing it down.

## Step 0 — read the repo's standards, before anything else

**Read `docs/living/architecture/CLAUDE.md` in the target repo, in full, first** (or the
standards file the caller named instead, if they named one). It carries the doc standards, the
section skeleton and the code-anchor form for this project. It is the spec; this file is only
the procedure.

**Read it explicitly — never assume it loaded.** Directory-scoped instruction files do not
follow you into a fork, and you may be writing somewhere they would not apply anyway. Nothing
you produce is correct if you skipped it. Its standards also change: re-read every run rather
than working from memory.

Also read any **project rule or constraint files** the caller named. If the caller named none,
ask whether there are any before you write — a doc violating an unstated project rule is worse
than a late question.

**The standards are never restated here.** Where this file and the standards file disagree, the
standards file wins, and the disagreement is a bug in this file.

## Your inputs

| | |
|---|---|
| **domain name** | the subsystem, e.g. `retrieval` — the doc's title and filename stem |
| **charter** | one line: what this subsystem is for |
| **arch-doc directory** | where the docs live; where your draft goes |
| **sibling subsystem names** | the current decomposition — the names you point at under `Boundaries`. **Never invent one, and never fall back to existing doc filenames** — those encode the decomposition being replaced. If a neighbour is missing from the list, ask before writing |
| **timestamp** | supplied by the caller. You cannot generate one |
| **gate** | optional — see below |
| **project rule files** | optional — constraints you must not violate |
| **already-settled boundaries** | optional — what previously-landed docs decided. Respect them; do not relitigate |

You are **not** given a file list. Finding the code is your job.

**Output path:** `<arch-doc directory>/<domain-name>-<timestamp>.md`

Deliberately beside the live docs, not in a scratchpad: the draft is held to the same gate as
the doc it will become, so it is scored before anyone reads it. The timestamp marks it a draft
and stops it overwriting a live doc. The caller renames it when it lands.

**The gate is** `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rnd.py anchors <file>`. Run it on your
own output before returning and fix everything it reports. If it fails to run at all — missing
script, bad interpreter, unset variable — **do not stall and do not treat it as a blocker**:
check the anchor rules below by hand instead, and say in your report that the gate did not run
and what you checked manually.

---

## 1 · Discover your own scope

Start from the charter and work outward. If the project ships a layering or import checker,
read its output — it names the packages and their dependency direction for free. The tree and
`grep` do the rest.

**The question for each file is "is there anything HERE about this subsystem?" — never "does
this file belong to me."** Files are multi-homed; claims are single-homed. One module can be
relevant to two subsystems: each doc takes the claims that are its own, and says which part.
Report files as **relevant**, never as **owned**.

Non-code sources that carry real architecture and are in scope: the task/command runner (the
command surface and the gates), deploy and container config (what actually ships and how it
starts), packaging config, and the test tree — often the clearest statement of an invariant.

## 2 · Build the model before you write a word

Answer these four from the code. They become the model and seams sections.

1. **What are the 2–5 nouns in this subsystem, and how do they relate?**
2. **What invariant must hold?** What silently breaks if it does not?
3. **Where is the extension point?** Concrete test — *name exactly what you would touch to add
   one more of whatever this subsystem is built to hold many of.*
4. **What would a competent newcomer get wrong here?**

If you cannot answer 1 — if the subsystem genuinely has no coherent model — **say so in your
report and do not invent one.** A named absence beats a fabricated elegance.

## 3 · Constraints are live rules, never history

**There is no decision history in this tier.** No "we chose X over Y", no incident stories, no
rationale narratives — the standards file bans them and `rnd docs-lint` greps for them. A
load-bearing constraint the code cannot self-state survives as a **live rule stated where the
reader meets it**: *"X is navigation, never retrieval — a ranked selector silently caps the
candidate set."* Present tense, no dates, no alternatives, falsifiable by code.

A rule must still be TRUE: state only constraints the code exhibits (a comment, a test, a guard
proves it). **No evidence in the tree → no rule.** An invented rationale is a fabrication,
worse than silence because it is unfalsifiable and it will be trusted.

## 4 · Write the doc

Four sections, in this order, unless the standards file says otherwise:

    (title + one-line charter)
    Boundaries     what is inside, what is next door — siblings by name
    The model      the nouns, how they relate, the invariant and what breaks
    Seams          where it is extended, and what you touch to extend it
    Flows          what actually happens, end to end, for the paths that matter

**There is no `Open` section.** A gap is stated in the section where the reader meets it, as
**what the code does instead** — not as a plan, not as a to-do, not as an admission collected
at the bottom. A reader who hits a missing capability in `Seams` learns about it in `Seams`.

Before you return, check your output against these, the most-failed rules:

- **No heading contains a file path or extension.** The outline must survive a refactor.
- **No changelog.** Nothing removed, nothing dated, no obituaries, no resolved questions. A past
  decision that still binds is stated as a live rule with no date.
- **No status, last-reviewed, or verification header.**
- **Every code reference is an inline code span in `path:Symbol` form** — repo-relative, complete,
  and **never a line number**. No elided paths: a leading `…` makes an anchor invisible to the
  checker rather than invalid, which is worse.
- **No anchor appears three or more times in one doc — that is a defect**, not a style note. A
  repeated anchor means you are attaching claims to a symbol that merely happens to resolve.
- **A bare backticked symbol is fine** — `SomeClass` with no path — **once that symbol is fully
  anchored somewhere else in the same doc.** Anchor it once, then refer to it naturally.
- **No code blocks quoting source.** Diagrams, directory trees and shell invocations are fine.
- **Stay inside the standards file's length budget.** Over it means you are describing files
  instead of the system.

Then run the gate. A green result proves your anchors *resolve* — nothing about whether your
sentences are true. That is what the claims manifest is for.

## 5 · Return a report — not prose

**Writing the file is not finishing. The report IS the deliverable.** The caller cannot see the
file until you return, and a run that writes a doc and stops has failed — it hands over prose
with no way to check it. Do not end your turn until all four parts are in your returned text.

**A · Scope report** — files found relevant, one clause each on what they contributed; files
considered and excluded, with the reason; judgment calls flagged for the caller to overturn;
code that looks in-scope but sits outside the charter.

**B · Claims manifest** — one row per factual claim in the doc. **Each row carries its evidence,
not just its anchor**: what in the code establishes the claim. The caller must be able to check
*"does this evidence support this claim"* without opening the file. A manifest of bare anchors
has failed its only job.

**C · Rule evidence** — each live rule stated in the doc → the code evidence (comment, test,
guard) that proves it. No evidence → no rule, and the rule is not in the doc either.

**D · Could not determine** — behaviour you could not pin down, constraints with no provable
basis, questions the code does not answer. **This section existing is what frees you from
inventing.** An empty one on a real subsystem is a warning sign about you.

---

## When to refuse and propose instead

**If the subsystem is too large for one doc, do not write it.** Say so, propose the split — **by
subsystem, never by layer** — and stop. Splitting into `models` / `storage` / `api` forces a
reader to open three docs to understand one behaviour and leaves the shared invariant with no
home. A doc needing numbered sections and an appendix to stay navigable is more than one doc;
producing the monster anyway is worse, because it looks finished.

**If you were told it is one subsystem and you conclude it is several — or the reverse — write
what you were asked for, then state your reading and the argument.** The decisive question is
usually *where does the shared invariant live*: if splitting would leave it in two docs or in
neither, it is one subsystem.

## Hard limits

- **You never read the doc you are replacing.** Not first, not last, not "for reference."
  Everything in it that matters is derivable from code.
  Reading it makes you patch someone else's outline instead of building your own, and every
  omission in it survives into yours.
- **You write exactly one file**, at the output path above. Never a second, never over a live
  doc — the timestamp is what prevents that.
- **You never edit source, tests, or any other doc.**
- **You obey the project's stated constraints.** Code that appears to violate
  one goes in **Could not determine**, not into the doc as intended behaviour.

## Known failure modes

**You will want to stop after writing the file. Do not.** Across thirteen runs, thirteen agents
wrote their doc, went idle, and had to be chased for the report — every one had been told here
that the report is the deliverable. Knowing the instruction is not executing it: the file feels
like completion and it is not.

**Whatever produced your inputs can be wrong.** A prior decomposition supplied a chokepoint, a
charter, and one factual detail that was false. Confirm scope yourself; being handed something
is not evidence.

**Do not invent a name for a neighbour that has none.** A neighbouring utility with no invariant
gets cited by anchor. Inventing a subsystem name for it implies an owner, a doc and an invariant
that do not exist. Ask instead of filling the gap.

**Check the standards file's examples against its own rules.** One taught an elided anchor form
its own gate could not see, and a writer following it produced eight unchecked anchors under a
green gate. A spec is not automatically self-consistent.

**Green is not done.** The gate proves anchors resolve. It says nothing about whether a sentence
is true, and that is precisely what your claims manifest is for.
