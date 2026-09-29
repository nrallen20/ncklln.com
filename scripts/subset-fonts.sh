#!/usr/bin/env bash
# Subsets the HeyGen fonts to the exact glyphs the playground's stand-in cards use.
# The originals stay outside the repo (Nick's Downloads); only the subsets are committed,
# so the public repo never carries a usable copy of a licensed font.
#
#   pip install fonttools brotli     # once
#   bash scripts/subset-fonts.sh
set -euo pipefail
cd "$(dirname "$0")/.."

SOLAR="$HOME/Downloads/DINAMO Order 2025-2860054/All Legal Solar Fonts/Solar Display/ABCSolarDisplay-Bold.woff2"
NORMS="$HOME/Downloads/Fonts/TT Norms Pro/TT Norms® Pro/woff2/TT_Norms_Pro_DemiBold.woff2"

# Every string the mock UI renders. Add here if you change the text in heygen-pyramid-playground.html.
TEXT='Nick Allen Step 2: Motion Make your avatar perfectly you! Create new video Add voice only Add Motion +'

subset() {
  pyftsubset "$1" --text="$TEXT" --flavor=woff2 --layout-features=kern --no-hinting --output-file="$2"
  printf '%-40s %6s bytes\n' "$2" "$(stat -f%z "$2")"
}
subset "$SOLAR" fonts/ABCSolarDisplay-Bold.subset.woff2
subset "$NORMS" fonts/TTNormsPro-DemiBold.subset.woff2
