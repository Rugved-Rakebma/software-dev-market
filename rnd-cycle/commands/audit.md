---
description: Deep analysis of codebases, spec docs, PRDs, architecture docs, or proposals
argument-hint: [target to audit — codebase path or document]
---

## Prerequisites

1. **Check `.rnd/` exists.** If not: "No R&D project found. Run `/rnd:init` first."
2. **Read `.rnd/state.md`** for project context.

## Target

**$ARGUMENTS**

## Route by Target Type

Determine whether the target is a document or code:

### Document Target
If the target is a spec, proposal, PRD, architecture document, or other written artifact:

Spawn **rnd-analyst** via the Agent tool:
- **description**: "Document audit: {target name}"
- **model**: opus
- **prompt**: Include:
  - The document content (inline or file path)
  - Project context from `.rnd/state.md`
  - Related `.rnd/` artifacts for cross-reference
  - Mode: document-audit
  - Reference to `skills/rnd-analyst/reference/audit-methodology.md` and `skills/rnd-analyst/templates/audit-document.md`

### Code Target
If the target is a codebase path or directory:

Spawn **rnd-code-analyst** via the Agent tool. For large codebases, spawn up to 4 parallel instances with focused scopes:

**Single instance (small/medium codebase):**
- **description**: "Codebase audit: {path}"
- **model**: opus
- **prompt**: Include scope, mode: audit, all reference docs from `skills/rnd-analyst/`

**Parallel instances (large codebase):**
1. `rnd-code-analyst` — focus: tech (tech stack analysis)
2. `rnd-code-analyst` — focus: arch (architecture analysis)
3. `rnd-code-analyst` — focus: quality (conventions and patterns)
4. `rnd-code-analyst` — focus: concerns (tech debt, security, performance)

Each receives the same codebase path but a focused scope directive.

## After Completion

Present findings to the user. Aggregate results if multiple parallel instances were used.

Save results to `.rnd/audit/`:
- Document audit: `.rnd/audit/{date}-{target-slug}-document.md`
- Codebase audit: `.rnd/audit/{date}-{target-slug}-codebase.md` (or multiple files if parallel)

## Persistence

Update `.rnd/state.md`:
- Add entry to Recent Activity: `{today's date}: Audited {target} via /rnd:audit → .rnd/audit/{filename}`
- Follow compression protocol: keep under 120 lines, compress oldest Recent Activity entries into History phase summaries when exceeding 15 entries. Never delete entries.
