#!/usr/bin/env bash
# Build outside-in-code-review-<version>.zip
# Packages all skill assets into a distributable archive
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_MD="$REPO_ROOT/skills/outside-in-code-review/SKILL.md"

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

mkdir -p "$STAGING/commands" "$STAGING/skill" "$STAGING/img"

# ── Skills folder layout (install into ~/.claude/skills/outside-in-code-review/) ──
# SKILL.md + references/ + assets/ (CSS, fonts, embedded Mermaid) + scripts/ (validation, PDF export)
SKILL_DIR="$REPO_ROOT/skills/outside-in-code-review"
cp "$SKILL_DIR/SKILL.md" "$STAGING/skill/"
for dir in references assets scripts; do
  cp -R "$SKILL_DIR/$dir" "$STAGING/skill/"
done
find "$STAGING/skill" \( -name '__pycache__' -o -name '.DS_Store' \) -prune -exec rm -rf {} +

# ── Claude Code commands (install into ~/.claude/commands/) ──────────────────────
cp "$REPO_ROOT/commands/gather_product_insights.md"  "$STAGING/commands/"
cp "$REPO_ROOT/commands/explain_the_architecture.md" "$STAGING/commands/"
cp "$REPO_ROOT/commands/detail_flow.md"              "$STAGING/commands/"
cp "$REPO_ROOT/commands/rate_code_quality.md"        "$STAGING/commands/"

# Skill definition and docs
cp -r "$REPO_ROOT/img/." "$STAGING/img/"
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
