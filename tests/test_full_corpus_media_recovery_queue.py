import json
import unittest
from pathlib import Path

from scripts.build_full_corpus_media_recovery_queue import main


ROOT = Path(__file__).resolve().parents[1]


class FullCorpusMediaRecoveryQueueTests(unittest.TestCase):
    def test_queue_routes_every_non_raw_fixed_corpus_video(self):
        main()
        report = json.loads((ROOT / "research/full-corpus-media-recovery-queue.json").read_text())
        coverage = json.loads((ROOT / "research/full-corpus-media-coverage.json").read_text())
        self.assertEqual(report["item_count"], coverage["counts"]["derived_features_only"] + coverage["counts"]["transcript_only_no_local_media"])
        self.assertEqual(sum(report["counts"]["by_priority"].values()), report["item_count"])
        self.assertIn("does not prove", report["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
