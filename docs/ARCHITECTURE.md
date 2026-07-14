# Architecture

## Current System

```text
Maya or Alexander
       │ type or tap the microphone (up to 30 seconds)
       ▼
robot-hosted web interface on port 8042
       │
       ├──► Reachy onboard mic ──► Groq Whisper transcription
       │
       ▼
Groq LLM ──► structured intent, entities, claims, reply, and mood
       │
       ▼
validation ──► embedded SQLite cognitive memory
                 ├── episodes and evidence
                 ├── entities and temporal claims
                 ├── FTS5 hybrid retrieval
                 └── registered safe skills
       │
       ▼
Piper speech + Reachy Mini SDK motion
       │
       ▼
speaker, head, and antennas on Reachy
```

`MayasReachyApp` runs on the CM4 through the official app manager. It owns the
FastAPI routes, a single action queue, the SDK connection, and the packaged web
interface. The browser requests actions but never controls motors directly.

The implementation is one wheel built from `code/`. Production modules live in
`code/src/mayas_reachy/`; Mac-only adapters live in `code/dev/`; behavioral
tests live in `code/tests/`.

## Two-Speed Brain

The robot splits work by latency and compute cost.

- **Local work:** The robot hosts the interface, validates model output, writes
  memory, synthesizes speech with Piper, and controls motion. It also retains a
  packaged greeting when the network is unavailable.
- **Cloud work:** Groq runs `whisper-large-v3-turbo` for transcription and
  `openai/gpt-oss-20b` for natural-language understanding and reply generation.
  A strict JSON schema keeps the boundary between model output and application
  state explicit.

The CM4 has no accelerator and is not a practical host for a conversational
model. It is a good host for the responsive physical loop and a small local
speech model. A larger local LLM would need a separate edge computer later.

## Cognitive Memory

The LLM interprets language and proposes entities and relationships, but it
cannot write arbitrary data. Application code permits a small relationship
vocabulary, resolves entities, validates values, and attaches each accepted
claim to the episode that supports it.

The embedded store is `~/.local/share/mayas-reachy/memory.sqlite3`. Episodic
memory records what happened. Semantic memory stores entities, claims,
confidence, origin, and validity periods. Procedural memory registers the safe
skills the runtime can execute. SQLite FTS5 complements structured graph lookup;
an optional embedding index can be added later without becoming the source of
truth.

Soft reset archives active beliefs while retaining episodes. Hard reset creates
a recoverable database backup, then starts with an empty memory. Raw microphone
audio remains transient and is not stored.

## Event and Policy Boundaries

Typed cognitive events describe observations, transcriptions, memory updates,
plans, skill requests, and actions. They currently use a small in-process
journal. The same event contracts can later feed ROS 2, Zenoh, debugging tools,
or LeRobot dataset recording without changing the child-facing interface.

Reasoning providers remain interchangeable. The current Groq adapter can later
sit beside a local model or remote VLA policy. Every policy produces a bounded
plan; only deterministic application code may invoke physical capabilities.

## Physical Control Boundary

One 50 Hz loop coordinates speech and movement. It looks toward the child,
starts the voice, layers small safe head and antenna motions over the reply,
performs a short mood gesture, and returns the robot to neutral. The LLM selects
one of the allowed moods. Code maps that mood to bounded SDK targets.

## Connection Facts

- The Reachy daemon is available at `reachy-mini.local:8000`.
- The native app interface is available at `reachy-mini.local:8042` while
  `mayas_reachy` is running.
- The native app uses Reachy Mini SDK 1.9.0 on the robot.
- The private Groq key is read from the process environment or
  `~/.config/mayas-reachy/groq_api_key`.
- The default Piper files are
  `~/.local/share/mayas-reachy/voices/en_US-lessac-low.onnx` and its matching
  `.onnx.json` configuration.

## Framework Adoption Boundary

- Reachy Mini SDK owns current hardware access.
- Arduino Bridge/RPC is the intended UNO Q hardware boundary.
- SQLite, FTS5, and later `sqlite-vec` provide embedded retrieval.
- LeRobot is the target format for future sensor-action datasets.
- ROS 2 or Zenoh adapters become useful when components leave this process.
- OpenVLA or NVIDIA GR00T run as remote policy providers, not on the CM4.
- LangGraph is reserved for genuinely branching, resumable reasoning workflows.

The adoption rule is: reuse directly, wrap behind an adapter, borrow a proven
pattern, and only then build the smallest missing component.

The phased implementation and verification plan lives in
[`SYSTEM-ROADMAP.md`](SYSTEM-ROADMAP.md).
