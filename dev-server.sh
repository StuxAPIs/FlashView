#!/bin/bash
# FlashView - Local dev server
# Usage: ./dev-server.sh [port] [--no-dev-mode]
#   port            default: 8000
#   --no-dev-mode   serve the site exactly as production does (no "local dev" banner)
#
# FlashView is a static site with no build step. This fetches the pinned Ruffle into ruffle/ if it's
# missing, then serves the repo root. Dev mode (on by default) shows a small banner so a local tab
# can't be mistaken for the live site; the dev server injects it, nothing in the repo changes.
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT=8000
DEV_MODE=1
for arg in "$@"; do
    case "$arg" in
        --no-dev-mode) DEV_MODE=0 ;;
        ''|*[!0-9]*) echo "Unknown argument: $arg" >&2; exit 1 ;;
        *) PORT="$arg" ;;
    esac
done

bash "$DIR/scripts/fetch-ruffle.sh"

PY="$(command -v python3 || command -v python || true)"
if [ -z "$PY" ]; then
    echo "python3 not found on PATH - install it to run the local server." >&2
    exit 1
fi
echo "Serving $DIR at http://127.0.0.1:$PORT (dev mode: $([ "$DEV_MODE" = 1 ] && echo on || echo off))"
DEV_MODE="$DEV_MODE" exec "$PY" -I "$DIR/scripts/dev-server.py" "$DIR" "$PORT"
