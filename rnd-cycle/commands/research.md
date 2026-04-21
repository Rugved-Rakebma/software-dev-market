---
description: Deep landscape research with parallel retrieval, source scoring, and citation-backed reports
argument-hint: [research topic]
---

## Prerequisites

1. **Check `.rnd/` exists.** If not: "No R&D project found. Run `/rnd:init` first."
2. **Read `.rnd/state.md`** for project context. Avoid re-researching topics already decided unless the user explicitly asks.

## Research Topic

**$ARGUMENTS**

## Depth Mode

Determine depth from `$ARGUMENTS` or ask the user:
- **Quick**: 5-10 sources, surface-level comparison (~10 min)
- **Standard** (default): 10-20 sources, balanced analysis with trade-offs (~20 min)
- **Deep**: 20-40 sources, comprehensive with benchmarks and case studies (~40 min)
- **UltraDeep**: 40+ sources, exhaustive with academic sources (~60+ min)

## Execution

Spawn **rnd-researcher** via the Agent tool:
- **description**: "Research: {topic summary}"
- **model**: opus
- **prompt**: Include:
  - The research topic from `$ARGUMENTS`
  - The depth mode
  - Project context from `.rnd/state.md` (what the project is about, so research is relevant)
  - Any existing research in `.rnd/research/` to avoid duplication
  - Instruction to save reports to `~/Documents/{Topic}_Research_{YYYYMMDD}/` and copy summary to `.rnd/research/`

## After Completion

When the researcher returns:
1. Summarize key findings for the user
2. Highlight any findings that affect existing decisions or spec requirements
3. Suggest next steps: `/rnd:decide` for technology decisions, or update spec if new requirements emerged

## Persistence

Update `.rnd/state.md`:
- Add entry to Recent Activity: `{today's date}: Research completed — {topic} → .rnd/research/{filename}`
- Follow compression protocol: keep under 120 lines, compress oldest Recent Activity entries into History phase summaries when exceeding 15 entries. Never delete entries.
