# Spec Methodology

A structured methodology for turning ideas into actionable, testable specifications.

## What Spec Owns

Spec owns **requirements only**. Everything else lives elsewhere:

| Concern | Lives in | Not in spec |
|---|---|---|
| What the system must do (REQs + acceptance) | Spec | — |
| Why it matters (problem framing, users) | Spec | — |
| How the system is shaped (mechanisms, contracts, tech choices) | Arch | Constraints / Technology / Compliance sections do **not** belong here |
| What gets built next (tasks, files, timelines) | Plan | Team / Timeline / Assumptions do **not** belong here |
| Open research questions | Spec (Open Questions, routed) | — |

The result: a spec tight enough that two developers would build the same thing from it, and small enough that downstream artifacts (arch, plan) don't drown in restated context.

## Scope-Gated Process

Spec process intensity matches project size. Assess scope from the clarifying conversation:

| Scope | Signals | Process |
|---|---|---|
| **Small** | Single dev, <1KLOC, 1–2 components, no new deps | Short clarify (3–5 questions); core gap subset only (5–7 items); minimal sections |
| **Standard** | 2–5 devs, 1–10KLOC, 3–5 components | Full clarify rounds; mid gap set (8–12 items) |
| **Large** | Multi-team, >10KLOC, greenfield | All rounds; full gap checklist (all 15 items) |

Capture the assessment in the spec frontmatter's `scope` field. Downstream commands (`/rnd:design`, `/rnd:plan`, `/rnd:decide`) fall back to this when arch hasn't run yet.

**Default to small unless the conversation proves otherwise.** Importing enterprise concerns into a project that doesn't have them is the most common spec failure mode.

---

## 1. Problem Framing

Always start with the problem, not the solution.

### The Problem Statement Formula

```
[WHO] experiences [PROBLEM] when [CONTEXT], which causes [IMPACT].
```

**Examples:**
- "Property managers lose 2–3 hours per week manually reconciling payments across multiple bank accounts, which delays monthly reporting."
- "New users abandon onboarding at step 3 because the form requires information they don't have yet, causing 40% drop-off."

### Framing Questions

1. **Who has this problem?** Be specific. "Users" is too broad.
2. **How do they solve it today?** The current workaround reveals the real requirement.
3. **What happens if we don't build this?** If "nothing much," challenge whether it's worth building.
4. **What triggered this now?** Urgency context helps scope v1.
5. **What does success look like to you?** Their answer reveals unstated requirements.

### Red Flags

- "We need this because competitors have it" — feature parity is not a problem statement
- "It would be cool if..." — solution-hunting, not problem-solving
- "We just need a simple..." — complexity is hiding; dig deeper
- "Everyone wants this" — who specifically? how do you know?

---

## 2. Requirement Extraction

### Interview Rounds (scope-gated)

**Round 1 — Broad Strokes (all scopes; 3–5 questions)**

Ask the questions that most change the shape of the spec:
- "Walk me through the happy path — what does a user do from start to finish?"
- "What's the one thing this absolutely must do on day one?"
- "Who else touches this system? What do they need?"
- "What existing systems does this need to talk to?"
- "What's your biggest worry about building this?"

**Round 2 — Gap Filling (standard / large only)**

After round 1, identify the 3–5 biggest gaps and ask about those specifically.

**Round 3 — Edge Cases (large only, or as needed)**

- "What happens when [input] is empty/null/huge/malformed?"
- "What if two users do [action] at the same time?"
- "What if the external service is down?"

### Requirement Format (canonical)

Every REQ row has exactly four columns:

| ID | Category | Requirement | Acceptance |
|----|----------|-------------|------------|
| REQ-AUTH-01 | Auth | Users must authenticate via SSO | User can log in with Google/Microsoft SSO; failed login returns 401 |
| REQ-UI-03 | UI | Dashboard shows real-time occupancy | Occupancy updates within 5 seconds of change |
| REQ-DATA-02 | Data | Import existing tenant records from CSV | 10K-row CSV imports in under 30 seconds |

**Rules for rows:**
- **Requirement** = behavior, not implementation. No signatures, no code, no impl prose.
- **Acceptance** = binary-testable check. "Pass" or "fail" — never "looks good."
- One row per requirement; no nested requirements.
- No restated arch contracts — if it needs a signature to explain, the arch doc owns that.

### ID Convention: REQ-{CATEGORY}-{NN}

Common categories:
- **AUTH** — Authentication and identity
- **UI** — User interface and experience
- **DATA** — Data storage, migration, import/export
- **API** — API contracts and integrations
- **PERF** — Performance and latency
- **SEC** — Security and encryption
- **INFRA** — Infrastructure and deployment
- **BIZ** — Business logic and rules
- **NOTIFY** — Notifications and messaging
- **REPORT** — Reporting and analytics
- **ADMIN** — Administration and configuration

