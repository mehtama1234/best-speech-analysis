import json
import unittest
from pathlib import Path
from scripts.build_passage_synthesis import resolve, digest


class PassageSynthesisTests(unittest.TestCase):
    def test_resolution_preserves_context_only_evidence(self):
        reviews = {"r": {"observations": [{"function": "example", "reason": "test",
                    "evidence_ids": ["v:1", "v:2"]}], "context_evidence_ids": ["v:1", "v:2"],
                    "core_evidence_ids": ["v:2"], "passage_id": "p", "format_evidence": "unknown", "writeup": "w"}}
        source = {"v:1": {"video_id": "v", "start_seconds": 1.5, "end_seconds": 4},
                  "v:2": {"video_id": "v", "start_seconds": 2, "end_seconds": 3}}
        row = resolve({"review_id": "r", "observation_index": 0}, reviews, source)
        self.assertEqual(row["sampled_core_overlap_count"], 1)
        self.assertEqual(row["context_only_count"], 1)
        self.assertEqual(row["end_seconds"], 4)
        self.assertTrue(row["url"].endswith("&t=1"))
        with self.assertRaises(ValueError):
            resolve({"review_id": "r", "observation_index": -1}, reviews, source)

    def test_published_links_and_input_hashes(self):
        root = Path(__file__).resolve().parents[1]
        report = json.loads((root / "research/passage-synthesis.json").read_text())
        reviews = {r["review_id"]: r for r in json.loads((root / "research/passage-context-reviews.json").read_text())["reviews"]}
        for path, expected in report["source_sha256"].items():
            self.assertEqual(digest(root / path), expected, path)
        self.assertEqual(report["reviewed_core_captions"], len({e for r in reviews.values() for e in r["core_evidence_ids"]}))
        for card in report["cards"]:
            self.assertTrue(card["supports"] and card["contrasts"] and card["limit"] and card["test"])
            self.assertEqual(card["delivery_effect"], "not measured")
            self.assertEqual(card["linked_support_video_count"], len({r["video_id"] for r in card["supports"]}))
            for item in card["supports"] + card["contrasts"]:
                observation = reviews[item["review_id"]]["observations"][item["observation_index"]]
                self.assertEqual(item["evidence_ids"], observation["evidence_ids"])
                self.assertEqual(item["reason"], observation["reason"])
                self.assertEqual(item["sampled_core_overlap_count"] + item["context_only_count"], len(set(item["evidence_ids"])))
