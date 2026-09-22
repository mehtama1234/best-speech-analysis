import unittest
import json
from pathlib import Path

from scripts.validate_practice_record import validate, validate_all_lesson_links


class PracticeRecordContractTests(unittest.TestCase):
    def test_all_18_lessons_have_valid_evidence_links(self):
        self.assertEqual(validate_all_lesson_links(), [])

    def test_json_schema_and_shared_model_require_the_same_fields(self):
        root = Path(__file__).resolve().parents[1]
        schema = json.loads((root / "research/practice-record.schema.json").read_text())
        model = json.loads((root / "research/shared-evidence-model.json").read_text())
        self.assertEqual(schema["required"], model["entity_types"]["practice_record"]["required"])

    def test_accepts_browser_native_shape(self):
        record = {
            "record_type": "local_communication_practice_record",
            "schema_version": "1.0",
            "lesson_id": "mobile:provisional-job-opening",
            "pattern_id": "provisional-job-opening",
            "canonical_job": "opening",
            "source_evidence_ids": ["dgkxN6RASpg:00000"],
            "delivery_sample_ids": ["delivery:opening:01"],
            "participant_code": "synthetic-local-user",
            "consent": True,
            "accessibility_or_modality": "typed",
            "step_responses": {"rehearse": "synthetic response"},
            "claim_boundary": "Local practice log only; not learner-validation evidence or effectiveness evidence.",
            "saved_at": "2026-09-19T00:00:00Z",
        }
        self.assertEqual(validate(record), [])

    def test_rejects_evidence_from_another_lesson(self):
        record = {
            "record_type": "local_communication_practice_record",
            "schema_version": "1.0",
            "lesson_id": "mobile:provisional-job-opening",
            "pattern_id": "provisional-job-opening",
            "canonical_job": "opening",
            "source_evidence_ids": ["not-linked:00001"],
            "delivery_sample_ids": ["delivery:closing:01"],
            "participant_code": "synthetic-local-user",
            "consent": True,
            "accessibility_or_modality": "typed",
            "step_responses": {},
            "claim_boundary": "Local practice log only; not learner-validation evidence or effectiveness evidence.",
            "saved_at": "2026-09-19T00:00:00Z",
        }
        errors = validate(record)
        self.assertTrue(any("source_evidence_ids" in error for error in errors))
        self.assertTrue(any("delivery_sample_ids" in error for error in errors))

    def test_rejects_missing_consent_and_unbounded_claim(self):
        record = {"record_type": "local_communication_practice_record", "schema_version": "1.0", "consent": False, "claim_boundary": "practice result"}
        errors = validate(record)
        self.assertIn("consent must be true before a record is saved", errors)
        self.assertIn("claim_boundary must preserve the non-effectiveness boundary", errors)


if __name__ == "__main__":
    unittest.main()
