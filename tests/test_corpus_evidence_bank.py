import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CorpusEvidenceBankTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bank = json.loads((ROOT / "research/corpus-evidence-bank.json").read_text())
        cls.registry = {}
        with (ROOT / "research/segment-registry.jsonl").open() as handle:
            for line in handle:
                row = json.loads(line)
                cls.registry[row["evidence_id"]] = row
        cls.browser = (ROOT / "writeups/corpus-evidence-bank.html").read_text()

    def test_links_all_function_records_and_segments(self):
        self.assertEqual(self.bank["summary"]["review_count"], 395)
        self.assertEqual(self.bank["summary"]["function_record_count"], 4016)
        self.assertEqual(self.bank["summary"]["missing_evidence_id_count"], 0)
        for record in self.bank["records"]:
            self.assertTrue(record["segments"])
            for segment in record["segments"]:
                source = self.registry[segment["evidence_id"]]
                self.assertEqual(segment["text"], source["text"])
                self.assertEqual(segment["start_seconds"], source["start_seconds"])

    def test_preserves_transcript_boundary_and_searchable_browser(self):
        self.assertIn("retained_caption_text_unrepaired", self.bank["records"][0]["caption_text_status"])
        self.assertIn("does not establish tone", self.bank["claim_boundary"])
        self.assertIn('id="search"', self.browser)
        self.assertIn("recognition errors", self.browser)


if __name__ == "__main__":
    unittest.main()
