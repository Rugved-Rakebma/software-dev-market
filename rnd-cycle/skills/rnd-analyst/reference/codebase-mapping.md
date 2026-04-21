# Codebase Mapping

Reference document for rnd-analyst codebase-audit mode. Defines the 4-track parallel analysis model, exploration patterns using native tools, output document templates, and writing guidelines.

## 4-Track Parallel Analysis Model

Codebase analysis is split into four independent tracks that can be investigated in parallel. Each track has a specific focus, exploration strategy, and output format.

| Track | Focus | Documents Produced |
|-------|-------|--------------------|
| tech | Technology stack, dependencies, external integrations | STACK profile |
| arch | Architecture patterns, directory structure, data flow | ARCHITECTURE map |
| quality | Coding conventions, testing patterns, style | CONVENTIONS guide |
| concerns | Technical debt, bugs, security, performance, fragile areas | CONCERNS register |

## Exploration Patterns by Track

All exploration MUST use native Read, Grep, and Glob tools. Never use bash commands like `find`, `cat`, `grep`, or `head` for file reading or searching.

### Tech Track

**Package manifests:**
- Glob: `**/package.json`, `**/requirements.txt`, `**/Cargo.toml`, `**/go.mod`, `**/pyproject.toml`, `**/Gemfile`
- Read each found manifest to extract dependencies, versions, scripts

**Configuration files:**
- Glob: `**/*.config.*`, `**/tsconfig.json`, `**/.nvmrc`, `**/.python-version`, `**/Dockerfile`, `**/docker-compose*.yml`
- Read config files to understand build pipeline, runtime requirements

**Environment files (existence only):**
- Glob: `**/.env*`
- NOTE EXISTENCE ONLY. Never read `.env` file contents. Record: "`.env` file present — contains environment configuration"

**External service imports:**
- Grep: `import.*stripe|import.*supabase|import.*aws|import.*firebase|import.*prisma|import.*mongoose` in source files
- Grep: `require\(.*stripe|require\(.*aws|require\(.*firebase` for CommonJS

### Arch Track

**Directory structure:**
- Glob: `**/src/**` to understand source layout
- Glob: `**/app/**`, `**/pages/**` for framework-specific patterns (Next.js, etc.)

**Entry points:**
- Glob: `**/index.ts`, `**/index.js`, `**/main.ts`, `**/main.js`, `**/app.ts`, `**/server.ts`
- Glob: `**/app/page.tsx`, `**/app/layout.tsx` for Next.js App Router
- Read each entry point to understand initialization flow

**Import patterns:**
- Grep: `^import` across source files to understand layer dependencies
- Grep: `from ['"]@/|from ['"]~/|from ['"]\.\.` to understand path aliasing and relative imports

**Data flow:**
- Grep: `fetch\(|axios\.|useSWR|useQuery|prisma\.|db\.` to find data access patterns
- Read files with data access to trace request -> processing -> response flow

### Quality Track

**Linting and formatting config:**
- Glob: `**/.eslintrc*`, `**/.prettierrc*`, `**/eslint.config.*`, `**/biome.json`, `**/.editorconfig`
- Read config files to understand enforced rules

**Test files and config:**
- Glob: `**/*.test.*`, `**/*.spec.*`, `**/__tests__/**`
- Glob: `**/jest.config.*`, `**/vitest.config.*`, `**/playwright.config.*`, `**/cypress.config.*`
- Read 3-5 test files to understand testing patterns, mocking approach, assertion style

**Source file sampling:**
- Read 5-10 representative source files across different directories
- Analyze: naming conventions, import organization, error handling, comment style, function design

### Concerns Track

**TODO/FIXME markers:**
- Grep: `TODO|FIXME|HACK|XXX|WORKAROUND` across source files (exclude node_modules, .git, dist)
- Read context around each match to assess severity

**Large files (potential complexity):**
- After identifying source directories, use Glob to find files and Read to check sizes
- Files over 300 lines warrant review for potential splitting

**Stubs and empty implementations:**
- Grep: `return null|return \[\]|return \{\}|=> \{\}` in source files
- Grep: `throw new Error\(['"]not implemented|throw new Error\(['"]TODO` for explicit stubs

