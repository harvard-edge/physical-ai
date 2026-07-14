# Robot App

`code/` is one installable Python project. Its wheel is installed into Reachy
Mini's app environment, where the official app manager starts the
`mayas_reachy` entry point from the neutral `robot_app` package. The robot then hosts the website, conversation loop,
memory, speech, and physical control in one process.

## Current Teaching Loop

1. Maya or Alexander types a message or taps the microphone in the website.
2. Reachy's onboard microphone records for up to 30 seconds; another tap or
   sustained silence ends the turn before the maximum.
3. Groq Whisper transcribes the transient audio, which is then discarded.
4. The robot sends the text and relevant memory to Groq with a strict schema.
5. The LLM proposes entities, claims, a reply, and a mood.
6. Application code validates relationships and attaches evidence.
7. SQLite stores episodes, entities, temporal claims, and registered skills.
8. Structured and full-text retrieval supply relevant context on later turns.
9. Piper speaks the reply while the Reachy SDK moves the robot safely.

There is no hardcoded phrase parser. The LLM interprets the language, while
ordinary code owns validation, persistence, and physical safety.

## Project Hierarchy

```text
code/
  pyproject.toml              package metadata and robot app entry point
  robot_app/
    app.py                    lifecycle, HTTP routes, queue, and robot loop
    conversation.py           teaching policy and memory-write boundary
    cloud.py                  Groq structured-output adapter
    memory.py                 SQLite episodic and semantic memory
    events.py                 typed cognitive event contracts
    policies.py               interchangeable reasoning and action contracts
    voice.py                  offline Piper adapter
    static/                   child-facing website
    assets/                   packaged greeting audio
  tests/                      behavior and boundary tests
  dev/                        Mac development and simulation adapters
```

This is intentionally small. When the domain grows beyond a few modules,
`cloud.py`, `memory.py`, and the physical adapters can become subpackages
without changing the website or the app entry point.

## Cognitive Memory

SQLite is the source of truth on the robot. Episodes preserve what was said;
entities and claims form an inspectable semantic graph; evidence links each
claim back to its episode. Claims carry confidence, origin, and temporal status,
so corrected knowledge can supersede old beliefs without destroying history.

The LLM should not receive raw database access. A retrieval layer selects the
relevant facts for each turn and adds them to the model context. A validated
write layer accepts only explicit, schema-conforming facts. FTS5 supplies text
retrieval now. Embeddings can later be added as a disposable `sqlite-vec` index,
while the graph and evidence remain authoritative.

Adult memory operations are available through `/api/memory` and
`/api/memory/reset`. A hard reset requires the exact confirmation phrase and
creates a backup before recreating the database.

## Run the Development Interface

```sh
./code/dev/run.sh
REACHY_FAKE=1 ./code/dev/run.sh
```

Open `http://127.0.0.1:8080`. `uv` resolves a current-platform development
environment without pulling the robot's Linux-only media stack onto the Mac.
Set `GROQ_API_KEY` for LLM turns. The installed robot app also looks for its
private key at `~/.config/mayas-reachy/groq_api_key`.

## Build the Robot Wheel

```sh
cd code
uv build
```

The resulting `dist/mayas_reachy-*.whl` contains the Python package, website,
and greeting audio. The Piper voice model and private credentials remain in the
robot's data and configuration directories so upgrades do not overwrite them.
