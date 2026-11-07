#!/usr/bin/env bash
# Checks VERSION.md: before the first stable release it's Semantic Versioning on 0.x.y; from the first
# stable release on it's a Date Version (https://datevers.ing): the UTC release date as YY.MM.DD, plus
# -1, -2... for later releases the same day. Never 1.0.0, and never back to 0.x.y after a Date Version.
# Run with: bash tests/version.sh
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PASS=0
FAIL=0
check() { # check "description" command...
    local name="$1"; shift
    if "$@"; then PASS=$((PASS + 1)); echo "ok   - $name"; else FAIL=$((FAIL + 1)); echo "FAIL - $name"; fi
}

SEMVER='^0\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$'
DATEVER='^[0-9]{2}\.(0[1-9]|1[0-2])\.(0[1-9]|[12][0-9]|3[01])(-[1-9][0-9]*)?$'
VERSION="$(tr -d '[:space:]' < "$ROOT/VERSION.md")"

is_semver()  { [[ "$VERSION" =~ $SEMVER ]]; }
is_datever() { [[ "$VERSION" =~ $DATEVER ]]; }
has_datever_tag() { git -C "$ROOT" tag 2>/dev/null | grep -qE '^v[0-9]{2}\.[0-9]{2}\.[0-9]{2}(-[1-9][0-9]*)?$'; }
valid_form() { is_semver || is_datever; }
real_date() {
    is_semver && return 0
    local d="${VERSION%%-*}" yy mm dd; IFS=. read -r yy mm dd <<< "$d"
    [ "$(date -u -d "20$yy-$mm-$dd" +%y.%m.%d 2>/dev/null)" = "$d" ]
}
not_future() { is_semver || [[ ! "${VERSION%%-*}" > "$(date -u +%y.%m.%d)" ]]; }
no_going_back() { ! { is_semver && has_datever_tag; }; }
changelog_leads() { [ "$(grep -m1 -oE '^## v[^[:space:]]+' "$ROOT/CHANGELOG.md" | sed 's/^## v//')" = "$VERSION" ]; }

check "VERSION.md ($VERSION) is 0.x.y or a Date Version (YY.MM.DD or YY.MM.DD-N)" valid_form
check "a Date Version is a real calendar date" real_date
check "a Date Version isn't dated in the future (UTC)" not_future
check "no 0.x.y once a Date Version tag exists" no_going_back
check "the newest '## v...' heading in CHANGELOG.md is VERSION.md" changelog_leads

echo "$PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
