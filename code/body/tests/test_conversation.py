import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from reachy_playground.cloud import GroqCloud, configured_api_key
from reachy_playground.conversation import Conversation
from reachy_playground.memory import MemoryStore


class FakeUnderstandingCloud:
    configured = True

    def __init__(self, result):
        self.result = result
        self.calls = []

    def analyze_turn(self, user_text, *, robot_name, history):
        self.calls.append((user_text, robot_name, list(history)))
        return dict(self.result)


class FailingCloud:
    configured = True

    def analyze_turn(self, user_text, *, robot_name, history):
        from reachy_playground.cloud import CloudUnavailable

        raise CloudUnavailable("temporary failure")


class ConversationTest(unittest.TestCase):
    def test_key_can_come_from_private_robot_config(self):
        with tempfile.TemporaryDirectory() as directory:
            key_file = Path(directory) / "groq_api_key"
            key_file.write_text("private-test-key\n", encoding="utf-8")
            with patch.dict(
                "os.environ",
                {"GROQ_API_KEY_FILE": str(key_file)},
                clear=True,
            ):
                self.assertEqual(configured_api_key(), "private-test-key")

    def test_llm_extraction_is_validated_and_persisted(self):
        with tempfile.TemporaryDirectory() as directory:
            memory = MemoryStore(Path(directory) / "memory.json")
            cloud = FakeUnderstandingCloud(
                {
                    "intent": "teach_robot_name",
                    "robot_name": "pixel",
                    "reply": "Pixel? I love it!",
                    "mood": "excited",
                }
            )

            plan = Conversation(memory, cloud).respond("I think Pixel fits you perfectly.")

            self.assertEqual(memory.robot_name(), "Pixel")
            self.assertEqual(plan.learned, {"robot_name": "Pixel"})
            self.assertEqual(plan.source, "groq-cloud")
            self.assertEqual(cloud.calls[0][0], "I think Pixel fits you perfectly.")

    def test_non_teaching_intent_cannot_write_a_name(self):
        with tempfile.TemporaryDirectory() as directory:
            memory = MemoryStore(Path(directory) / "memory.json")
            cloud = FakeUnderstandingCloud(
                {
                    "intent": "conversation",
                    "robot_name": "GuessedName",
                    "reply": "That sounds fun!",
                    "mood": "warm",
                }
            )

            plan = Conversation(memory, cloud).respond("Tell me a story.")

            self.assertIsNone(memory.robot_name())
            self.assertIsNone(plan.learned)

    def test_no_cloud_means_no_language_extraction(self):
        with tempfile.TemporaryDirectory() as directory:
            memory = MemoryStore(Path(directory) / "memory.json")
            cloud = GroqCloud(api_key=None)
            with patch.dict("os.environ", {}, clear=True):
                cloud.api_key = None
                plan = Conversation(memory, cloud).respond("Your name is Pixel.")

            self.assertIsNone(memory.robot_name())
            self.assertEqual(plan.source, "offline-fallback")

    def test_configured_cloud_failure_does_not_claim_key_is_missing(self):
        with tempfile.TemporaryDirectory() as directory:
            memory = MemoryStore(Path(directory) / "memory.json")
            with self.assertLogs("reachy_playground.conversation", level="WARNING"):
                plan = Conversation(memory, FailingCloud()).respond(
                    "Your name is Pixel."
                )

            self.assertIn("Please try again", plan.text)
            self.assertNotIn("key", plan.text.lower())
            self.assertIsNone(memory.robot_name())

    def test_groq_turn_requests_strict_structured_output(self):
        cloud = GroqCloud(api_key="test-key")
        captured = {}

        def fake_request(path, payload):
            captured["path"] = path
            captured["payload"] = payload
            return {
                "choices": [
                    {
                        "message": {
                            "content": (
                                '{"intent":"greeting","robot_name":null,'
                                '"reply":"Hello!","mood":"friendly"}'
                            )
                        }
                    }
                ]
            }

        with patch.object(cloud, "_request_json", side_effect=fake_request):
            result = cloud.analyze_turn("Hello", robot_name=None, history=[])

        self.assertEqual(result["intent"], "greeting")
        self.assertEqual(captured["path"], "/chat/completions")
        self.assertEqual(captured["payload"]["max_completion_tokens"], 768)
        self.assertEqual(captured["payload"]["reasoning_effort"], "low")
        self.assertEqual(captured["payload"]["reasoning_format"], "hidden")
        response_format = captured["payload"]["response_format"]
        self.assertEqual(response_format["type"], "json_schema")
        self.assertTrue(response_format["json_schema"]["strict"])


if __name__ == "__main__":
    unittest.main()
