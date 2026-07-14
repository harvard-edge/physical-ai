"""Robot-native Maya's Reachy app with a small, local web interface.

The Reachy Mini app manager creates the SDK connection and hands it to
``run``.  The browser only requests actions; this class remains the single
owner of the physical control loop.
"""
from __future__ import annotations

import logging
import queue
import threading
import time
import wave
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
from pydantic import BaseModel, Field
from reachy_mini import ReachyMini, ReachyMiniApp
from reachy_mini.utils import create_head_pose

from .cloud import GroqCloud
from .constants import GREETING_TEXT
from .conversation import Conversation
from .memory import MemoryStore
from .voice import PiperVoiceSynthesizer, VoiceUnavailable

HERE = Path(__file__).resolve().parent
GREETING_WAV = HERE / "assets" / "hello_alexander_and_maya.wav"


def wav_duration(path: Path) -> float:
    """Return the duration of a PCM WAV file in seconds."""
    with wave.open(str(path), "rb") as audio:
        return audio.getnframes() / float(audio.getframerate())


class ChatIn(BaseModel):
    text: str = Field(min_length=1, max_length=500)


@dataclass
class ChatJob:
    text: str
    ready: threading.Event = field(default_factory=threading.Event)
    result: dict[str, Any] | None = None


class MayasReachyApp(ReachyMiniApp):
    """Learn from Maya and Alexander, talk, and move as one native app."""

    custom_app_url: str | None = "http://0.0.0.0:8042"
    request_media_backend: str | None = None

    CONTROL_PERIOD = 0.02  # 50 Hz speech-motion loop

    def __init__(
        self,
        running_on_wireless: bool = False,
        *,
        memory: MemoryStore | None = None,
        cloud: GroqCloud | None = None,
        voice: PiperVoiceSynthesizer | None = None,
    ) -> None:
        super().__init__(running_on_wireless=running_on_wireless)
        if self.settings_app is None:  # guarded by custom_app_url above
            raise RuntimeError("Maya's Reachy web interface was not created")

        self._state_lock = threading.Lock()
        self._greet_requested = threading.Event()
        self._chat_queue: queue.Queue[ChatJob] = queue.Queue(maxsize=4)
        self._state = "starting"
        self._robot_ready = False
        self._last_error: str | None = None
        self._last_greeting_at: float | None = None
        self.greeting_duration = wav_duration(GREETING_WAV)
        self.memory = memory or MemoryStore()
        self.cloud = cloud or GroqCloud()
        self.voice = voice or PiperVoiceSynthesizer()
        self.conversation = Conversation(self.memory, self.cloud)

        @self.settings_app.get("/api/status")
        def status() -> dict[str, Any]:
            return self.status_snapshot()

        @self.settings_app.post("/api/greet")
        def greet() -> dict[str, Any]:
            accepted = self.request_greeting()
            snapshot = self.status_snapshot()
            snapshot["accepted"] = accepted
            return snapshot

        @self.settings_app.post("/api/chat")
        def chat(inp: ChatIn) -> dict[str, Any]:
            return self.submit_chat(inp.text)

    def status_snapshot(self) -> dict[str, Any]:
        """Return thread-safe state for the robot-hosted interface."""
        with self._state_lock:
            return {
                "state": self._state,
                "ready": self._robot_ready,
                "phrase": GREETING_TEXT,
                "duration_seconds": round(self.greeting_duration, 3),
                "last_error": self._last_error,
                "last_greeting_at": self._last_greeting_at,
                "runtime": "reachy-mini-app",
                "cloud_provider": "groq",
                "cloud_configured": self.cloud.configured,
                "speech_provider": "piper" if self.voice.configured else "browser",
                "robot_name": self.memory.robot_name(),
            }

    def request_greeting(self) -> bool:
        """Queue one greeting unless one is already queued or playing."""
        with self._state_lock:
            if not self._robot_ready or self._state in {"queued", "thinking", "speaking"}:
                return False
            self._state = "queued"
            self._last_error = None
            self._greet_requested.set()
            return True

    def submit_chat(self, text: str, *, timeout: float = 30.0) -> dict[str, Any]:
        """Queue a language turn and wait only until its response is ready."""
        cleaned = text.strip()
        if not cleaned:
            return {"ok": False, "error": "Type or say something first."}
        with self._state_lock:
            if not self._robot_ready:
                return {"ok": False, "error": "The robot is still waking up."}
        job = ChatJob(text=cleaned[:500])
        try:
            self._chat_queue.put_nowait(job)
        except queue.Full:
            return {"ok": False, "error": "I am still thinking about the last message."}
        if not job.ready.wait(timeout=timeout):
            return {"ok": False, "error": "The cloud brain took too long to answer."}
        return job.result or {"ok": False, "error": "No response was produced."}

    def run(self, reachy_mini: ReachyMini, stop_event: threading.Event) -> None:
        """Own the robot loop, autoplay once, and service chat requests."""
        with self._state_lock:
            self._robot_ready = True
            self._state = "ready"

        def warm_voice() -> None:
            try:
                self.voice.warm_up()
            except VoiceUnavailable:
                logging.getLogger(__name__).warning(
                    "Could not warm up Piper TTS", exc_info=True
                )

        voice_warm_started = False
        self.request_greeting()

        try:
            while not stop_event.is_set():
                if self._greet_requested.is_set():
                    self._greet_requested.clear()
                    self._set_state("speaking")
                    try:
                        self.perform_greeting(reachy_mini, stop_event)
                    except Exception as exc:
                        logging.getLogger(__name__).exception("Greeting failed")
                        self._set_state("error", error=str(exc))
                        self._reset_robot(reachy_mini)
                    else:
                        with self._state_lock:
                            self._last_greeting_at = time.time()
                        self._set_state("ready")
                        if not voice_warm_started:
                            threading.Thread(
                                target=warm_voice,
                                name="maya-reachy-piper-warmup",
                                daemon=True,
                            ).start()
                            voice_warm_started = True
                    continue

                try:
                    job = self._chat_queue.get(timeout=0.1)
                except queue.Empty:
                    continue
                self._process_chat(job, reachy_mini, stop_event)
        finally:
            self._reset_robot(reachy_mini)
            with self._state_lock:
                self._robot_ready = False
                self._state = "stopped"

    def perform_greeting(
        self,
        reachy_mini: ReachyMini,
        stop_event: threading.Event,
        *,
        duration_override: float | None = None,
    ) -> None:
        """Play the packaged greeting while animating an attentive, happy pose."""
        duration = self.greeting_duration if duration_override is None else duration_override
        self.perform_response(
            reachy_mini,
            stop_event,
            audio_path=GREETING_WAV,
            duration=duration,
            mood="excited",
        )

    def _process_chat(
        self,
        job: ChatJob,
        reachy_mini: ReachyMini,
        stop_event: threading.Event,
    ) -> None:
        """Understand one turn, publish its reply, then voice and embody it."""
        self._set_state("thinking")
        try:
            plan = self.conversation.respond(job.text)
            audio_path: Path | None = None
            speech_mode = "browser"
            if self.voice.configured:
                try:
                    audio_path = self.voice.synthesize(plan.text)
                except VoiceUnavailable:
                    logging.getLogger(__name__).warning("Piper TTS unavailable", exc_info=True)
                else:
                    speech_mode = "robot"

            duration = (
                wav_duration(audio_path)
                if audio_path is not None
                else max(1.2, min(8.0, len(plan.text.split()) * 0.34))
            )
            job.result = {
                "ok": True,
                "reply": plan.text,
                "mood": plan.mood,
                "source": plan.source,
                "learned": plan.learned,
                "speech_mode": speech_mode,
                "duration_seconds": round(duration, 3),
                "robot_name": self.memory.robot_name(),
            }
            job.ready.set()

            self._set_state("speaking")
            try:
                self.perform_response(
                    reachy_mini,
                    stop_event,
                    audio_path=audio_path,
                    duration=duration,
                    mood=plan.mood,
                )
            finally:
                if audio_path is not None:
                    audio_path.unlink(missing_ok=True)
            self._set_state("ready")
        except Exception as exc:
            logging.getLogger(__name__).exception("Chat turn failed")
            job.result = {"ok": False, "error": str(exc)}
            job.ready.set()
            self._set_state("error", error=str(exc))
            self._reset_robot(reachy_mini)

    def perform_response(
        self,
        reachy_mini: ReachyMini,
        stop_event: threading.Event,
        *,
        audio_path: Path | None,
        duration: float,
        mood: str,
    ) -> None:
        """Synchronize optional robot audio with a safe expressive gesture."""

        # First make eye contact. The voice starts only after the robot is looking up.
        reachy_mini.goto_target(
            head=create_head_pose(pitch=8, z=3, degrees=True, mm=True),
            antennas=np.deg2rad([5.0, -5.0]),
            duration=0.55,
        )

        playback_errors: list[BaseException] = []

        def play_voice() -> None:
            try:
                if audio_path is not None:
                    reachy_mini.media.play_sound(str(audio_path))
            except BaseException as exc:  # preserve playback errors across the thread
                playback_errors.append(exc)

        player = threading.Thread(target=play_voice, name="maya-reachy-audio", daemon=True)
        player.start()

        started = time.monotonic()
        while not stop_event.is_set():
            elapsed = time.monotonic() - started
            if elapsed >= duration:
                break

            # Small layered motions make the robot feel alive without obscuring speech.
            bob = np.sin(2.0 * np.pi * 1.1 * elapsed)
            sway = np.sin(2.0 * np.pi * 0.42 * elapsed)
            talk = np.sin(2.0 * np.pi * 3.2 * elapsed)
            head = create_head_pose(
                z=3.0 + 1.2 * bob,
                pitch=8.0 + 1.5 * bob,
                yaw=3.5 * sway,
                roll=1.5 * sway,
                degrees=True,
                mm=True,
            )
            antenna = np.deg2rad(10.0 + 8.0 * talk)
            reachy_mini.set_target(head=head, antennas=np.array([antenna, -antenna]))
            stop_event.wait(self.CONTROL_PERIOD)

        player.join(timeout=1.5)
        if playback_errors:
            raise RuntimeError(f"robot audio playback failed: {playback_errors[0]}")

        if not stop_event.is_set() and mood == "curious":
            reachy_mini.goto_target(
                head=create_head_pose(roll=11, pitch=7, z=3, degrees=True, mm=True),
                antennas=np.deg2rad([12.0, -12.0]),
                duration=0.35,
            )
            stop_event.wait(0.2)
        elif not stop_event.is_set() and mood in {"excited", "friendly"}:
            reachy_mini.goto_target(
                head=create_head_pose(pitch=7, z=3, degrees=True, mm=True),
                antennas=np.deg2rad([24.0, -24.0]),
                duration=0.35,
            )
            stop_event.wait(0.2)
        elif not stop_event.is_set():
            reachy_mini.goto_target(
                head=create_head_pose(pitch=13, z=2, degrees=True, mm=True),
                antennas=np.deg2rad([8.0, -8.0]),
                duration=0.3,
            )
            stop_event.wait(0.15)

        self._reset_robot(reachy_mini)

    def _set_state(self, state: str, *, error: str | None = None) -> None:
        with self._state_lock:
            self._state = state
            self._last_error = error

    @staticmethod
    def _reset_robot(reachy_mini: ReachyMini) -> None:
        try:
            reachy_mini.goto_target(
                head=create_head_pose(z=0, mm=True),
                antennas=np.array([0.0, 0.0]),
                body_yaw=0.0,
                duration=0.5,
            )
        except Exception:
            logging.getLogger(__name__).exception("Could not return Reachy to neutral")


def main() -> None:
    """Run the app outside the dashboard for development."""
    app = MayasReachyApp()
    try:
        app.wrapped_run()
    except KeyboardInterrupt:
        app.stop()


if __name__ == "__main__":
    main()
