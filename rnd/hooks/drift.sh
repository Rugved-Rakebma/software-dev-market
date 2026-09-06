#!/usr/bin/env bash
# drift.sh — the living-docs maintenance hook (rnd plugin).
#
# Fires after every Edit/Write. If the edited file is SOURCE that living docs
# cite by anchor, feed the model a structured instruction to verify drift and
# align those docs in the same change. This closes the hole the docs system
# names: tier CLAUDE.md files load when someone edits a DOC, never when someone
# edits the code that falsifies it.
#
# Exit 2 + stderr = message reaches the model (PostToolUse cannot block — the
# edit already happened; this is feedback, not a gate). Every failure path
# exits 0: this hook must never break an edit pipeline.

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

command -v jq >/dev/null 2>&1 || exit 0
command -v python3 >/dev/null 2>&1 || exit 0

input=$(cat 2>/dev/null) || exit 0
file=$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
[ -n "$file" ] || exit 0

# Docs editing themselves must not re-trigger; neither should non-repo paths.
case "$file" in
  */docs/*|*/.rnd/*|*.md) exit 0 ;;
esac

# Find the repo root from the edited file's directory.
dir=$(dirname "$file")
repo=""
probe="$dir"
while [ "$probe" != "/" ] && [ -n "$probe" ]; do
  if [ -d "$probe/.rnd" ] || [ -d "$probe/.git" ]; then repo="$probe"; break; fi
  probe=$(dirname "$probe")
done
[ -n "$repo" ] || exit 0
# Only repos that use the system.
[ -d "$repo/docs/living" ] || exit 0

rnd_py="${CLAUDE_PLUGIN_ROOT:-$(dirname "$0")/..}/scripts/rnd.py"
[ -f "$rnd_py" ] || exit 0

hits=$(cd "$repo" 2>/dev/null && python3 "$rnd_py" affected "$file" 2>/dev/null)
[ -n "$hits" ] || exit 0

n=$(printf '%s\n' "$hits" | wc -l | tr -d ' ')
{
  echo "ROUTINE living-docs check — not an error. $n living doc(s) anchor into the file you just edited:"
  printf '%s\n' "$hits"
  echo ""
  echo "Before this change is committed: open each doc listed, verify whether your edit"
  echo "falsified any claim near those anchors, and ALIGN the doc in the same commit."
  echo "Align ONLY — correct what changed, delete what is now false. Do NOT add new"
  echo "sections, status headers, or prose beyond what the change requires. Standards:"
  echo "the CLAUDE.md beside each doc. If nothing drifted, say so and move on."
} >&2
exit 2
