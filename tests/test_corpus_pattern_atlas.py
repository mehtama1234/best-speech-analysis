import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CorpusPatternAtlasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.atlas = json.loads((ROOT / "research/corpus-pattern-atlas.json").read_text())

    def test_atlas_preserves_transcript_boundary_and_corpus_scope(self):
        self.assertEqual(self.atlas["transcript_boundary"], "transcript_only")
        # The corpus has 395 nonempty transcript videos; one is excluded from
        # phrase indexing by an explicit source-restriction record.
        self.assertEqual(self.atlas["eligible_video_count"], 394)
        self.assertEqual(len(self.atlas["excluded_source_segments"]), 1)
        self.assertGreater(self.atlas["eligible_segment_count"], 100000)

    def test_every_video_has_candidate_and_phrase_fields(self):
        self.assertEqual(len(self.atlas["videos"]), self.atlas["eligible_video_count"])
        for video in self.atlas["videos"]:
            self.assertTrue(video["video_id"])
            self.assertIn("candidate_function_counts", video)
            self.assertIn("phrase_candidates", video)
            self.assertIn("phrase_segment_counts", video)
            self.assertIn("phrase_form_counts", video)
            self.assertIn(video["event_split"], {"train", "holdout"})
            self.assertEqual(video["transcript_evidence_status"], "full_retained_transcript_reviewed")

    def test_phrase_families_remain_provisional(self):
        self.assertGreaterEqual(len(self.atlas["phrase_forms"]), 8)
        for info in self.atlas["phrase_forms"].values():
            self.assertEqual(info["status"], "heuristic_retrieval_aid_requires_manual_review")
            self.assertTrue(info["phrase_forms"])
            self.assertGreaterEqual(info["segment_hit_count"], 0)
            self.assertGreaterEqual(info["video_hit_count"], 0)
            self.assertEqual(set(info["form_hit_counts"]), set(info["phrase_forms"]))
            for split in ("train", "holdout"):
                holdout = info["event_level_holdout"][split]
                self.assertEqual(set(holdout["form_hit_counts"]), set(info["phrase_forms"]))
                self.assertGreaterEqual(holdout["video_hit_count"], 0)

    def test_candidate_function_inventory_has_video_denominators(self):
        inventory = self.atlas["candidate_function_summary"]
        self.assertTrue(inventory)
        self.assertIn("question", inventory)
        for info in inventory.values():
            self.assertEqual(info["status"], "heuristic_candidate_label_requires_manual_review")
            self.assertGreaterEqual(info["video_hit_count"], 0)
            self.assertGreaterEqual(info["segment_hit_count"], 0)

    def test_candidate_function_review_queue_is_balanced(self):
        queue = self.atlas["candidate_function_review_queue"]
        self.assertEqual(queue["item_count"], len(queue["items"]))
        labels = {item["candidate_function"] for item in queue["items"]}
        self.assertEqual(len(labels), 8)
        for label in labels:
            items = [item for item in queue["items"] if item["candidate_function"] == label]
            self.assertLessEqual(len(items), 24)
            self.assertGreater(len(items), 0)
            self.assertEqual({item["event_split"] for item in items}, {"train", "holdout"})
            self.assertEqual(
                len(items),
                self.atlas["candidate_function_summary"][label]["stratified_review_queue_item_count"],
            )

    def test_recurrence_queue_is_stratified_and_deterministic(self):
        queue = self.atlas["recurrence_review_queue"]
        self.assertEqual(queue["item_count"], len(queue["items"]))
        self.assertEqual(queue["item_count"], 192)
        for label in self.atlas["phrase_forms"]:
            items = [item for item in queue["items"] if item["phrase_family"] == label]
            self.assertEqual(len(items), 24)
            self.assertEqual({item["event_split"] for item in items}, {"train", "holdout"})
            self.assertTrue(all(item["required_checks"] for item in items))


if __name__ == "__main__":
    unittest.main()
