# web

The chat website: how Maya and Alexander talk to the robot. Type a line (or tap
the mic and speak) and the robot says it out loud with an expressive gesture.
The person never sees the engineering; the engineering happens behind this page.

## Run it

```
./code/web/run.sh              # uses the robot if it's on the LAN, else simulates
REACHY_FAKE=1 ./code/web/run.sh   # no robot needed, browser voices the reply
```

Open http://127.0.0.1:8080.

## What it does right now (Milestone 1)

A kid's line comes in, and a small **local reflex** picks one gesture from it:

| The line ends with… | Robot does |
| --- | --- |
| `?` | looks up, says it, tilts (curious) |
| `!` | looks up, says it, wiggles (excited) |
| a greeting | looks up, says it, wiggles (friendly) |
| anything else | looks up, says it, nods (warm) |

No cloud, no memory. This is the honest hello-world: prove the whole pipe from a
kid's words to the robot's voice and body.

## The one seam that grows

`pick_reaction()` in `server.py` is the only thing the cloud brain replaces.
Swap that rule for a Claude call (see `../brain/`) and the same website suddenly
has a robot that chooses its own words, its own gestures, and what to remember.
The UI does not change.

## Files

```
server.py        FastAPI: serves the page, POST /api/say drives the robot
static/index.html   the page (inline SVG robot that mirrors the hardware)
static/styles.css   the playroom
static/app.js       send text, animate the robot, mic via the browser Web Speech API
run.sh           start it
```
