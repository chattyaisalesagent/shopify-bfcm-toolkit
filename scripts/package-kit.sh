#!/usr/bin/env bash
# Package the BFCM Support Kit for chatty.net/bfcm-2026/kit.
#
#   1. Copies prompts/<slug>.md into the site, where the kit page reads
#      them at build time.
#   2. Builds one zip per skill with the skill folder at the zip root
#      (claude.ai rejects a skill nested one level deeper), plus
#      bfcm-support-kit.zip holding all six and a short HOW-TO.txt.
#
# Usage: scripts/package-kit.sh [path-to-chatty.net-repo]
# Re-run whenever a skill or prompt changes.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
SITE="${1:-/Users/avada/chatty.net}"
PROMPT_OUT="$SITE/src/app/(main)/bfcm-2026/kit/prompts"
ZIP_OUT="$SITE/public/downloads/bfcm-support-kit"

# Public kit, in the order the kit page shows them. conversation-gap-analyzer
# is withdrawn from the public kit (overlaps Chatty's Unresolved questions).
SLUGS=(
  peak-season-readiness-audit
  campaign-rules-policy-qa
  delivery-cutoff-planner
  peak-load-cover-planner
  peak-season-playbook
  shipping-exception-watch
)

mkdir -p "$PROMPT_OUT" "$ZIP_OUT"
rm -f "$ZIP_OUT"/*.zip

STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

for slug in "${SLUGS[@]}"; do
  [ -f "$REPO/skills/$slug/SKILL.md" ] || { echo "missing skill: $slug" >&2; exit 1; }
  [ -f "$REPO/prompts/$slug.md" ] || { echo "missing prompt: $slug" >&2; exit 1; }
  cp "$REPO/prompts/$slug.md" "$PROMPT_OUT/$slug.md"
  (cd "$REPO/skills" && zip -qr -X "$ZIP_OUT/$slug.zip" "$slug" -x '*/__pycache__/*' '*.pyc' '*/.DS_Store')
  cp -R "$REPO/skills/$slug" "$STAGE/$slug"
done

cat > "$STAGE/HOW-TO.txt" <<'EOF'
The BFCM Support Kit, by Chatty (chatty.net/bfcm-2026)

Six folders, one skill each. Every skill drafts; nothing changes your
store or messages a customer until you do.

Claude (claude.ai or the desktop app)
  1. Settings > Capabilities: turn on code execution.
  2. Customize > Skills > upload a skill.
  3. Upload ONE folder at a time as its own zip (the skill folder must be
     at the root of the zip). Single-skill zips are on the kit page.

ChatGPT
  If your plan shows Skills, upload the same single-skill zips.
  Otherwise use the copy-paste prompts on the kit page.

Claude Code / Codex
  Install all six from GitHub:
  claude plugin marketplace add chattyaisalesagent/shopify-bfcm-toolkit
  claude plugin install shopify-peak-season-toolkit

Any other AI
  Use the copy-paste prompt for each tool on the kit page.
EOF

find "$STAGE" -name '__pycache__' -prune -exec rm -rf {} + 2>/dev/null || true
find "$STAGE" -name '.DS_Store' -delete 2>/dev/null || true
(cd "$STAGE" && zip -qr -X "$ZIP_OUT/bfcm-support-kit.zip" .)

echo "prompts -> $PROMPT_OUT"
echo "zips    -> $ZIP_OUT"
ls -la "$ZIP_OUT"
