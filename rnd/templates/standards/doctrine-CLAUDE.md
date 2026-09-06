# docs/living/doctrine/ — what the system SHOULD do

**Falsified by:** a new reading of the authority — a source read, a spec revision, a result, a
newly-noticed tension, a measurement that makes a promise undeliverable. **Not** by the code.

This is the one tier **upstream** of the source. Everywhere else the code is the authority and a
disagreeing doc is stale. Here it inverts:

> **Doctrine and the code disagree → that is a bug in the code, not a stale doc.**

**This tier is optional, and many projects do not need it.** It exists only where something
*outside the code* has authority over what the system should do — a specification, a standard, a
regulation, a body of research, a source corpus, or a body of surface law nothing in the codebase
can prove wrong. If this project has no such authority, delete this directory rather than leaving
it empty.

Doctrine is organised by **your problem** — never by author, never by document, never mirroring
the authority's own table of contents. Organising it their way makes it a summary; organising it
your way makes it a position.

## A doctrine doc is a list of laws

**One line per law. An id, the law, a provenance tag, a source id. Nothing else.**

```
| **S1** | A state is a place the person stands, not a property of them. | 📖 | `eternal-states` |
```

It must be readable start to finish by a person who is deciding something. That is the whole
test. **A law that needs a paragraph is two laws**, or it is not a law yet.

**What does NOT go in a doctrine doc** — every one of these was tried in one project and cut the
same day for burying the laws:

| | goes in |
|---|---|
| coverage counters, source ledgers, per-unit mappings | the dated audit that grounds the doc |
| named gaps in what has been read | same |
| verbatim quotes, prevalence counts, denominators | same |
| "where the code disagrees" | the design doc that owns the work — it is a build backlog, not a law |
| reading notes, methodology, frozen-input tables | same audit |

**The one apparatus that stays: the tensions register.** Unresolved positions are doctrine, not
metadata. One line each.

## Doctrine is not design, and not research

| | |
|---|---|
| frozen design records | a **decision**, at the moment it was made. Frozen, because the moment passed |
| dated audits and measurements | what an authority contains, or what the hardware did, on a date. Done; never revisited |
| **doctrine** | a **position held now**, grounded in the authority, that **accretes**. Never done |

**Doctrine docs are written FROM the frozen record, never moved out of it.** Old notes are
*inputs* — priming material with unresolved threads. A doctrine doc reads them, verifies against
the authority, and states the position. Notes → position is a rewrite, not a move.

## Staleness test

Nothing about the code can tell you a doctrine doc is stale.

**If the binding below is empty, this project has no corpus with a denominator, and the test is:
every rule names the alternative that was tried and why it was rejected.** A counter with an
invented denominator is worse than none.

**What that proves:** the rule is a *position*, arrived at, and a reader can tell whether their
new idea is the thing that already failed.

**What it does NOT prove:** that the position is still wanted. Nothing in the code or the tests
can tell you a law has been quietly abandoned by the product. **A rule with no rejected
alternative is a preference, not doctrine** — the most common way this tier misleads is by
promoting a default nobody chose into a law nobody may question.

<!-- rnd:binding authority -->
<!-- Leave empty if there is no outside corpus. If there IS one, name it here and state the
     coverage counter that every doctrine doc in this project must carry in its header —
     `**Coverage:** <Authority A> 13/16 · <Authority B> 20/391` — plus where the ledger lives.
     A low count is not a defect; an absent count is. Without it, silence reads as "the
     authority doesn't address this", which is the other most common way this tier misleads. -->
<!-- /rnd:binding -->

## Rules

**1. Accretes. Never rewritten to look finished.**
Add laws, extend the register. Do not delete a tension because it became inconvenient, and do not
smooth a doc into false completeness. **Incomplete and honest beats complete and invented.**

**2. Record tensions; do not resolve them silently.**
When two authorities disagree — or an authority disagrees with a measured result — it goes in the
**tensions register** with both positions and what would settle it. Picking a winner in prose and
dropping the loser destroys the only record that the question was ever open. A settled tension is
**marked settled and kept**, never deleted.

**3. Tag every law.**
📖 author-verbatim · ⚗️ our extension · 🔧 infrastructure. **You cannot honestly tag a passage you
have not read.** An ⚗️ law derived from other laws cites those ids instead of a source.

**4. Quote only from a full read.**
Search may LOCATE — absence checks are legitimate and valuable. Only a full read may QUOTE. A
search snippet is never quotable: it arrives stripped of the argument it sat inside. **A
retrieval null is never evidence of absence** — it means the selector did not rank it, not that
the authority is silent.

**5. Every law carries a source id.** The evidence behind it lives in the linked audit. **An
absence is a law too** — *"the authority nowhere says X"* is one of the most useful things this
tier holds, and it cites the denominator it was checked against.

**6. Doctrine states what should be, not what is.**
The moment a line describes what the code currently does, it belongs in `../architecture/` or in
a design doc. Doctrine is allowed to describe things that are not built — that is the point of
being upstream.

**7. Name what the authority underdetermines.**
Where the sources genuinely do not settle something, say so and stop. Reaching past that line is
how an ⚗️ invention gets read back later as 📖.

**8. A violation is named, not softened.**
If the code disagrees, say so in the same breath as the law it breaks. Quietly rewording doctrine
to match a regression is how this tier dies. **Naming it is the whole of the job here** — this
file scopes someone editing DOCS, and telling them to go fix the code turns a documentation task
into a licence to change the system. The disagreement is a finding; what to do about it is a
decision for whoever owns that code, in its own change.

## Changing doctrine → what to do

- **Update the linked audit in the same edit** if new source was read. Coverage lives there, and
  an edit that reads new source without raising it makes the count a lie.
- **Check `../architecture/` for a contradiction.** An as-built doc describing the thing doctrine
  now forbids is the work item — do not quietly soften the doctrine to match.
- **Check the dated measurements before promising anything about timing or perception.** A claim
  not traceable to one is a guess wearing a law's clothes.
- **Cite the frozen records for lineage** where a position originated there.
