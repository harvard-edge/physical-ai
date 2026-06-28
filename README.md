# Maya's Reachy

A Reachy Mini robot that Maya teaches. The act of teaching it is what keeps her
engaged and what helps her learn, and the system underneath is a small, honest
example of edge plus cloud AI.

This repository is the home for the robot's software and its design. We are
architecting first, then building in phases.

## The idea in one line

A robot Maya teaches: she gives it words, facts, and tricks, it remembers and
grows, and over the years it becomes a way to understand how AI actually works.

## Why this project exists

Two purposes at once. One is a robot for Maya. The other is a systems-thinking
exercise in how physical AI is actually built, with the real use case keeping the
engineering honest. The architecture is meant to double as a learning
progression, the kind of structure that could seed a hands-on kit or a book.
See `docs/PHYSICAL_AI.md` for the thesis (TinyML put intelligence on a device;
physical AI puts a device in a loop that generates its own data) and the module
spine.

## How it is put together

Three layers (full detail in `docs/ARCHITECTURE.md`):

- **Body**: the robot's motors, speaker, mic, and camera, driven by the
  `reachy_mini` SDK and wrapped as simple "skills."
- **Brain**: Claude, which reasons, talks, and decides which skills to call,
  connected through MCP.
- **Memory**: a knowledge graph that stores what Maya teaches, so the robot
  remembers across days.

The robot is a Raspberry Pi Compute Module 4. It is strong enough to host
always-on reflexes (wake word, simple motion, local voice) but not a full
conversational model, so the thinking runs in the cloud. That split is the
architecture, not a compromise.

## Status

- **Phase 0 (foundation) is proven on the real robot**: it speaks, moves, knows
  a name, and sang Happy Birthday. See `docs/ROADMAP.md`.
- Existing prototypes to fold in: a happy-birthday app and a skills playground
  (currently in sibling folders, to be integrated here).

## Docs

- `docs/ARCHITECTURE.md`: the system, the two-speed brain, component
  responsibilities, the hardware reality, and data flows.
- `docs/ROADMAP.md`: the phases, what each delivers, and the multi-year arc.
- `docs/DECISIONS.md`: decisions already made, and the open ones to lock.

## Guiding principles

1. Maya is the teacher, never just a user.
2. Long vision, short deliveries: every phase ships something she can touch.
3. Privacy by design: gated mic and camera, visible on and off, local first.
4. The two-speed boundary is sacred: cheap and instant stays local, expensive
   and occasional goes to the cloud.
5. Compose, do not reinvent: skills plus MCP plus Claude.
6. It is a triad: Maya, parent, and robot, building together.
