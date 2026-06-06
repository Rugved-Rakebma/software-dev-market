# Investigation Schema

The evidence report `rnd-domain-investigator` returns for each domain. Written to `.rnd/arch-docs/investigations/{domain}.md` and consumed by Phase 3 (Synthesize) when authoring `/docs/arch/{domain}.md`.

This is **evidence**, not the final doc. Investigators gather and cite; the orchestrator synthesizes. Separation of concerns.

## Required Frontmatter

```yaml
---
domain: {domain-name from plan}
investigated: {ISO timestamp}
files-examined: {count}
confidence: high | medium | low
---
```

`confidence` reflects the investigator's overall assessment of how well they understand this domain. Low confidence is fine — it signals to Phase 3 that the resulting doc should be cautious.

## Required Sections

### Scope
What was investigated, what wasn't, and why.

```markdown
## Scope
Investigated: src/auth/ (8 files), middleware in src/middleware/auth.ts, session handling in src/lib/session.ts.
Not investigated: oauth provider plugins under src/auth/providers/ (deferred — large, may warrant own subdomain).
```

### Key Files
Table — the files a reader should know about to understand this domain.

```markdown
## Key Files
| File | Role | Notes |
|---|---|---|
| src/auth/middleware.ts:12 | Request-level auth check (entry) | All routes pass through |
| src/auth/resolver.ts:34 | Token → User resolution | DB lookup with cache |
| src/auth/session.ts:8 | Session storage interface | Backed by Redis (src/auth/session.ts:42) |
| src/auth/errors.ts | Domain-specific error types | Used by all handlers |
```

Use file:line refs. Notes column captures "why this file matters", not what the code says.

### Flows
The main code paths through the domain. Numbered steps with file:line refs.

```markdown
## Flows

### Flow 1: Authenticated request
1. Request arrives → middleware fires (src/auth/middleware.ts:12)
2. Token extracted from `Authorization` header (src/auth/middleware.ts:24)
3. Token validated + decoded (src/auth/resolver.ts:34)
4. User loaded from DB or cache (src/auth/resolver.ts:48)
5. `req.user` attached for downstream handlers (src/auth/middleware.ts:31)
6. Failure cases: throws `AuthError` (src/auth/errors.ts:8) → caught by error middleware

### Flow 2: Token refresh
1. ...
```

Cite every step. ASCII diagrams allowed for forks/joins.

### Boundaries
What this domain owns and explicitly does *not* own.

```markdown
## Boundaries

**Owns**:
- Token issuance, validation, refresh (src/auth/)
- Session lifecycle (src/auth/session.ts)
- AuthN at the request layer (middleware)

**Does NOT own**:
- User lifecycle (signup, profile, deactivation) → `user-mgmt` domain
- AuthZ / RBAC checks → `permissions` domain (referenced by handlers, not auth)
- Email-based password reset → split: token generation here (src/auth/reset.ts), email sending in `notifications` domain
```

Boundary lines are how the doc set stays coherent. Be explicit.

### Contracts
What flows in and what flows out at the seams.

```markdown
## Contracts

**Provides** (consumed by other domains):
- `req.user: User` — middleware-attached identity (src/auth/middleware.ts:31)
- `authenticate(req)` — programmatic check for non-HTTP entry points (src/auth/index.ts:5)
- `AuthError` types — used by error middleware (src/auth/errors.ts)

**Consumes** (from other domains):
- `userRepo.findById(id)` — from `user-mgmt` (src/users/repo.ts:18); called in resolver
- `redisClient` — from `infra/redis` (src/infra/redis.ts); session backend
- `config.AUTH_*` — from `config` domain
```

### Notable Decisions (visible in code)
Architectural choices that show up in code, with evidence.

```markdown
## Notable Decisions

- **JWT over server-side sessions for primary auth** (src/auth/resolver.ts:34, no session DB lookup on hot path). Sessions exist (src/auth/session.ts) but only for refresh tokens.
- **Auth middleware applied globally, not per-route** (src/server.ts:42 — `app.use(authMiddleware)`). Public routes opt out via `req.route.public = true` flag.
- **Token validation cached for 60s** (src/auth/resolver.ts:48). Trade-off: 60s window for revoked tokens to keep working.
```

Decisions visible in code are evidence-backed. Decisions inferred from absence ("there's no rate limiting") go in Open Questions, not here.

### Open Questions
Things the investigator couldn't determine from code alone.

```markdown
## Open Questions
- Is there a token rotation policy beyond manual refresh? No evidence in code.
- Multi-tenant context isolation — middleware reads tenant from token but no enforcement visible at DB layer.
- src/auth/providers/ left uninvestigated — may contain SSO/OAuth integrations with their own arch.
```

## What the investigator does NOT produce

- A finished `/docs/arch/{domain}.md` — that's Phase 3's job
- Recommendations, suggestions, "should we…" — investigators report, not propose
- Code blocks (the no-code rule applies even to investigations — cite file:line)
- Prose paragraphs justifying why the system is well-designed (or badly) — observation, not opinion

## Length

Investigations should be **80-300 lines** depending on domain size. Concise where possible. Tables and numbered lists over paragraphs.

## Confidence calibration

| Level | When to use |
|---|---|
| **high** | Read all primary files, traced main flows end-to-end, contracts are clear |
| **medium** | Read enough to characterize the domain; some areas left unexamined |
| **low** | Spot-read only; many open questions; the resulting doc should be marked tentative |

Use medium by default — most investigations on a real codebase will leave something untouched.
