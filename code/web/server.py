"""Maya's Reachy - web chat backend (Milestone 1: the honest hello-world).

Serves a small chat website and drives the robot. Right now this is the LOCAL
REFLEX layer: text comes in, the robot says it out loud and performs one
expressive gesture chosen by a simple rule. No cloud, no memory. Its only job is
to prove the whole interface pipe end to end: a kid types or speaks, the metal
moves and talks.

The seam for later: `pick_reaction()` is the single function the brain replaces.
Instead of a rule choosing the gesture, Claude (brain/orchestrator.py) will
choose the words, the gestures, and what to remember, then call the same body
skills. The website above this file does not change when that happens.

If the robot is not reachable (or REACHY_FAKE=1), every action degrades to
"simulation": the backend reports what it would have done and the browser voices
it, so the site is fully usable without hardware.

Run it with code/web/run.sh, or directly:

    PYTHONPATH=code/body uvicorn web.server:app --port 8000   # from the code/ dir
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

HERE = Path(__file__).resolve().parent      # code/web
CODE = HERE.parent                          # code
BODY = CODE / "body"                        # code/body (the robot package lives here)
STATIC = HERE / "static"

# Make the folded-in robot package importable: code/body/reachy_playground/...
sys.path.insert(0, str(BODY))

FORCE_FAKE = os.environ.get("REACHY_FAKE") == "1"

# ---------------------------------------------------------------------------
# Robot access: lazy connect, degrade to simulation on any failure.
# ---------------------------------------------------------------------------

_robot = None
_simulating = FORCE_FAKE


def robot():
    """Return the live robot, or None when we are simulating.

    The first call connects over the network and takes a few seconds. If that
    fails (robot off, not on the LAN), we flip to simulation for the session.
    """
    global _robot, _simulating
    if _simulating:
        return None
    if _robot is None:
        try:
            from reachy_playground.robot import get_robot
            _robot = get_robot()
        except Exception as exc:  # robot unreachable; keep the website working
            print(f"[maya] robot unavailable, simulating: {exc}", file=sys.stderr)
            _simulating = True
            return None
    return _robot


# ---------------------------------------------------------------------------
# The local reflex: text -> one expressive gesture.
# This is the seam the cloud brain replaces later.
# ---------------------------------------------------------------------------

GREETINGS = ("hi", "hello", "hey", "hiya", "hola", "yo")


def pick_reaction(text: str) -> dict:
    """Choose how the robot reacts to a line of text. A tiny rule, for now.

    The mood drives the on-screen robot animation; `skills` is the list of body
    skills we report to the UI so the engineering is visible.
    """
    t = text.strip().lower()
    if t.endswith("?"):
        return {"mood": "curious", "closer": "tilt", "skills": ["look_up", "say", "tilt"]}
    if t.endswith("!"):
        return {"mood": "excited", "closer": "wiggle", "skills": ["look_up", "say", "wiggle"]}
    if any(t.startswith(g + " ") or t == g for g in GREETINGS):
        return {"mood": "friendly", "closer": "wiggle", "skills": ["look_up", "say", "wiggle"]}
    return {"mood": "warm", "closer": "nod", "skills": ["look_up", "say", "nod"]}


def perform(text: str, reaction: dict) -> str:
    """Drive the robot (or simulate). Returns 'robot' or 'simulation'."""
    r = robot()
    if r is None:
        return "simulation"
    r.look(pitch=10)          # attend: tip the head up toward the speaker
    r.say(text)               # speak on the robot's own speaker
    closer = reaction["closer"]
    if closer == "tilt":
        r.tilt()
    elif closer == "wiggle":
        r.wiggle()
    else:
        r.nod()
    return "robot"


# ---------------------------------------------------------------------------
# Web app
# ---------------------------------------------------------------------------

app = FastAPI(title="Maya's Reachy")


class SayIn(BaseModel):
    text: str


@app.get("/api/status")
def status():
    """Tell the UI whether we are wired to the robot or simulating."""
    return {
        "mode": "simulation" if _simulating else "ready",
        "host": os.environ.get("REACHY_HOST", "10.174.1.60"),
    }


@app.post("/api/say")
def say(inp: SayIn):
    text = (inp.text or "").strip()
    if not text:
        return {"ok": False, "error": "Type or say something first."}
    reaction = pick_reaction(text)
    mode = perform(text, reaction)
    return {
        "ok": True,
        "spoken": text,
        "mood": reaction["mood"],
        "skills": reaction["skills"],
        "mode": mode,
    }


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


app.mount("/static", StaticFiles(directory=STATIC), name="static")
