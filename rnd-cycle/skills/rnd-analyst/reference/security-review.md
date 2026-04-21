# Security Review

Reference document for rnd-analyst security-review mode. Defines the STRIDE threat model framework, OWASP Top 10 checklist with Grep patterns, secrets scanning, auth verification, input validation, security headers, and severity classification.

## STRIDE Threat Model Framework

STRIDE is a systematic approach to identifying security threats. For each component or data flow in the system, assess all six threat categories.

| Threat | Question | Examples | Mitigations |
|--------|----------|----------|-------------|
| **S**poofing | Can someone pretend to be another user or system? | Missing auth checks, weak session tokens, no CSRF protection | Strong authentication, CSRF tokens, signed requests |
| **T**ampering | Can someone modify data they should not? | No input validation, missing integrity checks, unprotected API endpoints | Input validation, checksums, signed payloads, parameterized queries |
| **R**epudiation | Can someone deny they performed an action? | No audit logging, missing timestamps, no user action trail | Audit logs, immutable event streams, digital signatures |
| **I**nformation Disclosure | Can someone access data they should not? | Exposed .env files, verbose error messages, missing access controls | Encryption at rest/transit, proper access controls, sanitized errors |
| **D**enial of Service | Can someone disrupt the service? | No rate limiting, unbounded queries, missing pagination | Rate limiting, query limits, pagination, circuit breakers |
| **E**levation of Privilege | Can someone gain unauthorized access? | Missing role checks, broken access control, privilege escalation paths | Role-based access control, principle of least privilege, authorization middleware |

### How to Apply STRIDE

1. **Identify components:** List all system components (frontend, API, database, external services)
2. **Map data flows:** Trace how data moves between components
3. **For each flow:** Ask each STRIDE question and look for evidence in the code
4. **Document findings:** Each finding gets a severity rating and recommended mitigation

## OWASP Top 10 Checklist

Systematic checks for the most critical web application security risks. Each check includes Grep patterns for detection.

### 1. Injection (A03:2021)

**Risk:** Untrusted data sent to an interpreter as part of a command or query.

**Detection patterns:**
- Grep: `\$\{.*\}.*query|\$\{.*\}.*sql|\.query\(.*\+|\.exec\(.*\+` — string interpolation in queries
- Grep: `eval\(|new Function\(|exec\(|spawn\(` — code execution from user input
- Grep: `\.raw\(|\.unsafeRaw\(` — raw SQL queries (might be intentional but needs review)

**What to verify:**
- All database queries use parameterized queries or ORM methods
- No string concatenation in SQL/NoSQL queries
- No `eval()` or `new Function()` with user-supplied data
- Command execution (spawn, exec) does not include user input directly

### 2. Broken Authentication (A07:2021)

**Risk:** Weak or missing authentication and session management.

**Detection patterns:**
- Grep: `token.*=.*["']|secret.*=.*["']|password.*=.*["']` — hardcoded credentials in source
- Grep: `jwt\.sign.*expiresIn.*['"](\d+d|never)` — long-lived or non-expiring tokens
- Grep for auth middleware missing on routes: compare API route files against middleware application

**What to verify:**
- No hardcoded tokens, passwords, or API keys in source files
- Sessions have reasonable expiration
- Password storage uses bcrypt/argon2/scrypt (not MD5/SHA1)
- Auth middleware applied to all sensitive routes
- Login has rate limiting or brute-force protection

### 3. Sensitive Data Exposure (A02:2021)

**Risk:** Sensitive data exposed through inadequate protection.

**Detection patterns:**
- Glob: `**/.env*` — existence check only, NEVER read contents
- Grep: `process\.env\.|os\.environ|System\.getenv` — environment variable usage (verify no logging of values)
- Grep: `console\.log.*password|console\.log.*token|console\.log.*secret` — logging sensitive data
- Grep: `JSON\.stringify.*user|JSON\.stringify.*session` — serializing sensitive objects

**What to verify:**
- `.env` files are in `.gitignore`
- Sensitive data not logged or exposed in error messages
- HTTPS enforced (no HTTP fallbacks in production config)
- API responses do not include unnecessary sensitive fields (password hashes, internal IDs)

### 4. XML External Entities / Insecure Deserialization (A08:2021)

**Risk:** Untrusted data deserialized without validation.

**Detection patterns:**
- Grep: `JSON\.parse\(` without surrounding try/catch — unhandled parse errors
- Grep: `yaml\.load\(|pickle\.load\(|unserialize\(` — unsafe deserialization
- Grep: `xml\.parse|parseXML|DOMParser` — XML parsing (check for XXE protection)

