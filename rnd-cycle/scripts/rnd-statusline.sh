#!/usr/bin/env bash
# rnd-statusline.sh — Claude Code status line for R&D projects
# Reads session JSON from stdin + .rnd/ state from filesystem
# Line 1: project │ model │ context bar │ cost │ duration
# Line 2: R&D state with phase, build progress, backlog (if .rnd/ exists)

set -euo pipefail

# --- Read stdin JSON ---
INPUT=$(cat)

if ! command -v jq &>/dev/null; then
  echo "R&D statusline requires jq"
  exit 0
fi

# --- Parse session data ---
PROJECT_DIR=$(echo "$INPUT" | jq -r '.workspace.project_dir // empty' 2>/dev/null)
MODEL=$(echo "$INPUT" | jq -r '.model.display_name // "unknown"' 2>/dev/null)
CTX_SIZE=$(echo "$INPUT" | jq -r '.context_window.context_window_size // 0' 2>/dev/null)
CTX_PCT=$(echo "$INPUT" | jq -r '.context_window.used_percentage // 0' 2>/dev/null)
COST=$(echo "$INPUT" | jq -r '.cost.total_cost_usd // 0' 2>/dev/null)
DURATION_MS=$(echo "$INPUT" | jq -r '.cost.total_duration_ms // 0' 2>/dev/null)

PROJECT_NAME=$(basename "${PROJECT_DIR:-$(pwd)}")

# --- ANSI colors ---
GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
CYAN="\033[36m"
DIM="\033[2m"
BOLD="\033[1m"
RESET="\033[0m"

# --- Context bar (35 chars wide) ---
PCT_INT=${CTX_PCT%.*}
PCT_INT=${PCT_INT:-0}

BAR_WIDTH=35
FILLED=$((PCT_INT * BAR_WIDTH / 100))
EMPTY=$((BAR_WIDTH - FILLED))
[ "$FILLED" -gt "$BAR_WIDTH" ] && FILLED=$BAR_WIDTH && EMPTY=0

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

# --- Context window size label ---
CTX_LABEL=""
if [ "$CTX_SIZE" -ge 1000000 ]; then
  CTX_LABEL=" (1M)"
elif [ "$CTX_SIZE" -ge 200000 ]; then
  CTX_LABEL=" (200K)"
fi

# --- Duration ---
DURATION_SEC=$((DURATION_MS / 1000))
if [ "$DURATION_SEC" -ge 3600 ]; then
  DURATION_FMT="$((DURATION_SEC / 3600))h$((DURATION_SEC % 3600 / 60))m"
elif [ "$DURATION_SEC" -ge 60 ]; then
  DURATION_FMT="$((DURATION_SEC / 60))m"
else
  DURATION_FMT="${DURATION_SEC}s"
fi

# --- Cost ---
COST_FMT=$(printf "\$%.2f" "$COST" 2>/dev/null || echo "\$${COST}")

# --- Line 1: Session data ---
printf "${BOLD}📁 %s${RESET} │ %s%s │ %b ${YELLOW}%s%%${RESET} │ ${CYAN}%s${RESET} │ ${DIM}⏱ %s${RESET}\n" \
  "$PROJECT_NAME" "$MODEL" "$CTX_LABEL" "$BAR" "$PCT_INT" "$COST_FMT" "$DURATION_FMT"

# --- Line 2: R&D state (only if .rnd/ exists) ---
RND_DIR="${PROJECT_DIR:-.}/.rnd"
if [ ! -d "$RND_DIR" ]; then
  exit 0
fi

# --- Phase / status ---
PHASE=""
if [ -f "$RND_DIR/state.md" ]; then
  # Try v2 header first, then v1
  PHASE=$(awk '/^## Current Status/{found=1; next} found && /^##/{exit} found && NF{print; exit}' "$RND_DIR/state.md" 2>/dev/null)
  if [ -z "$PHASE" ]; then
    PHASE=$(awk '/^## Current Phase/{found=1; next} found && /^##/{exit} found && NF{print; exit}' "$RND_DIR/state.md" 2>/dev/null)
  fi
