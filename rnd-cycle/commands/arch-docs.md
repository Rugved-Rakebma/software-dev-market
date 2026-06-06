---
description: Derive comprehensive arch docs from an existing codebase. Five phases: Prime → Plan (pause) → Investigate → Synthesize → Overview. Output to /docs/arch/.
argument-hint: [no arguments]
---

## Prerequisites

1. **Check `.rnd/` exists.** If not: "No R&D project found. Run `/rnd:init` first."
2. **Read `.rnd/state.md`** for project context.
3. **Ensure `.rnd/arch-docs/` exists.** Create if needed (`mkdir -p .rnd/arch-docs/investigations`).
4. **Ensure `docs/arch/` exists** at the project root. Create if needed (`mkdir -p docs/arch`).

## Skill Loading

Load `rnd-arch-docs` skill. The skill defines:
- `reference/prime-protocol.md` — what to read in Phase 0
- `reference/plan-format.md` — what `.rnd/arch-docs/plan.md` contains
- `reference/investigation-schema.md` — what investigator agents return
- `reference/principles.md` — arch doc dos and don'ts (no code, file:line refs, ASCII)
- `templates/domain.md` — per-domain doc shape
- `templates/system-overview.md` — overview shape

## Scope

This command operates on the **entire codebase**. It does not take arguments. It runs all five phases or pauses for user review after Phase 1.

The result is a multi-doc set at `/docs/arch/` — the maintained truth source about the codebase's architecture.

## Distinct from `/rnd:design`

| | `/rnd:design` | `/rnd:arch-docs` |
|---|---|---|
| Mode | Design-time (new effort) | Bootstrap (existing code) |
| Output | `.rnd/architecture/current.md` (single doc) | `/docs/arch/{N domain docs + overview}` |
| Source of truth | Spec + design intent | Code (cited file:line) |

They coexist. Use `/rnd:design` for new architecture work; use `/rnd:arch-docs` to document what's already built.

---

## Phase 0 — Prime

**Goal**: build a high-level mental model of the codebase. No pause. No todos yet.

Follow `reference/prime-protocol.md`. Read (in order):

1. **Project intent** — `README.md`, package manifest (`package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod`), any top-level `ABOUT.md` / `OVERVIEW.md`.
2. **Stack & runtime** — manifests for language and key deps; configs for build (`tsconfig`, `vite.config.*`, `Makefile`, `Dockerfile`); CI (`.github/workflows/`).
3. **Structure** — `ls` at root + one level into primary source dir.
4. **Entry points** — server start, CLI scripts, public API surface, test entry.
5. **Deep samples** — 1-2 directories that look central, 2-3 files each.

Time budget: **single-digit minutes of orchestrator time**. The deep dive is Phase 2, not Phase 0.

Write `.rnd/arch-docs/codebase-survey.md` following the schema in `reference/prime-protocol.md`.

---

## Phase 1 — Plan

**Goal**: derive the doc plan from the survey. Create todos. Pause for user review.

1. Read the survey just written.
2. Identify domains:
   - Cluster files/directories by responsibility
   - Each domain must trace back to **observable code structure** (a directory, a coherent group of files, a feature folder). No fabricated domains.
   - Target: 3-7 domains for most projects; fewer for small projects; more only with strong rationale.
3. For each domain, capture: name, purpose, code location, rationale, in scope, out of scope.
4. Decide what's **out of the doc set** (third-party code, generated code, non-arch surface like docs/scripts).
5. Write `.rnd/arch-docs/plan.md` following the schema in `reference/plan-format.md`.

**Create todos via TaskCreate** — one for each:
- `Investigate: {domain}` per domain
- `Write doc: {domain}` per domain
- `Write doc: system-overview` (singleton)

Optionally set dependencies via TaskUpdate `addBlockedBy`: each `Write doc: {domain}` blocked by `Investigate: {domain}`; `Write doc: system-overview` blocked by all per-domain `Write doc:` tasks.

**PAUSE**:

> Plan written to `.rnd/arch-docs/plan.md`. {N} domains proposed: {names}.
> {N} investigation + {N} write-doc + 1 overview todos created.
> Review the plan and confirm — edit `plan.md` to adjust, then say "go". Or tell me what to change.

Wait for explicit user confirmation before Phase 2.

---

## Phase 2 — Investigate

**Goal**: parallel evidence gathering, one investigator per domain.

For each domain in the confirmed plan, spawn `rnd-domain-investigator` via the Agent tool. **All spawns in parallel** (one message, multiple tool calls).

For each spawn:

