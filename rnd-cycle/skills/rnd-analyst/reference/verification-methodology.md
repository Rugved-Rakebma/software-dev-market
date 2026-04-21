# Verification Methodology

Reference document for rnd-analyst verification mode. Defines the goal-backward verification framework, 4-level checks, stub detection, re-verification, requirements coverage, anti-pattern scanning, spot-checks, and human verification flagging.

## Goal-Backward Verification Principle

**Task completion does not equal goal achievement.**

A task "create chat component" can be marked complete when the component is a placeholder `<div>`. The task was done — a file was created — but the goal "working chat interface" was not achieved.

Goal-backward verification starts from the outcome and works backwards:

1. **What must be TRUE** for the goal to be achieved? (Observable truths)
2. **What must EXIST** for those truths to hold? (Required artifacts)
3. **What must be WIRED** for those artifacts to function? (Key links)
4. **What DATA must FLOW** for the wiring to produce real results? (Data flow)

Then verify each level against the actual codebase.

### Establishing Must-Haves

**From spec:** If `.rnd/spec/spec.md` defines success criteria for the scope being verified, use those directly as observable truths.

**From architecture:** If `.rnd/architecture/current.md` defines expected components, use those as required artifacts.

**Derived from goal:** If no explicit criteria exist, derive them:
1. State the goal
2. List 3-7 observable, testable behaviors that must be true
3. For each truth, identify artifacts that must exist
4. For each artifact, identify connections that must be wired
5. Document derived must-haves before proceeding

## Level 1: EXISTS

**Check:** Does the file exist at the expected path?

**Method:** Use Glob to search for the expected file path.

**Status:**
- **FOUND**: File exists at expected path
- **MISSING**: File does not exist

**This is necessary but wildly insufficient.** A file existing tells you nothing about what it contains.

## Level 2: SUBSTANTIVE

**Check:** Does the file contain real implementation, not just a stub?

**Method:** Use Read to load the file. Check:
- Line count (a React component under 10 lines is suspicious)
- Presence of expected patterns (imports, function bodies, return statements with real content)
- Absence of stub indicators

**Status:**
- **REAL**: File has meaningful implementation
- **STUB**: File exists but contains placeholder/minimal content

### Stub Detection Patterns

**React/Vue/Svelte Components:**
```
RED FLAGS:
- return <div>Component</div>
- return <div>Placeholder</div>
- return <div>{/* TODO */}</div>
- return null
- return <></>
- Component body is <20 lines total
- No imports of child components or hooks
- Empty event handlers: onClick={() => {})
- Handlers that only log: onChange={() => console.log('clicked'))
- Submit handlers that only prevent default: onSubmit={(e) => e.preventDefault()}
```

**API Routes:**
```
RED FLAGS:
- return Response.json({ message: "Not implemented" })
- return Response.json([])  // Empty array with no DB query
- return Response.json({ ok: true })  // Static success with no logic
- Route handler body is <10 lines
- No imports of database client or business logic
- GET handler returns hardcoded data
- POST handler doesn't read request body
```

**Utility/Service Files:**
```
RED FLAGS:
- throw new Error('not implemented')
- throw new Error('TODO')
- return undefined
- Function body is empty or single-line return
- Only contains type definitions with no implementation
```

**Stub vs Initial State Distinction:**
A grep match is a STUB only when the value flows to rendering or user-visible output AND no other code path populates it with real data. Check for data-fetching patterns (useEffect, fetch, useSWR, useQuery, subscribe) that write to the same variable before flagging.

- `useState([])` followed by `useEffect(() => { fetch(...).then(setData) })` = NOT a stub (initial state before fetch)
- `useState([])` with no fetch/query anywhere in the component = STUB (never populated)

## Level 3: WIRED

**Check:** Is the file imported AND used (not just imported)?

**Method:** Use Grep to search for:
1. **Import check**: `import.*{artifact_name}` or `from.*{artifact_path}` across source files
2. **Usage check**: `{artifact_name}` in files that import it, excluding the import line itself

**Both checks must pass.** An import without usage is dead code.

**Status:**
- **WIRED**: Imported AND used (appears in JSX, called as function, referenced in logic)
- **ORPHANED**: Exists but not imported anywhere
- **PARTIAL**: Imported but not used (dead import) OR used via side-effect import

### Wiring Red Flags

```
- fetch('/api/messages')  // No await, no .then, no assignment — fire and forget
- await prisma.message.findMany()
  return Response.json({ ok: true })  // Query result discarded, static return
- onSubmit={(e) => e.preventDefault()}  // Only prevents default, no actual handling
- const [messages, setMessages] = useState([])
  return <div>No messages</div>  // State exists but always shows empty message
```

## Level 4: DATA FLOWS

**Check:** Does the data source produce real data (not empty/hardcoded)?

**When to run:** For artifacts that pass Level 3 (WIRED) and render dynamic data (components, pages, dashboards). Skip for utilities, configs, and pure logic files.

**Method:**
1. **Identify the data variable** — use Grep to find `useState|useQuery|useSWR|useStore|props\.` in the artifact
2. **Trace the data source** — use Grep to find what populates that variable (fetch, query, store dispatch)
3. **Verify the source produces real data** — use Read on the API route or data source, Grep for `prisma\.|db\.|query\(|findMany|select|FROM`
4. **Check for disconnected props** — use Grep to find where the component is used and check if props are hardcoded empty

