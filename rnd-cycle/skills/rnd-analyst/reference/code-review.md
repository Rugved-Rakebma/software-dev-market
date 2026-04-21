# Code Review

Reference document for rnd-analyst code-review mode. Defines the line-by-line review methodology, severity tiers, review comment format, integration wiring checks, requirements integration map, and anti-pattern catalog.

## Line-by-Line Review Methodology

Code review is not skimming. It is systematic examination of every meaningful change for correctness, security, maintainability, and integration.

**Review order:**
1. **Understand intent** — Read the PR description, spec reference, or task description to understand WHAT the code should do and WHY
2. **Architecture check** — Do the files and patterns match the project's architecture? Does new code land in the right place?
3. **Line-by-line quality** — Read every changed line for bugs, security issues, edge cases, naming, and style
4. **Integration verification** — Check that new code properly connects to existing code (exports used, APIs called, data flows)
5. **Test coverage** — Are the changes tested? Are the tests meaningful (not just asserting true)?

**Reading strategy:**
- Start with the "widest" files (routes, pages, orchestrators) to understand the flow
- Then read the "deepest" files (utilities, models, services) to understand the implementation
- Finally read tests to verify coverage matches implementation

## Severity Tiers

### Blocker

**Definition:** Issues that must be fixed before merge. These represent security vulnerabilities, data loss risks, race conditions, broken APIs, or crashes.

**Examples:**
- SQL injection or XSS vulnerability
- Race condition that can corrupt data
- API that returns wrong status codes or data shape
- Unhandled null/undefined that will crash in production
- Missing authentication on sensitive endpoint
- Data mutation without transaction (partial writes possible)
- Breaking change to public API without version bump

**Action:** Must fix. Do not merge with blockers.

### Suggestion

**Definition:** Issues that should be addressed but do not block merge. These represent missing validation, unclear naming, missing tests, performance concerns, or code duplication.

**Examples:**
- Missing input validation on API endpoint
- Function or variable name that does not communicate intent
- Missing error handling (catch block empty or too generic)
- Missing tests for new functionality
- N+1 query pattern (works but will be slow at scale)
- Code duplication that should be extracted to shared utility
- Missing TypeScript types (using `any`)
- Missing loading/error states in UI components

**Action:** Should fix in this PR or create a follow-up task.

### Nit

**Definition:** Style preferences, naming alternatives, documentation suggestions, and alternative approaches. These are optional improvements.

**Examples:**
- Naming alternative (both work, one reads slightly better)
- Import ordering preference
- Comment that could be clearer
- Alternative approach that might be simpler
- Documentation addition for complex logic
- Spacing or formatting that linter does not catch

**Action:** Author decides. Reviewer should not block on nits.

## Review Comment Format

Every review finding follows this structure:

```
[severity] [file:line] What --> Why --> Suggestion
```

**Examples:**

```
[Blocker] src/app/api/users/route.ts:23
Missing auth check on DELETE handler --> Any unauthenticated user can delete users -->
Add `const user = await getCurrentUser(); if (!user) return Response.json({ error: 'Unauthorized' }, { status: 401 });`

[Suggestion] src/components/UserCard.tsx:45
`data` is too generic as a variable name --> Makes code harder to understand when reading quickly -->
Rename to `userProfile` to match what it actually contains

[Nit] src/utils/format.ts:12
Could use template literal instead of string concatenation --> Slightly more readable -->
`return `${firstName} ${lastName}`` instead of `return firstName + ' ' + lastName`
```

**Rules:**
- Always include file path and line number
- "What" describes the observation (what you see)
- "Why" explains the impact (why it matters)
- "Suggestion" provides a concrete fix (what to do about it)
- Be specific enough that the author can fix it without asking follow-up questions

## Integration Wiring Checks

Code review must verify not just that code is correct in isolation, but that it properly connects to the rest of the system.

### Step 1: Build Export/Import Map

For the files under review, identify:
- **What does this code export?** (functions, components, types, constants)
- **What does this code import?** (from other project files, not just packages)
- **What SHOULD import this code?** (based on the feature being built)

### Step 2: Verify Each Export is Imported AND Used

For each export in the reviewed code:

1. Use Grep to find imports of the exported name across the project
2. For each importing file, verify the import is actually USED (not just imported and forgotten)
3. Flag orphaned exports (exported but never imported)

**Not just imported — actually called/rendered/referenced:**
```
BAD: import { formatDate } from '../utils/format'
     // formatDate never appears again in the file

GOOD: import { formatDate } from '../utils/format'
      <span>{formatDate(user.createdAt)}</span>
```

### Step 3: Check API Routes Have Consumers

For new API routes in the review:

1. Use Grep to find fetch/axios calls to the route path
2. Verify the consumer handles the response (not fire-and-forget)
3. Verify request/response shapes match between consumer and route

