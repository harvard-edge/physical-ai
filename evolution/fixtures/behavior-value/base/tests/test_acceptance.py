import unittest

from src.behavior import current_value


class BehaviorAcceptanceTest(unittest.TestCase):
    def test_returns_preregistered_value(self) -> None:
        self.assertEqual(current_value(), "new")


if __name__ == "__main__":
    unittest.main()