**Debug leftovers:**
- Grep: `console\.log|console\.debug|console\.warn` in non-test source files
- Grep: `debugger` statements

**Security concerns:**
- Glob: `**/.env*`, `**/credentials.*`, `**/secrets.*` (existence only)
- Grep: `eval\(|new Function\(|innerHTML|dangerouslySetInnerHTML` for dangerous patterns
- Grep: `password.*=.*['"]|api_key.*=.*['"]|secret.*=.*['"]` for hardcoded secrets in source

## Writing Guide: Prescriptive Not Descriptive

Your documents guide future work. Every statement should be actionable.

**DO write prescriptively:**
- "Use camelCase for function names — see `src/utils/formatDate.ts` for reference"
- "Place new API routes in `src/app/api/` following the Next.js App Router convention"
- "Error handling uses try/catch with custom `AppError` class — see `src/lib/errors.ts`"

**DO NOT write descriptively:**
- "Some functions use camelCase" (how many? which ones? is it the standard?)
- "There are some API routes" (where? what pattern? how to add new ones?)
- "Errors are handled in various ways" (which ways? what's the preferred approach?)

**Write current state only.** Describe what IS, never what WAS or what you considered. No temporal language ("we found that," "after investigation"). State facts directly.

## File Path Citation Requirements

Every finding MUST include at least one file path. File paths are formatted in backticks.

**Good:** "Authentication middleware at `src/middleware/auth.ts` validates JWT tokens using the `jsonwebtoken` package"

**Bad:** "The authentication middleware validates JWT tokens" (which file? where?)

**Multiple files:** "The data access layer uses Prisma ORM — schema at `prisma/schema.prisma`, client at `src/lib/db.ts`, used in routes like `src/app/api/users/route.ts`"

## Forbidden Files

**NEVER read or quote contents from these files (even if they exist):**

- `.env`, `.env.*`, `*.env` — Environment variables with secrets
- `credentials.*`, `secrets.*`, `*secret*`, `*credential*` — Credential files
- `*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.jks` — Certificates and private keys
- `id_rsa*`, `id_ed25519*`, `id_dsa*` — SSH private keys
- `.npmrc`, `.pypirc`, `.netrc` — Package manager auth tokens
- `config/secrets/*`, `.secrets/*`, `secrets/` — Secret directories
- `*.keystore`, `*.truststore` — Java keystores
- `serviceAccountKey.json`, `*-credentials.json` — Cloud service credentials

**If you encounter these files:**
- Note their EXISTENCE only: "`.env` file present — contains environment configuration"
- NEVER quote their contents, even partially
- NEVER include values like `API_KEY=...` or `sk-...` in any output

## Output Document Templates

The following templates define the structure for each output document. Fill in templates with findings from exploration. Replace placeholder text with actual findings. Use "Not detected" or "Not applicable" when something is not found.

### STACK Template

```markdown
# Technology Stack

**Analysis Date:** [YYYY-MM-DD]

## Languages

**Primary:**
- [Language] [Version] — [Where used, cite file paths]

**Secondary:**
- [Language] [Version] — [Where used, cite file paths]

## Runtime

**Environment:**
- [Runtime] [Version] — source: [how determined, e.g., `.nvmrc`, `package.json engines`]

**Package Manager:**
- [Manager] [Version]
- Lockfile: [present/missing, which format]

## Frameworks

**Core:**
- [Framework] [Version] — [Purpose, cite entry point files]

**Testing:**
- [Framework] [Version] — [Purpose, cite config file]

**Build/Dev:**
- [Tool] [Version] — [Purpose, cite config file]

## Key Dependencies

**Critical (core functionality depends on these):**
- [Package] [Version] — [Why critical, what breaks without it]

**Infrastructure (build/deploy/dev tooling):**
- [Package] [Version] — [Purpose]

## Configuration

**Environment:**
- [How configured — cite config files]
- [Key configs required — do NOT list actual values]

**Build:**
- [Build config files — cite paths]

## Platform Requirements

**Development:**
- [Minimum requirements to run locally]

**Production:**
- [Deployment target, infrastructure requirements]

---
*Stack analysis: [date]*
```

### ARCHITECTURE Template

```markdown
# Architecture

**Analysis Date:** [YYYY-MM-DD]

## Pattern Overview

**Overall:** [Pattern name — Monolith, Modular Monolith, Microservices, Serverless, etc.]

**Key Characteristics:**
- [Characteristic 1]
- [Characteristic 2]
- [Characteristic 3]

## Layers

**[Layer Name]:**
- Purpose: [What this layer does]
- Location: `[path]`
- Contains: [Types of code]
- Depends on: [What it imports/uses]
- Used by: [What imports/uses it]

[Repeat for each architectural layer]

## Data Flow

**[Flow Name] (e.g., "User Request"):**
1. [Step 1 — cite file paths]
2. [Step 2 — cite file paths]
3. [Step 3 — cite file paths]

**State Management:**
- [How state is handled — cite relevant files]

## Key Abstractions

**[Abstraction Name]:**
- Purpose: [What it represents]
- Examples: `[file paths]`
- Pattern: [Pattern used — factory, singleton, repository, etc.]

## Entry Points

**[Entry Point Name]:**
- Location: `[path]`
- Triggers: [What invokes it — HTTP request, CLI command, cron, etc.]
- Responsibilities: [What it initializes/handles]

## Error Handling

**Strategy:** [Overall approach — try/catch, error boundaries, middleware, etc.]

**Patterns:**
- [Pattern 1 — cite example file]
- [Pattern 2 — cite example file]

## Cross-Cutting Concerns

**Logging:** [Approach — cite config/usage files]
**Validation:** [Approach — cite validation files]
**Authentication:** [Approach — cite auth files]

---
*Architecture analysis: [date]*
```

### STRUCTURE Template

```markdown
# Codebase Structure

**Analysis Date:** [YYYY-MM-DD]

## Directory Layout

[project-root]/
├── [dir]/          # [Purpose]
├── [dir]/          # [Purpose]
└── [file]          # [Purpose]

## Directory Purposes

**[Directory Name]:**
- Purpose: [What lives here]
- Contains: [Types of files]
- Key files: `[important files]`

[Repeat for each significant directory]

## Key File Locations

**Entry Points:**
- `[path]`: [Purpose]

**Configuration:**
- `[path]`: [Purpose]

**Core Logic:**
- `[path]`: [Purpose]

**Testing:**
- `[path]`: [Purpose]

## Naming Conventions

**Files:**
- [Pattern]: [Example]

**Directories:**
- [Pattern]: [Example]

## Where to Add New Code

**New Feature:**
- Primary code: `[path pattern]`
- Tests: `[path pattern]`

**New Component/Module:**
- Implementation: `[path pattern]`

**Utilities:**
- Shared helpers: `[path pattern]`

## Special Directories

**[Directory]:**
- Purpose: [What it contains]
- Generated: [Yes/No]
- Committed: [Yes/No]

---
*Structure analysis: [date]*
```

### CONVENTIONS Template

```markdown
# Coding Conventions

**Analysis Date:** [YYYY-MM-DD]

## Naming Patterns

**Files:**
- [Pattern — e.g., kebab-case for files, PascalCase for components]

**Functions:**
- [Pattern — e.g., camelCase, verb-first for actions]

**Variables:**
- [Pattern — e.g., camelCase, UPPER_SNAKE for constants]

**Types:**
- [Pattern — e.g., PascalCase, I-prefix for interfaces or not]

## Code Style

**Formatting:**
- [Tool used — e.g., Prettier]
- [Key settings — cite config file]

**Linting:**
- [Tool used — e.g., ESLint]
- [Key rules — cite config file]

## Import Organization

**Order:**
1. [First group — e.g., Node built-ins]
2. [Second group — e.g., External packages]
3. [Third group — e.g., Internal modules]

**Path Aliases:**
- [Aliases used — e.g., `@/` maps to `src/`]

## Error Handling

**Patterns:**
- [How errors are handled — cite example files]

## Logging

**Framework:** [Tool or "console"]

**Patterns:**
- [When/how to log — cite example files]

## Comments

**When to Comment:**
- [Guidelines observed — e.g., complex logic only, no obvious comments]

**JSDoc/TSDoc:**
- [Usage pattern — e.g., public APIs only, all exports, none]

## Function Design

**Size:** [Guidelines — e.g., prefer <50 lines]

**Parameters:** [Pattern — e.g., object destructuring for >2 params]

**Return Values:** [Pattern — e.g., explicit return types, Result pattern]

## Module Design

**Exports:** [Pattern — e.g., named exports only, default for components]

**Barrel Files:** [Usage — e.g., index.ts re-exports, or avoided]

---
*Convention analysis: [date]*
```

### TESTING Template

```markdown
# Testing Patterns

**Analysis Date:** [YYYY-MM-DD]

## Test Framework

**Runner:**
- [Framework] [Version]
- Config: `[config file path]`

**Assertion Library:**
- [Library — e.g., built-in, chai, jest matchers]

**Run Commands:**
- All tests: `just test`
- Watch mode: `just test-watch`
- Coverage: `just test-coverage`

## Test File Organization

**Location:**
- [Pattern — co-located with source or separate __tests__ directory]

**Naming:**
- [Pattern — e.g., `*.test.ts`, `*.spec.ts`]

**Structure:**
[Directory pattern showing where tests live relative to source]

## Test Structure

**Suite Organization:**
[Show actual pattern from codebase — describe/it nesting, test grouping]

**Patterns:**
- Setup: [How test setup works — beforeEach, fixtures, factories]
- Teardown: [How cleanup works — afterEach, database reset]
- Assertion: [Assertion style — expect().toBe, assert, should]

## Mocking

**Framework:** [Tool — e.g., jest.mock, vi.mock, sinon]

**Patterns:**
[Show actual mocking pattern from codebase]

**What to Mock:**
- [Guidelines — e.g., external services, database, network calls]

**What NOT to Mock:**
- [Guidelines — e.g., internal logic, pure functions, data transformations]

## Fixtures and Factories

**Test Data:**
[Show pattern from codebase — factories, fixtures, builders]

**Location:**
- [Where fixtures live — e.g., `__fixtures__/`, `test/helpers/`]

## Coverage

**Requirements:** [Target or "None enforced"]

**View Coverage:**
- `just test-coverage`

## Test Types

**Unit Tests:**
- [Scope and approach]

**Integration Tests:**
- [Scope and approach]

**E2E Tests:**
- [Framework or "Not used"]

## Common Patterns

**Async Testing:**
[Pattern — async/await, done callbacks, promises]

**Error Testing:**
[Pattern — expect().toThrow, try/catch assertions]

---
*Testing analysis: [date]*
```

### CONCERNS Template

```markdown
# Codebase Concerns

**Analysis Date:** [YYYY-MM-DD]

## Tech Debt

**[Area/Component]:**
- Issue: [What shortcut/workaround exists]
- Files: `[file paths]`
- Impact: [What breaks or degrades]
- Fix approach: [How to address it]

## Known Bugs

**[Bug description]:**
- Symptoms: [What happens]
- Files: `[file paths]`
- Trigger: [How to reproduce]
- Workaround: [If any]

## Security Considerations

**[Area]:**
- Risk: [What could go wrong]
- Files: `[file paths]`
- Current mitigation: [What is in place]
- Recommendations: [What should be added]

## Performance Bottlenecks

**[Slow operation]:**
- Problem: [What is slow]
- Files: `[file paths]`
- Cause: [Why it is slow]
- Improvement path: [How to speed up]

## Fragile Areas

**[Component/Module]:**
- Files: `[file paths]`
- Why fragile: [What makes it break easily]
- Safe modification: [How to change safely]
- Test coverage: [Gaps]

## Scaling Limits

**[Resource/System]:**
- Current capacity: [Numbers]
- Limit: [Where it breaks]
- Scaling path: [How to increase]

## Dependencies at Risk

**[Package]:**
- Risk: [What is wrong — deprecated, unmaintained, vulnerability]
- Impact: [What breaks]
- Migration plan: [Alternative]

## Missing Critical Features

**[Feature gap]:**
- Problem: [What is missing]
- Blocks: [What cannot be done without it]

## Test Coverage Gaps

**[Untested area]:**
- What is not tested: [Specific functionality]
- Files: `[file paths]`
- Risk: [What could break unnoticed]
- Priority: [High/Medium/Low]

---
*Concerns audit: [date]*
```