- **description**: `Investigate: {domain}`
- **subagent_type**: `rnd-domain-investigator`
- **model**: opus
- **prompt** — include inline:
  - **`domain`** — the domain name
  - **`scope_hint`** — the plan's entry for this domain (code location, in/out scope, rationale)
  - **`codebase_root`** — absolute path of the repo
  - **`codebase_survey`** — full text of `.rnd/arch-docs/codebase-survey.md`
  - **`output_path`** — `.rnd/arch-docs/investigations/{domain}.md`
  - Reference to `skills/rnd-arch-docs/reference/investigation-schema.md` for the expected report shape

**Toggle todos**:
- Before spawning: TaskUpdate `Investigate: {domain}` → `in_progress`
- After return: TaskUpdate → `completed`

**Status report handling**:
- **DONE** → continue
- **DONE_LOW_CONFIDENCE** → note for Phase 3 (the resulting doc should be marked tentative)
- **BLOCKED** → surface to user, pause execution

### Wave Gate

All investigations must complete before Phase 3 begins.

---

## Phase 3 — Synthesize

**Goal**: write per-domain docs using the template + investigation evidence.

**Sequential**, one doc at a time (the orchestrator authors directly — no agent spawn).

For each domain (in plan order):

1. TaskUpdate `Write doc: {domain}` → `in_progress`
2. Read `.rnd/arch-docs/investigations/{domain}.md`
3. Read `templates/domain.md` from the skill
4. Write `/docs/arch/{domain}.md`:
   - Follow the template structure
   - Pull evidence from the investigation (Key Files, Flows, Boundaries, Contracts, Notable Decisions, Open Questions)
   - **Apply principles** (`reference/principles.md`): no code blocks, file:line for every concrete claim, ASCII diagrams encouraged, tables over prose, mark uncertainties
   - Skip template sections that have nothing meaningful to say
   - Length proportional to domain size (50-300 lines)
   - If investigation was `DONE_LOW_CONFIDENCE`, add `(uncertain)` markers liberally
5. TaskUpdate → `completed`

---

## Phase 4 — System Overview

**Goal**: write `/docs/arch/system-overview.md` last, after all domain docs exist.

1. TaskUpdate `Write doc: system-overview` → `in_progress`
2. Read all `/docs/arch/{domain}.md` files written in Phase 3
3. Read `templates/system-overview.md` from the skill
4. Write `/docs/arch/system-overview.md`:
   - Stack table (from survey)
   - Domains table (one row per domain, linking to its doc)
   - **High-Level Shape** ASCII diagram — show primary inter-domain connections only
   - Entry Points table (from survey, refined by what investigations surfaced)
   - Cross-Cutting Concerns (logging, errors, config, observability) — 1-3 lines each, with file:line refs
   - Build & Deploy — brief, link to runbooks
5. TaskUpdate → `completed`

The overview ties the doc set together. It's written last because it depends on every per-domain doc being honest first.

---

## After All Phases

1. **Summary to user**:

   > Arch docs generated:
   > - `/docs/arch/system-overview.md`
   > - `/docs/arch/{domain}.md` × {N}
   >
   > Working state in `.rnd/arch-docs/`.
   >
   > Suggested next: spot-check 2-3 file:line citations in a domain doc, then commit `/docs/arch/`.

2. **Flag low-confidence investigations** if any returned `DONE_LOW_CONFIDENCE`:
   > Note: investigation of {domain} returned low confidence — the doc is marked tentative. Re-run after the area is better understood.

3. **Backlog candidates**: if any investigation surfaced gaps that look like real architectural concerns (not just doc gaps), offer:
   > {N} architectural concerns surfaced during investigation. Run `/rnd:backlog add` to capture them.

---

## Persistence

Update `.rnd/state.md`:
- Add entry to Recent Activity: `{today's date}: Arch docs generated via /rnd:arch-docs — {N} domains → /docs/arch/`
- Follow compression protocol: keep under 120 lines, compress oldest Recent Activity entries into History phase summaries when exceeding 15 entries. Never delete entries.

---

## Re-running

This command is idempotent — re-running overwrites:
- `.rnd/arch-docs/codebase-survey.md`
- `.rnd/arch-docs/plan.md`
- `.rnd/arch-docs/investigations/*.md`
- `/docs/arch/*.md`

It does not preserve manual edits. If you've hand-edited a doc in `/docs/arch/`, commit it first or copy it aside before re-running.

Resume mid-run is **not supported in v1** — re-run from Phase 0.

## v2 (deferred)

- Maintenance loop — diff-driven update after `/rnd:c-build` instead of full re-derive
- Adversarial verification (analog of `rnd-code-spec-checker`)
- Stale detection
- Resume mid-run
- Reconciliation with `/rnd:design` outputs

None of these require structural change here — v1 is forward-compatible.
