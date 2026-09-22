import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CompoundPatternTriadTests(unittest.TestCase):
    def test_triads_retain_full_candidate_set_and_source_examples(self):
        report = json.loads((ROOT / "research/compound-pattern-triads.json").read_text())
        self.assertEqual(report["status"], "source_linked_three_move_candidates_not_validated")
        self.assertEqual(report["candidate_triad_count"], 160)
        self.assertEqual(report["practice_triad_count"], 24)
        self.assertTrue(all(item["examples"] for item in report["triads"]))
        self.assertIn("not", report["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
