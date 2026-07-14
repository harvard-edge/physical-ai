# code

All of Maya's Reachy software lives here, the way the book lives in `../book/`.
The design and the phases are in `../docs/` (`ARCHITECTURE.md`, `ROADMAP.md`,
`DECISIONS.md`); this file is the map of the code and how to run it.

## Start here: the website

The interface comes first. A local web page is how Maya and Alexander talk to the
robot; the engineering happens behind it.

```
./web/run.sh                 # drive the robot if it's on the LAN, else simulate
REACHY_FAKE=1 ./web/run.sh    # no robot needed (the browser voices the reply)
```

Open http://127.0.0.1:8080, then type or tap the mic and speak. Milestone 1 is
the honest hello-world: your words come out of the robot with an expressive
gesture. No cloud, no memory yet.

## The layers

```
code/
  web/       the chat website (text + mic → the robot speaks & moves)   ← today
  body/      the robot's skills and driver (reachy_mini SDK)  [folded in, proven]
  brain/     the cloud mind: Claude + memory, via MCP         [scaffolded]
  memory/    the knowledge graph Maya teaches into            [scaffolded]
  voice/     on-robot text-to-speech (Piper)                  [later phase]
  senses/    wake word, camera vision, identity               [later phase]
```

## How it grows (one seam at a time)

Today the website calls the body directly through a small **local reflex**
(`web/server.py` → `pick_reaction()`): a rule picks the gesture. That one
function is the seam. Replace it with the **brain** (`brain/orchestrator.py`, or
Claude Desktop via `brain/claude_desktop_config.example.json`) and the same page
gets a robot that chooses its own words, its own gestures, and what to remember
in `memory/`. Nothing above the seam changes.

- **Milestone 1 (now):** website → reflex → body. Say + gesture.
- **Milestone 2:** website → brain (Claude) → body. Claude picks the reaction.
- **Milestone 3:** brain writes/reads `memory/`. Teach it its name; it remembers.
- **Later:** mic and voice move onto the robot; wake word; camera show-and-tell.

## One-time setup

The robot SDK is already in the shared venv. The website needs `fastapi` +
`uvicorn` (present). The memory server (Milestone 3) needs Node's `npx` (present).

```
MAYA_VENV=/Users/VJ/GitHub/PhysicalAI/reachy_mini_happy_birthday/.venv
"$MAYA_VENV/bin/pip" install mcp        # for body/server.py as an MCP tool server
```

Robot address defaults to `10.174.1.60` (override with `REACHY_HOST`).
