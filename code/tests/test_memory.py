import tempfile
import unittest
from pathlib import Path

from app.memory import MemoryStore


class MemoryStoreTest(unittest.TestCase):
    def test_robot_name_survives_a_new_store_instance(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "memory.json"
            MemoryStore(path).remember_robot_name("Pixel")

            self.assertEqual(MemoryStore(path).robot_name(), "Pixel")
            self.assertTrue(path.with_suffix(".sqlite3").exists())
            self.assertEqual(MemoryStore(path).snapshot()["counts"]["claims"], 1)

    def test_missing_memory_is_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            store = MemoryStore(Path(directory) / "missing.json")
            self.assertIsNone(store.robot_name())

    def test_soft_reset_forgets_claims_but_preserves_episodes(self):
        with tempfile.TemporaryDirectory() as directory:
            store = MemoryStore(Path(directory) / "memory.sqlite3")
            episode = store.record_episode("Maya", "I like dinosaurs")
            store.remember_claim(
                "Maya", "likes", object_name="dinosaurs", subject_kind="person",
                episode_id=episode,
            )

            store.reset(hard=False)

            self.assertEqual(store.relevant_context("Maya"), [])
            self.assertEqual(store.snapshot()["counts"]["episodes"], 1)

    def test_hard_reset_creates_backup_and_starts_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            store = MemoryStore(Path(directory) / "memory.sqlite3")
            store.remember_robot_name("Pixel")

            backup = store.reset(hard=True)

            self.assertIsNotNone(backup)
            self.assertTrue(backup.exists())
            self.assertIsNone(store.robot_name())


if __name__ == "__main__":
    unittest.main()
