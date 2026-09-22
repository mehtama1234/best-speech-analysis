import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AutonomousFullMediaReconciliationTest(unittest.TestCase):
    def test_all_fixed_corpus_videos_have_explicit_media_status(self):
        report = json.loads((ROOT / "research/autonomous-full-media-reconciliation.json").read_text(encoding="utf-8"))
        self.assertEqual(report["video_count"], 395)
        self.assertEqual(len(report["rows"]), 395)
        self.assertEqual(len({row["video_id"] for row in report["rows"]}), 395)
        self.assertTrue(all(row["delivery_interpretation_status"] == "not_interpreted_internal_proxy_only" for row in report["rows"]))

    def test_media_report_retains_effectiveness_boundary(self):
        text = (ROOT / "writeups/autonomous-full-media-reconciliation.md").read_text(encoding="utf-8")
        self.assertIn("effectiveness", text)
        self.assertIn("Coverage counts", text)


if __name__ == "__main__":
    unittest.main()
