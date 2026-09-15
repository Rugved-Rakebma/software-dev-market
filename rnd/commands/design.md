---
description: Explore and attack a design in conversation — a dated record only for design work that guides an upcoming build
argument-hint: <what to design>
---

## Process

Design: **$ARGUMENTS**

1. **Explore in conversation.** Read the relevant code (or spawn an Explore agent for breadth), lay out the options with real tradeoffs. This is a discussion with the user, not artifact production.

2. **Attack the leading option before endorsing it.** Argue against it seriously: what breaks, what it costs later, what the rejected option did better. Present the attack to the user — they rule.

3. **Most design work produces ZERO artifacts.** The conversation was the design; the code will be the record. Write a record only when the design is **bigger than the session** — a worked design that must guide an upcoming build across days or sessions: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rnd.py record new "<title>"`, then fill the body with the target shape, boundaries, and constraints.

4. **A record is design, never history.** No decision log, no alternatives narrative, no evolution notes — git holds how thinking changed. A constraint worth surviving into the built system gets stated later in the living docs as a live rule (present tense, no dates), where the code can falsify it.

## Notes

- Records land in `docs/design/` **live**, at the top level. They freeze later by `git mv` into `v#-{slug}/` — never write into a frozen dir directly.
- A plan that will be executed this week belongs in plan mode, not on disk.
- Never write a record that restates code, the living docs, or the backlog.
