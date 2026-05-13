# Handoff Contracts

Defines the input/output contract for every agent-to-agent handoff in the build and verify flows. Each contract specifies exactly what the main session sends to the agent and what it expects back.

## Build Flow Contracts

### MAIN SESSION -> rnd-coder

**Input:** The coder receives three blocks inline in its spawn prompt. The coder NEVER reads `.rnd/` files directly.

```yaml
plan_text: |
  Full plan text — the *task* (Goal / Wires to / Tasks with Build + Done per task).
arch_slices: |
  Sections of .rnd/architecture/current.md referenced by the plan's "Wires to" section.
  Carries the *shape*: contracts, mechanisms, data flow, component boundaries.
  If plan has no "Wires to" section, falls back to full arch.
spec_req_rows: |
  Spec rows for the REQ-IDs listed in the plan's `requirements` frontmatter field.
  Carries the *requirements*: REQ descriptions and acceptance criteria from .rnd/spec/spec.md.
project_context: |
  Project state from .rnd/state.md and locked decisions from .rnd/decisions/.
prior_wave_summaries: |
  Status reports from previously completed waves.
```

**Output:**
```yaml
status: DONE | DONE_WITH_ADVISORIES | BLOCKED | NEEDS_CONTEXT
tasks_completed:
  - task_name: "description"
    status: completed | partial | skipped
files_changed:
  - path: "src/path/to/file.ts"
    action: created | modified | deleted
    lines: "+120 -5"
commits:
  - hash: "abc1234"
    message: "feat(01-02): implement user auth flow"
advisories:
  - "src/auth/token.ts:45 — token refresh not handling 401 edge case (BACKLOG CANDIDATE: BUG, medium)"
```

### MAIN SESSION -> code-simplifier

**Input:**
```yaml
files_changed:
  - List of file paths from the coder's output
  # code-simplifier focuses on recently modified files
```

**Output:**
```yaml
files_simplified:
  - path: "src/path/to/file.ts"
changes_made:
  - "Extracted duplicated validation into shared helper"
  - "Simplified nested conditionals in auth flow"
```

## Verify Flow Contracts

### MAIN SESSION -> rnd-code-spec-checker

**Input:**
```yaml
spec_requirements: |
  REQ-IDs and their descriptions from .rnd/spec/spec.md,
  filtered to requirements relevant to the scope being verified.
files_to_check:
  - List of files changed during the build
coder_report: |
  The coder's status report — provided for context only.
  The spec-checker MUST NOT trust this report. It reads
  the actual code independently to verify.
```

**Output:**
```yaml
verdict: PASS | FAIL
findings:
  - file: "src/auth/login.ts"
    line: 45
    requirement_id: "REQ-AUTH-01"
    issue: "Login handler returns 200 on invalid credentials instead of 401"
    severity: blocker
  - file: "src/api/users.ts"
    line: 12
    requirement_id: "REQ-API-03"
    issue: "Pagination not implemented — spec requires cursor-based pagination (BACKLOG CANDIDATE)"
    severity: suggestion
```

### MAIN SESSION -> rnd-code-reviewer

**Input:**
```yaml
files_to_review:
  - List of files changed during the build
architecture_context: |
  Relevant architecture from .rnd/architecture/current.md —
  component boundaries, patterns, naming conventions.
```

**Output:**
```yaml
verdict: PASS | CONDITIONAL | FAIL
# PASS = no findings of any kind
# CONDITIONAL = advisories only, no blockers — does NOT trigger fix-up
# FAIL = blockers present — gates fix-up
blockers:
  - file: "src/api/client.ts"
    line: 23
    issue: "SQL injection via string concatenation in query builder"
    severity: blocker
advisories:
  - file: "src/components/Dashboard.tsx"
    line: 67
    issue: "Missing loading state — should show skeleton while fetching (BACKLOG CANDIDATE: UX, low)"
    severity: advisory
integration_map:
  - requirement: "REQ-AUTH-01"
    path: "LoginForm -> /api/auth/login -> authHandler -> userService"
    status: WIRED
  - requirement: "REQ-API-03"
    path: "UserList -> /api/users -> (no pagination param)"
    status: PARTIALLY_WIRED
```

### MAIN SESSION -> rnd-code-analyst

**Input:**
```yaml
scope: |
  Description of what to analyze — specific files, directories,
  or the entire codebase.
mode: audit | security | verification
  # audit: 4-track codebase analysis
  # security: STRIDE + OWASP scanning
  # verification: 4-level goal-backward verification
```

**Output:**
```yaml
findings:
  - file: "src/auth/middleware.ts"
    line: 12
    severity: high
    category: security
    evidence: "Auth middleware skips token validation when X-Debug header is present"
  - file: "src/db/queries.ts"
    line: 45
    severity: medium
    category: debt
    evidence: "Raw SQL queries duplicated across 4 files — should use query builder (BACKLOG CANDIDATE)"
summary: |
  Concise summary of overall findings, risk level,
  and recommended actions.
```

## Contract Rules

1. **Inputs are provided by the main session.** Agents do not read `.rnd/` files directly unless explicitly told to in their spawn prompt.
2. **Outputs follow the standardized reporting format** from `reference/reporting-format.md`.
3. **Every finding must cite file:line.** No assertions without proof.
4. **BACKLOG CANDIDATE items** are clearly marked in the advisories/findings sections for the main session to collect.
5. **Status values are from the escalation protocol** — see `reference/escalation-protocol.md`.
6. **BLOCKER vs ADVISORY routing** — blockers gate fix-up loops; advisories route to backlog. Verifier verdicts: `FAIL` = blockers present, `CONDITIONAL` = advisories only, `PASS` = clean.
