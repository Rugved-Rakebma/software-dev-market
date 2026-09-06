---
description: Explore a change in conversation, attack it, and record it as a dated design record ONLY if a real alternative was rejected
argument-hint: <what to design>
---

## Process

Design: **$ARGUMENTS**

1. **Explore in conversation.** Read the relevant code (or spawn an Explore agent for breadth), lay out the options with real tradeoffs. This is a discussion with the user, not artifact production.

2. **Attack the leading option before endorsing it.** Argue against it seriously: what breaks, what it costs later, what the rejected option did better. Present the attack to the user — they rule.

3. **Apply the bar for a record:** *did this decision close off a viable alternative?* 
   - **No** (obvious choice, no real fork) → no artifact. Say so: "no record — nothing was rejected." The conversation was the design.
   - **Yes** → `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rnd.py record new "<title>" --kind decision` and fill the body: the decision · **the alternative that was rejected and why** · the constraint that decided it — stated as a live constraint, not a story. Add `refs:` anchors (`path:Symbol`) for the code it governs.

4. **A `design` record** (kind `design`, same command without `--kind decision`) is for a worked design that guides an upcoming build — bigger than a decision, still dated, still frozen once executed. Use sparingly; a plan that will be executed this week belongs in plan mode, not on disk.

## Notes

- Records land in `docs/design/` **live**, at the top level. They freeze later by `git mv` into `v#-{slug}/` — never write into a frozen dir directly.
- Most design work produces ZERO records. The record is for the reasoning git can't hold — a diff shows what you chose, never what you turned down.
- Never write a record that restates code, the living docs, or the backlog.
