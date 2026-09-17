import unittest
import json
from pathlib import Path
from scripts.build_blind_passage_sample import choose
from scripts.review_evidence import context_digest


class BlindPassageSampleTests(unittest.TestCase):
    def test_saved_selection_and_review_provenance(self):
        root = Path(__file__).resolve().parents[1]
        sample = json.loads((root / "research/blind-passage-sample.json").read_text())
        expected = choose({v: r["block_count"] for v, r in sample["sampling_frame"].items()},
                          sample["video_sample_size"], sample["seed"])
        self.assertEqual({r["video_id"]: r["block_index"] for r in sample["passages"]}, expected)
        passages = {r["passage_id"]: r for r in sample["passages"]}
        reviews = json.loads((root / "research/passage-context-reviews.json").read_text())["reviews"]
        needed = {eid for r in reviews for eid in r["context_evidence_ids"]}
        sources = {}
        with (root / "research/segment-registry.jsonl").open() as stream:
            for line in stream:
                row = json.loads(line)
                if row["evidence_id"] in needed:
                    sources[row["evidence_id"]] = row
        for review in reviews:
            passage = passages[review["passage_id"]]
            self.assertEqual(review["core_evidence_ids"], passage["core_evidence_ids"])
            self.assertTrue(set(review["core_evidence_ids"]) <= set(review["context_evidence_ids"]))
            self.assertEqual(context_digest([sources[eid] for eid in review["context_evidence_ids"]]), review["context_sha256"])
            self.assertEqual(review["modality"], "transcript_only")
            self.assertTrue((root / review["writeup"]).is_file())
            for observation in review["observations"]:
                self.assertTrue(set(observation["evidence_ids"]) <= set(review["context_evidence_ids"]))
        self.assertEqual(len({r["passage_id"] for r in reviews}), len(reviews))

    def test_reproducible_and_input_order_independent(self):
        counts = {"z": 3, "b": 2, "a": 1, "m": 5}
        self.assertEqual(choose(counts, 3), choose(dict(reversed(list(counts.items()))), 3))
        selected = choose(counts, 3)
        self.assertEqual(len(selected), 3)
        for vid, block in selected.items():
            self.assertGreaterEqual(block, 0)
            self.assertLess(block, counts[vid])

    def test_short_video_and_empty_frame(self):
        self.assertEqual(choose({"a": 1}), {"a": 0})
        self.assertEqual(choose({}), {})
        with self.assertRaises(ValueError):
            choose({"a": 0})
