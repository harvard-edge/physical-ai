import tempfile
import threading
import types
import unittest
from pathlib import Path

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

from mayas_reachy.app import MayasReachyApp
from mayas_reachy.cloud import GroqCloud
from mayas_reachy.memory import MemoryStore
from mayas_reachy.voice import PiperVoiceSynthesizer


class FakeMedia:
    def __init__(self):
        self.played = []

    def play_sound(self, path):
        self.played.append(path)


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
                / "src"
                / "mayas_reachy"
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
            self.assertNotIn("history", status)

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
