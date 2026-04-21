#!/usr/bin/env bash
# rnd-session-start.sh — SessionStart hook for R&D projects
# Auto-loads critical .rnd/ context into new Claude Code sessions
# Provides orientation, not full context — agents read full files when needed
# Exit silently if not an R&D project (no .rnd/ directory)

set -euo pipefail

RND_DIR=".rnd"

# Not an R&D project — exit silently
if [ ! -d "$RND_DIR" ]; then
  exit 0
fi

# --- Extract project name from state.md ---
PROJECT_NAME=""
if [ -f "$RND_DIR/state.md" ]; then
  PROJECT_NAME=$(grep -m1 '^# Project:' "$RND_DIR/state.md" 2>/dev/null | sed 's/^# Project: *//' || true)
fi
PROJECT_NAME="${PROJECT_NAME:-$(basename "$(pwd)")}"

echo "━━━ R&D: ${PROJECT_NAME} ━━━"
echo ""

# --- Priority 1: Interrupted build warning ---
if [ -f "$RND_DIR/live-progress.md" ]; then
  echo "⚠️  INTERRUPTED BUILD — resume with /rnd:c-build"
  # Extract wave info if available
  WAVE_INFO=$(grep -m1 'Wave' "$RND_DIR/live-progress.md" 2>/dev/null || true)
  if [ -n "$WAVE_INFO" ]; then
    echo "   ${WAVE_INFO}"
  fi
  echo ""
fi

# --- Priority 2: Current status from state.md ---
if [ -f "$RND_DIR/state.md" ]; then
  STATUS=$(awk '/^## Current Status/{found=1; next} found && /^##/{exit} found && NF{print}' "$RND_DIR/state.md" 2>/dev/null || true)
  if [ -n "$STATUS" ]; then
    echo "Status: ${STATUS}"
    echo ""
  fi
fi

# --- Priority 3: Backlog summary ---
if [ -d "$RND_DIR/backlog" ]; then
  TOTAL=0
  CRITICAL=0
  HIGH=0
  MEDIUM=0
  LOW=0

  for item in "$RND_DIR/backlog"/*.md; do
    [ -f "$item" ] || continue
    TOTAL=$((TOTAL + 1))
    PRIORITY=$(grep -m1 '^priority:' "$item" 2>/dev/null | sed 's/^priority: *//' || true)
    case "$PRIORITY" in
      critical) CRITICAL=$((CRITICAL + 1)) ;;
      high)     HIGH=$((HIGH + 1)) ;;
      medium)   MEDIUM=$((MEDIUM + 1)) ;;
      low)      LOW=$((LOW + 1)) ;;
    esac
  done

  if [ "$TOTAL" -gt 0 ]; then
    BREAKDOWN=""
    [ "$CRITICAL" -gt 0 ] && BREAKDOWN+="${CRITICAL} critical"
    if [ "$HIGH" -gt 0 ]; then
      [ -n "$BREAKDOWN" ] && BREAKDOWN+=", "
      BREAKDOWN+="${HIGH} high"
    fi
    if [ "$MEDIUM" -gt 0 ]; then
      [ -n "$BREAKDOWN" ] && BREAKDOWN+=", "
      BREAKDOWN+="${MEDIUM} medium"
    fi
    # Skip low in summary for brevity
  fi
fi

# --- Priority 4: Artifact inventory ---
echo "Artifacts:"

# Spec
if [ -f "$RND_DIR/spec/spec.md" ]; then
  echo "  Spec: ✅ .rnd/spec/spec.md"
else
  echo "  Spec: ❌ missing"
fi

# Architecture
if [ -f "$RND_DIR/architecture/current.md" ]; then
  echo "  Architecture: ✅ .rnd/architecture/current.md"
else
  echo "  Architecture: ❌ missing"
fi

# Plans
PLAN_COUNT=0
WAVE_COUNT=0
if [ -d "$RND_DIR/build/plans" ]; then
  PLAN_COUNT=$(find "$RND_DIR/build/plans" -name '*-PLAN.md' -o -name '*.md' 2>/dev/null | grep -v '^$' | wc -l | tr -d ' ')
  if [ "$PLAN_COUNT" -gt 0 ]; then
    # Count unique wave numbers from plan frontmatter
    WAVE_COUNT=$(grep -rh '^wave:' "$RND_DIR/build/plans/" 2>/dev/null | sort -u | wc -l | tr -d ' ')
    echo "  Plans: ✅ ${PLAN_COUNT} plans, ${WAVE_COUNT} waves"
  else
    echo "  Plans: ❌ missing"
  fi
else
  echo "  Plans: ❌ missing"
fi

# Build progress
if [ -f "$RND_DIR/live-progress.md" ]; then
  echo "  Build: ⏳ in progress (see interrupted build warning above)"
elif [ -f "$RND_DIR/build/progress.md" ]; then
  echo "  Build: ✅ complete"
else
  echo "  Build: ❌ not started"
fi

# Backlog (using counts from Priority 3)
if [ "${TOTAL:-0}" -gt 0 ]; then
  echo "  Backlog: ${TOTAL} open${BREAKDOWN:+ (${BREAKDOWN})}"
fi

echo ""

# --- Priority 2 continued: Recent activity ---
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

# --- Priority 5: Locked decisions ---
if [ -f "$RND_DIR/decisions/index.md" ]; then
  # Parse decision table — skip header rows (first 3 lines: header, separator, blank)
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
