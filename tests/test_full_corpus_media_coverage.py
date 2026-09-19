import json
import unittest
from pathlib import Path

from scripts.build_full_corpus_media_coverage import main


ROOT = Path(__file__).resolve().parents[1]


class FullCorpusMediaCoverageTests(unittest.TestCase):
    def test_audit_accounts_for_every_transcript_video_without_promoting_media(self):
        main()
        report = json.loads((ROOT / "research/full-corpus-media-coverage.json").read_text())
        self.assertEqual(report["video_count"], 395)
        self.assertEqual(sum(report["counts"].values()), 395)
        self.assertIn("not_audiovisual_validation", report["status"])
        self.assertIn("does not prove", report["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
