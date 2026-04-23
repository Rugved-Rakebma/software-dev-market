#!/usr/bin/env bash
# rnd-command-tracker.sh — UserPromptSubmit hook for R&D projects
# Fires on EVERY user prompt (matchers not supported for this hook type)
# Exits immediately if not an /rnd: command — minimal overhead
# Appends command to session file + writes .last-command for statusline

set -euo pipefail

INPUT=$(cat)

# Fast exit: check if prompt contains /rnd:
PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty' 2>/dev/null)
echo "$PROMPT" | grep -q '/rnd:' || exit 0

# Not an R&D project
[ -d ".rnd" ] || exit 0

# Extract command name (first /rnd:word match)
CMD=$(echo "$PROMPT" | grep -oE '/rnd:[a-zA-Z0-9_:-]+' | head -1)
[ -z "$CMD" ] && exit 0

TIMESTAMP=$(date +%Y-%m-%dT%H:%M:%S)
TIME_SHORT=$(date +%H:%M)

# --- Write to session file ---
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty' 2>/dev/null)
if [ -n "$SESSION_ID" ] && [ -f ".rnd/sessions/${SESSION_ID}.md" ]; then
  echo "- ${TIME_SHORT} ${CMD}" >> ".rnd/sessions/${SESSION_ID}.md"
fi

# --- Write quick-access marker for statusline ---
echo "${CMD} ${TIMESTAMP}" > ".rnd/.last-command"

exit 0