**Check both directions:**
- Route expects `{ name, email }` in POST body — consumer sends `{ name, email }`
- Route returns `{ user: { id, name } }` — consumer destructures `{ user }`

### Step 4: Check Auth Protection on Sensitive Routes

For routes that handle user data, financial data, admin actions, or private resources:

1. Use Grep to verify auth middleware/hook usage in the route handler
2. Verify authorization (not just authentication) — does it check the user has permission?
3. Flag unprotected sensitive routes as Blocker

### Step 5: Trace E2E Flows

For features under review, trace the complete data flow:

```
Component --> API call --> Route handler --> Database query --> Response --> State update --> Render
```

At each step, verify:
- The connection exists (not just planned)
- Data shapes match (TypeScript types align, or runtime shapes match)
- Error cases are handled (what happens when the API returns 404? 500? network error?)
- Loading states are handled (what shows while waiting for response?)

## Requirements Integration Map

For each requirement in scope of the review, trace the implementation wiring:

```markdown
| Requirement | Integration Path | Status | Issue |
|-------------|-----------------|--------|-------|
| REQ-001 | UserForm.tsx --> /api/users POST --> prisma.user.create | WIRED | -- |
| REQ-002 | Dashboard.tsx --> /api/stats GET | PARTIAL | API route exists but component doesn't call it |
| REQ-003 | -- | UNWIRED | No implementation found |
```

**Status definitions:**
- **WIRED**: Full path from UI to data layer exists and is connected
- **PARTIAL**: Some pieces exist but connections are broken or incomplete
- **UNWIRED**: No implementation evidence found for this requirement

## Anti-Pattern Catalog

### Orphaned Exports

**Pattern:** Code is exported but never imported anywhere in the project.

**Detection:** Use Grep to search for the export name across all source files. If only found in the defining file, it is orphaned.

**Risk:** Dead code that adds maintenance burden. May indicate incomplete feature — the export was created but the consumer was never built.

**Severity:** Suggestion (usually) or Blocker (if the orphaned export IS the feature)

### Unused Imports

**Pattern:** A module is imported but never referenced in the file body.

**Detection:** Use Grep within the file for the imported name, excluding the import line. If no other reference exists, the import is unused.

**Risk:** Dead code. May indicate removed functionality where cleanup was incomplete.

**Severity:** Nit (usually) or Suggestion (if many unused imports indicate confused code)

### Form Without Handler

**Pattern:** A `<form>` element exists but has no meaningful `onSubmit` handler, or the handler only calls `e.preventDefault()` without doing anything else.

**Detection:**
- Grep: `<form` in component file
- Grep: `onSubmit` — if missing, no handler at all
- Read the handler — if it only contains `e.preventDefault()` or `console.log`, it is a stub

**Risk:** User fills out form, clicks submit, nothing happens. Core feature broken.

**Severity:** Blocker (if this is a core form) or Suggestion (if form is secondary)

### API Without Consumer

**Pattern:** An API route file exists but nothing in the frontend calls it.

**Detection:**
- Identify the route path from the file location (e.g., `src/app/api/users/route.ts` = `/api/users`)
- Grep for that path in component/page files
- If no fetch/axios call found, the API is orphaned

**Risk:** Backend work was done but never connected to frontend. Feature appears complete from backend perspective but is invisible to users.

**Severity:** Blocker (if this API is core to the feature) or Suggestion (if it's a utility API)

### State Without Render

**Pattern:** A state variable (useState, store, etc.) exists but is never referenced in the component's JSX/template output.

**Detection:**
- Grep: `useState|useReducer|useStore` to find state declarations
- Grep for the state variable name in JSX context (within `{...}` in template)
- If state is set but never rendered, it is invisible to the user

**Risk:** Data is fetched and stored but never displayed. Feature appears to work (no errors) but produces no visible output.

**Severity:** Blocker (if this is the primary data display) or Suggestion (if auxiliary)

### Catch Without Handle

**Pattern:** A try/catch block catches an error but does nothing meaningful with it (empty catch, or only console.log).

**Detection:**
- Grep: `catch\s*\(` followed by empty block or only `console`
- Read the catch body — if it does not rethrow, display error to user, or log to monitoring, it swallows errors

**Risk:** Errors are silently swallowed. Users see broken UI with no explanation. Developers see no errors in monitoring.

**Severity:** Suggestion (non-critical paths) or Blocker (critical paths like auth, payments, data mutation)

### Hardcoded Configuration

**Pattern:** Configuration values (URLs, ports, API keys, feature flags) hardcoded in source instead of read from environment or config.

**Detection:**
- Grep: `http://localhost|https://api\.|:3000|:8080` in non-test source files
- Grep: `apiKey.*=.*["']|baseUrl.*=.*["']` in non-config files

**Risk:** Cannot deploy to different environments without code changes. May accidentally expose development credentials.

**Severity:** Suggestion (URLs) or Blocker (credentials/secrets)
