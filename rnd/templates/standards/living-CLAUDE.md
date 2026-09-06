# docs/living/ — the maintenance contract

Auto-loaded under `docs/living/`. Everything here **must be true today**. A living doc that has
drifted is not "out of date" — it is a **bug**, and it is worse than no doc, because it is
confidently wrong at the moment someone is trusting it.

Three tiers, distinguished by **what falsifies them**. Each has its own `CLAUDE.md` with its own
test; this file is what they share.

| Tier | Falsified by | Direction |
|---|---|---|
| `architecture/` | the code changed | **downstream** of code |
| `operations/` | an interface or procedure changed | **downstream** of code |
| `doctrine/` | a new reading of an outside authority | **upstream** — code can't falsify it |

*(A repo may have only one or two of these. An empty tier is worse than an absent one — delete
the directory rather than leaving it as a promise.)*

## The five rules

**1. Update in the same commit as the change. Never "flag it."**
A living doc is part of the change, not follow-up work. If a route, command, entity, path, or
contract changes, the living doc that mirrors it changes in that commit or the change is
incomplete.

**2. Never restate what a command already answers.**
`ls`, `--help`, `git log`, and your task runner are the source for their own facts. A doc that
copies them is stale the moment either side moves, and nothing signals it. Point at the command;
explain what the output *means*.

**3. No index files. Ever.**
No `README.md`, no doc-of-docs, no status table, no "Verified" column. `find docs -name '*.md'`
is the list; each doc's first five lines say what it is. An index is a restatement of the
filesystem with a human maintaining the copy — it always loses.

**4. State the staleness test, and state what it does NOT prove.**
Every tier names how you check it. Each also names its blind spot, because a green gate read as
proof is how one project's architecture docs accumulated seventeen uses of a single unrelated
symbol as an anchor. **Green is necessary, never sufficient.**

**5. A doc that cannot be kept true gets deleted, not downgraded.**
There is no "mostly accurate" tier. If nobody will maintain it, version control already holds it.

## The known hole

**These files load when you edit the doc. They do not load when you edit the code that falsifies
the doc.** Nothing in context knows a doc mirrors the route list while you are editing the source
that registers it. That gap is how a CLI reference ends up documenting half the commands: they
were added in the source tree, and nothing in context knew a doc mirrored them.

Two mitigations, both real:

- **The always-loaded file:** the repo-root instruction file — the one loaded in every session
  regardless of what you touch — carries the same-commit obligation and the anchor form. Put
  cross-cutting obligations there, not only here.
- **The gate:** `rnd docs-check` diffs each living doc against the real surface, and `rnd
  anchors` resolves every code citation. These exist; they are not honour-system any more. Rule 4
  still stands — a gate that passes is not a doc that is true.

<!-- rnd:binding gate-name -->
**In this repo the gate is invoked as `rnd docs-check` and `rnd anchors`.** *(Replace with the
task-runner wrapper if this repo has one — e.g. `just docs-check`. If neither is wired up yet,
say exactly that here: until it is, rule 1 is honour-system and rule 4's manual tests are the
only defence.)*
<!-- /rnd:binding -->
