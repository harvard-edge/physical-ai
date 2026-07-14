# Decisions

A short log of what we have settled and what is still open. Keep new entries at
the top of each section.

## Accepted

These are settled, with the reasoning, so we do not relitigate them.

- **The title is *Physical AI: Machine Learning Systems That Sense and Act*.**
  The title keeps the recognized field name while the subtitle makes the
  progression from machine learning systems explicit.
- **Hybrid brain: reflexes local, thinking in the cloud.** The robot is a CM4
  with no accelerator, which cannot run a conversational model at usable speed.
  So the always-on loop lives on the robot and Claude does the reasoning.
- **Audio to the robot: warm up then stream in chunks.** Start playing, wait
  about three seconds for the WebRTC audio send chain, then push samples in
  real time chunks. A single bulk push plays silent.
- **Memory is a knowledge graph.** It is inspectable (you can show Maya exactly
  what the robot knows), which a vector store is not, and it matches the teach
  it loop. Use the off the shelf knowledge graph MCP server.
- **Compose, do not reinvent.** Capabilities are skills plus MCP servers plus
  Claude. We snap in existing servers rather than build from scratch.
- **Dev voice is macOS say, robot voice is Piper.** Speech is pre rendered or
  synthesized on the host for development; the always-on robot uses Piper
  locally so it never needs the cloud just to speak.

## Open (lock these to make the plan executable)

Each changes what we build first, so we want answers before Phase 1 to 2.

1. **Emphasis.** They coexist, but which leads: Maya's engagement, her learning
   to program, a personal physical AI lab, or a teaching artifact? Tilts what we
   build first.
2. **Brain location, long term.** Claude in the cloud (recommended: smart, needs
   wifi) versus eventually a local edge box (private and offline, more work).
3. **Listening model.** Always-on wake word versus push to talk or a gesture.
   This is the privacy call for a child's room.
4. **Heartbeat and ownership.** A daily ritual on her shelf versus robot time
   pulled out together, and how hands on the parent stays over the long run.

Recommended starting point: lead with engagement (decision 1), Claude cloud
brain (decision 2), push to talk first then add wake word later (decision 3),
daily ritual on the shelf (decision 4). None of these block writing Phase 1.
