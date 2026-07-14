# Voice

The native app uses Piper to synthesize replies locally on Reachy's CM4. The
default voice is `en_US-lessac-low`, a 16 kHz model suited to Raspberry Pi 4
hardware. The browser speaks only when the local model is unavailable or the
app is running in simulation.

The implementation lives in `body/reachy_playground/voice.py`. The default
model path is
`~/.local/share/mayas-reachy/voices/en_US-lessac-low.onnx`. Set
`MAYAS_REACHY_PIPER_MODEL` to select another model.
