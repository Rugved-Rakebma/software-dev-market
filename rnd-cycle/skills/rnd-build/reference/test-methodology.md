# Test Methodology

Reference material for requirement-driven test generation. Covers mapping requirements to test cases, test categories, and the debug loop.

## Requirement-Driven Test Generation

Every test exists because a requirement demands it. No orphan tests. No requirements without tests.

### Mapping Flow
```
REQ-{CAT}-{NN} (from spec)
        ↓
Determine requirement type
        ↓
Select test category
        ↓
Write test cases
        ↓
Each test references its REQ-ID in description
```

### Test Case Structure
```
Test: REQ-AUTH-01 — valid credentials return JWT
  Given: user exists with email "test@example.com" and password "hashed"
  When: POST /api/auth/login with { email: "test@example.com", password: "correct" }
  Then: response status 200, body contains { token: <valid JWT> }

Test: REQ-AUTH-01 — invalid credentials return 401
  Given: user exists with email "test@example.com"
  When: POST /api/auth/login with { email: "test@example.com", password: "wrong" }
  Then: response status 401, body contains { error: "Invalid credentials" }
```

Each requirement should map to 1+ test cases:
- At least one happy path test
- At least one error/edge case test
- Additional tests for boundary conditions if applicable

## Test Categories

### Unit Tests
**Purpose**: Test isolated logic — pure functions, utilities, transformations.
**Characteristics**:
- No external dependencies (no DB, no network, no filesystem)
- Fast (<100ms per test)
- Deterministic (same input always produces same output)

**When to use**: Business logic, data transformations, validation functions, state machines, calculators.

**Example**:
```
// REQ-BIZ-02: Calculate order total with tax
test("calculateTotal applies 8.5% tax to subtotal", () => {
  expect(calculateTotal(100.00, "CA")).toBe(108.50)
})
```

### Integration Tests
**Purpose**: Test component interaction — how pieces work together.
**Characteristics**:
- May use real databases (test instances), HTTP clients, message queues
- Moderate speed (<5s per test)
- Tests the seams between components

**When to use**: API endpoints, database queries, service-to-service calls, middleware chains.

**Example**:
```
// REQ-API-01: GET /api/users returns paginated user list
test("GET /api/users returns first page of users", async () => {
  await seedUsers(25)
  const res = await request(app).get("/api/users?page=1&limit=10")
  expect(res.status).toBe(200)
  expect(res.body.data).toHaveLength(10)
  expect(res.body.pagination.total).toBe(25)
})
```

### End-to-End Tests
**Purpose**: Test complete user flows from UI to database and back.
**Characteristics**:
- Exercises the full stack
- Slower (<30s per test)
- Tests what the user actually experiences

**When to use**: Critical user journeys, flows that span multiple components, features where integration correctness matters more than unit correctness.

**Example**:
```
// REQ-UI-01: User can complete signup flow
test("new user can sign up and see dashboard", async () => {
  await page.goto("/signup")
  await page.fill("#email", "new@example.com")
  await page.fill("#password", "SecurePass123!")
  await page.click("button[type=submit]")
  await expect(page).toHaveURL("/dashboard")
  await expect(page.locator("h1")).toContainText("Welcome")
})
```

## Test Classification by Requirement Type

| Requirement Type | Primary Test Category | Rationale |
|---|---|---|
| Data requirements | Integration tests | Need real DB to verify queries return expected data |
| UI requirements | E2E tests | Need browser/renderer to verify user can complete flow |
| API requirements | Integration tests | Need HTTP layer to verify endpoints respond correctly |
| Auth requirements | Security tests (integration) | Need to verify unauthorized access is blocked |
| Business logic | Unit tests | Pure logic, no external dependencies |
| Performance | Load tests | Need to verify under realistic load conditions |
| Infrastructure | Integration tests | Need real infra to verify config and connectivity |

### Security Test Patterns for Auth Requirements
```
// REQ-SEC-01: Unauthenticated users cannot access protected routes
test("GET /api/admin returns 401 without token", async () => {
  const res = await request(app).get("/api/admin")
  expect(res.status).toBe(401)
})

// REQ-SEC-02: Users cannot access other users' data
test("GET /api/users/:id returns 403 for non-owner", async () => {
  const res = await request(app)
    .get("/api/users/other-user-id")
    .set("Authorization", `Bearer ${userToken}`)
  expect(res.status).toBe(403)
})
```

## Verification Command Format

Every plan task's Verify field should contain a runnable command that:
- Completes in <10 seconds
- Is read-only (no side effects — doesn't modify data or state)
- Returns a clear pass/fail signal (exit code 0 = pass, non-zero = fail)

### Examples
```
# Run specific test file
just test -- --filter auth.test.ts

# Type check
just typecheck

# Lint specific file
just lint -- src/api/auth.ts

# Check file exists and exports expected symbol
just check-export src/services/user.ts UserService

# Run integration test suite
just test-integration -- --filter users
```

### Anti-patterns
- `just test` (runs ALL tests — too slow, not targeted)
- "Manually verify in browser" (not automated)
- "Check the logs" (not deterministic)
- Commands that modify data (not read-only)

## Debug Loop

When a test fails during execution:

### Step 1: Read the Error
Understand the exact failure — expected vs actual, stack trace, error message.

### Step 2: Check Implementation First
The most common cause of test failure is incorrect implementation, not incorrect tests. Read the implementation code and compare against the spec requirement.

### Step 3: Fix and Re-run
Make a targeted fix to the implementation. Re-run the specific test.

### Step 4: Iteration Limit
Maximum 3 fix iterations per failing test. If the test still fails after 3 attempts:
- The issue is likely architectural, not a simple bug
- Mark the task as partially complete
- Document the failure in the execution summary
- Escalate — don't keep guessing

### Debug Decision Tree
```
Test fails
    ↓
Read error message
    ↓
Is the test correct? (matches spec requirement)
├── No  → Fix the test, re-run
└── Yes → Is the implementation correct?
          ├── Clearly wrong → Fix implementation, re-run
          ├── Unclear → Read spec requirement again
          └── Implementation looks correct → Check integration
              ├── Missing dependency → Rule 2 deviation
              ├── Wrong wiring → Fix wiring, re-run
              └── Architectural mismatch → Rule 4, STOP
```
