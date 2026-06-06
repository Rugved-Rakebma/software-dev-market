# Arch Doc Principles

The dos and don'ts that make an arch doc valuable to its readers (Claude in future sessions, humans onboarding, reviewers). These apply to every doc under `/docs/arch/`.

## What an arch doc is for

It answers: **"Where does new work fit in this system?"** A reader should be able to:
- Locate the right domain for a change
- Understand the contracts that change has to honor
- See the flows the change participates in
- Spot the decisions that shape what's allowed

It does **not** answer: "How does function X work?" That's the code's job.

## Do

### Cite file:line for every concrete claim
```
The auth middleware verifies tokens before any handler runs (src/auth/middleware.ts:42).
```
Concrete, navigable, evidence-rich. Readers can verify. Future maintainers can locate.

### Use ASCII diagrams for shape and flow
Diagrams force clarity about structure and survive any renderer. Use them for:
- Component relationships (boxes + arrows)
- Request/event flow (sequence)
- Domain boundaries (zones)

### Use tables for structured data
Contracts, file lists, decisions, entry points — all tables. Faster to scan than prose. Easier to keep accurate.

### Stay at the decision-making abstraction level
Too high → "the auth system handles auth" (useless).
Too low → directory listing of every file.
Right → "auth owns request-level identity; it does not own user lifecycle (that's user-mgmt). Tokens flow in via middleware, out via response headers."

### Mark uncertainties explicitly
```
The retry policy is set per-call (uncertain: only investigated the GET path; POST may differ).
```
Confident wrong is worse than honest unclear.

### Reference, don't restate
If domain A talks to domain B, link to B's doc. Don't re-describe B in A's doc. Drift compounds.

## Don't

### Don't paste code
**No function bodies. No class definitions. No signatures with type annotations. No code snippets.**

Why: arch docs operate above the code. If a reader can get the same info from the file in 5 seconds, the doc is noise. Worse — pasted code drifts the moment the file changes, silently misleading readers.

Use file:line references instead:
- ❌ `async def authenticate(token: str) -> User: ...`
- ✅ `Token-to-user resolution: src/auth/resolver.py:23`

(This rule is enforced by `arch_docs_no_code` in user memory.)

### Don't restate what the code says
If a function is well-named and one screenful, the code is the doc. Arch docs cover what the code can't see by itself: the shape, the seams, the why.

### Don't write fluffy prose
"This robust and extensible authentication system" — strike everything except the load-bearing nouns. No "robust", "scalable", "production-grade" unless you can point to the file that makes it so.

### Don't describe implementation
"How" belongs in code. Arch docs cover:
- **What** parts exist
- **How they connect** (mechanisms, contracts, data flow at the boundary)
- **Why** the system is shaped this way

### Don't keep stale claims
If the doc says X and the code does Y, the doc is wrong. Fix the doc. (This becomes critical in the v2 maintenance loop — but the discipline starts here.)

## Length proportional to system size

| System scope | Per-domain doc | System overview |
|---|---|---|
| Small project (1-2 domains, <10KLOC) | 50-100 lines | 40-80 lines |
| Standard (3-6 domains, 10-100KLOC) | 100-200 lines | 80-150 lines |
| Large (6+ domains, >100KLOC) | 150-300 lines | 150-250 lines |

Padding a doc to look comprehensive is a failure mode. A 60-line doc that gets the shape right beats a 300-line doc that buries the signal.

## What the doc must answer

Every per-domain doc must answer:
1. What does this domain own? (Boundaries → in)
2. What does it explicitly *not* own? (Boundaries → out)
3. What does it depend on / who depends on it? (Contracts)
4. What's the main flow through it? (Flows)
5. What significant choices shape it? (Notable Decisions)

If any of these are missing or hand-waved, the doc isn't done.

## What the doc must *not* contain

| Content | Belongs in |
|---|---|
| Function bodies, class definitions, signatures | the codebase |
| Bash commands, deploy scripts, env config | runbooks / ops docs |
| Acceptance criteria, success metrics | spec |
| Build task lists, effort estimates | build plans |
| Marketing language ("highly scalable", "world-class") | nowhere |

If you start writing one of these, stop and convert it to a reference + table.
