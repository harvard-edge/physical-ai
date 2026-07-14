#!/usr/bin/env bash
# Start the Maya's Reachy website.
#
#   ./code/dev/run.sh                 # drive the real robot if it's on the LAN,
#                                     # otherwise fall back to simulation
#   REACHY_FAKE=1 ./code/dev/run.sh   # force simulation (no robot needed)
#   PORT=9000 ./code/dev/run.sh       # a different port
#
# Then open http://127.0.0.1:8080
# (8000 is taken by the Reachy Mini desktop app, so we default to 8080.)
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODE="$(dirname "$HERE")"

export REACHY_HOST="${REACHY_HOST:-reachy-mini.local}"

cd "$CODE"
PORT="${PORT:-8080}"
echo "Maya's Reachy → http://127.0.0.1:${PORT}   (host: $REACHY_HOST${REACHY_FAKE:+, SIMULATION})"
exec uv run \
  --no-project \
  --with-editable . \
  --with 'fastapi>=0.115,<1' \
  --with 'uvicorn>=0.30,<1' \
  uvicorn dev.server:app --host 127.0.0.1 --port "$PORT"
