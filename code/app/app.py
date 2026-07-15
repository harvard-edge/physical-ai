"""Robot-native Maya's Reachy app with a small, local web interface.

The Reachy Mini app manager creates the SDK connection and hands it to
``run``.  The browser only requests actions; this class remains the single
owner of the physical control loop.
"""
from __future__ import annotations

import io
import logging
import queue
import threading
import time
import wave
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
from pydantic import BaseModel, Field
from reachy_mini import ReachyMini, ReachyMiniApp
from reachy_mini.utils import create_head_pose

from .cloud import CloudUnavailable, GroqCloud
from .constants import GREETING_TEXT
from .conversation import Conversation
from .events import EventJournal
from .memory import MemoryStore
from .robot_gateway import ControlWatchdog, SafeRobotGateway
from .voice import PiperVoiceSynthesizer, VoiceUnavailable

HERE = Path(__file__).resolve().parent
GREETING_WAV = HERE / "assets" / "hello_alexander_and_maya.wav"


def wav_duration(path: Path) -> float:
    """Return the duration of a PCM WAV file in seconds."""
    with wave.open(str(path), "rb") as audio:
        return audio.getnframes() / float(audio.getframerate())


class ChatIn(BaseModel):
    text: str = Field(min_length=1, max_length=500)


class MemoryResetIn(BaseModel):
    mode: str = Field(pattern="^(soft|hard)$")
    confirmation: str


