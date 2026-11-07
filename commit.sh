#!/bin/bash
# FlashView - Git commit + tag script
# Commits whatever's staged/unstaged and tags it with the version in VERSION.md, read dynamically so this
# script never goes stale the way a hardcoded version number does.
#
# Two versioning stages:
#   * Pre-stable: Semantic Versioning on 0.x.y (0.1.0, 0.2.0, 0.2.1 ...), tagged v0.x.y.
#   * Stable: the first stable release (what would have been 1.0.0) is the first Date Version
#     (https://datevers.ing): the UTC release date as YY.MM.DD, then -1, -2 ... for later releases that
#     day. There is no 1.0.0, and once a Date Version tag exists there's no going back to 0.x.y.
#
#   ./commit.sh          check VERSION.md, then commit and tag it (never pushes)
#   ./commit.sh --next   print a suggested next version
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

TODAY="$(date -u +%y.%m.%d)"
semver_re='^0\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$'
datever_re='^([0-9]{2})\.(0[1-9]|1[0-2])\.(0[1-9]|[12][0-9]|3[01])(-([1-9][0-9]*))?$'

has_datever() { git tag | grep -qE '^v[0-9]{2}\.[0-9]{2}\.[0-9]{2}(-[1-9][0-9]*)?$'; }

# Highest same-day Date Version release number: -1 none, 0 unsuffixed, N for -N.
highest_release() {
    local highest=-1 tag n
    for tag in $(git tag -l "v$1" "v$1-*"); do
        if [ "$tag" = "v$1" ]; then n=0; else n="${tag#v"$1"-}"; fi
        [[ "$n" =~ ^[0-9]+$ ]] && [ "$n" -gt "$highest" ] && highest="$n"
    done
    echo "$highest"
}

next_version() {
    if has_datever; then
        local h; h="$(highest_release "$TODAY")"
        if [ "$h" -lt 0 ]; then echo "$TODAY"; else echo "$TODAY-$((h + 1))"; fi
        return
    fi
    local last
    last="$(git tag -l 'v0.*' | sed 's/^v//' | grep -E "$semver_re" | sort -t. -k2,2n -k3,3n | tail -1)"
    if [ -z "$last" ]; then echo "0.1.0"; else echo "$last" | awk -F. '{print $1"."$2"."$3+1}'; fi
}

if [ "${1:-}" = "--next" ]; then next_version; exit 0; fi

VERSION="$(tr -d '[:space:]' < "$DIR/VERSION.md")"
fail() {
    echo "VERSION.md says '$VERSION': $1" >&2
    echo "A suggested next version is $(next_version) (./commit.sh --next)." >&2
    exit 1
}

if [[ "$VERSION" =~ $semver_re ]]; then
    if has_datever; then fail "the project has moved to Date Versioning and can't go back to 0.x.y."; fi
elif [[ "$VERSION" =~ $datever_re ]]; then
    DATE="${VERSION%%-*}"
    if [ "$(date -u -d "20${DATE//./-}" +%y.%m.%d 2>/dev/null)" != "$DATE" ]; then fail "that isn't a real calendar date."; fi
    if [[ "$DATE" > "$TODAY" ]]; then fail "it's dated after today ($TODAY UTC). Date Versions can't be in the future."; fi
    if [[ "$DATE" < "$TODAY" ]]; then echo "Warning: VERSION.md is dated $DATE, but today is $TODAY (UTC). Releasing today? Use $TODAY." >&2; fi
    if ! has_datever; then echo "This is FlashView's first stable release: its first Date Version." >&2; fi
else
    fail "not a pre-stable 0.x.y version or a Date Version (YY.MM.DD or YY.MM.DD-N). There is no 1.0.0: the first stable release is a Date Version."
fi

if git rev-parse -q --verify "refs/tags/v${VERSION}" >/dev/null; then
    fail "tag v${VERSION} already exists, and released versions can't change."
fi

git add -A
if ! git diff --cached --quiet; then
    git commit -m "Release v${VERSION}" -m "See CHANGELOG.md for details."
else
    echo "Nothing to commit - tagging the current HEAD as v${VERSION}."
fi

git tag -a "v${VERSION}" -m "FlashView v${VERSION}"
echo "Tagged v${VERSION}."
echo "Push with: git push origin test v${VERSION}, then open a pull request from test into main."
