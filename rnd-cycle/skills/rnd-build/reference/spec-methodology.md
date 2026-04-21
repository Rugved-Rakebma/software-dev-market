# Spec Methodology

A structured methodology for turning ideas into actionable, testable specifications. The goal is a spec tight enough that two developers would build the same thing from it.

---

## 1. Problem Framing

**Always start with the problem, not the solution.**

Most specification failures begin with "I want to build X" instead of "Users struggle with Y." Problem framing forces clarity before commitment.

### The Problem Statement Formula

```
[WHO] experiences [PROBLEM] when [CONTEXT], which causes [IMPACT].
```

**Examples:**
- "Property managers lose 2-3 hours per week manually reconciling payments across multiple bank accounts, which delays monthly reporting."
- "New users abandon onboarding at step 3 because the form requires information they don't have yet, causing 40% drop-off."

### Framing Questions

1. **Who has this problem?** Be specific. "Users" is too broad. "Property managers with 50+ units using QuickBooks" is useful.
2. **How do they solve it today?** The current workaround reveals the real requirement.
3. **What happens if we don't build this?** If the answer is "nothing much," challenge whether it's worth building.
4. **What triggered this now?** Urgency context helps scope v1.
5. **What does success look like to you?** Their answer reveals unstated requirements.

### Red Flags in Problem Framing

- "We need this because competitors have it" — feature parity is not a problem statement
- "It would be cool if..." — solution-hunting, not problem-solving
- "We just need a simple..." — complexity is hiding; dig deeper
- "Everyone wants this" — who specifically? how do you know?

---

## 2. Requirement Extraction

### The Interview Process

Requirements rarely arrive fully formed. They emerge through structured conversation.

**Round 1 — Broad Strokes (3-5 questions)**

Ask the questions that most change the shape of the spec. Prioritize by information value, not by topic coverage.

Good first-round questions:
- "Walk me through the happy path — what does a user do from start to finish?"
- "What's the one thing this absolutely must do on day one?"
- "Who else touches this system? What do they need?"
- "What existing systems does this need to talk to?"
- "What's your biggest worry about building this?"

**Round 2 — Gap Filling (targeted)**

After round 1, identify the 3-5 biggest gaps and ask about those specifically. Don't ask about everything — ask about what matters most.

**Round 3 — Edge Cases**

- "What happens when [input] is empty/null/huge/malformed?"
- "What if two users do [action] at the same time?"
- "What if the external service is down?"
- "What if the user is on a slow connection?"

### Requirement Format

Every requirement gets a unique ID and testable acceptance criteria.

```
| ID           | Category | Requirement                              | Acceptance Criteria                        |
|--------------|----------|------------------------------------------|--------------------------------------------|
| REQ-AUTH-01  | Auth     | Users must authenticate via SSO           | User can log in with Google/Microsoft SSO  |
| REQ-UI-03   | UI       | Dashboard shows real-time occupancy       | Occupancy updates within 5 seconds of change |
| REQ-DATA-02 | Data     | Import existing tenant records from CSV   | 10K-row CSV imports in under 30 seconds    |
```

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

