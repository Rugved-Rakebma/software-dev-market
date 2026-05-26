#!/usr/bin/env bash
# rnd-statusline.sh — Claude Code status line for R&D projects
# Line 1: 📦 project • 🌿 branch • model context-bar pct% • cost • duration
# Line 2: Overview: 📝 specs • 🏗️ arch • 📐 plans • ⚠️ backlog • 🔒 decisions

set -euo pipefail

INPUT=$(cat)

if ! command -v jq &>/dev/null; then
  echo "R&D statusline requires jq"
  exit 0
fi

# --- Parse session data ---
PROJECT_DIR=$(echo "$INPUT" | jq -r '.workspace.project_dir // empty' 2>/dev/null)
MODEL=$(echo "$INPUT" | jq -r '.model.display_name // "unknown"' 2>/dev/null)
CTX_PCT=$(echo "$INPUT" | jq -r '.context_window.used_percentage // 0' 2>/dev/null)
COST=$(echo "$INPUT" | jq -r '.cost.total_cost_usd // 0' 2>/dev/null)
DURATION_MS=$(echo "$INPUT" | jq -r '.cost.total_duration_ms // 0' 2>/dev/null)

PROJECT_NAME=$(basename "${PROJECT_DIR:-$(pwd)}")

# --- Git branch ---
BRANCH=""
if [ -n "$PROJECT_DIR" ] && [ -d "$PROJECT_DIR/.git" ]; then
  BRANCH=$(git -C "$PROJECT_DIR" --no-optional-locks branch --show-current 2>/dev/null || true)
fi
BRANCH="${BRANCH:-—}"

# --- Colors (matte 256-color palette) ---
ORANGE="\033[38;5;208m"
GREEN="\033[38;5;114m"
YELLOW="\033[38;5;179m"
RED="\033[38;5;167m"
CYAN="\033[38;5;116m"
BLUE="\033[38;5;110m"
MAGENTA="\033[38;5;139m"
WHITE="\033[97m"
DIM="\033[2m"
BOLD="\033[1m"
RESET="\033[0m"
SEP="${DIM} • ${RESET}"

# --- Context bar (30 chars) ---
PCT_INT=${CTX_PCT%.*}
PCT_INT=${PCT_INT:-0}

BAR_WIDTH=30
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

# =====================================================================
# LINE 1: 📦 project • 🌿 branch • model bar pct% • cost • duration
# =====================================================================
printf "${ORANGE}${BOLD}📦 %s${RESET}${SEP}${GREEN}🌿 %s${RESET}${SEP}${BAR_COLOR}${BOLD}%s${RESET} %b ${BAR_COLOR}%s%%${RESET}${SEP}${CYAN}%s${RESET}${SEP}${MAGENTA}${DIM}⏱ %s${RESET}\n" \
  "$PROJECT_NAME" "$BRANCH" "$MODEL" "$BAR" "$PCT_INT" "$COST_FMT" "$DURATION_FMT"

# =====================================================================
# LINE 2: Overview (only if .rnd/ exists)
# =====================================================================
RND_DIR="${PROJECT_DIR:-.}/.rnd"
if [ ! -d "$RND_DIR" ]; then
  exit 0
fi

# --- Count specs ---
SPEC_COUNT=0
if [ -d "$RND_DIR/spec" ]; then
  shopt -s nullglob 2>/dev/null
  for f in "$RND_DIR/spec"/*.md; do SPEC_COUNT=$((SPEC_COUNT + 1)); done
  shopt -u nullglob 2>/dev/null
fi

# --- Count architecture docs (current + history) ---
ARCH_COUNT=0
[ -f "$RND_DIR/architecture/current.md" ] && ARCH_COUNT=$((ARCH_COUNT + 1))
if [ -d "$RND_DIR/architecture/history" ]; then
  shopt -s nullglob 2>/dev/null
  for f in "$RND_DIR/architecture/history"/*.md; do ARCH_COUNT=$((ARCH_COUNT + 1)); done
  shopt -u nullglob 2>/dev/null
fi

# --- Count plans ---
PLAN_COUNT=0
if [ -d "$RND_DIR/build/plans" ]; then
  shopt -s nullglob 2>/dev/null
  for f in "$RND_DIR/build/plans"/*/*.md; do PLAN_COUNT=$((PLAN_COUNT + 1)); done
  shopt -u nullglob 2>/dev/null
