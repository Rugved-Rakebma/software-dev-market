# Phase 1: Plan Format

What main Claude writes to `.rnd/arch-docs/plan.md` after Phase 0, and how the domain list is justified.

The plan is the **visible interface for user review**. Before any parallel investigation fires, the user reads this and either confirms or edits. The plan is also the source of truth for the todos (2 per domain + 1 overview singleton).

## Required Sections

### Codebase Summary (from Prime)
One paragraph distilling the survey: what this project is, the stack, the rough shape. Not a copy of the survey — a tight summary.

### Domain List
For each domain proposed:

| Field | What it captures |
|---|---|
| **Name** | Short, lowercase-kebab (e.g. `auth`, `user-onboarding`, `agent-convo-flow`) |
| **Purpose** | One line: what this domain owns |
| **Code location** | The primary directories/files. Must point to real paths from the survey. |
| **Rationale** | Why this is a domain (cleaner boundary, common owners, distinct flows) |
| **In scope** | What's covered |
| **Out of scope** | What's *not* covered here (with pointer to the domain that does) |

### Scope: What's Out
A short list of areas the doc set explicitly **doesn't** cover. Examples:
- `node_modules/` (third-party code)
- `docs/`, `scripts/` (not arch surface)
- Tests (covered inline in domain docs as flows where relevant)
- Vendored or generated code

Calling this out prevents scope creep and makes the plan honest.

### Doc Set
The expected output:
- `/docs/arch/{domain-1}.md`
- `/docs/arch/{domain-2}.md`
- ...
- `/docs/arch/system-overview.md`

### Todos
List the todos that will be created (mirrors what TaskCreate produces):
- `Investigate: {domain}` x N
- `Write doc: {domain}` x N
- `Write doc: system-overview` (singleton; blocked by all per-domain writes)

This makes the user-facing pipeline state explicit *before* execution.

## Required Shape

```markdown
---
generated: {ISO timestamp}
generator: /rnd:arch-docs (Phase 1)
status: pending-review
---

# Arch Docs Plan

## Codebase Summary
{One paragraph from Prime survey}

## Domains

### 1. {domain-name}
- **Purpose**: {one line}
- **Code location**: {paths}
- **Rationale**: {why this is a domain}
- **In scope**: {what it covers}
- **Out of scope**: {explicit exclusions, with pointers}

### 2. {domain-name}
... (repeat)

## Scope: Out of Doc Set
- {area}: {why excluded}

## Doc Set
- `/docs/arch/{domain-1}.md`
- `/docs/arch/{domain-2}.md`
- `/docs/arch/system-overview.md`

## Todos
- [ ] Investigate: {domain-1}
- [ ] Investigate: {domain-2}
- [ ] Write doc: {domain-1}
- [ ] Write doc: {domain-2}
- [ ] Write doc: system-overview
```

## How domains are justified

A domain must trace back to **observable code structure** — not vibes, not categories from a textbook.

✅ Good rationale:
- "`auth/` directory contains middleware + token resolution + session storage; all auth concerns are physically colocated"
- "Cross-cutting `notifications` show up wherever events fire; lives in `lib/notifications/` and is consumed by 4+ other areas — own domain"

❌ Bad rationale:
- "Every system needs an auth domain" (not derived from this codebase)
- "Best practices say split frontend and backend" (template thinking)

If you can't point to code that justifies the cut, drop the domain.

## How many domains?

For most projects: **3 to 7 domains**.
- <3: the cut is too coarse; readers will be lost in a single 500-line doc
- \>7: the cut is too fine; readers will lose the shape

Monorepos may legitimately have more (one set of domains per package). Use judgement; explain in rationale.

## Edge cases

### "This whole thing is one domain"
For very small projects (a single-purpose CLI, a 500-line script), the right answer might be **only `system-overview.md`** and no per-domain docs. The plan should say so explicitly. Don't fabricate domains to fill a template.

### "I'm not sure if X and Y are 1 or 2 domains"
Plan them as 1, with a note: "may split if investigation reveals distinct flows". Then the investigation answers. Splitting after evidence is cheaper than fabricating distinction up front.

### Cross-cutting concerns
Things like logging, error handling, config — these typically belong in `system-overview.md` under "Cross-Cutting Concerns", not as their own domain. Unless they're substantial (e.g. a full observability subsystem), keep them cross-cutting.

## Pause behavior

After writing the plan and creating todos, the orchestrator **pauses** with a message like:

> Plan written to `.rnd/arch-docs/plan.md`. {N} domains proposed: {names}. Todos created.
> Review and confirm — edit `plan.md` to adjust, then say "go" to start investigation. Or tell me what to change.

The user can:
- Confirm → orchestrator proceeds to Phase 2
- Edit the plan file → orchestrator re-reads on next prompt
- Tell the orchestrator what to change → orchestrator edits the plan

No investigation starts until the user confirms.
