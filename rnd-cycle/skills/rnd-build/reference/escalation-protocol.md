# Escalation Protocol

Defines when agents should stop vs. continue, and how to communicate status to the main session.

## Status Definitions

### DONE
All tasks implemented, tests pass, commits created. The plan is fully executed with no open concerns.

**When to use**: Every task in the plan has been implemented, every verification check passes, and you have no doubts about correctness.

### DONE_WITH_ADVISORIES
Completed all tasks. The agent surfaced advisories — observations, concerns, or BACKLOG CANDIDATE items found during execution. **Advisories do NOT block execution** — they are reported for triage and routed to the backlog by `/rnd:c-run` Stage 8.

**When to use**: You finished the work, but you noticed things worth reporting — a pattern doesn't quite match the architecture, a test passes but seems fragile, adjacent code has debt, you made a judgment call worth surfacing.

**What to include**: Specific advisories, each with:
- File path and line number
- What the advisory is
- Why it matters
- BACKLOG CANDIDATE tag with category and priority (if applicable)

### BLOCKED
Cannot proceed. Missing dependency, architectural ambiguity, or failing precondition. Describes what's blocking and what was attempted.

**When to use**: You cannot complete the plan without external input. This is not "I'm unsure" — this is "I literally cannot proceed."

**Blocking conditions**:
- A dependency from a prior wave doesn't exist or doesn't match the expected interface
- The plan describes a pattern that contradicts the codebase's existing architecture
- A test environment or external service required by the plan is unavailable
- The plan's instructions are ambiguous enough that two valid interpretations would produce incompatible code

**What to include**:
- What is blocking (specific file, dependency, or instruction)
- What you attempted to resolve it
- What information or action would unblock you

### NEEDS_CONTEXT
Missing information that isn't a hard blocker but risks quality. Describes what information would help.

**When to use**: You can proceed, but proceeding without more context risks producing code that will need significant revision. The cost of asking is lower than the cost of guessing wrong.

**Examples**:
- Plan says "integrate with the payment service" but you can't find the payment service interface
- Multiple valid approaches exist and the plan doesn't specify which
- You're unsure whether an existing utility does what you need or should be replaced

## Retry Limits

- **Max 2 re-attempts** per review gate failure — but only on BLOCKERS (a `FAIL` verdict means blockers present)
- `CONDITIONAL` verdict (advisories only, no blockers) does NOT trigger a retry — advisories route to backlog
- After 2 failed re-attempts on blockers, **escalate to user** with:
  - The original plan
  - What was implemented
  - The reviewer's feedback (both rounds)
  - What the coder tried differently each time
  - Why it's still not passing

## Escalation Triggers

Stop and report BLOCKED or NEEDS_CONTEXT when you encounter:

1. **Architectural decisions with multiple valid approaches** — Don't guess. The wrong choice creates work to undo.

2. **Code beyond provided context** — If the plan references files or patterns you can't find, don't invent them. Report what's missing.

3. **Uncertainty about correctness** — If you're not confident your implementation is correct but can't prove it either way, say so. "I think this works but I'm not sure about X" is more valuable than shipping uncertain code silently.

4. **Restructuring not anticipated by the plan** — If implementing the plan correctly requires changes to files or patterns not mentioned in the plan, stop. The plan may need revision, or there may be context you're missing.

5. **Test failures you can't explain** — If tests fail and you can't determine why after 2 attempts, report BLOCKED. Don't loop indefinitely.

## Backlog Discipline

During execution, agents will discover issues outside their current task scope:
- Bugs in adjacent code
- Technical debt they notice while reading context
- Missing edge case handling
- Security concerns in existing code

**Rule**: Do NOT fix these. Report them as `BACKLOG CANDIDATE` in the Advisories section of your status report. Include enough detail for a backlog item:
- Category suggestion (BUG/DEBT/UX/PERF/SEC/FEAT)
- Priority suggestion (critical/high/medium/low)
- File path and line number
- Description of the issue
- Why it matters

The main session will create formal backlog items from these candidates.
