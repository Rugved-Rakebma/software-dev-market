---
description: Run one build end to end via a dev-team — manager investigates, composes coder/reviewer/qa, runs the fix loop, reports one settled outcome
argument-hint: <backlog-id | design-record-path | inline description>
---

## Process

Build: **$ARGUMENTS**

1. **Resolve the intent.**
   - Looks like a backlog id (`BUG-001`)? → `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rnd.py fm --where id=<ID>` — read the matched file in full.
   - A path under `docs/design/`? → read it in full.
   - Otherwise it is an inline ask.

   **Clarify gate:** if the intent is ambiguous on any axis that would change what gets built (scope, data model, UX, non-functionals, integrations, edge cases, constraints, terminology, completion signals), ask the user now via AskUserQuestion — max 5 questions, ranked by impact × uncertainty, concrete options with your recommendation first. The dev-manager runs the same scan and will escalate what you miss; answered here it costs one message, answered mid-run it costs a stalled coder.

2. **Spawn the dev-manager** — Agent tool, `subagent_type: "dev-manager"`, a descriptive `name` (e.g. `build-BUG-001`), `run_in_background: true`. Its prompt gets the FULL bundle inline:
   - the intent artifact's complete text (or the inline ask)
   - acceptance criteria as binary checks (derive them if the artifact lacks them — state your derivation)
   - constraints you know from this session (branch, style rules, files to avoid)
   - the plugin scripts path: `${CLAUDE_PLUGIN_ROOT}/scripts/rnd.py`

3. **Keep working.** The run is autonomous below you. When the manager's report or an escalation arrives, relay it to the user compressed.

4. **On escalation** (disputed BLOCKER, budget exhausted, BLOCKED, NEEDS_CONTEXT, scope explosion): present both positions in point form, get the user's ruling, SendMessage it back to the manager by name.

5. **On completion:** relay outcome · files · verdicts · QA results. Offer the report's backlog candidates: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rnd.py backlog new <kind> "<title>" --files ...` — one per candidate the user accepts. If the intent was a backlog item and the run is DONE, offer `backlog close <ID> --resolution "<summary>"`.

## Notes

- Master context is the scarce resource: never paste agent transcripts; summaries only.
- If the user already approved a plan in this session, pass it in the bundle — the manager hands it to the coder instead of having the coder self-plan.
- The manager never auto-files backlog items or closes anything — the user is the final triage step.
- Dispatch seam: the manager is spawned via the Agent tool today; an alternate backend (e.g. herdr panes) may replace step 2 without changing anything else.
