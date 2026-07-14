"""The robot ENGINE: connection + low-level movement and speech primitives.

Kids usually do NOT need to edit this file. New behaviors go in skills.py,
which is built out of the simple primitives defined here.

Speech is synthesized on this Mac with the built-in `say` command and streamed
to the robot's speaker, so the robot itself needs no speech software.
"""
from __future__ import annotations

import atexit
import contextlib
import glob
import hashlib
import os
import subprocess
import threading
import time
import wave
from pathlib import Path

import numpy as np

HOST = os.environ.get("REACHY_HOST", "reachy-mini.local")
SAMPLE_RATE = 16_000
CACHE = Path(__file__).resolve().parent.parent / "assets" / "cache"
CACHE.mkdir(parents=True, exist_ok=True)


def _fix_dyld():
    """Help macOS GStreamer find libpython (needed by the SDK's WebRTC audio).
    Sets DYLD_FALLBACK_LIBRARY_PATH before we connect, if it isn't already set."""
    if os.environ.get("DYLD_FALLBACK_LIBRARY_PATH"):
        return
    for pat in (
        "/opt/homebrew/Cellar/python@3.11/*/Frameworks/Python.framework/Versions/3.11/lib",
        "/opt/homebrew/opt/python@3.11/Frameworks/Python.framework/Versions/3.11/lib",
    ):
        hits = glob.glob(pat)
        if hits:
            os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = hits[0]
            return


_fix_dyld()

from reachy_mini import ReachyMini  # noqa: E402
from reachy_mini.utils import create_head_pose  # noqa: E402


# ---- speech helpers (macOS `say` -> 16 kHz mono WAV, cached by text) --------

def _synth_speech(text: str, voice: str | None = None) -> Path:
    key = hashlib.md5(f"{voice}|{text}".encode()).hexdigest()[:16]
    wav = CACHE / f"{key}.wav"
    if wav.exists():
        return wav
    aiff = CACHE / f"{key}.aiff"
    say_cmd = ["say"] + (["-v", voice] if voice else []) + ["-o", str(aiff), text]
    subprocess.run(say_cmd, check=True)
    subprocess.run(
        ["afconvert", "-f", "WAVE", "-d", "LEI16@16000", str(aiff), str(wav)],
        check=True,
    )
    aiff.unlink(missing_ok=True)
    return wav


def _load_mono(path: Path):
    with wave.open(str(path), "rb") as w:
        ch, fr, n = w.getnchannels(), w.getframerate(), w.getnframes()
        a = np.frombuffer(w.readframes(n), dtype="<i2").astype(np.float32) / 32768.0
    if ch > 1:
        a = a.reshape(-1, ch).mean(axis=1)
    return a, fr


def _resample(a, src, dst):
    if not dst or dst <= 0 or src == dst:
        return a
    n = int(round(len(a) * dst / src))
    return np.interp(np.linspace(0, len(a) - 1, n), np.arange(len(a)), a).astype(np.float32)


class Robot:
    """A live connection to the Reachy Mini. One instance is shared by all skills."""

    def __init__(self, host: str = HOST):
        self._es = contextlib.ExitStack()
        self.mini = self._es.enter_context(ReachyMini(host=host, connection_mode="network"))
        atexit.register(self._es.close)
        self._audio_ready = False
        self._lock = threading.Lock()

    # ---- speech ----

    def _ensure_audio(self):
        # The WebRTC audio send chain is set up lazily; warm it up once so the
        # first chunk of speech does not race the pipeline coming online.
        if not self._audio_ready:
            self.mini.media.start_playing()
            time.sleep(3.0)
            self._audio_ready = True

    def say(self, text: str, voice: str | None = None) -> str:
        """Speak `text` on the robot while gently moving the antennas."""
        with self._lock:
            samples, fr = _load_mono(_synth_speech(text, voice))
            out_sr = self.mini.media.get_output_audio_samplerate() or fr
            samples = _resample(samples, fr, out_sr)
            self._ensure_audio()
            chunk = max(1, int(0.10 * out_sr))
            t0 = time.time()
            for i in range(0, len(samples), chunk):
                block = samples[i:i + chunk]
                self.mini.media.push_audio_sample(block)
                t = time.time() - t0
                a = np.deg2rad(8.0 * np.sin(2 * np.pi * 3.0 * t))  # little "talking" wiggle
                self.mini.set_target(antennas=np.array([a, -a]))
                time.sleep(len(block) / out_sr)
            self.mini.set_target(antennas=np.array([0.0, 0.0]))
        return f'said: "{text}"'

    # ---- movement primitives ----

    def look(self, yaw: float = 0.0, pitch: float = 0.0, z: float = 0.0, duration: float = 0.6) -> str:
        """Point the head: yaw=left/right, pitch=up/down (degrees), z=rise (mm)."""
        self.mini.goto_target(
            head=create_head_pose(yaw=yaw, pitch=pitch, z=z, degrees=True, mm=True),
            duration=duration,
        )
        return f"looked (yaw={yaw}, pitch={pitch})"

    def tilt(self, roll: float = 18.0, duration: float = 0.5) -> str:
        """Curious head tilt to one side and back."""
        self.mini.goto_target(head=create_head_pose(roll=roll, degrees=True), duration=duration)
        self.mini.goto_target(head=create_head_pose(roll=0, degrees=True), duration=duration)
        return "tilted"

    def wiggle(self, times: int = 3) -> str:
        """Wiggle both antennas back and forth."""
        for _ in range(times):
            self.mini.goto_target(antennas=[0.4, -0.4], duration=0.2)
            self.mini.goto_target(antennas=[-0.4, 0.4], duration=0.2)
        self.mini.goto_target(antennas=[0.0, 0.0], duration=0.2)
        return "wiggled"

    def nod(self, times: int = 2) -> str:
        """Nod the head yes."""
        for _ in range(times):
            self.mini.goto_target(head=create_head_pose(pitch=15, degrees=True), duration=0.3)
            self.mini.goto_target(head=create_head_pose(pitch=-5, degrees=True), duration=0.3)
        return self.reset()

    def shake(self, times: int = 2) -> str:
        """Shake the head no."""
        for _ in range(times):
            self.mini.goto_target(head=create_head_pose(yaw=22, degrees=True), duration=0.25)
            self.mini.goto_target(head=create_head_pose(yaw=-22, degrees=True), duration=0.25)
        return self.reset()

    def reset(self, duration: float = 0.5) -> str:
        """Return to a calm, neutral pose."""
        self.mini.goto_target(
            head=create_head_pose(z=0, mm=True), antennas=[0.0, 0.0], body_yaw=0.0, duration=duration
        )
        return "reset"


_ROBOT: Robot | None = None
_robot_lock = threading.Lock()


def get_robot() -> Robot:
    """Return the shared Robot, connecting on first use (takes a few seconds)."""
    global _ROBOT
    with _robot_lock:
        if _ROBOT is None:
            _ROBOT = Robot()
    return _ROBOT
