import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RecoveredTranscriptCandidateTests(unittest.TestCase):
    def test_recovered_candidate_layer_is_separate_and_non_promotional(self):
        report = json.loads((ROOT / "research/recovered-transcript-review-candidates.json").read_text())
        patterns = json.loads((ROOT / "research/recovered-transcript-pattern-candidates.json").read_text())
        self.assertEqual(report["status"], "recovered_candidates_not_canonical_reviews")
        self.assertEqual(len(report["reviews"]), 32)
        self.assertEqual(patterns["status"], "recovered_language_pattern_candidates_not_validated")
        self.assertIn("not_contextually_reviewed", (ROOT / "writeups/recovered-transcript-pattern-candidates.md").read_text())
        self.assertEqual(len(patterns["patterns"]), 22)


if __name__ == "__main__":
    unittest.main()
