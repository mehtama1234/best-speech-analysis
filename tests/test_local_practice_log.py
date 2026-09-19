import unittest

from scripts.validate_local_practice_log import validate


class LocalPracticeLogTests(unittest.TestCase):
    def test_contract_accepts_bounded_record(self):
        record = {
            "schema_version": "1.0",
            "record_type": "local_learner_practice_log",
            "claim_boundary": "This is not proof of effectiveness.",
            "records": [{
                "record_type": "local_learner_practice",
                "schema_version": "1.0",
                "created_at": "2026-09-19T00:00:00Z",
                "card_id": "example:1",
                "video_id": "example",
                "title": "Synthetic contract fixture",
                "canonical_job": "opening",
                "source_evidence_ids": ["example:00001"],
                "delivery_mode": "typed",
                "adapted_wording": "I will explain the decision and its limit.",
                "listener_restatement": "The listener restated the purpose.",
                "non_fit_or_safety_note": "No personal disclosure required.",
                "revision": "Shorten the first sentence.",
                "claim_boundary": "This record is not effectiveness evidence."
            }]
        }
        self.assertEqual(validate(record), [])

    def test_contract_rejects_unbounded_mode(self):
        record = {"schema_version": "1.0", "record_type": "local_learner_practice_log", "claim_boundary": "not effectiveness", "records": [{"record_type": "local_learner_practice", "delivery_mode": "unbounded"}]}
        self.assertTrue(validate(record))


if __name__ == "__main__":
    unittest.main()
