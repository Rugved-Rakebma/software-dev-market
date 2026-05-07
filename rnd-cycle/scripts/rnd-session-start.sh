#!/usr/bin/env bash
# rnd-session-start.sh — SessionStart hook for R&D projects
# 1. Creates session tracking file at .rnd/sessions/{session_id}.md
# 2. Outputs progressive disclosure context for the agent
# Exit silently if not an R&D project (no .rnd/ directory)

set -euo pipefail

# --- Read stdin JSON ---
INPUT=$(cat)

RND_DIR=".rnd"

# Not an R&D project — exit silently
if [ ! -d "$RND_DIR" ]; then
  exit 0
fi

# --- Parse session data ---
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty' 2>/dev/null)
MODEL=$(echo "$INPUT" | jq -r '.model.display_name // "unknown"' 2>/dev/null)
TIMESTAMP=$(date +%Y-%m-%dT%H:%M:%S)

# --- Create session tracking ---
if [ -n "$SESSION_ID" ]; then
  mkdir -p "$RND_DIR/sessions"

  SESSION_FILE="$RND_DIR/sessions/${SESSION_ID}.md"
  cat > "$SESSION_FILE" << EOF
---
session_id: ${SESSION_ID}
started: ${TIMESTAMP}
model: ${MODEL}
status: active
ended: null
---

## Commands
EOF

  # Write active session marker for statusline quick access
  echo "$SESSION_ID" > "$RND_DIR/.active-session"
fi

# --- Extract project name ---
PROJECT_NAME=""
if [ -f "$RND_DIR/state.md" ]; then
  PROJECT_NAME=$(grep -m1 '^# Project:' "$RND_DIR/state.md" 2>/dev/null | sed 's/^# Project: *//' || true)
fi
PROJECT_NAME="${PROJECT_NAME:-$(basename "$(pwd)")}"

echo "━━━ R&D: ${PROJECT_NAME} ━━━"
echo ""

# --- Priority 2: Previous session summary ---
if [ -n "$SESSION_ID" ] && [ -d "$RND_DIR/sessions" ]; then
  # Find the most recent ENDED session (not current one)
  PREV_SESSION=$(grep -rl 'status: ended' "$RND_DIR/sessions"/*.md 2>/dev/null | while read -r f; do
    [ "$(basename "$f" .md)" = "$SESSION_ID" ] && continue
    echo "$f"
  done | head -1 || true)

  if [ -n "$PREV_SESSION" ]; then
    PREV_CMDS=$(grep -c '^- ' "$PREV_SESSION" 2>/dev/null || echo "0")
    PREV_ENDED=$(grep -m1 '^ended:' "$PREV_SESSION" 2>/dev/null | sed 's/^ended: *//' || true)
    if [ "$PREV_CMDS" -gt 0 ]; then
      LAST_CMD=$(grep '^- ' "$PREV_SESSION" 2>/dev/null | tail -1 | sed 's/^- [0-9:T-]* //' || true)
      echo "Previous session: ${PREV_CMDS} commands, last: ${LAST_CMD}"
      echo ""
    fi
  fi
fi

# --- Priority 3: Current status from state.md ---
if [ -f "$RND_DIR/state.md" ]; then
  # Try v2 header first, then v1
  STATUS=$(awk '/^## Current Status/{found=1; next} found && /^##/{exit} found && NF{print}' "$RND_DIR/state.md" 2>/dev/null || true)
  if [ -z "$STATUS" ]; then
    STATUS=$(awk '/^## Current Phase/{found=1; next} found && /^##/{exit} found && NF{print}' "$RND_DIR/state.md" 2>/dev/null || true)
  fi
  if [ -n "$STATUS" ]; then
    echo "Status: ${STATUS}"
    echo ""
  fi
fi

# --- Priority 4: Backlog summary ---
BACKLOG_TOTAL=0
BACKLOG_BREAKDOWN=""
if [ -d "$RND_DIR/backlog" ]; then
  CRITICAL=0; HIGH=0; MEDIUM=0

  shopt -s nullglob 2>/dev/null
  for item in "$RND_DIR/backlog"/*.md; do
    BACKLOG_TOTAL=$((BACKLOG_TOTAL + 1))
    PRIORITY=$(grep -m1 '^priority:' "$item" 2>/dev/null | sed 's/^priority: *//' || true)
    case "$PRIORITY" in
      critical) CRITICAL=$((CRITICAL + 1)) ;;
      high)     HIGH=$((HIGH + 1)) ;;
      medium)   MEDIUM=$((MEDIUM + 1)) ;;
    esac
  done
  shopt -u nullglob 2>/dev/null

  if [ "$BACKLOG_TOTAL" -gt 0 ]; then
    [ "$CRITICAL" -gt 0 ] && BACKLOG_BREAKDOWN+="${CRITICAL} critical"
    if [ "$HIGH" -gt 0 ]; then
      [ -n "$BACKLOG_BREAKDOWN" ] && BACKLOG_BREAKDOWN+=", "
      BACKLOG_BREAKDOWN+="${HIGH} high"
    fi
  fi
