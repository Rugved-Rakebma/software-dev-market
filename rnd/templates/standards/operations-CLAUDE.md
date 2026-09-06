# docs/living/operations/ — how the system is driven

**Falsified by:** an interface or a procedure changing. Also **downstream** of the code, but
addressed outward — to whoever is operating the system, not reading its internals.

Two shapes, one contract:

- **Surface** — a reference: every registered entry, what it hits, what it returns.
  **Completeness is the property**; prose is not.
- **Procedure** — a runbook: do these steps, in this order, with these guards.

`architecture/` explains how it is built. This explains how you drive it. **If a doc is doing
both, it is in the wrong tier.**

**Surfaces live here, not in `architecture/`, because the tier is decided by what falsifies a
doc — and a surface goes false when an *interface* changes, not when the code behind it does.**
Genre decides the doc's shape; the falsifier decides its tier. They are different questions.
Surface docs still cite code, so the anchor gate covers this directory too.

**Do not write docs for procedures nobody has run.** A runbook for a release that has never
shipped is fiction with a shell prompt in front of it.

## Staleness test — enumerate, then diff

**Ask the assembled program, never a grep of source patterns.** A registration idiom you did not
think to grep for is invisible, and it fails in the safe-looking direction: the count looks fine.
One project had a command registered as a group *callback* rather than through the usual
decorator, so every grep-based count was short by exactly one, silently, for months.

<!-- rnd:binding surface-commands -->
```sh
# One block per surface. Each must read the BUILT program — the route table off the
# assembled app, the registered command tree including group callbacks, the job registry —
# not a pattern match over source.

# Procedure docs: every script, recipe, flag and path they name must still exist.
```
<!-- /rnd:binding -->

Diff each against the rows its doc claims. Anything registered-but-undocumented is a hole;
anything documented-but-unregistered is a lie.

**What having no gate costs, measured:** one project's CLI reference documented **13 of 27**
commands and still listed two that had been deleted. Nobody was wrong on purpose — the commands
were added in source, and nothing in context knew a doc mirrored them.

`rnd docs-check` folds the enumeration above into a gate, so this is no longer a habit that
depends on someone remembering. Run it; the manual blocks stay here because they are what the
gate is checking and what you fall back to when a new surface has no rule yet.

**Gaps are stated where the reader meets them** — see `../architecture/CLAUDE.md` standard 7. A
surface doc states a gap as what the system does *instead*, never as a bullet list of absences
and never as the fix.

## Rules

**1. A procedure doc names commands verbatim, and they are checked.**
A repo-wide rename once rewrote prose *through* command names, leaving a runbook instructing
`tool group thing start` for a command that is `tool thing start`. Reading a runbook is often the
one time a wrong command costs real money. Re-run the commands, or at minimum `--help` them,
whenever you edit.

**2. Never restate `--help`.**
Document what the output *means*, which flags are dangerous, and the order operations must happen
in. If a script already prints its own sequence, a doc that copies that text is a second copy to
keep true.

**3. A destructive procedure is prose when the danger is SELECTION, a recipe when it is
MECHANICS.** The distinction decides the artifact, and getting it backwards produces either a
script nobody should trust or a runbook nobody follows correctly.

A **surgical cleanup stays prose.** It picks which records die and leaves the rest, so a mistake
is partial and silent, and there is no check a script can make that a human reading the diff
cannot make better. Forward-commit, never force-push.

A **total wipe is a recipe.** There is nothing to select — one destination state, and it is
`empty`. What can go wrong is entirely mechanical: destroying history, destroying something that
never reached the remote, leaving files the service cannot write. A recipe checks all of that
every time; a human pasting shell commands checks them when they remember to.

Whichever it is, three properties are not optional: **it backs up before it destroys**, it is
**dry-run by default**, and it **names the restore point** in its own output and in whatever
record it writes. A destructive operation that cannot tell you where the previous state went is
not finished being designed.

**The gate token is `-confirm`, in every recipe, with no exceptions.** The bare invocation
previews; `<recipe> -confirm` acts. It reads as a flag at the call site, it cannot be typed by
accident, and the destructive form is visibly different from the safe one in shell history.

The "no exceptions" is load-bearing rather than tidy: **these recipes call each other.** A wipe
recipe passes its own confirm token through to the backup recipe it refuses to proceed without.
Give the two different tokens and the inner call silently falls to its dry-run branch, exits 0,
and the wipe deletes data that was never backed up — a data-loss bug produced entirely by a
naming inconsistency.

<!-- rnd:binding command-list -->
*(List this repo's destructive recipes and their guards here — one line each: what it destroys,
what it backs up first, where it prints the restore point. If there are none, say so.)*
<!-- /rnd:binding -->

**4. Name the safety rail, not just the step.**
Every dangerous step carries the reason it is guarded — why this env var must be unset
afterwards, why this flag is needed, what breaks without it. **A step without its reason gets
"optimised" away by the next reader.**

**5. State the prerequisite state, not just the actions.**
What must be true before step 1: credentials present, tree clean, service reachable, device
authorised. A procedure that assumes a starting state it never names fails confusingly halfway
through.

**6. Secrets are never quoted, ever.**
A doc may name the *key* and the file it lives in. It never shows a value, and never shows a
command whose output would print one.
