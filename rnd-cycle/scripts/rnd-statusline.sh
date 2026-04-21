#!/usr/bin/env bash
# rnd-statusline.sh — Claude Code status line for R&D projects
# Reads session JSON from stdin, reads .rnd/ state from filesystem
# Output: Line 1 = session data, Line 2 = R&D state (if .rnd/ exists)

set -euo pipefail

# --- Read stdin JSON ---
INPUT=$(cat)

# Parse JSON fields (requires jq)
if ! command -v jq &>/dev/null; then
  echo "R&D statusline requires jq"
  exit 0
fi

PROJECT_DIR=$(echo "$INPUT" | jq -r '.workspace.project_dir // empty' 2>/dev/null)
MODEL=$(echo "$INPUT" | jq -r '.model.display_name // "unknown"' 2>/dev/null)
CONTEXT_PCT=$(echo "$INPUT" | jq -r '.context.used_percent // 0' 2>/dev/null)
COST=$(echo "$INPUT" | jq -r '.cost.total_cost_usd // 0' 2>/dev/null)
DURATION_MS=$(echo "$INPUT" | jq -r '.cost.total_duration_ms // 0' 2>/dev/null)

# Basename of project directory
PROJECT_NAME=$(basename "${PROJECT_DIR:-$(pwd)}")

# --- Context bar ---
# 10-char bar with color thresholds
PCT_INT=${CONTEXT_PCT%.*}  # truncate to integer
PCT_INT=${PCT_INT:-0}
FILLED=$((PCT_INT / 10))
EMPTY=$((10 - FILLED))

# ANSI colors
GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
RESET="\033[0m"

if [ "$PCT_INT" -lt 50 ]; then
  BAR_COLOR="$GREEN"
elif [ "$PCT_INT" -lt 70 ]; then
  BAR_COLOR="$YELLOW"
else
  BAR_COLOR="$RED"
fi

BAR="${BAR_COLOR}"
for ((i = 0; i < FILLED; i++)); do BAR+="█"; done
for ((i = 0; i < EMPTY; i++)); do BAR+="░"; done
BAR+="${RESET}"

# --- Duration formatting ---
DURATION_SEC=$((DURATION_MS / 1000))
if [ "$DURATION_SEC" -ge 3600 ]; then
  DURATION_FMT="$((DURATION_SEC / 3600))h$((DURATION_SEC % 3600 / 60))m"
elif [ "$DURATION_SEC" -ge 60 ]; then
  DURATION_FMT="$((DURATION_SEC / 60))m"
else
  DURATION_FMT="${DURATION_SEC}s"
fi

# --- Cost formatting ---
COST_FMT=$(printf "\$%.2f" "$COST" 2>/dev/null || echo "\$${COST}")

# --- Line 1: Session data ---
printf "📁 %s | [%s] %s%% %b | %s | ⏱ %s\n" \
  "$PROJECT_NAME" "$MODEL" "$PCT_INT" "$BAR" "$COST_FMT" "$DURATION_FMT"

# --- Line 2: R&D state (only if .rnd/ exists) ---
RND_DIR="${PROJECT_DIR:-.}/.rnd"
if [ ! -d "$RND_DIR" ]; then
  exit 0
fi

# Read current status from state.md
RND_STATUS=""
if [ -f "$RND_DIR/state.md" ]; then
  RND_STATUS=$(awk '/^## Current Status/{found=1; next} found && /^##/{exit} found && NF{print; exit}' "$RND_DIR/state.md" 2>/dev/null)
fi
RND_STATUS="${RND_STATUS:-Unknown}"

# Check for build wave progress
BUILD_INFO=""
if [ -f "$RND_DIR/live-progress.md" ]; then
  BUILD_INFO=$(grep -m1 'Wave' "$RND_DIR/live-progress.md" 2>/dev/null || true)
elif [ -f "$RND_DIR/build/progress.md" ]; then
  BUILD_INFO=$(awk '/^## /{found=1; next} found && NF{print; exit}' "$RND_DIR/build/progress.md" 2>/dev/null || true)
fi

# Count backlog items
BACKLOG_INFO=""
if [ -d "$RND_DIR/backlog" ]; then
  TOTAL=0
  CRITICAL=0
  HIGH=0

  for item in "$RND_DIR/backlog"/*.md; do
    [ -f "$item" ] || continue
    TOTAL=$((TOTAL + 1))
    if grep -q 'priority: critical' "$item" 2>/dev/null; then
      CRITICAL=$((CRITICAL + 1))
    elif grep -q 'priority: high' "$item" 2>/dev/null; then
      HIGH=$((HIGH + 1))
    fi
  done

  if [ "$TOTAL" -gt 0 ]; then
    BACKLOG_DETAIL=""
    [ "$CRITICAL" -gt 0 ] && BACKLOG_DETAIL+="${CRITICAL} critical"
    if [ "$HIGH" -gt 0 ]; then
      [ -n "$BACKLOG_DETAIL" ] && BACKLOG_DETAIL+=", "
      BACKLOG_DETAIL+="${HIGH} high"
    fi
    BACKLOG_INFO="Backlog: ${TOTAL}${BACKLOG_DETAIL:+ (${BACKLOG_DETAIL})}"
  fi
fi

# Assemble line 2
LINE2="[R&D] ${RND_STATUS}"
if [ -n "$BUILD_INFO" ]; then
  LINE2+=" | ${BUILD_INFO}"
fi
if [ -n "$BACKLOG_INFO" ]; then
  LINE2+=" | ${BACKLOG_INFO}"
fi

echo "$LINE2"