fi

# --- Priority 5: Artifact inventory ---
echo "Artifacts:"

if [ -f "$RND_DIR/spec/spec.md" ]; then
  echo "  Spec: ✅ .rnd/spec/spec.md"
else
  echo "  Spec: ❌ missing"
fi

if [ -f "$RND_DIR/architecture/current.md" ]; then
  echo "  Architecture: ✅ .rnd/architecture/current.md"
else
  echo "  Architecture: ❌ missing"
fi

PLAN_COUNT=0
if [ -d "$RND_DIR/build/plans" ]; then
  shopt -s nullglob 2>/dev/null
  for f in "$RND_DIR/build/plans"/*/*.md; do PLAN_COUNT=$((PLAN_COUNT + 1)); done
  shopt -u nullglob 2>/dev/null
fi
if [ "$PLAN_COUNT" -gt 0 ]; then
  echo "  Plans: ✅ ${PLAN_COUNT} plans"
else
  echo "  Plans: ❌ missing"
fi

if [ -f "$RND_DIR/build/progress.md" ]; then
  if grep -qm1 '^status: in-progress' "$RND_DIR/build/progress.md" 2>/dev/null; then
    echo "  Build: ⏳ in progress"
  else
    echo "  Build: ✅ complete"
  fi
else
  echo "  Build: ❌ not started"
fi

if [ "$BACKLOG_TOTAL" -gt 0 ]; then
  echo "  Backlog: ${BACKLOG_TOTAL} open${BACKLOG_BREAKDOWN:+ (${BACKLOG_BREAKDOWN})}"
fi

echo ""

# --- Priority 6: Recent activity ---
if [ -f "$RND_DIR/state.md" ]; then
  ACTIVITY=$(awk '/^## Recent Activity/{found=1; next} found && /^##/{exit} found && /^- /{print}' "$RND_DIR/state.md" 2>/dev/null | head -5 || true)
  if [ -n "$ACTIVITY" ]; then
    echo "Recent Activity:"
    echo "$ACTIVITY" | while IFS= read -r line; do
      echo "  $line"
    done
    echo ""
  fi
fi

# --- Priority 7: Locked decisions ---
if [ -f "$RND_DIR/decisions/index.md" ]; then
  DECISIONS=$(awk 'NR > 3 && /\|/ && !/^[[:space:]]*$/ {
    gsub(/^[[:space:]]*\|[[:space:]]*/, "")
    split($0, cols, /[[:space:]]*\|[[:space:]]*/)
    if (cols[3] != "" && cols[3] != "Decision") {
      printf "  - ADR-%s: %s\n", cols[1], cols[3]
    }
  }' "$RND_DIR/decisions/index.md" 2>/dev/null || true)

  if [ -n "$DECISIONS" ]; then
    echo "Locked Decisions:"
    echo "$DECISIONS"
    echo ""
  fi
fi