fi

# --- Count pending plans (only meaningful once a build has started) ---
PENDING_PLANS=0
PROGRESS_FILE="$RND_DIR/build/progress.md"
if [ -f "$PROGRESS_FILE" ] && [ "$PLAN_COUNT" -gt 0 ]; then
  # New format: count "- " entries under ## Completed and ## Deferred sections
  COMPLETED_PLANS=$(awk '/^## Completed/{f=1;next} f && /^## /{exit} f && /^- /{c++} END{print c+0}' "$PROGRESS_FILE" 2>/dev/null)
  COMPLETED_PLANS=${COMPLETED_PLANS:-0}
  DEFERRED_PLANS=$(awk '/^## Deferred/{f=1;next} f && /^## /{exit} f && /^- /{c++} END{print c+0}' "$PROGRESS_FILE" 2>/dev/null)
  DEFERRED_PLANS=${DEFERRED_PLANS:-0}
  # Legacy fallback: markdown table rows containing "completed" / "deferred"
  if [ "$COMPLETED_PLANS" -eq 0 ]; then
    COMPLETED_PLANS=$(grep -ic '^|.*| *completed *|' "$PROGRESS_FILE" 2>/dev/null || true)
    COMPLETED_PLANS=${COMPLETED_PLANS:-0}
  fi
  if [ "$DEFERRED_PLANS" -eq 0 ]; then
    DEFERRED_PLANS=$(grep -ic '^|.*| *deferred *|' "$PROGRESS_FILE" 2>/dev/null || true)
    DEFERRED_PLANS=${DEFERRED_PLANS:-0}
  fi
  PENDING_PLANS=$((PLAN_COUNT - COMPLETED_PLANS - DEFERRED_PLANS))
  [ "$PENDING_PLANS" -lt 0 ] && PENDING_PLANS=0
fi

