"""Transcript evidence must not depend on availability of sampled media."""
import unittest
import json
from pathlib import Path

from scripts.build_reviewed_delivery_report import build_patterns


class DeliveryProvenanceTests(unittest.TestCase):
    def make_pattern(self, segments, measured):
        rows = {"definition": [{"annotation_id": "r1", "evidence_id": "v:00000"}]}
        videos = {"v": {"url": "https://www.youtube.com/watch?v=v", "channel": "u"}}
        return build_patterns(rows, videos, measured, segments)["definition"]

    def test_transcript_survives_absent_media(self):
        result = self.make_pattern({"v:00000": {
            "text": "A definition.", "start_seconds": 12.5, "end_seconds": 14,
            "source_transcript_file": "data/transcripts/v.json",
        }}, {})
        example = result["examples"][0]
        self.assertEqual(example["text"], "A definition.")
        self.assertEqual(example["url"], "https://www.youtube.com/watch?v=v&t=12")
        self.assertEqual(example["end_seconds"], 14)
        self.assertEqual(example["measurement_status"], "no_aligned_features")
        self.assertEqual(result["measurement_summary"]["mean_rms_db"]["count"], 0)

    def test_registry_is_authoritative_for_text_and_time(self):
        result = self.make_pattern({"v:00000": {"text": "Original", "start_seconds": 0}},
                                   {"v:00000": {"text": "Stale", "start_seconds": 99,
                                                "mean_rms_db": -20}})
        example = result["examples"][0]
        self.assertEqual(example["text"], "Original")
        self.assertTrue(example["url"].endswith("&t=0"))
        self.assertEqual(example["measurements"]["mean_rms_db"], -20)

    def test_missing_transcript_is_explicit(self):
        result = self.make_pattern({}, {})
        example = result["examples"][0]
        self.assertEqual(example["transcript_evidence_status"], "missing_registry_segment")
        self.assertIsNone(example["text"])
        self.assertIsNone(example["start_seconds"])

    def test_published_examples_resolve_to_registry(self):
        root = Path(__file__).resolve().parents[1]
        report = json.loads((root / "research/reviewed-delivery-patterns.json").read_text())
        needed = {example["evidence_id"] for pattern in report["patterns_by_reviewed_function"].values()
                  for example in pattern["examples"]}
        with (root / "research/segment-registry.jsonl").open() as source:
            registry = {row["evidence_id"]: row for line in source for row in [json.loads(line)]
                        if row["evidence_id"] in needed}
        for pattern in report["patterns_by_reviewed_function"].values():
            for example in pattern["examples"]:
                source = registry[example["evidence_id"]]
                self.assertEqual(example["text"], source["text"])
                self.assertEqual(example["start_seconds"], source["start_seconds"])
                self.assertEqual(example["source_transcript_file"], source["source_transcript_file"])
                self.assertTrue(example["url"].endswith(f"&t={int(source['start_seconds'])}"))


if __name__ == "__main__":
    unittest.main()
