import json
import tempfile
import unittest
from pathlib import Path

from mayas_reachy.memory import MemoryStore


class MemoryStoreTest(unittest.TestCase):
    def test_robot_name_survives_a_new_store_instance(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "memory.json"
            MemoryStore(path).remember_robot_name("Pixel")

            self.assertEqual(MemoryStore(path).robot_name(), "Pixel")
            data = json.loads(path.read_text())
            self.assertEqual(data["robot"]["source"], "family web chat")

    def test_missing_memory_is_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            store = MemoryStore(Path(directory) / "missing.json")
            self.assertIsNone(store.robot_name())


if __name__ == "__main__":
    unittest.main()
