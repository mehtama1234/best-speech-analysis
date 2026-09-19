import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class FullCorpusTimingCandidateAtlasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / "research/full-corpus-timing-candidate-atlas.json").read_text())

    def test_full_local_alignment_and_bounded_density_sampling(self):
        self.assertEqual(self.report["status"], "full_local_feature_proxy_atlas_manual_listening_pending")
        self.assertEqual(self.report["coverage"]["aligned_video_count"], 357)
        self.assertEqual(self.report["coverage"]["aligned_segment_count"], 97743)
        self.assertEqual(self.report["coverage"]["candidate_record_count"], 5557)
        self.assertEqual(self.report["coverage"]["candidate_video_count"], 357)
        self.assertIn("intentional pause", self.report["claim_boundary"])

    def test_density_cap_is_per_video_and_gap_rows_are_preserved(self):
        rows = self.report["items"]
        reasons = Counter(row["candidate_reason"] for row in rows)
        self.assertEqual(reasons["gap_before_captioned_unit"], 2079)
        self.assertEqual(reasons["gap_after_captioned_unit"], 2079)
        for reason in ("lower_caption_density_proxy", "higher_caption_density_proxy"):
            by_video = Counter(row["video_id"] for row in rows if row["candidate_reason"] == reason)
            self.assertTrue(all(count <= 3 for count in by_video.values()))
        for row in rows:
            self.assertEqual(row["status"], "proxy_candidate_requires_full_media_and_manual_listening")


if __name__ == "__main__":
    unittest.main()