**What to verify:**
- All JSON.parse calls wrapped in try/catch
- No use of unsafe deserialization (pickle, PHP unserialize) with user data
- XML parsers configured to disable external entities

### 5. Broken Access Control (A01:2021)

**Risk:** Users able to access resources or actions beyond their permissions.

**Detection patterns:**
- Grep for routes without auth middleware: find API route files, check for auth imports/usage
- Grep: `role.*admin|isAdmin|hasPermission` — verify these checks exist where needed
- Grep: `req\.params\.id|req\.query\.id` — verify ownership checks on resource access (user can only access their own data)

**What to verify:**
- All API routes that modify data require authentication
- Resource access includes ownership verification (not just auth)
- Admin routes have role-based authorization
- No direct object reference without access check (IDOR)
- Server-side enforcement (not just client-side hiding)

### 6. Security Misconfiguration (A05:2021)

**Risk:** Insecure default configurations or incomplete setup.

**Detection patterns:**
- Grep: `cors.*\*|Access-Control-Allow-Origin.*\*` — overly permissive CORS
- Grep: `debug.*true|DEBUG.*=.*1|NODE_ENV.*development` in non-dev config — debug mode in production
- Grep: `allowAll|permitAll|anonymous` — overly permissive access rules

**What to verify:**
- CORS configured with specific origins (not wildcard in production)
- Debug mode disabled in production configuration
- Default passwords/keys changed from defaults
- Unnecessary features/endpoints disabled
- Error messages do not reveal stack traces in production

### 7. Cross-Site Scripting / XSS (A03:2021)

**Risk:** Injecting malicious scripts into web pages.

**Detection patterns:**
- Grep: `dangerouslySetInnerHTML|v-html|innerHTML` — raw HTML insertion
- Grep: `document\.write|\.html\(` — direct DOM manipulation with potential user data
- Grep: `\$\{.*\}.*<|<.*\$\{` — template literals in HTML context

**What to verify:**
- User-generated content is escaped/sanitized before rendering
- `dangerouslySetInnerHTML` only used with sanitized content (DOMPurify or similar)
- Content Security Policy (CSP) headers configured
- No inline event handlers constructed from user data

### 8. Insecure Dependencies (A06:2021)

**Risk:** Using components with known vulnerabilities.

**Detection patterns:**
- Read: `package.json`, `requirements.txt`, `Gemfile.lock` — check for outdated packages
- Grep: `"version".*"[0-9]+\.[0-9]+\.[0-9]+"` in lockfiles — pin versions

**What to verify:**
- Dependencies are pinned to specific versions (lockfile present and committed)
- No known CVEs in current dependency versions (flag for external research if uncertain)
- Development dependencies not included in production builds
- Package sources are official registries (not custom/unknown registries)

### 9. Insufficient Logging & Monitoring (A09:2021)

**Risk:** Attacks go undetected due to lack of logging.

**Detection patterns:**
- Grep: `catch.*\{(\s*\}|.*console\.error)` — empty catch blocks or console-only error handling
- Grep for auth-related code without logging: login attempts, failed auth, permission denials

**What to verify:**
- Failed authentication attempts are logged
- Authorization failures are logged
- Input validation failures are logged
- Application errors are logged with context (not swallowed)
- Logs do not contain sensitive data (passwords, tokens)
- Log aggregation/monitoring is configured (or flagged as needed)

### 10. Server-Side Request Forgery / SSRF (A10:2021)

**Risk:** Application makes requests to attacker-controlled URLs.

**Detection patterns:**
- Grep: `fetch\(.*req\.|axios\(.*req\.|request\(.*req\.` — user-supplied URLs in server-side requests
- Grep: `url.*=.*req\.(body|query|params)` — URL from request parameters
- Grep: `redirect\(.*req\.|Location.*req\.` — open redirects

**What to verify:**
- Server-side HTTP requests do not use user-supplied URLs directly
- URL allowlists/denylists for external requests
- No open redirects (redirect targets validated against allowlist)
- Internal network addresses blocked in outbound requests

## Secrets Scanning

**File existence checks (Glob, NEVER read contents):**
- `**/.env*` — environment files
- `**/credentials.*`, `**/secrets.*` — credential files
- `**/*.pem`, `**/*.key`, `**/*.p12` — certificates and keys
- `**/id_rsa*`, `**/id_ed25519*` — SSH keys
- `**/.npmrc`, `**/.pypirc` — package manager auth
- `**/serviceAccountKey.json`, `**/*-credentials.json` — cloud credentials

