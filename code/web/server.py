"""Development server for the Maya's Reachy native app interface.

The production app is ``reachy_playground.app.MayasReachyApp`` and runs on the
robot. This server reuses the same packaged interface, Groq language layer, and
memory store while allowing simulation or development from a Mac.

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
STATIC = BODY / "reachy_playground" / "static"

# Make the folded-in robot package importable: code/body/reachy_playground/...
sys.path.insert(0, str(BODY))

from reachy_playground.app import GREETING_TEXT  # noqa: E402
from reachy_playground.cloud import GroqCloud  # noqa: E402
from reachy_playground.conversation import Conversation  # noqa: E402
from reachy_playground.memory import MemoryStore  # noqa: E402

FORCE_FAKE = os.environ.get("REACHY_FAKE") == "1"

# ---------------------------------------------------------------------------
# Robot access: lazy connect, degrade to simulation on any failure.
# ---------------------------------------------------------------------------

_robot = None
_simulating = FORCE_FAKE
_cloud = GroqCloud()
_memory = MemoryStore()
_conversation = Conversation(_memory, _cloud)


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


def reaction_for_mood(mood: str) -> dict:
    closer = {
        "curious": "tilt",
        "excited": "wiggle",
        "friendly": "wiggle",
        "warm": "nod",
    }.get(mood, "nod")
    return {
        "mood": mood,
        "closer": closer,
        "skills": ["look_up", "say", closer],
    }


# ---------------------------------------------------------------------------
# Web app
# ---------------------------------------------------------------------------

app = FastAPI(title="Maya's Reachy")


class SayIn(BaseModel):
    text: str


@app.get("/api/status")
def status():
    """Tell the UI whether we are wired to the robot or simulating."""
    mode = "simulation" if _simulating else "robot"
    return {
        "state": "simulation" if _simulating else "ready",
        "mode": mode,
        "host": os.environ.get("REACHY_HOST", "reachy-mini.local"),
        "phrase": GREETING_TEXT,
        "duration_seconds": 4.2,
        "runtime": "development-server",
        "cloud_provider": "groq",
        "cloud_configured": _cloud.configured,
        "robot_name": _memory.robot_name(),
    }


@app.post("/api/greet")
def greet():
    reaction = reaction_for_mood("excited")
    mode = perform(GREETING_TEXT, reaction)
    return {
        "ok": True,
        "accepted": True,
        "state": "simulation" if mode == "simulation" else "ready",
        "mode": mode,
        "phrase": GREETING_TEXT,
        "duration_seconds": 4.2,
    }


@app.post("/api/chat")
def chat(inp: SayIn):
    text = (inp.text or "").strip()
    if not text:
        return {"ok": False, "error": "Type or say something first."}
    plan = _conversation.respond(text)
    reaction = reaction_for_mood(plan.mood)
    mode = perform(plan.text, reaction)
    return {
        "ok": True,
        "reply": plan.text,
        "mood": plan.mood,
        "source": plan.source,
        "learned": plan.learned,
        "speech_mode": "browser" if mode == "simulation" else "robot",
        "duration_seconds": max(1.2, min(8.0, len(plan.text.split()) * 0.34)),
        "robot_name": _memory.robot_name(),
        "mode": mode,
    }
@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


app.mount("/static", StaticFiles(directory=STATIC), name="static")
