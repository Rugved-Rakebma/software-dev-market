# Planning Methodology

Reference material for the rnd-planner agent. Covers how to decompose project phases into executable build plans that prime rnd-coder agents.

## Plans Are Prompts

Plans are not documentation for humans. They are prompts consumed by rnd-coder agents running in fresh context windows. This drives every planning decision:

| Human Documentation | Plan-as-Prompt |
|---|---|
| Assumes reader has project context | Coder receives plan + arch slice + spec slice in priming prompt |
| Can be vague ("implement authentication") | Must be precise ("create JWT middleware validating tokens from Authorization header") |
| Organized for reference/scanning | Organized for sequential execution |
| Restates context inline | Points at the canonical source (arch §X, spec REQ-Y) |

## Plan = Task / Arch = Shape / Spec = Reqs

Three artifacts, three roles. Never duplicate content across them:

- **Plan** — the *task*: what to build, what files to touch, how to verify it's done
- **Arch** (`.rnd/architecture/current.md`) — the *shape*: contracts at the seams, mechanisms, data flow, component boundaries
- **Spec** (`.rnd/spec/spec.md`) — the *requirements*: REQ-IDs, acceptance criteria, success metrics

When the coder is spawned (per `commands/c-build.md` and `commands/c-run.md`), it receives all three: the plan text, the arch sections referenced by the plan's "Wires to" section, and the spec REQ rows for the IDs in the plan's `requirements` frontmatter. Plans do not re-embed contracts or requirements — they point.

## No Code in Plans

Plans describe *what* to build and *what done looks like*. They never include:

- Class bodies, function signatures with type annotations/defaults, decorators, async function bodies
- Type definitions, Pydantic schemas, API contracts in code form
- Bash one-liners as task content (commands belong in `Done:` verification lines, not task bodies)

If the contract matters, it lives in the arch doc. The plan points at it.

❌ Don't put this in a plan task:
```python
async def retrieve_sources(query: str, depth: Literal["shallow","balanced","deep"]) -> SourceBundle: ...
```

✅ Do put this in a plan task:
> **Build:** Implement `retrieve_sources` per arch §5.1. Three async LLM selection calls (books, chapters, lectures) per arch §2.3; run books and lectures in parallel, chapters sequentially after book selection. Return a `SourceBundle` per arch §4.
> **Done:** `python -c "import asyncio; from agent_mani.vault import retrieve_sources; asyncio.run(retrieve_sources('test'))"` returns a populated SourceBundle within ~5s.

## Plan Anatomy

### Frontmatter (5 flat fields)

```yaml
---
id: NN-short-name
wave: N
depends_on: [NN-other-id]
files: [src/path/to/file.ts, ...]
requirements: [REQ-XXX-NN]
---
```

### Body

- `# Plan NN — Name` (H1)
- `## Goal` — one paragraph: what + why, pointing at arch + spec
- `## Wires to` — bullet list of arch sections and spec REQs the plan touches
- `## Tasks` — H3 task sections (2-3 per plan), each with `**Build:**` and `**Done:**`

### Task Anatomy

Each task has exactly two fields:

**Build:** What to build, in behavior terms. Reference arch sections for shape. Reference spec REQs for acceptance. Never include code or signatures.
- What behavior to implement
- Which patterns to follow (point at arch sections)
- Which existing utilities/libraries to use (by name, not by code)

**Done:** Binary acceptance — unambiguous pass/fail. Often IS the verify command:
- `just typecheck` exits 0
- `python -c "from agent_mani.vault import retrieve_sources"` succeeds
- `pytest tests/test_vault_retrieve.py` passes
- File `src/middleware/auth.ts` exports `authMiddleware`

If Done can't be expressed as a command, use a binary statement:
- "All existing tests pass and 3 new tests added covering REQ-AUTH-01..03"
- "Component renders without errors at the URL shown in spec REQ-UI-02"

## Scope Estimation

Target ~50% context window utilization per plan (~100K tokens of work).

### Context Budget
| Activity | Tokens |
|---|---|
| Plan + arch slice + spec slice (priming) | ~20K |
| File reads (existing code) | ~20K |
| Implementation (code written) | ~30K |
| Verification + debugging | ~20K |
| Summary creation | ~5K |
| Safety buffer | ~5K |
| **Total** | **~100K** |

### Sizing Heuristic
- 2-3 tasks per plan
- Each task: 15-60 minutes of estimated implementation work
- If a task would take >60 minutes, split it into subtasks across plans

Quality degrades sharply above 50% context. Keep plans lean.

## Dependency Graph + Waves

### Building the Graph
1. List all plans for the phase
2. For each plan, identify what it **produces** (exports, types, APIs, DB tables)
3. For each plan, identify what it **consumes** (imports, API calls, type references)
4. Draw edges: if Plan B consumes what Plan A produces, B depends on A

### Wave Assignment
1. Plans with no dependencies → Wave 1
2. Plans whose dependencies are all in Wave 1 → Wave 2
3. Continue until all plans are assigned

Plans in the same wave run in parallel; waves run sequentially.

### Rules
- No circular dependencies. If found, extract shared dep into its own plan, merge cyclic plans, or introduce an interface plan.
- All `depends_on` references must point to existing plan IDs.
- Minimize wave count (fewer waves = faster execution).

## Vertical Slices Over Horizontal Layers

Prefer plans that deliver a complete vertical slice (DB + API + UI for one feature) over horizontal layers (all DB, then all API, then all UI). Vertical slices are independently testable and produce working increments.

When horizontal is acceptable: shared infrastructure (database migrations, config setup) — Wave 1 horizontal plan, then vertical slices in Wave 2+.

## File Ownership

No two plans in the same wave may modify the same file. Hard constraint for parallel execution.

### Strategies for Shared Files
- **Defer to a wiring plan** — Wave N+1 handles shared files (index, routes, config) after Wave N plans complete
- **Single owner per file** — one plan owns the file; others document what they need added (acted on in the wiring plan)
- **Append-only patterns** — each plan adds to the file without modifying existing content (rare; usually creates merge headaches)

The planner builds a file ownership map during decomposition and assigns waves accordingly.

## Interface-First Within a Plan

When the contract is NOT already in the arch doc, order tasks so contracts come first:

1. **Task 1**: Define types/interfaces
2. **Task 2**: Implement against the contracts
3. **Task 3**: Wire up and verify integration

When the contract IS in the arch doc (the common case), skip Task 1 — the coder reads the arch slice instead.