**Status:**
- **FLOWING**: Data source found, produces real data from DB/API/store
- **STATIC**: Fetch exists but returns hardcoded/fallback data only
- **DISCONNECTED**: No data source found — variable is never populated
- **HOLLOW_PROP**: Props passed to component are hardcoded empty at the call site

### Final Artifact Status Matrix

| Exists | Substantive | Wired | Data Flows | Status |
|--------|-------------|-------|------------|--------|
| yes | yes | yes | yes | VERIFIED |
| yes | yes | yes | no | HOLLOW — wired but data disconnected |
| yes | yes | no | — | ORPHANED |
| yes | no | — | — | STUB |
| no | — | — | — | MISSING |

## Re-Verification Mode

When a previous verification report exists with a `gaps:` section:

1. **Parse previous report** — extract must-haves, gaps, and passed items
2. **Focus on failed items** — run full 4-level verification on every previously-failed truth/artifact
3. **Quick regression on passed items** — existence + basic sanity check only (Level 1 + quick Level 2)
4. **Track changes:**
   - `gaps_closed`: Previously-failed items that now pass
   - `gaps_remaining`: Items still failing
   - `regressions`: Previously-passed items that now fail (critical — these indicate new breakage)

## Requirements Coverage Checking

Every requirement ID from `.rnd/spec/spec.md` that maps to the scope being verified must trace to verified artifacts.

**Process:**
1. Extract requirement IDs from the spec or plan that apply to this scope
2. For each requirement, find artifacts that fulfill it
3. Determine status:
   - **SATISFIED**: Implementation evidence found that fulfills the requirement
   - **BLOCKED**: No evidence or contradicting evidence
   - **NEEDS HUMAN**: Cannot verify programmatically (visual, UX quality)
4. Check for orphaned requirements — IDs expected for this scope that no artifact claims

**Orphaned requirements are a red flag.** They represent work that was planned but never implemented.

## Anti-Pattern Scanning

Run on all files in the verification scope:

**Incomplete markers:**
- Grep: `TODO|FIXME|XXX|HACK|PLACEHOLDER|WORKAROUND`

**Placeholder text:**
- Grep (case insensitive): `placeholder|coming soon|will be here|not yet implemented|not available|lorem ipsum`

**Empty implementations:**
- Grep: `return null|return \{\}|return \[\]|=> \{\}`

**Hardcoded empty data:**
- Grep: `=\s*\[\]|=\s*\{\}|=\s*null|=\s*undefined` in non-test source files

**Debug leftovers:**
- Grep: `console\.log|console\.debug|debugger` in non-test source files

**Severity classification:**
- **Blocker**: Prevents the goal from being achieved (empty handler for core feature, missing DB query in data route)
- **Warning**: Incomplete but not blocking (TODO in non-critical path, missing error handling)
- **Info**: Notable but not impacting (console.log in development code, minor naming issue)

## Behavioral Spot-Checks

Quick automated tests to verify key behaviors actually work.

**When to run:** Phases that produce runnable code (APIs, CLI tools, build scripts, data pipelines). Skip for documentation-only or config-only phases.

**Constraints:**
- Each check must complete in under 10 seconds
- Do not start servers or services — only test what is already runnable
- Do not modify state (no writes, mutations, or side effects)
- If the project has no runnable entry points yet, skip with: "Behavioral spot-checks: SKIPPED (no runnable entry points)"

**Select 2-4 behaviors from must-haves truths that can be tested with a single command:**
- Build produces output files
- Module exports expected functions
- CLI command produces expected output
- Test suite passes for relevant files

**Record results:**

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| {truth} | {command} | {output} | PASS / FAIL / SKIP |

**Status:**
- **PASS**: Command succeeded and output matches expected
- **FAIL**: Command failed or output is empty/wrong — flag as gap
- **SKIP**: Cannot test without running server/external service — route to human verification

## Human Verification Flagging

Some things cannot be verified programmatically. Always flag these for human testing:

**Always needs human:**
- Visual appearance and layout
- User flow completion (multi-step interactions)
- Real-time behavior (WebSockets, live updates)
- External service integration (payments, email, SMS)
- Performance feel (perceived speed, responsiveness)
- Error message clarity and helpfulness
- Accessibility (screen reader, keyboard navigation)

**Needs human if uncertain:**
- Complex wiring that grep cannot trace (dynamic imports, runtime composition)
- Dynamic state behavior (race conditions, timing)
- Edge cases (boundary conditions, concurrent access)

**Format for each human verification item:**
```markdown
### {N}. {Test Name}

**Test:** {What to do — step by step}
**Expected:** {What should happen}
**Why human:** {Why this cannot be verified programmatically}
```

## Overall Status Determination

| Status | Criteria |
|--------|----------|
| **passed** | All truths VERIFIED, all artifacts pass levels 1-4, all key links WIRED, no blocker anti-patterns |
| **gaps_found** | One or more truths FAILED, artifacts MISSING/STUB/ORPHANED, key links NOT_WIRED, or blocker anti-patterns |
| **human_needed** | All automated checks pass but items flagged for human verification remain |

**Score:** `verified_truths / total_truths`

## Gap Output Structure

When gaps are found, structure them in YAML frontmatter for downstream consumption:

```yaml
gaps:
  - truth: "Observable truth that failed"
    status: failed
    reason: "Brief explanation"
    artifacts:
      - path: "src/path/to/file"
        issue: "What is wrong"
    missing:
      - "Specific thing to add/fix"
```

Group related gaps by concern — if multiple truths fail from the same root cause, note this to help create focused fix plans.