fi
# Truncate long phase text
if [ ${#PHASE} -gt 60 ]; then
  PHASE="${PHASE:0:57}..."
fi
PHASE="${PHASE:-No status}"

# --- Interrupted build check (highest priority) ---
INTERRUPTED=false
if [ -f "$RND_DIR/live-progress.md" ]; then
  INTERRUPTED=true
  WAVE_INFO=$(grep -m1 -oP 'Wave \d+/\d+' "$RND_DIR/live-progress.md" 2>/dev/null || echo "")
fi

# --- Build progress ---
BUILD_PROGRESS=""
if [ -f "$RND_DIR/build/progress.md" ]; then
  BUILD_STATUS=$(grep -m1 'Status:' "$RND_DIR/build/progress.md" 2>/dev/null | sed 's/.*Status: *//' || true)
  if [ -n "$BUILD_STATUS" ]; then
    BUILD_PROGRESS="$BUILD_STATUS"
  fi
fi

# --- Requirement count ---
REQ_COUNT=""
if [ -f "$RND_DIR/spec/spec.md" ]; then
  COUNT=$(grep -c 'REQ-' "$RND_DIR/spec/spec.md" 2>/dev/null || echo "0")
  [ "$COUNT" -gt 0 ] && REQ_COUNT="${COUNT} reqs"
fi

# --- Backlog ---
BACKLOG=""
if [ -d "$RND_DIR/backlog" ]; then
  TOTAL=0; CRITICAL=0; HIGH=0
  shopt -s nullglob 2>/dev/null
  for item in "$RND_DIR/backlog"/*.md; do
    TOTAL=$((TOTAL + 1))
    grep -q 'priority: critical' "$item" 2>/dev/null && CRITICAL=$((CRITICAL + 1))
    grep -q 'priority: high' "$item" 2>/dev/null && HIGH=$((HIGH + 1))
  done
  shopt -u nullglob 2>/dev/null
  if [ "$TOTAL" -gt 0 ]; then
    DETAIL=""
    [ "$CRITICAL" -gt 0 ] && DETAIL="${CRITICAL} critical"
    if [ "$HIGH" -gt 0 ]; then
      [ -n "$DETAIL" ] && DETAIL+=", "
      DETAIL+="${HIGH} high"
    fi
    BACKLOG="${TOTAL}${DETAIL:+ (${DETAIL})}"
  fi
fi

# --- Decision count ---
DECISION_COUNT=""
if [ -d "$RND_DIR/decisions" ]; then
  COUNT=$(find "$RND_DIR/decisions" -maxdepth 1 -name '*.md' ! -name 'index.md' 2>/dev/null | wc -l | tr -d ' ')
  [ "$COUNT" -gt 0 ] && DECISION_COUNT="${COUNT}"
fi

# --- Assemble Line 2 ---
if [ "$INTERRUPTED" = true ]; then
  # Interrupted build — red alert, most urgent
  LINE2="${RED}🔴 INTERRUPTED${RESET}"
  [ -n "$WAVE_INFO" ] && LINE2+=" ${WAVE_INFO}"
  LINE2+=" ${DIM}— resume /rnd:c-build${RESET}"
  [ -n "$BACKLOG" ] && LINE2+=" │ ${YELLOW}⚠️ ${BACKLOG} backlog${RESET}"
else
  # Normal state
  LINE2="${CYAN}[R&D]${RESET} ${PHASE}"

  # Add segments
  SEGMENTS=""
  [ -n "$REQ_COUNT" ] && SEGMENTS+=" │ ${DIM}📋 ${REQ_COUNT}${RESET}"
  if [ -n "$BACKLOG" ]; then
    if [ "$CRITICAL" -gt 0 ]; then
      SEGMENTS+=" │ ${RED}⚠️ ${BACKLOG} backlog${RESET}"
    else
      SEGMENTS+=" │ ${YELLOW}⚠️ ${BACKLOG} backlog${RESET}"
    fi
  fi
  [ -n "$DECISION_COUNT" ] && SEGMENTS+=" │ ${DIM}🔒 ${DECISION_COUNT} decisions${RESET}"

  LINE2+="${SEGMENTS}"
fi

printf "%b\n" "$LINE2"
