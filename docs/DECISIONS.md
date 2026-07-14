# Decisions

A short log of what we have settled and what is still open. Keep new entries at
the top of each section.

## Accepted

These are settled, with the reasoning, so we do not relitigate them.

- **Hybrid brain: reflexes local, thinking in the cloud.** The robot is a CM4
  with no accelerator, which cannot run a conversational model at usable speed.
  The always-on loop lives on the robot. The starter app uses Groq for language
  understanding while keeping the provider boundary replaceable.
- **Audio to the robot: warm up then stream in chunks.** Start playing, wait
  about three seconds for the WebRTC audio send chain, then push samples in
  real time chunks. A single bulk push plays silent.
- **Memory is inspectable and locally validated.** The working name memory is a
  small JSON file. A knowledge graph remains the planned extension when more
  fact types are introduced.
- **Compose, do not reinvent.** The app combines the Reachy SDK, Groq structured
  output, Piper, and small readable adapters.
- **Dev voice is macOS say, robot voice is Piper.** Speech is pre rendered or
  synthesized on the host for development; the always-on robot uses Piper
  locally so it never needs the cloud just to speak.

## Open (lock these to make the plan executable)

Each changes what we build first, so we want answers before Phase 1 to 2.

1. **Emphasis.** They coexist, but which leads: Maya's engagement, her learning
   to program, a personal physical AI lab, or a teaching artifact? Tilts what we
   build first.
2. **Brain location, long term.** Keep a cloud LLM (smart, needs Wi-Fi) or move
   to a local edge box later (private and offline, more work).
3. **Listening model.** Always-on wake word versus push to talk or a gesture.
   This is the privacy call for a child's room.
4. **Heartbeat and ownership.** A daily ritual on her shelf versus robot time
   pulled out together, and how hands on the parent stays over the long run.

Recommended starting point: lead with engagement (decision 1), a cloud LLM
(decision 2), push to talk first then add wake word later (decision 3),
daily ritual on the shelf (decision 4). None of these block writing Phase 1.