Number sequentially within each category. Gaps in numbering are fine.

### Acceptance Criteria Rules

| Bad | Good |
|-----|------|
| "Fast page loads" | "Page loads in under 2 seconds on 3G" |
| "Good error messages" | "Error messages include: what happened, why, and what to do next" |
| "Secure authentication" | "Passwords hashed with bcrypt, min 12 rounds" |
| "Easy to use" | "New user completes first task without documentation in under 3 minutes" |
| "Scalable" | "Handles 1000 concurrent users with p99 latency under 500ms" |

---

## 3. Version Classification (v1 / v2 / out-of-scope)

For each proposed requirement, classify which version it belongs to. (This is "version" classification — distinct from the small/standard/large size scope above.)

### Decision Tree

```
Does it block the core value proposition?
├── YES → v1 (must have)
└── NO
    ├── Does the user expect it on day one? → YES → v1
    ├── Does it significantly improve adoption/retention? → YES → v2
    ├── Aligned with product vision? → YES → v2
    └── otherwise → Out of scope
```

### Classification Phrases

- "If we ship without this, can users still get core value?" — if yes, v2
- "What's the cost of adding this in month 2 vs. month 1?" — if low, defer
- "Is this solving a problem you have, or a problem you might have?" — speculative → v2+
- "What's the simplest version that delivers value?" — find the v1 kernel
- "If you had to cut half, which half survives?" — forces prioritization

### Documentation

- **v1** entries: full requirement rows with acceptance.
- **v2** entries: requirement + brief deferral reason.
- **Out of scope** entries: short bullet + reason (no row needed).

---

## 4. Gap Identification (scope-gated)

Systematically check gap areas. The set you review depends on scope.

### Core Gaps (review for **all scopes** — small / standard / large)

| # | Gap Area | Key Question |
|---|----------|--------------|
| 1 | **Auth** | Who can access the system? |
| 2 | **Error handling** | What happens when things fail? |
| 3 | **Edge cases** | Empty / null / max / concurrent / malformed inputs? |
| 4 | **Data migration** | Is there existing data to move? |
| 5 | **Monitoring** | How do you know the system is healthy? |
| 6 | **Rollback** | How do you undo a bad deploy? |
| 7 | **Permissions** | What's the authorization model? |

### Standard Gaps (add for **standard / large**)

| # | Gap Area | Key Question |
|---|----------|--------------|
| 8 | **Rate limiting** | What prevents abuse? |
| 9 | **External dependencies** | Third-party SLAs? Fallback behavior? |
| 10 | **Audit trail** | Do actions need to be logged? |
| 11 | **Deployment strategy** | Blue/green? Canary? |
| 12 | **Backup / recovery** | RPO/RTO? Tested restores? |

### Large-Only Gaps (add for **large**)

| # | Gap Area | Key Question |
|---|----------|--------------|
| 13 | **Multi-tenancy** | Shared or isolated resources? |
| 14 | **Accessibility** | WCAG level? Screen reader support? |
| 15 | **Internationalization** | Multiple languages? RTL? Date/number formats? |

### Using the Checklist

1. Pick the gap set per scope (core / +standard / +large).
2. For each gap area, ask 1–2 clarifying questions in conversation.
3. Either capture as a REQ row, mark "reviewed, not applicable" in mental notes, or route as Open Question.

Don't dump all 15 gaps on the user in one round — pick the ones most likely to bite this project.

---

## 5. Open Questions

Open questions are gaps that can't be resolved in the spec session and need dedicated research.

### Format

```markdown
- [ ] **OQ-NN**: [Question in plain language]
  - **Impact**: HIGH | MEDIUM | LOW
  - **Route**: /rnd:research [specific research prompt]
```

### Impact Triage

- **HIGH** — Answer changes the spec shape. Blocks `/rnd:design` until resolved. Route to `/rnd:research` immediately.
- **MEDIUM** — Proceed with a stated assumption; revisit if the assumption breaks. Document the assumption inline.
- **LOW** — Defer to implementation phase; coder resolves in context.

### Example

```markdown
- [ ] **OQ-01**: What's the maximum practical CSV size before background processing is needed?
  - **Impact**: HIGH — determines whether REQ-DATA-02 needs a job queue in v1
  - **Route**: /rnd:research CSV import performance limits in Node.js with PostgreSQL COPY
```

---

## Output Contract

The downstream consumer of the spec is the planner (and via the planner, the coder + spec-checker). Plans reference REQ rows by ID; the coder receives the matching rows in its spawn prompt.

Everything in the spec must therefore be:
- **REQ-rowed if it's a requirement** — every "the system must X" becomes a REQ row with binary acceptance.
- **Behavior-only** — no signatures, no code, no impl details.
- **Single-source** — don't restate things arch will own. If you find yourself writing about tech stack, mechanisms, or roadmap, stop — that's the design doc's job.