@dataclass
class ChatJob:
    text: str | None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: float = field(default_factory=time.monotonic)
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
        self._listen_stop = threading.Event()
        self._listening_started_at: float | None = None
        self._chat_queue: queue.Queue[ChatJob] = queue.Queue(maxsize=4)
        self._jobs_lock = threading.Lock()
        self._listen_jobs: dict[str, ChatJob] = {}
        self._state = "starting"
        self._robot_ready = False
        self._last_error: str | None = None
        self._last_greeting_at: float | None = None
        self.greeting_duration = wav_duration(GREETING_WAV)
        self.memory = memory or MemoryStore()
        self.cloud = cloud or GroqCloud()
        self.voice = voice or PiperVoiceSynthesizer()
        self.robot_gateway = SafeRobotGateway()
        self.conversation = Conversation(self.memory, self.cloud)
        self.events = EventJournal()

        @self.settings_app.get("/api/status")
        def status() -> dict[str, Any]:
            return self.status_snapshot()

        @self.settings_app.get("/api/doctor")
        def doctor() -> dict[str, Any]:
            return self.doctor_snapshot()

        @self.settings_app.get("/api/activity")
        def activity(limit: int = 20) -> dict[str, Any]:
            return {"events": self.events.recent(max(1, min(limit, 100)))}

        @self.settings_app.get("/api/brain")
        def brain() -> dict[str, Any]:
            snapshot = self.memory.snapshot()
            return {
                "version": snapshot["version"],
                "robot": snapshot["robot"],
                "counts": snapshot["counts"],
                "concepts": [
                    {"subject": fact.get("subject"), "predicate": fact.get("predicate"), "evidence": fact.get("episode_id")}
                    for fact in snapshot.get("facts", [])
                ],
                "redacted": True,
            }

        @self.settings_app.get("/api/maintenance")
        def maintenance() -> dict[str, Any]:
            return {"mode": "INTERACTION", "scheduler": "native-app", "maintenance_supported": True}

        @self.settings_app.post("/api/greet")
        def greet() -> dict[str, Any]:
            accepted = self.request_greeting()
            snapshot = self.status_snapshot()
            snapshot["accepted"] = accepted
            return snapshot

        @self.settings_app.post("/api/chat")
        def chat(inp: ChatIn) -> dict[str, Any]:
            return self.submit_chat(inp.text)

        @self.settings_app.post("/api/listen")
        def listen() -> dict[str, Any]:
            return self.submit_listen()

        @self.settings_app.post("/api/listen/start")
        def start_listening() -> dict[str, Any]:
            return self.start_listening()

        @self.settings_app.get("/api/listen/result/{job_id}")
        def listening_result(job_id: str) -> dict[str, Any]:
            return self.listening_result(job_id)

        @self.settings_app.post("/api/listen/stop")
        def stop_listening() -> dict[str, Any]:
            self._listen_stop.set()
            return {"ok": True}

        @self.settings_app.get("/api/memory")
        def memory_snapshot() -> dict[str, Any]:
            return self.memory.snapshot()

        @self.settings_app.post("/api/memory/reset")
        def reset_memory(inp: MemoryResetIn) -> dict[str, Any]:
            if inp.confirmation != "RESET MAYA'S REACHY":
                return {"ok": False, "error": "Adult confirmation did not match."}
            backup = self.memory.reset(hard=inp.mode == "hard")
            return {"ok": True, "mode": inp.mode, "backup_created": backup is not None}

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
                "supports_robot_listening": True,
                "listening_max_seconds": 30,
                "listening_elapsed_seconds": (
                    round(time.monotonic() - self._listening_started_at, 1)
                    if self._listening_started_at is not None else None
                ),
                "robot_name": self.memory.robot_name(),
            }

    def doctor_snapshot(self) -> dict[str, Any]:
        """Return redacted readiness checks for the operator dashboard."""
        status = self.status_snapshot()
        checks = [
            {
                "id": "memory",
                "status": "pass",
                "severity": "info",
                "observed": "sqlite available",
                "remediation": None,
            },
            {
                "id": "safety-gateway",
                "status": "pass" if not self.robot_gateway.stopped else "degraded",
                "severity": "critical",
                "observed": "stopped" if self.robot_gateway.stopped else "armed-boundary",
                "remediation": "operator authorization required" if self.robot_gateway.stopped else None,
            },
            {
                "id": "robot",
                "status": "pass" if status["ready"] else "degraded",
                "severity": "warning",
                "observed": status["state"],
                "remediation": "wait for robot startup" if not status["ready"] else None,
            },
            {
                "id": "cloud",
                "status": "pass" if status["cloud_configured"] else "degraded",
                "severity": "info",
                "observed": "configured" if status["cloud_configured"] else "offline",
                "remediation": "configure approved provider or use local fallback" if not status["cloud_configured"] else None,
            },
        ]
        state = "READY" if all(check["status"] == "pass" for check in checks) else "DEGRADED"
        return {"schema_version": "1.0.0", "state": state, "checks": checks, "redacted": True}

    def request_greeting(self) -> bool:
        """Queue one greeting unless one is already queued or playing."""
        with self._state_lock:
            if not self._robot_ready or self._state in {
                "queued",
                "listen_queued",
                "listening",
                "thinking",
                "speaking",
            }:
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
        return self._submit_job(ChatJob(text=cleaned[:500]), timeout=timeout)

    def submit_listen(self, *, timeout: float = 60.0) -> dict[str, Any]:
        """Queue one short onboard-microphone turn."""
        with self._state_lock:
            if not self._robot_ready:
                return {"ok": False, "error": "The robot is still waking up."}
        self._listen_stop.clear()
        return self._submit_job(ChatJob(text=None), timeout=timeout)

    def start_listening(self) -> dict[str, Any]:
        """Queue a microphone turn and return immediately for a responsive UI."""
        with self._state_lock:
            if not self._robot_ready:
                return {"ok": False, "error": "The robot is still waking up."}
            if self._state not in {"ready"}:
                return {"ok": False, "error": "The robot is busy right now."}
            self._state = "listen_queued"
            self._last_error = None
            self._listen_stop.clear()
        job = ChatJob(text=None)
        try:
            self._chat_queue.put_nowait(job)
        except queue.Full:
            self._set_state("ready")
            return {"ok": False, "error": "I am still thinking about the last message."}
        with self._jobs_lock:
            cutoff = time.monotonic() - 300
            self._listen_jobs = {
                key: value
                for key, value in self._listen_jobs.items()
                if not value.ready.is_set() or value.created_at >= cutoff
            }
            self._listen_jobs[job.id] = job
        return {"ok": True, "accepted": True, "job_id": job.id}

    def listening_result(self, job_id: str) -> dict[str, Any]:
        """Poll a queued microphone turn without holding an HTTP request open."""
        with self._jobs_lock:
            job = self._listen_jobs.get(job_id)
            if job is None:
                return {"ok": False, "error": "That listening session was not found."}
            if not job.ready.is_set():
                with self._state_lock:
                    current_state = self._state
                return {"ok": True, "complete": False, "state": current_state}
            result = dict(job.result or {"ok": False, "error": "No response was produced."})
        result["complete"] = True
        return result

    def _submit_job(self, job: ChatJob, *, timeout: float) -> dict[str, Any]:
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
        try:
            transcript: str | None = None
            if job.text is None:
                self._set_state("listening")
                self._listening_started_at = time.monotonic()
                try:
                    audio = self.capture_microphone(
                        reachy_mini, stop_event, stop_requested=self._listen_stop
                    )
                    self._set_state("thinking")
                    transcript = self.cloud.transcribe(audio)
                    self.events.publish("speech_transcribed", text=transcript)
                except CloudUnavailable as exc:
                    job.result = {"ok": False, "error": str(exc)}
                    job.ready.set()
                    self._set_state("ready")
                    return
                finally:
                    self._listening_started_at = None
                text = transcript
            else:
                self._set_state("thinking")
                text = job.text

            self.events.publish(
                "observation_recorded",
                modality="speech" if transcript is not None else "text",
                text=text,
            )
            plan = self.conversation.respond(text)
            if plan.learned:
                self.events.publish("memory_updated", learned=plan.learned)
            self.events.publish("plan_created", reply=plan.text, mood=plan.mood)
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
                "context_id": plan.context_id,
                "proposal_id": plan.proposal_id,
                "memory_mutations": plan.memory_mutations,
                "speech_mode": speech_mode,
                "duration_seconds": round(duration, 3),
                "robot_name": self.memory.robot_name(),
            }
            if transcript is not None:
                job.result["transcript"] = transcript
            job.ready.set()

            self._set_state("speaking")
            self.events.publish("skill_requested", capability="speak_and_gesture", mood=plan.mood)
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
            self.events.publish("action_executed", capability="speak_and_gesture")
            self._set_state("ready")
        except Exception as exc:
            logging.getLogger(__name__).exception("Chat turn failed")
            job.result = {"ok": False, "error": str(exc)}
            job.ready.set()
            self._set_state("error", error=str(exc))
            self._reset_robot(reachy_mini)

    @staticmethod
    def capture_microphone(
        reachy_mini: ReachyMini,
        stop_event: threading.Event,
        *,
        duration: float = 30.0,
        stop_requested: threading.Event | None = None,
        silence_seconds: float = 1.8,
    ) -> bytes:
        """Capture until stopped, sustained silence follows speech, or 30 seconds pass."""
        chunks: list[np.ndarray] = []
        reachy_mini.media.start_recording()
        started = time.monotonic()
        speech_started = False
        last_voice_at: float | None = None
        noise_levels: list[float] = []
        try:
            while (
                not stop_event.is_set()
                and not (stop_requested and stop_requested.is_set())
                and time.monotonic() - started < duration
            ):
                sample = reachy_mini.media.get_audio_sample()
                if sample is not None and np.size(sample):
                    chunk = np.asarray(sample, dtype=np.float32)
                    chunks.append(chunk)
                    level = float(np.sqrt(np.mean(np.square(chunk))))
                    elapsed = time.monotonic() - started
                    if elapsed < 0.6:
                        noise_levels.append(level)
                    baseline = float(np.median(noise_levels)) if noise_levels else 0.0
                    voice_threshold = max(0.012, min(0.05, baseline * 2.5))
                    if level >= voice_threshold:
                        speech_started = True
                        last_voice_at = time.monotonic()
                    elif (
                        speech_started
                        and last_voice_at is not None
                        and time.monotonic() - last_voice_at >= silence_seconds
                    ):
                        break
                stop_event.wait(0.02)
        finally:
            reachy_mini.media.stop_recording()

        if not chunks:
            raise CloudUnavailable("I could not hear the microphone. Please try again.")
        samples = np.concatenate(chunks, axis=0)
        if samples.ndim > 1:
            samples = samples.mean(axis=1)
        samples = np.clip(samples.reshape(-1), -1.0, 1.0)
        pcm = (samples * 32767.0).astype("<i2").tobytes()
        sample_rate = reachy_mini.media.get_input_audio_samplerate()
        if not isinstance(sample_rate, int) or sample_rate <= 0:
            sample_rate = 16_000

        output = io.BytesIO()
        with wave.open(output, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(pcm)
        return output.getvalue()

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

        authorization = self.robot_gateway.gesture(mood, duration)
        if authorization.status != "AUTHORIZED":
            raise RuntimeError(f"robot gateway rejected response: {authorization.reason}")
        watchdog = ControlWatchdog(timeout_seconds=max(0.25, self.CONTROL_PERIOD * 12))

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
            if watchdog.expired():
                self.robot_gateway.protective_stop()
                raise RuntimeError("robot control watchdog expired")
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
            watchdog.heartbeat()
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
