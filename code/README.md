# Robot App

`code/` is one installable Python project. Its wheel is installed into Reachy
Mini's app environment, where the official app manager starts the
`mayas_reachy` entry point. The robot then hosts the website, conversation loop,
memory, speech, and physical control in one process.

## Current Teaching Loop

1. Maya or Alexander types or dictates a message in the website.
2. The robot sends the text to Groq with a strict response schema.
3. The LLM returns an intent, a candidate fact, a reply, and a mood.
4. Application code validates the candidate before memory can change.
5. The fact is stored locally and included in later LLM context.
6. Piper speaks the reply while the Reachy SDK moves the robot safely.

There is no hardcoded phrase parser. The LLM interprets the language, while
ordinary code owns validation, persistence, and physical safety.

## Project Hierarchy

```text
code/
  pyproject.toml              package metadata and robot app entry point
  src/mayas_reachy/
    app.py                    lifecycle, HTTP routes, queue, and robot loop
    conversation.py           teaching policy and memory-write boundary
    cloud.py                  Groq structured-output adapter
    memory.py                 local persistent memory interface
    voice.py                  offline Piper adapter
    static/                   child-facing website
    assets/                   packaged greeting audio
  tests/                      behavior and boundary tests
  dev/                        Mac development and simulation adapters
```

This is intentionally small. When the domain grows beyond a few modules,
`cloud.py`, `memory.py`, and the physical adapters can become subpackages
without changing the website or the app entry point.

## Memory Direction

The current JSON store is enough for teaching one robot name and proving that
the fact survives restarts. The next storage implementation should be SQLite on
the robot behind the same memory interface. SQLite provides transactions,
structured facts, provenance, and migrations without operating a database
server on a small CM4.

The LLM should not receive raw database access. A retrieval layer selects the
relevant facts for each turn and adds them to the model context. A validated
write layer accepts only explicit, schema-conforming facts. A hosted database or
vector index becomes useful only if the project later needs multi-device sync,
large documents, or semantic search across many memories.

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