**Source code scanning (Grep):**
- `sk-[a-zA-Z0-9]` — OpenAI API keys
- `pk_live_|pk_test_|sk_live_|sk_test_` — Stripe keys
- `AKIA[0-9A-Z]{16}` — AWS access keys
- `ghp_[a-zA-Z0-9]{36}` — GitHub personal access tokens
- `glpat-[a-zA-Z0-9\-]{20}` — GitLab personal access tokens
- `xoxb-|xoxp-` — Slack tokens
- `password\s*=\s*["'][^"']+["']|api_key\s*=\s*["'][^"']+["']` — hardcoded credentials in source

**If found:** Report as Critical severity. Note the file and pattern matched. NEVER include the actual secret value in the report.

## Auth Verification

Verify authentication and authorization are properly implemented:

**Protected routes check:**
1. Use Glob to find all API route files
2. Use Grep to check each for auth middleware/hooks: `useAuth|useSession|getCurrentUser|authMiddleware|requireAuth|isAuthenticated`
3. Identify routes that handle sensitive data but lack auth checks
4. Check for role-based authorization on admin routes

**Session management:**
- Grep: `session|cookie|token` in auth-related files
- Verify session expiration is configured
- Verify secure cookie flags (httpOnly, secure, sameSite)
- Check for session invalidation on logout

**Password handling:**
- Grep: `bcrypt|argon2|scrypt|pbkdf2` — proper password hashing
- Grep: `md5|sha1|sha256` in password context — weak hashing (flag as High severity)
- Verify passwords are never stored in plaintext or logged

## Input Validation

Verify user input is validated and sanitized:

**Validation checks:**
- Grep: `zod|yup|joi|validate|sanitize|escape|DOMPurify` — validation library usage
- Verify validation exists on both client AND server side
- Check that API endpoints validate request body schema
- Verify file uploads have type and size restrictions

**Parameterized queries:**
- Grep: `\?\s*,|:\w+|\$\d+` in SQL context — parameterized query syntax
- Verify no string concatenation in database queries

**Output encoding:**
- Verify HTML output is escaped (framework default or explicit)
- Verify JSON responses use proper serialization
- Check for content-type headers on API responses

## Security Headers

Check for security-related HTTP headers:

| Header | Purpose | Grep Pattern |
|--------|---------|-------------|
| Content-Security-Policy | Prevent XSS, clickjacking | `Content-Security-Policy|CSP` |
| Strict-Transport-Security | Enforce HTTPS | `Strict-Transport-Security|HSTS` |
| X-Frame-Options | Prevent clickjacking | `X-Frame-Options|DENY|SAMEORIGIN` |
| X-Content-Type-Options | Prevent MIME sniffing | `X-Content-Type-Options|nosniff` |
| X-XSS-Protection | Legacy XSS filter | `X-XSS-Protection` |
| Referrer-Policy | Control referrer information | `Referrer-Policy` |
| Permissions-Policy | Control browser features | `Permissions-Policy|Feature-Policy` |

**Where to check:**
- Grep in middleware files, server configuration, response headers setup
- Check for `helmet` (Node.js) or equivalent security header middleware
- Verify headers are set in production configuration (not just development)

## Output Format

Structure findings by severity, highest first:

### Critical
Immediate exploitation risk. Must fix before any deployment.
- Exposed secrets in source code
- SQL injection vulnerabilities
- Authentication bypass paths
- Unprotected admin endpoints

### High
Significant risk requiring prompt fix. Fix within current sprint.
- Cross-site scripting (XSS) vulnerabilities
- Broken access control (IDOR)
- Missing encryption for sensitive data
- Weak password hashing

### Medium
Should fix soon. Schedule within next sprint.
- Missing rate limiting on auth endpoints
- Verbose error messages in production
- Missing input validation on non-critical endpoints
- Overly permissive CORS

### Low
Best practice improvements. Address during refactoring.
- Missing security headers
- Audit logging gaps
- Dependencies slightly outdated
- Development-only vulnerabilities

**Finding format:**
```markdown
### [Severity] [Category]: [Brief description]

**Files:** `[affected file paths]`
**Pattern:** [What was found — Grep pattern or observation]
**Risk:** [What could be exploited and how]
**Recommendation:** [Specific fix with code example if applicable]
```
