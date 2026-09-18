import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RawMediaOnlyVisualAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / "research/raw-media-only-visual-audit.json").read_text())

    def test_report_covers_all_raw_only_items_without_promoting_them(self):
        self.assertEqual(self.report["item_count"], 8)
        self.assertEqual(self.report["status"], "internal_visual_source_audit_complete_transcript_missing")
        self.assertEqual(self.report["independence"], "not_independent")
        for item in self.report["items"]:
            self.assertEqual(item["transcript_status"], "no_retained_transcript_in_segment_registry")
            self.assertEqual(item["review_status"], "internal_visual_source_audit_not_independent")
        self.assertIn("speech function", self.report["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
