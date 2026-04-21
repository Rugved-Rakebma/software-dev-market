---
phase: NN-name
plan: NN
wave: N
depends_on: []
files_modified: []
requirements: [REQ-XXX-NN]
must_haves:
  truths:
    - "Observable truth that must hold"
  artifacts:
    - path: "src/path/to/file"
      provides: "What this artifact delivers"
  key_links:
    - from: "src/component.tsx"
      to: "src/api/endpoint.ts"
      via: "fetch call in useEffect"
---

## Plan NN: [Plan Name]

### Task 1: [Task Name]
- **Files:** `src/path/to/file.ts`
- **Action:** [Specific implementation instructions]
- **Verify:** [Command or check to verify task is done]
- **Done:** [Acceptance criteria — binary testable]

### Task 2: [Task Name]
- **Files:** `src/path/to/file.ts`
- **Action:** [Specific implementation instructions]
- **Verify:** [Command or check to verify task is done]
- **Done:** [Acceptance criteria — binary testable]
