import json
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("expanded_record_validator", ROOT / "scripts/validate_expanded_pattern_practice_record.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class ExpandedPatternPracticeRecordValidatorTests(unittest.TestCase):
    def test_example_record_is_valid(self):
        record = json.loads((ROOT / "research/expanded-pattern-practice-record.example.json").read_text())
        self.assertEqual(MODULE.validate(record), [])

    def test_unlinked_evidence_is_rejected(self):
        record = json.loads((ROOT / "research/expanded-pattern-practice-record.example.json").read_text())
        record["source_evidence_ids"].append("not-linked:00001")
        self.assertTrue(any("not linked" in error for error in MODULE.validate(record)))


if __name__ == "__main__":
    unittest.main()
