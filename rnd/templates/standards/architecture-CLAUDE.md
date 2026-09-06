# docs/living/architecture/ — as-built truth

**Falsified by:** the code changing. These docs are **downstream** of the source. On any conflict
the code wins and the doc is the bug.

**Who reads them:** someone about to modify the code. They need to know where a thing lives,
where the seams are, why it is shaped this way, and what breaks if they change it.

**Nothing regenerates them.** A stale claim stays stale until a human fixes it, which makes rule
1 of `../CLAUDE.md` — update in the same commit — the load-bearing one.

The nine standards below are general and were earned: each one replaced something that
demonstrably went wrong. Change them if this project needs different ones, but change them
deliberately — the doc-writing agents read this file as their spec and follow it exactly.

---

## The nine standards

### 1 · Live code only

No removed features. No "was X until <date>". No changelog, no obituaries, no
resolved-questions graveyard. **Version control and release notes hold history; these docs hold
the present.**

If a past decision still constrains the code, state it as a **rule** — drop the date and the
corpse.

| | |
|---|---|
| ✅ | *"X is navigation, never retrieval — the whole index fits in a prompt, so a ranked selector would silently cap the candidate set for no gain."* |
| ❌ | *"`retrieve_x` was deleted on \<date\>."* |

Removal notes only ever accrue. A section titled `<Thing> — REMOVED` is a permanent monument to
something a reader does not need to know about.

**An incident may be stated tenselessly, and often should be.** The strongest rationale in a
codebase is frequently a night something failed. Standard 8 wants the rejected alternative; this
standard bans the date and the corpse. Both are satisfied by *"was paid for once, when one bad
argument took the service down and the phone stayed silent"* — the force survives, the changelog
entry does not. A naive reading of this standard deletes the most persuasive material in the
file; do not let it.

### 2 · Structure by concern, never by file

Headings are behaviours and questions. **Never a filename.**

**Test: the outline survives a refactor that moves files.** `## Data model — store/models.py`
fails it; `## What a focus area is made of` passes.

When section headings are file paths, the doc's structure is the file tree — that is a mirror,
and the code is always a better mirror of itself.

### 3 · Every code reference is structured and machine-extractable

One form, always inside an inline code span: `<repo-relative-path>:<Symbol>`, or a bare
repo-relative path for a whole file.

<!-- rnd:binding language-forms -->
| Citing | Write |
|---|---|
| a function | `src/pkg/module.ext:function_name` |
| a class | `src/pkg/module.ext:ClassName` |
| a method | `src/pkg/module.ext:ClassName.method_name` |
| a constant | `src/pkg/module.ext:CONSTANT_NAME` |
| a nested symbol or callback | `src/pkg/module.ext:ClassName.Inner.on_event` — go as deep as the nesting, do not stop at `Class.method` |
| a whole file | `src/pkg/module.ext` (no colon) |
| a block with no symbol | the enclosing symbol + prose ("…in the `finally` of `X`") |
| a dated measurement in a frozen tier | its **filename**, in prose — deliberately outside the anchor form and outside the gate, because a frozen doc cannot break |

*(Replace these with real paths and real symbol kinds from this repo, and add the forms this
language needs — a writer copies the form it sees here. If the project has multiple source sets
or generated/platform-specific variants of one symbol, say which side must be cited.)*
<!-- /rnd:binding -->

**One anchor must not carry many unrelated claims.** If the same `path:Symbol` appears **three or
more times in one doc**, attached to different assertions, that is a **defect** — re-anchor it.
This is the failure that kept one project's gate green for weeks while a doc hung eight unrelated
claims off a single function that happened to resolve. It is a rule, not advice.

**A non-public symbol is a legal anchor.** Visibility is a language concern, not a documentation
one, and the reader you are writing for is about to open the file anyway.

**Banned, all of it:**

- **Line numbers** — `module.ext:1612`, `` `:325` ``, `module.ext:353-357`, `module.ext:60,67`.
- **`Symbol:line` with no path** — `ClassName:46`, `method:262`. Most checkers cannot see these,
  so they slip the gate silently.
