import tempfile
import threading
import types
import unittest
import wave
import time
from io import BytesIO
from pathlib import Path

import numpy as np

try:
    import reachy_mini  # noqa: F401
except ModuleNotFoundError:
    import sys

    from fastapi import FastAPI

    sdk = types.ModuleType("reachy_mini")
    sdk_utils = types.ModuleType("reachy_mini.utils")

    class ReachyMini:
        pass

    class ReachyMiniApp:
        custom_app_url = None

        def __init__(self, running_on_wireless=False):
            self.settings_app = FastAPI() if self.custom_app_url else None

    def create_head_pose(**kwargs):
        return kwargs

    sdk.ReachyMini = ReachyMini
    sdk.ReachyMiniApp = ReachyMiniApp
    sdk_utils.create_head_pose = create_head_pose
    sys.modules["reachy_mini"] = sdk
    sys.modules["reachy_mini.utils"] = sdk_utils

from app.app import MayasReachyApp
from app.cloud import GroqCloud
from app.memory import MemoryStore
from app.voice import PiperVoiceSynthesizer


class FakeMedia:
    def __init__(self):
        self.played = []
        self.recording = False
        self.samples = [np.array([[0.2, 0.1], [-0.2, -0.1]], dtype=np.float32)]

    def play_sound(self, path):
        self.played.append(path)

    def start_recording(self):
        self.recording = True

    def get_audio_sample(self):
        return self.samples.pop(0) if self.samples else None

    def get_input_audio_samplerate(self):
        return 16_000

    def stop_recording(self):
        self.recording = False


class FakeMini:
    def __init__(self):
        self.media = FakeMedia()
        self.goto_calls = []
        self.set_calls = []

    def goto_target(self, **kwargs):
        self.goto_calls.append(kwargs)

    def set_target(self, **kwargs):
        self.set_calls.append(kwargs)


class NativeAppTest(unittest.TestCase):
    def test_short_response_plays_audio_moves_and_returns_to_neutral(self):
        with tempfile.TemporaryDirectory() as directory:
            app = MayasReachyApp(
                memory=MemoryStore(Path(directory) / "memory.json"),
                cloud=GroqCloud(api_key=None),
            )
            mini = FakeMini()
            app.perform_response(
                mini,
                threading.Event(),
                audio_path=Path(__file__).parents[1]
                / "app"
                / "assets"
                / "hello_alexander_and_maya.wav",
                duration=0.04,
                mood="excited",
            )

            self.assertEqual(len(mini.media.played), 1)
            self.assertGreater(len(mini.set_calls), 0)
            self.assertEqual(mini.goto_calls[-1]["body_yaw"], 0.0)

    def test_status_exposes_cloud_and_memory_without_conversation_history(self):
        with tempfile.TemporaryDirectory() as directory:
            memory = MemoryStore(Path(directory) / "memory.json")
            memory.remember_robot_name("Pixel")
            app = MayasReachyApp(memory=memory, cloud=GroqCloud(api_key=None))

            status = app.status_snapshot()

            self.assertEqual(status["robot_name"], "Pixel")
            self.assertFalse(status["cloud_configured"])
            self.assertEqual(status["speech_provider"], "browser")
            self.assertTrue(status["supports_robot_listening"])
            self.assertNotIn("history", status)

    def test_operator_snapshots_are_redacted_and_read_only(self):
        with tempfile.TemporaryDirectory() as directory:
            app = MayasReachyApp(
                memory=MemoryStore(Path(directory) / "memory.json"),
                cloud=GroqCloud(api_key=None),
            )
            doctor = app.doctor_snapshot()
            brain = app.memory.snapshot()
            self.assertIn(doctor["state"], {"READY", "DEGRADED"})
            self.assertTrue(all("remediation" in check for check in doctor["checks"]))
            self.assertNotIn("history", brain)

    def test_listening_session_starts_without_waiting_for_completion(self):
        with tempfile.TemporaryDirectory() as directory:
            app = MayasReachyApp(
                memory=MemoryStore(Path(directory) / "memory.sqlite3"),
                cloud=GroqCloud(api_key=None),
            )
            app._robot_ready = True
            app._state = "ready"

            started = app.start_listening()
            pending = app.listening_result(started["job_id"])

            self.assertTrue(started["accepted"])
            self.assertEqual(app._state, "listen_queued")
            self.assertFalse(pending["complete"])

    def test_microphone_capture_returns_mono_pcm_wav(self):
        mini = FakeMini()

        audio = MayasReachyApp.capture_microphone(
            mini, threading.Event(), duration=0.03
        )

        self.assertFalse(mini.media.recording)
        with wave.open(BytesIO(audio), "rb") as recording:
            self.assertEqual(recording.getnchannels(), 1)
            self.assertEqual(recording.getsampwidth(), 2)
            self.assertEqual(recording.getframerate(), 16_000)
            self.assertGreater(recording.getnframes(), 0)

    def test_microphone_capture_can_be_stopped_before_maximum(self):
        mini = FakeMini()
        stop_requested = threading.Event()
        timer = threading.Timer(0.04, stop_requested.set)
        started = time.monotonic()
        timer.start()
        try:
            audio = MayasReachyApp.capture_microphone(
                mini, threading.Event(), duration=1.0, stop_requested=stop_requested
            )
        finally:
            timer.cancel()

        self.assertLess(time.monotonic() - started, 0.3)
        self.assertGreater(len(audio), 44)

    def test_piper_is_configured_only_with_model_and_config(self):
        with tempfile.TemporaryDirectory() as directory:
            model = Path(directory) / "voice.onnx"
            voice = PiperVoiceSynthesizer(model)
            self.assertFalse(voice.configured)
            model.write_bytes(b"model")
            Path(f"{model}.json").write_text("{}", encoding="utf-8")
            self.assertTrue(voice.configured)


if __name__ == "__main__":
    unittest.main()
