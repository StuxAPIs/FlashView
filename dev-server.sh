#!/bin/bash
# FlashView - Local dev server
# Usage: ./dev-server.sh [port] [--no-dev-mode] [--lan]
#   port            default: 8000
#   --no-dev-mode   serve the site exactly as production does (no "local dev" banner)
#   --lan           listen on all interfaces so phones/tablets on your network can
#                   connect (prints the addresses to open); default is 127.0.0.1 only
#
# FlashView is a static site with no build step. This fetches the pinned Ruffle into ruffle/ if it's
# missing, then serves the repo root. Dev mode (on by default) shows a small banner so a local tab
# can't be mistaken for the live site; the dev server injects it, nothing in the repo changes.
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT=8000
DEV_MODE=1
HOST=127.0.0.1
for arg in "$@"; do
    case "$arg" in
        --no-dev-mode) DEV_MODE=0 ;;
        --lan) HOST=0.0.0.0 ;;
        ''|*[!0-9]*) echo "Unknown argument: $arg" >&2; echo "Usage: ./dev-server.sh [port] [--no-dev-mode] [--lan]" >&2; exit 1 ;;
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
if [ "$HOST" = "0.0.0.0" ]; then
    # This machine's IPv4 addresses (Windows, macOS or Linux), minus loopback
    case "$OSTYPE" in
        msys*|cygwin*|win32*) ADDRS="$(ipconfig | awk -F': *' '/IPv4/{print $2}' | tr -d '\r')" ;;
        darwin*) ADDRS="$(ifconfig | awk '/inet /{print $2}')" ;;
        *) ADDRS="$(hostname -I 2>/dev/null)" ;;
    esac
    echo "On your local network (--lan), open one of these on the other device:"
    for a in $ADDRS; do
        case "$a" in 127.*|'') ;; *) echo "    http://$a:$PORT" ;; esac
    done
    echo "  (usually the 192.168.x.x one; allow Python through the firewall if asked)"
fi
DEV_MODE="$DEV_MODE" exec "$PY" -I "$DIR/scripts/dev-server.py" "$DIR" "$PORT" "$HOST"