- **Elided paths** — `…/pkg/module.ext:ClassName`, and the package-shortened `pkg/module.ext`.
  **The worst of the four**, because it fails *silently in the safe direction*: an anchor pattern
  needs a real leading path, so an elided one is not resolved-and-rejected, it is **never seen**.
  Measured on a real checker: a doc citing `…/nope/absolutely_not.ext:NotReal` passes green. One
  project's own standards file taught the elided form in its examples table, and a writer
  following it produced eight unchecked anchors under a green gate.
- **Prose-only references** — *"the stages package"*. Unextractable, therefore invisible to
  tooling. **A bare backticked symbol is fine once that symbol carries a full anchor somewhere in
  the same doc** — repeating a 95-character path every time you mention it costs more than it
  buys. First mention anchors; later mentions may be bare.
- **Partial paths** — not `app.ext`, not `api/app.ext`, but the complete repo-relative path.
  Bare filenames are ambiguous in most trees, and near-identical filenames across source sets
  make them dangerous in some.

**Why the form is rigid.** A script can then emit every path a doc claims, which buys three
things nothing else does: **orphan detection** (the doc cites a path that no longer exists),
**coverage** (code no doc mentions at all), and **blast radius** (which docs a file appears in,
so a change knows what it invalidates). That only works if **every** reference is in the form —
one prose mention is a hole in all three.

**Why not line numbers.** They don't break, they *lie* — a stale line resolves to different code
with no error anywhere. One added comment silently shifted seven anchors by twelve lines, leaving
a class citation pointing into the middle of an unrelated method. A symbol survives every edit
that isn't a rename, and a rename makes the anchor *checkably* wrong instead of quietly wrong.
The trade — `path:line` is clickable, `path:Symbol` is not — is accepted: a wrong-but-clickable
link is worse than a right-but-greppable one.

### 4 · No status, verified, or reviewed header

No `Status: as-built`, no `Last reviewed: <date>`, no verification table.

`living/architecture/` in the path already means current. Keeping the doc true is the
**obligation**, not a field to update, and a date nobody maintains is a lie with a timestamp on
it. One project deleted its whole doc index for exactly this, at index scale.

### 5 · One doc = one subsystem a person can hold in their head

If a doc needs numbered sections and an appendix to stay navigable, it is more than one doc.

Split by **subsystem, not by layer** — not `models` / `storage` / `api`. A layer split forces the
reader to open three files to understand one behaviour, and leaves the shared invariant with no
home. A module or package boundary that carries no information is never the split.

**Length budget: 100–180 lines, measured with the characters inside code spans removed first.**
Over it, you are describing files instead of the system. Under it is fine — a short honest doc
beats a padded one.

Strip the anchors, then count what is left:

