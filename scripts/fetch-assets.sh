#!/usr/bin/env bash
# Downloads every image the site uses from Wix's CDN into ./images/
# Safe to re-run: skips files that already exist.
#
#   cd "Nick's Portfolio Site" && bash scripts/fetch-assets.sh
#
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/images"
MANIFEST="$ROOT/scripts/assets.txt"
mkdir -p "$OUT"

ok=0; skipped=0; failed=0
while read -r id file; do
  [[ -z "${id:-}" || "$id" == \#* ]] && continue
  dest="$OUT/$file"
  if [[ -s "$dest" ]]; then skipped=$((skipped+1)); continue; fi
  # Requesting the bare media id returns the original, full-resolution upload.
  if curl -fsSL --retry 3 -o "$dest" "https://static.wixstatic.com/media/$id"; then
    echo "  ✓ $file"; ok=$((ok+1))
  else
    echo "  ✗ $file  (https://static.wixstatic.com/media/$id)"; rm -f "$dest"; failed=$((failed+1))
  fi
done < "$MANIFEST"

echo
echo "Downloaded $ok, skipped $skipped already present, $failed failed."
[[ $failed -eq 0 ]] || exit 1
