# Body and Native App

This package contains the current application, not only a motor library.
`MayasReachyApp` subclasses the official `ReachyMiniApp`, serves its packaged
web UI on port 8042, and remains the single owner of physical motion and audio.

Important files are grouped by responsibility.

- `reachy_playground/app.py` owns lifecycle, API routes, the action queue, and
  synchronized speech and motion.
- `reachy_playground/cloud.py` calls Groq with a strict JSON schema.
- `reachy_playground/conversation.py` validates model output and decides what
  may be persisted.
- `reachy_playground/memory.py` performs atomic local memory writes.
- `reachy_playground/voice.py` creates speech locally with Piper.
- `reachy_playground/static/` is the interface bundled into the app wheel.
- `tests/` covers the native loop, LLM contract, and persistent memory.

## Build

```sh
python -m pip wheel --no-deps . -w dist
```

The `reachy_mini_apps` entry point is named `mayas_reachy`. The Piper voice
model is kept outside the wheel at
`~/.local/share/mayas-reachy/voices/en_US-lessac-low.onnx` with its matching
`.onnx.json` file.
