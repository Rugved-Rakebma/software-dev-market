#!/usr/bin/env bash
# rnd-session-stop.sh — Stop hook for R&D projects
# Marks session as ended in the session tracking file
# Removes active session marker

set -euo pipefail

INPUT=$(cat)

# Not an R&D project
[ -d ".rnd" ] || exit 0

SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty' 2>/dev/null)
[ -z "$SESSION_ID" ] && exit 0

TIMESTAMP=$(date +%Y-%m-%dT%H:%M:%S)
SESSION_FILE=".rnd/sessions/${SESSION_ID}.md"

# Update session file frontmatter
if [ -f "$SESSION_FILE" ]; then
  # Replace status and ended fields in frontmatter
  if command -v sed &>/dev/null; then
    sed -i '' "s/^status: active/status: ended/" "$SESSION_FILE" 2>/dev/null || true
    sed -i '' "s/^ended: null/ended: ${TIMESTAMP}/" "$SESSION_FILE" 2>/dev/null || true
  fi
fi

# Remove active session marker
rm -f ".rnd/.active-session"

exit 0