```sh
sed 's/`[^`]*`//g' <doc> | grep -cE '[A-Za-z0-9]'
```

Strip the code spans **then** drop lines with nothing alphanumeric left. A wrapped anchor leaves
behind a line holding a stray comma or bracket, and counting those reintroduces the path-length
effect this rule exists to remove.

A long anchor sits *inline mid-sentence*, so it wraps across two prose lines and neither line is
"wholly a citation" — which is why an exclusion phrased per-line does not work, and why this one
is phrased per-character. Counted raw, the budget stops measuring *"am I describing files"* and
starts measuring **path length**, which no author controls.

### 6 · A fact lives in exactly one doc — and you NAME the other doc, never link it

Two copies means one is maintained and the other is a trap. So point elsewhere instead of
repeating — but point at the **subsystem name**, never at a file path.

`turn generation → **turn-executor**` ✅ · `turn generation → [chat-agent](./chat-agent.md)` ❌

**Names are stable; paths are not.** A doc gets renamed, split or merged and every link into it
dies silently — one directory rename produced forty-five dangling links in a single repo. And
nothing checks doc-to-doc links; anchor gates validate code references only. Listing the
directory finds a doc by name in one step, and there is no index to maintain. Same principle as
`path:Symbol` over `path:line`: point at the durable thing.

**`Does NOT own` still has to say where it lives** — a bare "not us" costs the reader everything
the section exists to save. **But not every neighbour is a subsystem:**

| The neighbour is | Point at it as |
|---|---|
| another subsystem | its **name** |
| a subsystem that exists but has **no doc yet** | say exactly that — *"a separate subsystem with no doc yet"* — plus code anchors. Never its name: a name implies a doc, and every doc written before the set is complete hits this case |
| a surface | its name, said to be one — *"the HTTP API, a surface"* |
| a rule about what a surface may do | **doctrine**, by doc name |
| a utility with no invariant of its own | a code anchor (standard 3), never a name |

Inventing a subsystem name for a utility implies an owner, an invariant and a doc that do not
exist.

### 7 · One skeleton, every doc, same order, same heading names

| Order | Section | Holds |
|---|---|---|
| 1 | *(title + one-line purpose)* | what this subsystem is for |
| 2 | **Boundaries** | Owns · Does NOT own · Talks to |
| 3 | **The model** | the 2–5 concepts and how they relate — what you must understand before reading code |
| 4 | **Seams** | where it is extended, what is pluggable, what is load-bearing |
| 5 | **Decisions** | each with its reason and the alternative rejected |
| 6 | **Flows** | non-obvious paths only. Omit the section if there are none |

Exact casing: `Boundaries` · `The model` · `Seams` · `Decisions` · `Flows`.

**Where a gap goes: the section where the reader meets it.** A gap is stated as what the code
does *instead* — never as a bullet list of absences. *"X is not enforced at fire time; the
fallback tone is the guarantee instead"* belongs in `The model`, and a future commit can make it
false. *"X is untested"*, *"Y would fix this"*, *"Z is the next win"* are not facts about the
system and belong nowhere in this tier.

There is no `Open` section. A gap parked at the bottom is a gap nobody acts on, nothing falsifies
it, and a reader can finish the paragraph that matters believing something the doc contradicts
eight sections later.

**No `Key Files` table.** With standard 3 holding, a script scans the whole doc for references,
so the table is duplication that drifts — and it puts an annotated directory listing in the
position that should carry the model.

**`Boundaries` is the highest-value section.** Owns / Does NOT own is what answers "where does
this go?" before someone puts it in the wrong place.

### 8 · A decision without its reason is not architecture

"What" is recoverable from the code. **"Why this and not the obvious alternative" is not** — it
is the entire reason the doc exists. Every entry under `Decisions` names the alternative that was
rejected and what made it wrong, stated as a live constraint rather than a story. *"A foreground
service, not a receiver — a receiver dies in ten seconds and the sitting is twelve minutes"* is
the shape.

### 9 · Map, not mirror. No code blocks

If a reader needs the code, the reference takes them there. A code block in an architecture doc
is a second copy of a file, stale the moment the file changes.

*(Fenced blocks for a diagram, a directory tree, or a shell invocation are fine — they are not
citations of source. **Tables are fine too**, and are often the right shape for contrasting two
variants of one thing — two wire dialects, two platforms, two result channels.)*

---

## Staleness test

<!-- rnd:binding anchor-gate -->
```sh
rnd anchors                 # every anchor resolves (hard failure on a miss)
rnd anchors --orphans       # paths cited by no doc, and docs citing dead paths
```

*(Replace with this repo's task-runner wrapper if it has one — e.g. `just anchors`. Whatever it
is, it must be the invocation someone can actually run before committing.)*
<!-- /rnd:binding -->

**What it proves:** every `path:Symbol` citation names something that exists in the tree.

**What it does NOT prove:** that a single sentence is true. This gap gets exploited — one
project's docs accumulated seventeen uses of a single real symbol as the anchor for unrelated
claims, and the gate was green the whole time.

**So: green is necessary, never sufficient.** When you touch a doc, re-read the prose around the
anchors you touched. **An anchor reused three or more times in one doc is a defect** (standard
3), not a smell to note and move past.

## Changing code → what to check here

<!-- rnd:binding changed-code-table -->
| You changed | Check |
|---|---|
| *(one row per subsystem, filled in from this repo's approved decomposition)* | |

*(Leave this **empty on purpose** until the decomposition has been derived and approved. A
guessed table here is the exact failure this tier exists to prevent.)*
<!-- /rnd:binding -->

**A change usually lands in more than one row.** Then run the gate before committing.
