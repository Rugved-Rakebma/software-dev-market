# Reporting Format

Standardized status report format for all code agents. Every agent that produces code or reviews code uses this format to communicate results to the main session.

## Status Report Template

```markdown
## Status: [DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT]

## Tasks Completed
- [x] Task 1: {description} — completed
- [x] Task 2: {description} — completed
- [ ] Task 3: {description} — {reason if incomplete}

## Files Changed
| File | Action | Lines |
|------|--------|-------|
| src/auth/login.ts | created | +120 |
| src/api/users.ts | modified | +45 -12 |
| src/types/auth.ts | created | +35 |

## Commits
- abc1234: feat(01-02): implement user auth flow
- def5678: test(01-02): add auth integration tests

## Test Results
- Unit tests: pass (12 passed, 0 failed)
- Integration tests: pass (4 passed, 0 failed)
- Type check: pass

## Concerns
- src/auth/token.ts:45 — Token refresh doesn't handle concurrent requests; race condition possible under load (BACKLOG CANDIDATE: PERF, medium)
- src/api/client.ts:23 — Error messages expose internal paths in development mode (BACKLOG CANDIDATE: SEC, low)

## Evidence
Every claim must cite file:line. No assertions without proof.
```

## Report Sections

### Status
One of the four escalation statuses. See `reference/escalation-protocol.md` for definitions.

### Tasks Completed
Checkbox list of all tasks from the plan. Use `[x]` for completed, `[ ]` for incomplete. Incomplete tasks must include a reason (blocked, skipped, deferred).

### Files Changed
Table of every file created, modified, or deleted. Include line counts (additions/removals) for quick scope assessment.

### Commits
List of commits created during execution. Each commit should follow the convention: `{type}({phase}-{plan}): {description}`.

Commit types:
- `feat`: New feature or capability
- `fix`: Bug fix
- `test`: Test additions or modifications
- `refactor`: Code restructuring without behavior change
- `chore`: Build, config, or tooling changes

### Test Results
Results of all test suites run. Include pass/fail counts. If tests weren't run (no test infrastructure, no relevant tests), state why.

### Concerns
Issues discovered during execution that are outside the current task scope. Each concern must include:
- File path and line number
- Description of the issue
- `BACKLOG CANDIDATE` tag with suggested category and priority (if applicable)

### Evidence
This section reinforces the core discipline: **every claim in the report must cite file:line**. If you say "authentication is implemented," point to the file and line where the auth check happens. If you say "tests pass," show the test command output. No assertions without proof.

## Review Report Template (for rnd-code-reviewer, rnd-code-spec-checker, rnd-code-analyst)

```markdown
## Verdict: [PASS | CONDITIONAL | FAIL]

## Summary
{2-3 sentence overview of findings}

## Blockers
- [severity] src/path/file.ts:line — What -> Why -> Suggestion

## Suggestions
- [severity] src/path/file.ts:line — What -> Why -> Suggestion

## Nits
- [severity] src/path/file.ts:line — What -> Why -> Suggestion

## Integration Map (rnd-code-reviewer only)
| Requirement | Integration Path | Status | Issue |
|-------------|-----------------|--------|-------|
| REQ-AUTH-01 | LoginForm -> /api/auth -> handler | WIRED | — |
| REQ-API-03 | UserList -> /api/users | PARTIALLY_WIRED | Missing pagination |

## Backlog Candidates
- {CATEGORY}-{priority}: src/path/file.ts:line — {description}

## Evidence
Every finding cites file:line. No assertions without proof.
```

## Rules

1. **No report without evidence.** If you can't cite a file and line, you can't make the claim.
2. **Concerns are not fixes.** The Concerns section reports issues — it does not fix them. Fixing issues outside scope is scope creep.
3. **BACKLOG CANDIDATE tags are structured.** Format: `(BACKLOG CANDIDATE: {CATEGORY}, {priority})` — e.g., `(BACKLOG CANDIDATE: BUG, high)`.
4. **Reports are self-contained.** The main session should be able to understand the report without reading the code. Include enough context in each finding.
5. **Be specific, not comprehensive.** Report what you actually found, not every possible thing that could go wrong. Quality over quantity.
