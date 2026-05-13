---
phase: NN-name
plan: NN
status: completed | partial | blocked
key_files:
  - src/path/modified.ts
  - src/path/created.ts
decisions:
  - "Decision made during execution with rationale"
deviations:
  - rule: 1
    description: "What deviated and why"
metrics:
  tasks_completed: N/N
  commits: N
  duration_minutes: N
---

## Plan NN: [Plan Name] — Execution Summary

**One-liner:** [What was accomplished in one sentence]

### Deviations
[List any deviations from the plan, which deviation rule was applied, and rationale]

### Known Stubs
[Any placeholder implementations left behind, with TODO markers]

### Advisories
[Findings flagged by the coder during execution — file:line, description, BACKLOG CANDIDATE tags. Observations, not blockers. Routed to backlog in Stage 8 of /rnd:c-run.]

### Self-Check
- [ ] All files in key_files exist
- [ ] All commits referenced are valid
- [ ] All tasks marked done meet acceptance criteria
