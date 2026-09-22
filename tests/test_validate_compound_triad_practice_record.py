import json
import unittest
from pathlib import Path

from scripts.validate_compound_triad_practice_record import validate


ROOT = Path(__file__).resolve().parents[1]


class CompoundTriadPracticeRecordTests(unittest.TestCase):
    def test_valid_example_shape(self):
        triad = json.loads((ROOT / "research/compound-pattern-triads.json").read_text())["triads"][0]
        record = {
            "record_type": "local_compound_triad_practice_record",
            "triad_id": triad["triad_id"],
            "source_review_ids": [example["review_id"] for example in triad["examples"]],
            "source_evidence_ids": [evidence for example in triad["examples"] for group in example["evidence_ids"] for evidence in group],
            "draft": "Move one. Move two. Move three.",
            "reflections": {"listener": "clear", "unclear": "none", "nonfit": "none", "revision": "shorten bridge"},
            "claim_boundary": "This is not effectiveness evidence.",
            "saved_at": "2026-09-20T00:00:00+00:00",
        }
        self.assertEqual(validate(record), [])


if __name__ == "__main__":
    unittest.main()
