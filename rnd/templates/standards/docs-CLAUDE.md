# docs/ — placement and authority

Auto-loaded when working under `docs/`. Two tiers, and the split is the whole scheme:

- **`living/`** — must be true **today**. Its own `CLAUDE.md` says what that obligates, and
  each sub-tier declares what falsifies it.
- **everything else** — **dated records**. True as of the day they were written, and never
  updated to stay true.

The path tells you which. There is no index, no status table, and no doc that restates what
`find docs -name '*.md'` already answers.

## Placement

| The doc is… | goes in |
|---|---|
| as-built truth — falsified when the **code** changes | `living/architecture/` |
| how to drive the system — falsified when an **interface or procedure** changes | `living/operations/` |
| what the system *should* do — falsified by a **new reading of an outside authority**, never by code | `living/doctrine/` |
| live design work — the decision as it currently stands | `design/` **top level** (editable) |
| design work superseded by a later generation | `design/v#-{slug}/` (frozen — see below) |
<!-- rnd:binding frozen-tiers -->
| a dated notice to another team or repo | `handoff/` |
| a dated audit or investigation of an outside authority | `research/` |
<!-- /rnd:binding -->
| a plan, a status, or an intention | **nowhere in `docs/`.** A plan belongs in the commit that executes it. One project's status log was kept in-tree and became the most confidently wrong file it had |

**Never create a doc at `docs/` root.** Only this file lives there.

## Two ladders — one order cannot answer both questions

A single authority chain silently answers the wrong question for doctrine. There are two:

**"What is TRUE about the system?"** → code › `living/architecture/` › `living/operations/`
The code wins. A doc that disagrees is stale; fix the doc.

**"What SHOULD the system do?"** → `living/doctrine/` › frozen design records (provenance only)
Doctrine wins. **Code that disagrees with doctrine is a bug, not a stale doc.** Doctrine is
upstream of the code — it is a reading of something outside the codebase, and the code cannot
falsify it.

Dated audits and measurements ground the second ladder and sit on neither. Handoffs are on
neither — they record what something looked like on a date.

## `design/` has two floors, and only one is frozen

| | |
|---|---|
| **`design/*.md`** — top level | **LIVE.** The decision as it currently stands. **Editable, in place.** This is where design work is done. |
| **`design/v#-{slug}/`** | **FROZEN.** A generation that a later one superseded. Closed forever. |
| **`design/archive/`** | superseded **and** dead — describes nothing that runs. |

A doc is **born at the top level and stays there** for its whole working life. It becomes frozen
by being **moved**, never by being written into a versioned directory in the first place. If
`git mv` into `v#-{slug}/` is not the thing that froze it, it is not frozen. One project froze
every generation as it was authored, left the top floor permanently empty, and the rules drifted
into describing only the basement.

## Frozen records — append-never, remove-never

The dated tiers and `design/v#-*/` are closed to edits. Not "low-priority to update" —
**closed**. (`design/` top level is not; see above.)

- **Never move a doc OUT of a frozen directory.** A frozen dir that can be emptied is a staging
  area, not a record: it stops meaning *"what we believed then"* and starts meaning *"what we
  haven't promoted yet."* If a frozen doc should inform live work, **write a new living doc that
  cites it.** Synthesis, not relocation.
- **Never rewrite a body to match new reality.** That erases the provenance that is the entire
  reason the file was kept. A later record that *refines* an earlier one says so in its own body.
- **Dead links inside frozen docs are correct.** They point at what existed then. Do not chase
  them; a sweep that "fixes" them falsifies the record.
- Each frozen doc carries a `> **FROZEN <date> · non-authoritative**` banner, added **at the
  moment it is moved**, never before. A live `design/` doc carries a LIVE banner instead. Those
  two banners plus `living/` in the path are the only status markers in use.

**Freezing a generation** (a coherent redesign supersedes a batch of live design work): `git mv`
the whole batch **from `design/` top level** into `design/v{next}-{slug}/` — `#` is a global
monotonic era counter and `{slug}` names the subject; a later redesign of the same subject takes
the next number and the same slug. Swap the LIVE banner for FROZEN, re-base the relative links,
and fix the **live** docs that pointed in. Then it is closed forever.

## A frozen tier in another repo is not a guarantee

Cite another repo's dated records **by number, never by path** — `handoff #016 §3`. That is
allowed, because a dated record describes what an interface looked like on a day and nothing
here mirrors it.

**But we do not own them, and "frozen" is their convention rather than our guarantee.** One
project cited a sibling's handoff that was later deleted outright, leaving the citations
pointing at nothing. **Cite by number and state the FACT beside it**, so a dead reference costs
a provenance line and never the meaning. **A citation is not a substitute for saying what is
true.**

Sample payloads are a different thing again and live in the other repo's tests, not its records:
a dated sample is real content that is **not maintained**, so it is something to copy from once
and never to diff against.

## No README, no index

Both were considered and rejected: an index restates a changing list of files, so it rots, and a
stale orientation file costs most precisely when someone arrives cold. One project deleted two of
them in as many days — a root README that sold the system on a file that had been deleted, and a
sixty-row `docs/README.md` restating `ls` with a stale "Verified" column. **Do not create
either.** The directory listing is the index; `CLAUDE.md` files carry orientation, beside the
thing they govern.
