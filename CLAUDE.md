# software-dev-market — Plugin Marketplace

Personal Claude Code plugin marketplace. Ships one plugin: **`rnd` v3** from
`./rnd/`. `rnd-cycle/` is the retired v2 — reference only, not listed in the
marketplace, never edited except for archaeology.

## Structure

```
software-dev-market/
├── .claude-plugin/marketplace.json    # one entry: rnd → ./rnd/ (v3.0.0)
├── rnd/                               # THE plugin — dev guide at rnd/CLAUDE.md
│   ├── .claude-plugin/plugin.json
│   ├── commands/   (5)   design · build · verify · backlog · docs
│   ├── agents/     (4)   dev-manager · coder · code-reviewer · qa-lead
│   ├── skills/     (3)   map · write-doc · write-surface  (context: fork)
│   ├── scripts/rnd.py    the CLI — every schema, every gate
│   ├── hooks/            PostToolUse drift hook
│   └── templates/        standards canon + record/backlog/config seeds
└── rnd-cycle/                         # v2, condemned by audit — see rnd/CLAUDE.md § Design lineage
```

## Working on the plugin

- **Dev guide, schemas, testing:** `rnd/CLAUDE.md`. Start there.
- **Standards canon** (`rnd/templates/standards/`) is byte-diffed by
  `rnd standards` in every consuming repo — a canon edit is a breaking change
  for all of them; bump the minor version and rerun `standards --write`
  downstream.
- **Version** lives in `rnd/.claude-plugin/plugin.json` AND the marketplace
  entry — bump both together.
- Installed copies are **pinned cache snapshots** — after pushing, consumers
  need `/plugin marketplace update` to pick changes up.

## Plugin-packaging facts (hard-won, still true)

- Plugin `name` in plugin.json sets the command namespace (`/rnd:*`), not the
  directory name.
- `commands/`, `agents/`, `skills/`, `hooks/hooks.json` are auto-discovered —
  plugin.json declares no paths.
- `${CLAUDE_PLUGIN_ROOT}` works inside plugin-owned files (commands, hooks.json,
  skills); it does NOT work in user-space config like settings.json.
- Hook input arrives as stdin JSON; PostToolUse feedback channel is exit 2 +
  stderr (cannot block — the tool already ran). Hooks get a minimal PATH —
  export a real one first. Every error path exits 0 (fail open).
- Agent frontmatter: `model`, `skills` (preload) are honored;
  `permissionMode` is static per agent — no mid-run mode flips.
- Skill frontmatter `context: fork` + `agent:` runs the skill body as an
  isolated subagent's prompt.
