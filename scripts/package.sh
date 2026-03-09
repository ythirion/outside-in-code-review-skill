#!/usr/bin/env bash
# Build outside-in-code-review-<version>.zip
# Packages all skill assets into a distributable archive
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_MD="$REPO_ROOT/SKILL.md"

# ── Extract metadata (YAML frontmatter between --- delimiters) ─────────────────
YAML=$(awk 'BEGIN{found=0} /^---/{found++; next} found==1{print} found==2{exit}' "$SKILL_MD")
VERSION=$(echo "$YAML" | grep '^version:' | sed 's/^version: *//')
NAME=$(echo "$YAML" | grep '^name:' | sed 's/^name: *//')

if [[ -z "$VERSION" || -z "$NAME" ]]; then
  echo "ERROR: could not extract name/version from $SKILL_MD" >&2; exit 1
fi

ARCHIVE="$REPO_ROOT/${NAME}-${VERSION}.zip"

# ── Build staging directory ────────────────────────────────────────────────────
STAGING=$(mktemp -d)
trap 'rm -rf "$STAGING"' EXIT

mkdir -p "$STAGING/commands" "$STAGING/skill/references" "$STAGING/img"

# ── Skills folder layout (install into ~/.claude/skills/outside-in-code-review/) ──
cp "$REPO_ROOT/SKILL.md"              "$STAGING/skill/"
cp "$REPO_ROOT/references/catalog.md" "$STAGING/skill/references/"

# ── Claude Code commands (install into ~/.claude/commands/) ──────────────────────
cp "$REPO_ROOT/.claude/commands/gather_product_insights.md"  "$STAGING/commands/"
cp "$REPO_ROOT/.claude/commands/explain_the_architecture.md" "$STAGING/commands/"
cp "$REPO_ROOT/.claude/commands/detail_flow.md"              "$STAGING/commands/"
cp "$REPO_ROOT/.claude/commands/rate_code_quality.md"        "$STAGING/commands/"

# Skill definition and docs
cp "$REPO_ROOT/img/outside-in-code-review.webp" "$STAGING/img/"
cp "$REPO_ROOT/README.md"   "$STAGING/"

# ── Create archive ─────────────────────────────────────────────────────────────
rm -f "$ARCHIVE"
(cd "$STAGING" && zip -r "$ARCHIVE" .)

echo "✅ Packaged: $ARCHIVE"
echo "   name:    $NAME"
echo "   version: $VERSION"
echo "   size:    $(du -sh "$ARCHIVE" | cut -f1)"
echo ""
echo "Contents:"
unzip -l "$ARCHIVE" | grep -v "^Archive\|^---\|files$" | awk 'NF'
