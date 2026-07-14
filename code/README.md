# Code

The working Maya's Reachy app lives in `body/reachy_playground/`. It is a native
Reachy Mini SDK app, so the robot hosts both the physical control loop and the
web interface.

## Use the Native App

Start `mayas_reachy` from the Reachy app manager, then open
`http://reachy-mini.local:8042`. Maya and Alexander can type a message or use
the microphone button.

The turn follows one path.

1. The browser sends the transcript to the robot-hosted `/api/chat` route.
2. Groq interprets the natural language and returns a strict structured result
   containing the intent, possible robot name, reply, and mood.
3. The app validates any extracted name before writing it to local memory.
4. Piper creates speech on the robot. The SDK plays it while a safe motion loop
   animates the head and antennas.
5. The robot returns to a neutral pose and waits for the next turn.

There is no hardcoded language parser. Code maps the model's structured mood to
safe physical motions, but the LLM decides what the child meant.

## Develop or Simulate on a Mac

```sh
./web/run.sh
REACHY_FAKE=1 ./web/run.sh
```

Open `http://127.0.0.1:8080`. The simulation uses the same UI, Groq adapter, and
memory logic. Browser speech replaces robot audio when no robot is connected.

Set `GROQ_API_KEY` before starting the development server. The native app also
looks for a private key file at `~/.config/mayas-reachy/groq_api_key`.

## Layout

```text
code/
  body/      native app, SDK control, LLM adapter, memory, voice, UI, and tests
  web/       development and simulation server for the packaged UI
  brain/     earlier Claude and MCP experiment, retained as a future option
  memory/    notes for the larger knowledge-graph phase
  voice/     notes for local speech
  senses/    wake word, on-robot speech recognition, and vision in later phases
```

The current memory deliberately stores only the taught robot name. The next
memory phase can generalize the same validated-write pattern to family facts and
a human-readable knowledge graph.
