# Architecture

## Current System

```text
Maya or Alexander
       │ type or tap the microphone
       ▼
robot-hosted web interface on port 8042
       │
       ├──► Reachy onboard mic ──► Groq Whisper transcription
       │
       ▼
Groq LLM ──► structured intent, candidate fact, reply, and mood
       │
       ▼
validation ──► local JSON memory
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

## Safety and Memory Boundary

The LLM interprets language, but it cannot write arbitrary data. The application
persists a name only when the structured intent is `teach_robot_name` and the
candidate passes local length and character checks. Conversation history stays
in RAM and only explicit facts survive a restart.

The first store is an atomic JSON file at
`~/.local/share/mayas-reachy/memory.json`. A knowledge graph can extend this
validated-write pattern when the children begin teaching more kinds of facts.

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

## Next Extensions

The microphone button now records a short clip through Reachy's onboard media
API. Later work can add local speech recognition for offline privacy, a wake-word
policy, and camera turns. Those changes should preserve the current rule that
one native app owns the physical loop.
