import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CommunicationJobStimuliTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bank = json.loads((ROOT / "research/communication-job-listener-stimuli-draft.json").read_text())
        cls.cards = json.loads((ROOT / "research/communication-job-cards.json").read_text())["cards"]

    def test_one_newly_authored_pair_per_job_and_unlocked_status(self):
        self.assertEqual(self.bank["status"], "draft_not_locked")
        self.assertEqual(self.bank["pair_count"], 18)
        self.assertEqual({r["card_id"] for r in self.bank["records"]}, {c["card_id"] for c in self.cards})
        for record in self.bank["records"]:
            self.assertTrue(record["control_text"])
            self.assertTrue(record["pattern_informed_text"])
            self.assertEqual(record["source_boundary"], "Newly authored study material; not copied from corpus speakers.")
            self.assertEqual(record["status"], "draft_requires_matching_readability_accessibility_and_safety_review")

    def test_word_count_audit_is_reproducible(self):
        for record in self.bank["records"]:
            self.assertEqual(record["word_count_delta"], record["pattern_informed_word_count"] - record["control_word_count"])
            self.assertLess(abs(record["word_count_delta"]), 30)
        self.assertIn("independent content-equivalence review", self.bank["review_requirements"])


if __name__ == "__main__":
    unittest.main()
