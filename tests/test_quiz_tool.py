"""Tests for the spaced-repetition logic in tools/quiz.py and the question bank itself."""
import importlib.util
import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("quiz", ROOT / "tools" / "quiz.py")
quiz = importlib.util.module_from_spec(spec); spec.loader.exec_module(quiz)
sys.path.insert(0, str(ROOT / "tools"))
import validate  # noqa: E402


class TestLeitner(unittest.TestCase):
    def test_promote_demote_and_due(self):
        p, now = {}, time.time()
        quiz.record(p, "x", 2, now)
        self.assertEqual(p["x"]["box"], 1)
        self.assertFalse(quiz.is_due(p["x"], now + 3600))           # box 1 → due after 1 day
        self.assertTrue(quiz.is_due(p["x"], now + 86400 + 1))
        quiz.record(p, "x", 1, now)
        self.assertEqual(p["x"]["box"], 1)                           # hard keeps the box
        quiz.record(p, "x", 0, now)
        self.assertEqual(p["x"]["box"], 0)                           # wrong resets
        for _ in range(10):
            quiz.record(p, "x", 2, now)
        self.assertEqual(p["x"]["box"], len(quiz.INTERVAL_DAYS) - 1) # capped

    def test_selection_prefers_due_then_new(self):
        bank = quiz.load_bank()
        topic = next(iter(bank))
        qs = bank[topic]["questions"]
        now = time.time()
        progress = {qs[0]["id"]: {"box": 1, "seen": 1, "correct": 1, "last": now - 2 * 86400},   # due
                    qs[1]["id"]: {"box": 5, "seen": 5, "correct": 5, "last": now}}               # not due
        picked, n_due, n_new = quiz.select(bank, [topic], progress, 3, "mixed", None, None, False, seed=1)
        self.assertEqual(n_due, 1)
        self.assertIn(qs[0]["id"], [q["id"] for q in picked])
        self.assertNotIn(qs[1]["id"], [q["id"] for q in picked])


class TestBank(unittest.TestCase):
    def test_bank_is_valid(self):
        self.assertEqual(validate.validate(), [])


if __name__ == "__main__":
    unittest.main()
