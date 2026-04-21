# Audit Methodology

Reference document for rnd-analyst codebase-audit and document-audit modes. Defines confidence classification, calibration tiers, evidence format, and document audit categories.

## Two Modes

### Codebase Audit
Systematic exploration and analysis of an existing codebase. Produces structured reference documents (stack, architecture, conventions, concerns) that serve as living documentation for future work.

**When to use:** Starting a new project on an existing codebase, onboarding to unfamiliar code, periodic health checks, pre-planning investigation.

**Output:** Structured documents following templates in `templates/audit-*.md`.

### Document Audit
Systematic analysis of a spec, PRD, proposal, or design document for completeness and quality. Surfaces gaps, assumptions, risks, and ambiguities before implementation begins.

**When to use:** Before implementation of any spec, after major spec revisions, when stakeholders disagree on scope, when timeline seems unrealistic.

**Output:** Structured analysis following template in `templates/audit-document.md`.

## Confidence Classification

Every assumption, finding, and assessment must carry a confidence tier.

### Confident
**Definition:** Clear from code or evidence. The pattern is explicit and unambiguous.

**Criteria:**
- Direct evidence in source code (function signatures, config files, explicit patterns)
- Consistent pattern across multiple files (>3 instances)
- Documented in project configuration or comments
- No contradicting evidence found

**Example:** "The project uses TypeScript — `tsconfig.json` exists, all source files are `.ts`/`.tsx`, and `package.json` lists `typescript` as a dependency."

### Likely
**Definition:** Reasonable inference from available evidence. The pattern is implied and consistent but not explicitly stated.

**Criteria:**
- Evidence supports the conclusion but is indirect
- Pattern appears in some files but not universally
- Inference from related code patterns
- No strong contradicting evidence

**Example:** "Authentication likely uses JWT — `jsonwebtoken` is in `package.json` dependencies and `jwt.verify()` appears in `src/middleware/auth.ts`, though no explicit auth documentation exists."

### Unclear
**Definition:** Could go multiple ways. Evidence is thin, contradictory, or absent.

**Criteria:**
- Minimal or no direct evidence
- Contradicting patterns found
- Multiple valid interpretations of the evidence
- Would need external research or human clarification

**Example:** "Unclear whether the project intends to support multi-tenancy — `tenantId` appears in one database model but no routing or middleware references it."

### Minimizing Unclear
Before classifying anything as Unclear, exhaust investigation:
1. Read more files related to the area (at least 5 additional)
2. Search for alternative naming patterns (the concept might exist under a different name)
3. Check configuration files and environment setup
4. Look for test files that might reveal intended behavior

Only classify as Unclear after genuine investigation, not as a shortcut.

## Calibration Tiers

Calibration tiers control the depth and breadth of analysis output. The invoking context determines which tier applies.

### full_maturity
**Areas:** 3-5 assumption/analysis areas
**Alternatives:** 2-3 per Likely/Unclear item
**Evidence depth:** Detailed file path citations with line-level specifics
**When:** Major architectural decisions, high-stakes specs, unfamiliar codebases

### standard
**Areas:** 3-4 assumption/analysis areas
**Alternatives:** 2 per Likely/Unclear item
**Evidence depth:** File path citations
**When:** Regular pre-implementation checks, routine audits, known codebases

### minimal_decisive
**Areas:** 2-3 assumption/analysis areas
**Alternatives:** Single decisive recommendation per item
**Evidence depth:** Key file paths only
**When:** Quick checks, minor features, time-constrained reviews

## Evidence Format

Every finding follows this structure:

```markdown
### [Area Name] (e.g., "Authentication Approach")

- **Assumption:** [Decision statement — what is believed to be true]
  - **Evidence:** [What supports this — cite file paths with backticks]
  - **If Wrong:** [Concrete consequence — not vague "could cause issues"]
  - **Confidence:** Confident | Likely | Unclear
```

**Rules:**
1. Every assumption MUST cite at least one file path as evidence
2. Every "If Wrong" MUST state a concrete consequence (delays, rework, security breach, data loss — not "could cause issues")
3. Confidence levels must be honest — do not inflate Confident when evidence is thin
4. Do NOT pad with obvious assumptions — only surface decisions that could go multiple ways
5. If prior decisions already lock a choice, mark as Confident and cite the prior decision source

## Needs External Research

When codebase analysis alone is insufficient, flag topics for external research rather than guessing.

```markdown
## Needs External Research

- **[Topic]**: [Why codebase evidence is insufficient]
  - What to research: [Specific questions to answer]
  - Impact on analysis: [What changes if the answer goes one way vs another]
```

**Valid reasons for external research:**
- Library version compatibility (new version may break patterns)
- Ecosystem best practices (conventions beyond what code reveals)
- Performance characteristics (benchmarks needed, not guessable from code)
- Security advisories (CVEs for specific dependency versions)

**Invalid reasons (investigate harder instead):**
- "Not sure how auth works" — read more auth-related files
- "Don't know the architecture" — trace imports from entry points
- "Unclear testing approach" — find and read test files

## Document Audit Categories

When auditing a document (spec, PRD, proposal), analyze across five dimensions:

### Gap Categories
- **Missing requirements**: Features or behaviors described but not specified in detail
- **Unaddressed scenarios**: Edge cases, error states, concurrent access, offline behavior
- **Undefined interfaces**: API contracts, data formats, integration points left vague
- **Missing non-functionals**: Performance targets, scalability needs, security requirements
- **Absent acceptance criteria**: No way to verify "done"

### Assumption Surfacing
- **Stated assumptions**: Explicitly mentioned in the document
- **Implied assumptions**: Not stated but required for the spec to work (e.g., "users have internet" for a web app)
- **Contradicted assumptions**: Stated in one section, contradicted in another
- **External assumptions**: Depend on third parties, market conditions, or team capacity

### Risk Identification
For each risk, assess:
- **Category**: Technical, Business, Timeline, Resource, External
- **Likelihood**: High (>70%), Medium (30-70%), Low (<30%)
- **Impact**: Critical (blocks launch), High (significant rework), Medium (delays), Low (minor adjustment)
- **Mitigation**: What can be done to reduce likelihood or impact

### Ambiguity Detection
Flag statements that could be interpreted multiple ways:
- **Vague quantifiers**: "fast," "scalable," "user-friendly" — without metrics
- **Undefined terms**: Domain-specific terms used without definition
- **Scope creep signals**: "and more," "etc.," "as needed" — unbounded scope
- **Contradictions**: Two sections that say different things about the same feature

### Implementability Assessment
Can this actually be built with the stated constraints?
- **Timeline feasibility**: Is the scope achievable in the stated timeframe?
- **Skill requirements**: Does the team have the needed expertise?
- **Dependency risks**: Are external dependencies available and reliable?
- **Technical feasibility**: Are there any technically impossible or extremely difficult requirements?
- **Resource constraints**: Does budget/infrastructure support the requirements?
