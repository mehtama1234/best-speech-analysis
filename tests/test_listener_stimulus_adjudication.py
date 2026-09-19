import json
from pathlib import Path
import unittest

from scripts.validate_listener_stimulus_adjudication import validate


ROOT = Path(__file__).resolve().parents[1]


class ListenerStimulusAdjudicationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = json.loads((ROOT / "research/communication-job-listener-stimulus-review-workbook.json").read_text())

    def test_empty_record_is_rejected(self):
        self.assertTrue(validate({}, self.workbook))

    def test_lock_requires_accessibility_safety_pass(self):
        record = {
            "record_type": "listener_stimulus_adjudication",
            "workbook_id": self.workbook["workbook_id"],
            "claim_boundary": "Explicit stimulus lock decision after independent review; lock is pilot readiness only, not listener outcome or communication-effectiveness evidence.",
            "adjudicator_code": "adj-1", "adjudication_date": "2026-09-18",
            "review_a_code": "review-a", "review_b_code": "review-b",
            "source_review_a": "a.json", "source_review_b": "b.json", "responses": {},
        }
        for number in range(1, 19):
            record["responses"][f"item_{number}_final_decision"] = "lock_for_pilot"
            record["responses"][f"item_{number}_accessibility_safety"] = "revise"
            record["responses"][f"item_{number}_rationale"] = "Synthetic test rationale."
        errors = validate(record, self.workbook)
        self.assertTrue(any("cannot lock" in error for error in errors))
