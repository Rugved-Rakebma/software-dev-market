---
description: Adversarial review of the current diff or branch — no team, one reviewer, BLOCKER/ADVISORY verdict
argument-hint: [branch | path | blank = working tree diff]
---

## Process

Verify: **$ARGUMENTS**

1. **Establish the diff surface.** Blank → `git status --short` + `git diff --stat` for the working tree. A branch → `git diff <default-branch>...<branch> --stat`. A path → that path. Capture the file list.

2. **Write a scope statement** for the reviewer: what this change appears to be (from commits/diff), and any acceptance criteria the user states. If the user gave none, say so — the reviewer judges correctness and integration on the code alone.

3. **Spawn `code-reviewer`** (Agent tool, background) with scope statement + file list + how to reproduce the diff. Never pre-chew findings for it.

4. **Relay the verdict** compressed: `BLOCKERS: n / ADVISORIES: n`, each finding one line with its `path:Symbol` anchor.

5. **Offer routing:** each ADVISORY → `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rnd.py backlog new <kind> "<title>" --files ...` on the user's accept. BLOCKERs → offer `/rnd:build` to fix, or hand the list to the user.

## Notes

- This is the standalone half of the dev-team loop — review without build. The full loop (fix rounds, budget, QA) lives in `/rnd:build`.
- One reviewer, fresh context, reads code itself. Its verdict is evidence-based; do not soften it in relay.
