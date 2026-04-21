# Coding Conventions

**Analysis Date:** [YYYY-MM-DD]

## Naming Patterns

**Files:**
- [Pattern — e.g., kebab-case for utility files, PascalCase for components]

**Functions:**
- [Pattern — e.g., camelCase, verb-first for actions like `getUser`, `handleSubmit`]

**Variables:**
- [Pattern — e.g., camelCase for locals, UPPER_SNAKE for constants]

**Types:**
- [Pattern — e.g., PascalCase, I-prefix for interfaces or not, T-prefix for generics or not]

## Code Style

**Formatting:**
- [Tool used — e.g., Prettier]
- [Key settings — cite config file path]

**Linting:**
- [Tool used — e.g., ESLint]
- [Key rules — cite config file path]

## Import Organization

**Order:**
1. [First group — e.g., Node built-ins]
2. [Second group — e.g., External packages]
3. [Third group — e.g., Internal modules with path aliases]
4. [Fourth group — e.g., Relative imports]

**Path Aliases:**
- [Aliases used — e.g., `@/` maps to `src/`, `~/` maps to root]

## Error Handling

**Patterns:**
- [How errors are handled — cite example files showing the pattern]

## Logging

**Framework:** [Tool or "console"]

**Patterns:**
- [When/how to log — cite example files]

## Comments

**When to Comment:**
- [Guidelines observed — e.g., complex logic only, no restating code, explain "why" not "what"]

**JSDoc/TSDoc:**
- [Usage pattern — e.g., all public exports, or none, or only complex functions]

## Function Design

**Size:** [Guidelines — e.g., prefer under 50 lines, extract early]

**Parameters:** [Pattern — e.g., options object for 3+ params, destructured args]

**Return Values:** [Pattern — e.g., explicit return types, Result/Either pattern, throw on error]

## Module Design

**Exports:** [Pattern — e.g., named exports for utilities, default for components]

**Barrel Files:** [Usage — e.g., `index.ts` re-exports in each directory, or not used]

---
*Convention analysis: [date]*
