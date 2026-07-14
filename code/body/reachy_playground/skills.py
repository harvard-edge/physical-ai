"""SKILLS — this is where you program the robot!

Each skill is a small function. Read one, change a number, run it, and watch
what the robot does. When you want a new trick, copy a skill, give it a new
name, and add @skill on the line above it. It will instantly show up in the
`play` command AND as a tool Claude can use.

The robot's moves come from get_robot(): .say(), .look(), .tilt(), .wiggle(),
.nod(), .shake(), .reset()  (see robot.py for the full list).
"""
from __future__ import annotations

from .robot import get_robot

# Every @skill function is collected here so `play.py` and the MCP server can
# find them automatically.
SKILLS: dict = {}


def skill(fn):
    SKILLS[fn.__name__] = fn
    return fn


# ---------------------------------------------------------------------------
# Talking skills
# ---------------------------------------------------------------------------

@skill
def say_text(text: str = "Hello there!") -> str:
    """Make the robot say anything you type."""
    return get_robot().say(text)


@skill
def greet(name: str = "friend") -> str:
    """Look up, say hi to someone, and wiggle the antennas."""
    r = get_robot()
    r.look(pitch=10)          # tip the head up a little
    r.say(f"Hi {name}! Nice to see you!")
    r.wiggle()
    return f"greeted {name}"


@skill
def ask_my_name(kid_name: str = "Maya") -> str:
    """Greet a kid and ask what they would like to name the robot."""
    r = get_robot()
    r.look(pitch=12)
    r.tilt()                  # curious head tilt
    r.say(f"Hi {kid_name}! What would you like to name me?")
    r.wiggle()
    return f"asked {kid_name} for a name"


@skill
def accept_name(my_new_name: str = "Pixel") -> str:
    """React happily to being given a name. (Claude calls this once the kid
    tells it the name they chose.)"""
    r = get_robot()
    r.nod()
    r.say(f"{my_new_name}? I love it! Hi everyone, my name is {my_new_name}!")
    r.wiggle(times=4)
    return f"accepted the name {my_new_name}"


# ---------------------------------------------------------------------------
# Movement skills (no talking)
# ---------------------------------------------------------------------------

@skill
def nod(times: int = 2) -> str:
    """Nod the head yes."""
    return get_robot().nod(times=times)


@skill
def shake_head(times: int = 2) -> str:
    """Shake the head no."""
    return get_robot().shake(times=times)


@skill
def wiggle(times: int = 3) -> str:
    """Wiggle the antennas."""
    return get_robot().wiggle(times=times)


@skill
def look_around() -> str:
    """Look left, then right, then up, then back to center."""
    r = get_robot()
    r.look(yaw=30)
    r.look(yaw=-30)
    r.look(pitch=20)
    r.reset()
    return "looked around"


@skill
def happy_dance() -> str:
    """A short happy dance: bob, sway, and wiggle."""
    r = get_robot()
    for _ in range(3):
        r.look(yaw=20, z=6)
        r.wiggle(times=1)
        r.look(yaw=-20, z=6)
        r.wiggle(times=1)
    r.reset()
    return "danced"


@skill
def reset() -> str:
    """Return the robot to a calm, neutral pose."""
    return get_robot().reset()
