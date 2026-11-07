#!/usr/bin/env bash
# Downloads the Ruffle release pinned in ruffle.json, checks its SHA-256, and unpacks it into ruffle/
# (gitignored), which the site serves at /ruffle/. The Pages deploy and the dev server both run this.
#   bash scripts/fetch-ruffle.sh           fetch if ruffle/ is missing or a different version
#   bash scripts/fetch-ruffle.sh --force   fetch again anyway
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
json() { sed -n "s/.*\"$1\": *\"\([^\"]*\)\".*/\1/p" "$ROOT/ruffle.json"; }
VERSION="$(json version)"; TAG="$(json tag)"; ASSET="$(json asset)"; SHA="$(json sha256)"
DEST="$ROOT/ruffle"

if [ "${1:-}" != "--force" ] && [ -f "$DEST/package.json" ] && grep -q "\"version\":\"$VERSION\"" "$DEST/package.json"; then
    echo "Ruffle $VERSION is already in ruffle/."
    exit 0
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
URL="https://github.com/ruffle-rs/ruffle/releases/download/$TAG/$ASSET"
echo "Downloading $URL"
curl -fsSL --retry 3 -o "$TMP/ruffle.zip" "$URL"

GOT="$( (sha256sum "$TMP/ruffle.zip" 2>/dev/null || shasum -a 256 "$TMP/ruffle.zip") | cut -d' ' -f1)"
if [ "$GOT" != "$SHA" ]; then
    echo "SHA-256 mismatch for $ASSET: expected $SHA, got $GOT" >&2
    exit 1
fi

mkdir -p "$TMP/x"
unzip -q "$TMP/ruffle.zip" -d "$TMP/x"
[ -f "$TMP/x/ruffle.js" ] || { echo "$ASSET has no ruffle.js" >&2; exit 1; }
rm -f "$TMP/x"/*.map
rm -rf "$DEST"
mv "$TMP/x" "$DEST"
echo "Ruffle $VERSION unpacked into ruffle/."
