---
id: NN-short-name
wave: N
depends_on: [NN-other-id]
files: [src/path/to/file.ts, ...]
requirements: [REQ-XXX-NN]
---

# Plan NN — Name

## Goal

One paragraph: what this plan delivers and why. Point at arch sections + spec REQs. Do not restate contracts, signatures, or code — arch carries the contract, spec carries the requirements.

## Wires to

- arch §<n> — <contract or data flow or module this plan touches>
- spec REQ-<X>, REQ-<Y>

## Tasks

### Task 1 — Name

**Build:** Describe behavior. No code, no signatures, no class bodies. Reference arch sections for shape (e.g. "per arch §5.1"). Reference spec REQs for acceptance.

**Done:** Binary check. Often the verify command itself, e.g. `python -c "from agent_mani.vault import retrieve_sources"` exits 0.

### Task 2 — Name

**Build:** ...

**Done:** ...