Number sequentially within each category. Gaps in numbering are fine (don't renumber if you remove one).

### Acceptance Criteria Rules

Every acceptance criterion must be **binary-testable** — you can definitively say "pass" or "fail."

| Bad | Good |
|-----|------|
| "Fast page loads" | "Page loads in under 2 seconds on 3G" |
| "Good error messages" | "Error messages include: what happened, why, and what to do next" |
| "Secure authentication" | "Passwords hashed with bcrypt, min 12 rounds" |
| "Easy to use" | "New user completes first task without documentation in under 3 minutes" |
| "Scalable" | "Handles 1000 concurrent users with p99 latency under 500ms" |

---

## 3. Scope Classification

### The Decision Tree

For each proposed feature or requirement, run through this tree:

```
Does it block the core value proposition?
├── YES → v1 (must have)
└── NO
    ├── Does the user expect it on day one?
    │   ├── YES → v1 (must have)
    │   └── NO
    │       ├── Does it significantly improve adoption/retention?
    │       │   ├── YES → v2 (planned)
    │       │   └── NO
    │       │       ├── Is it aligned with the product vision?
    │       │       │   ├── YES → v2 (planned)
    │       │       │   └── NO → Out of scope
    │       │       └── ...
    │       └── ...
    └── ...
```

### Scope Challenge Phrases

Use these to push back constructively:

- "If we ship without this, can users still get core value?" — if yes, it's v2
- "What's the cost of adding this in month 2 vs. month 1?" — if low, defer it
- "Is this solving a problem you have, or a problem you might have?" — speculative features are v2+
- "What's the simplest version of this that delivers value?" — find the v1 kernel inside a v2 feature
- "If you had to cut half the features, which half survives?" — forces prioritization

### Scope Documentation

**v1 entries** need full requirement rows with acceptance criteria.

**v2 entries** need the requirement and a note on why it was deferred:
```
| REQ-REPORT-01 | Reporting | Custom report builder | Deferred: standard reports cover 80% of use cases in v1 |
```

**Out-of-scope entries** need a brief reason:
```
- Mobile app — v1 is responsive web; native app re-evaluated after launch metrics
- Multi-language support — all initial users are English-speaking
- Offline mode — target users have reliable internet
```

---

## 4. Gap Identification Checklist

Systematically check each area. Not all will apply to every project, but reviewing the list prevents blind spots.

| # | Gap Area | Key Questions | Common Oversights |
|---|----------|---------------|-------------------|
| 1 | **Error Handling** | What happens when things fail? How are errors displayed? How are they logged? | Silent failures, generic error messages, no retry logic |
| 2 | **Authentication** | Who can access the system? SSO? MFA? Session management? | Token expiration, password reset flow, account lockout |
| 3 | **Authorization / Permissions** | Who can do what? Role-based? Resource-based? | Admin escalation paths, permission inheritance, default permissions |
| 4 | **Edge Cases** | Empty states, max limits, concurrent operations, Unicode, timezones? | Null handling, boundary values, race conditions |
| 5 | **Data Migration** | Is there existing data? What format? How much? Quality issues? | Data cleaning needs, mapping mismatches, rollback of migration |
| 6 | **Monitoring / Observability** | How do you know the system is healthy? Alerts? Dashboards? | No alerting thresholds, missing business metrics, log retention |
| 7 | **Rollback / Recovery** | How do you undo a bad deploy? Data rollback? Feature flags? | Database migration rollback, partial rollback scenarios |
| 8 | **Rate Limiting** | What prevents abuse? Per-user? Per-endpoint? Global? | Bot traffic, API key abuse, cost overrun from external services |
| 9 | **Multi-tenancy** | Shared or isolated resources? Data isolation? Noisy neighbor? | Cross-tenant data leaks, per-tenant config, billing isolation |
| 10 | **Accessibility (a11y)** | WCAG level? Screen reader support? Keyboard navigation? | Focus management, color contrast, aria labels, form errors |
| 11 | **Internationalization (i18n)** | Multiple languages? RTL support? Date/number formats? | Hardcoded strings, pluralization, currency formatting |
| 12 | **Backup / Recovery** | RPO? RTO? Automated backups? Tested restores? | Untested backup restores, point-in-time recovery gaps |
| 13 | **Audit Trail** | Do actions need to be logged? Who changed what, when? Compliance? | Immutability of audit logs, retention period, queryability |
| 14 | **Deployment Strategy** | Blue/green? Rolling? Canary? Zero-downtime? | Database schema changes during deploy, CDN cache invalidation |
| 15 | **External Dependencies** | Third-party APIs? SLAs? Fallback behavior? Cost at scale? | Vendor lock-in, API deprecation, rate limits from providers |

### Using the Checklist

Don't ask about all 15 areas upfront. Instead:
1. Scan the list mentally for the 3-5 most relevant to this project
2. Ask about those in your clarification round
3. Flag the rest as "reviewed, not applicable" or "needs investigation" in open questions

---

## 5. Success Criteria Writing

Success criteria answer: "How do we know this project succeeded?"

### Rules for Good Success Criteria

1. **Binary-testable**: Someone can answer YES or NO, not "sort of"
2. **Measurable**: Includes a number, threshold, or observable outcome
3. **Time-bound**: Specifies when measurement happens (at launch, after 30 days, etc.)
4. **Owned**: Someone specific can verify it
5. **Independent**: Each criterion stands alone; failing one doesn't invalidate others

### Success Criteria Patterns

**Functional**: "User can [action] resulting in [outcome]"
```
- User can import a 10K-row CSV and see all records in the dashboard within 60 seconds
- Admin can disable a user account and that user is immediately locked out of all sessions
```

**Performance**: "[Metric] stays [below/above] [threshold] under [conditions]"
```
- API response time stays below 200ms at p95 under 500 concurrent users
- Page load time under 3 seconds on 4G connection
```

**Adoption**: "[X users/actions] within [timeframe] of launch"
```
- 50 properties onboarded within 30 days of launch
- 80% of daily active users complete at least one core workflow per session
```

**Reliability**: "[System] achieves [uptime/error rate] over [period]"
```
- System achieves 99.9% uptime over first 90 days
- Error rate stays below 0.1% of all API requests
```

### Anti-Patterns

| Anti-Pattern | Why It's Bad | Fix |
|-------------|-------------|-----|
| "Improved UX" | Not measurable | "Task completion rate above 90%" |
| "Fast and reliable" | No thresholds | "p99 < 500ms, 99.9% uptime" |
| "Users love it" | Subjective | "NPS score above 40 after 30 days" |
| "Scalable architecture" | Not testable at launch | "Handles 10x current load in staging" |
| "Secure" | Too vague | "Passes OWASP Top 10 audit" |

---

## 6. Open Questions Format

Open questions are gaps that can't be resolved in the spec session and need dedicated research.

### Structured Format

```markdown
## Open Questions

- [ ] **OQ-01**: [Question in plain language]
  - **Context**: [Why this matters to the spec]
  - **Impact**: [What changes depending on the answer — HIGH/MEDIUM/LOW]
  - **Route**: /rnd:research [specific research prompt]

- [ ] **OQ-02**: [Question]
  - **Context**: [Why this matters]
  - **Impact**: [HIGH/MEDIUM/LOW]
  - **Route**: /rnd:research [specific research prompt]
```

### Example

```markdown
- [ ] **OQ-01**: What's the maximum practical size for a CSV import before we need background processing?
  - **Context**: REQ-DATA-02 says "import CSV" but doesn't specify size limits
  - **Impact**: HIGH — determines whether we need a job queue in v1
  - **Route**: /rnd:research CSV import performance limits in Node.js with PostgreSQL COPY

- [ ] **OQ-02**: Does Stripe support split payments to multiple connected accounts in a single transaction?
  - **Context**: REQ-BIZ-03 requires splitting rent payment between owner and management company
  - **Impact**: MEDIUM — if not, we need an intermediary ledger
  - **Route**: /rnd:research Stripe Connect split payment capabilities and limitations
```

### Triage Rules

- **HIGH impact** questions should block design until answered
- **MEDIUM impact** questions can proceed with an assumption (document the assumption)
- **LOW impact** questions can be resolved during implementation