# --- Count backlog ---
BACKLOG_TOTAL=0; BACKLOG_CRITICAL=0; BACKLOG_HIGH=0; BACKLOG_STALE=0
STALE_DAYS=30
NOW_EPOCH=$(date "+%s" 2>/dev/null || echo 0)
if [ -d "$RND_DIR/backlog" ]; then
  shopt -s nullglob 2>/dev/null
  for item in "$RND_DIR/backlog"/*.md; do
    BACKLOG_TOTAL=$((BACKLOG_TOTAL + 1))
    grep -q 'priority: critical' "$item" 2>/dev/null && BACKLOG_CRITICAL=$((BACKLOG_CRITICAL + 1))
    grep -q 'priority: high' "$item" 2>/dev/null && BACKLOG_HIGH=$((BACKLOG_HIGH + 1))
    # Stale detection — discovered > STALE_DAYS ago
    DISCOVERED=$(awk -F': *' '/^discovered:/ {gsub(/[ \t]+$/, "", $2); print $2; exit}' "$item" 2>/dev/null)
    if [ -n "$DISCOVERED" ] && [ "$NOW_EPOCH" -gt 0 ]; then
      DISC_EPOCH=$(date -j -f "%Y-%m-%d" "$DISCOVERED" "+%s" 2>/dev/null || date -d "$DISCOVERED" "+%s" 2>/dev/null || echo 0)
      if [ "$DISC_EPOCH" -gt 0 ]; then
        AGE_DAYS=$(( (NOW_EPOCH - DISC_EPOCH) / 86400 ))
        [ "$AGE_DAYS" -gt "$STALE_DAYS" ] && BACKLOG_STALE=$((BACKLOG_STALE + 1))
      fi
    fi
  done
  shopt -u nullglob 2>/dev/null
fi

# --- Count research reports ---
RESEARCH_COUNT=0
if [ -d "$RND_DIR/research" ]; then
  shopt -s nullglob 2>/dev/null
  for f in "$RND_DIR/research"/*.md; do RESEARCH_COUNT=$((RESEARCH_COUNT + 1)); done
  shopt -u nullglob 2>/dev/null
fi

# --- Count decisions ---
DECISION_COUNT=0
if [ -d "$RND_DIR/decisions" ]; then
  shopt -s nullglob 2>/dev/null
  for f in "$RND_DIR/decisions"/*.md; do
    [ "$(basename "$f")" = "index.md" ] && continue
    DECISION_COUNT=$((DECISION_COUNT + 1))
  done
  shopt -u nullglob 2>/dev/null
fi

# --- Assemble Line 2 ---
SEGMENTS=""

[ "$SPEC_COUNT" -gt 0 ] && SEGMENTS+="${WHITE}📝 ${SPEC_COUNT} specs${RESET}"
if [ "$ARCH_COUNT" -gt 0 ]; then
  [ -n "$SEGMENTS" ] && SEGMENTS+="${SEP}"
  SEGMENTS+="${WHITE}🏗️ ${ARCH_COUNT} arch${RESET}"
fi
if [ "$RESEARCH_COUNT" -gt 0 ]; then
  [ -n "$SEGMENTS" ] && SEGMENTS+="${SEP}"
  SEGMENTS+="${WHITE}📚 ${RESEARCH_COUNT} research${RESET}"
fi
if [ "$PLAN_COUNT" -gt 0 ]; then
  [ -n "$SEGMENTS" ] && SEGMENTS+="${SEP}"
  SEGMENTS+="${WHITE}📐 ${PLAN_COUNT} plans${RESET}"
  if [ "$PENDING_PLANS" -gt 0 ]; then
    SEGMENTS+=" ${DIM}[${PENDING_PLANS} pending]${RESET}"
  fi
fi
if [ "$BACKLOG_TOTAL" -gt 0 ]; then
  [ -n "$SEGMENTS" ] && SEGMENTS+="${SEP}"
  SEGMENTS+="${WHITE}📬 ${BACKLOG_TOTAL} backlog${RESET}"
  ANNOTS=""
  if [ "$BACKLOG_CRITICAL" -gt 0 ]; then
    ANNOTS+="${BACKLOG_CRITICAL} critical"
  elif [ "$BACKLOG_HIGH" -gt 0 ]; then
    ANNOTS+="${BACKLOG_HIGH} high"
  fi
  if [ "$BACKLOG_STALE" -gt 0 ]; then
    [ -n "$ANNOTS" ] && ANNOTS+=" · "
    ANNOTS+="${BACKLOG_STALE} stale"
  fi
  [ -n "$ANNOTS" ] && SEGMENTS+=" \033[38;5;180m(${ANNOTS})${RESET}"
fi
if [ "$DECISION_COUNT" -gt 0 ]; then
  [ -n "$SEGMENTS" ] && SEGMENTS+="${SEP}"
  SEGMENTS+="${WHITE}🔒 ${DECISION_COUNT} decisions${RESET}"
fi

# --- Last command ---
LAST_CMD_DISPLAY=""
if [ -f "$RND_DIR/.last-command" ]; then
  LAST_NAME=$(awk '{print $1}' "$RND_DIR/.last-command" 2>/dev/null)
  if [ -n "$LAST_NAME" ]; then
    LAST_CMD_DISPLAY="${WHITE}⚡ ${LAST_NAME}${RESET}"
  fi
fi

if [ -n "$SEGMENTS" ]; then
  LINE2="${DIM}┗${RESET} ${SEGMENTS}"
  [ -n "$LAST_CMD_DISPLAY" ] && LINE2+="${SEP}${LAST_CMD_DISPLAY}"
else
  LINE2="${DIM}┗ empty — run /rnd:spec${RESET}"
fi

printf "%b\n" "$LINE2"
