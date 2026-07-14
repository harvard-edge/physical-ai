#!/usr/bin/env bash
# Start the Maya's Reachy website.
#
#   ./code/web/run.sh                 # drive the real robot if it's on the LAN,
#                                     # otherwise fall back to simulation
#   REACHY_FAKE=1 ./code/web/run.sh   # force simulation (no robot needed)
#   PORT=9000 ./code/web/run.sh       # a different port
#
# Then open http://127.0.0.1:8080
# (8000 is taken by the Reachy Mini desktop app, so we default to 8080.)
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"   # code/web
CODE="$(dirname "$HERE")"                               # code

VENV="${MAYA_VENV:-/Users/VJ/GitHub/PhysicalAI/reachy_mini_happy_birthday/.venv}"
export REACHY_HOST="${REACHY_HOST:-10.174.1.60}"
# GStreamer/WebRTC audio needs libpython on its path when we drive the robot.
export DYLD_FALLBACK_LIBRARY_PATH="${DYLD_FALLBACK_LIBRARY_PATH:-/opt/homebrew/Cellar/python@3.11/3.11.15/Frameworks/Python.framework/Versions/3.11/lib}"

cd "$CODE"
PORT="${PORT:-8080}"
echo "Maya's Reachy → http://127.0.0.1:${PORT}   (host: $REACHY_HOST${REACHY_FAKE:+, SIMULATION})"
# Call uvicorn through python -m: the venv's uvicorn console-script has a stale
# shebang from before the repo moved under PhysicalAI/, but python -m works.
exec "$VENV/bin/python" -m uvicorn web.server:app --host 127.0.0.1 --port "$PORT"
