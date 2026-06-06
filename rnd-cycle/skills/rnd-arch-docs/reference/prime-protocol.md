# Phase 0: Prime Protocol

What main Claude reads in Phase 0 to build a working mental model of the codebase, and what gets written to `.rnd/arch-docs/codebase-survey.md`.

The depth of Prime determines the quality of every downstream phase. A shallow Prime → shallow Plan → shallow investigations → shallow docs. Take this seriously.

## What to Read (in order)

### 1. Project intent
- `README.md` at repo root — what the project says it is
- `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` / `Gemfile` — name, description, scripts, key dependencies
- Any `ABOUT.md`, `OVERVIEW.md`, or top-level docs

**Goal**: in one sentence, "this project is a {kind} that {does what}".

### 2. Stack & runtime
- Language(s) from manifests + file extensions
- Primary framework(s) (Next.js, FastAPI, Rails, etc.)
- Database / persistence (from manifest deps and any `schema.sql`, `migrations/`, `prisma/`)
- Build/bundle config: `tsconfig.json`, `vite.config.*`, `webpack.config.*`, `Makefile`, `Dockerfile`
- CI: `.github/workflows/`, `.gitlab-ci.yml`, `.circleci/`

**Goal**: know how this thing builds, runs, and deploys at a high level.

### 3. Structure
- Top-level `ls` of the repo
- One level deep into the primary source directory (`src/`, `lib/`, `app/`, `pkg/`, etc.)
- Note conventions visible from naming: monorepo packages, plugin dirs, feature folders, layered architecture

**Goal**: map the directories to *what* lives where (not yet *which domain*).

### 4. Entry points
- `bin/` entries, CLI scripts (from package manifest `scripts` or `bin`)
- Server start (`server.ts`, `main.go`, `wsgi.py`, `app.py`, `index.js`)
- Public API surface (`__init__.py` exports, `index.ts` re-exports)
- Test entry (`vitest.config.*`, `pytest.ini`, `jest.config.*`) — tests reveal seams

**Goal**: know where execution begins and where the surface area is.

### 5. Deep samples (1-2 directories)
Pick **1 or 2** directories that look most central from the survey so far, and read 2-3 files from each. Goal: confirm the directory contains what its name suggests, surface unexpected patterns.

**Don't read everything.** This is a sample, not a comprehensive read. Investigators handle depth later.

## Time budget

Prime should take **single-digit minutes of orchestrator time**, not a deep dive. The deep dive is Phase 2 (investigators, parallel). Prime is the high-altitude flyover.

If you find yourself reading 10+ source files in Phase 0, stop — that's Phase 2 work.

## What `codebase-survey.md` Contains

Write to `.rnd/arch-docs/codebase-survey.md` with this shape:

```markdown
---
generated: {ISO timestamp}
generator: /rnd:arch-docs (Phase 0)
---

# Codebase Survey

## Project
{One-sentence: what is this thing}

## Stack
- **Language(s)**: {primary, secondary}
- **Framework(s)**: {primary framework, key libs}
- **Persistence**: {db, ORM, schema location} or "none/file-based"
- **Build**: {how it builds}
- **Runtime/deploy**: {what runs where} or "TBD"

## Structure
{ASCII tree, 2 levels deep, with one-line annotation per dir}

src/
├── auth/       — login, tokens, middleware
├── api/        — HTTP handlers, routing
├── db/         — schema, queries, migrations
├── workers/    — background jobs
└── shared/     — types, utils

## Entry Points
| Entry | Path | Purpose |
|---|---|---|
| Server | src/server.ts | HTTP listener, route registration |
| CLI | bin/admin.ts | Admin commands |
| Worker | src/workers/index.ts | Job runner |

## Notable Patterns (observed in code)
- {pattern}: {evidence file path}
- e.g. "Plugin architecture: src/plugins/*/plugin.json — each plugin self-registers"
- e.g. "Feature-folder organization under src/features/{name}/{component,api,store}.ts"

## Observations / Open Questions for Planning
- {anything noticed that affects domain identification}
- e.g. "auth and user-mgmt look intertwined — needs investigation to see if they should be 1 or 2 domains"
- e.g. "no clear domain boundary in src/lib/ — could be infra or shared utilities"
```

## What this is NOT

The survey is **not** a list of every directory and file. It's an *interpretive snapshot*: what kind of system is this, what shape is it, where would domains likely be cut.

Length target: **40-100 lines** for most projects. Longer is fine for monorepos with many packages.

## Hand-off to Phase 1

The orchestrator reads the survey it just wrote and uses it as the foundation for the doc plan. Domains in the plan must trace back to observations in the survey — no plucked-from-air domain names.
