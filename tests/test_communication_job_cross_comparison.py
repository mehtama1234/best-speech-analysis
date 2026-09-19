import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CommunicationJobCrossComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / "research/communication-job-cross-comparison.json").read_text())

    def test_has_all_jobs_and_pairwise_denominators(self):
        self.assertEqual(self.report["status"], "transcript_video_level_comparison_not_independently_validated")
        self.assertEqual(self.report["job_count"], 18)
        self.assertEqual(self.report["pair_count"], 153)
        self.assertEqual(self.report["video_denominator"], 394)
        self.assertEqual(len(self.report["job_rows"]), 18)
        self.assertEqual(len(self.report["pair_rows"]), 153)
        for row in self.report["job_rows"]:
            self.assertEqual(row["video_count"], row["train_video_count"] + row["holdout_video_count"] + row["unassigned_video_count"])

    def test_boundary_does_not_promote_same_video_to_independent_recurrence(self):
        self.assertIn("do not establish effectiveness", self.report["claim_boundary"])
        self.assertIn("not an independently verified speaker/event", self.report["claim_boundary"])
        self.assertTrue((ROOT / "writeups/communication-job-cross-comparison.html").exists())


if __name__ == "__main__":
    unittest.main()
