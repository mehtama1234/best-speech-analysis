import json
import unittest
from pathlib import Path

from scripts.validate_compound_pattern_practice_record import validate


ROOT = Path(__file__).resolve().parents[1]


class CompoundPracticeRecordTests(unittest.TestCase):
    def test_example_record_is_valid(self):
        record = json.loads((ROOT / "research/compound-pattern-practice-record.example.json").read_text())
        self.assertEqual(validate(record), [])

    def test_unlinked_evidence_is_rejected(self):
        record = json.loads((ROOT / "research/compound-pattern-practice-record.example.json").read_text())
        record["source_evidence_ids"].append("not-linked:00000")
        self.assertTrue(any("source_evidence_ids" in error for error in validate(record)))


if __name__ == "__main__":
    unittest.main()
