import copy
import json
import unittest
from pathlib import Path

from scripts.validate_communication_job_listener_record import validate


ROOT = Path(__file__).resolve().parents[1]


class CommunicationJobListenerProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.protocol = json.loads((ROOT / "research/communication-job-listener-outcome-protocol.json").read_text())
        cls.html = (ROOT / "writeups/communication-job-listener-record.html").read_text()
        cls.markdown = (ROOT / "writeups/communication-job-listener-outcome-protocol.md").read_text()

    def test_design_covers_all_jobs_and_is_not_run(self):
        self.assertEqual(self.protocol["status"], "design_complete_not_run")
        self.assertEqual(len(self.protocol["patterns"]), 18)
        self.assertFalse(self.protocol["stimulus_pairs_locked"])
        self.assertEqual(self.protocol["stimulus_pair_count"], 18)
        self.assertEqual(self.protocol["stimulus_preflight_status"], "automated_screening_not_independent_review")
        self.assertEqual(self.protocol["patterns"][0]["draft_stimulus_status"], "draft_requires_matching_readability_accessibility_and_safety_review")
        self.assertEqual(len(self.protocol["listener_tasks"]), 6)
        self.assertIn("trust", self.protocol["claim_boundary"])
        self.assertEqual(self.protocol["scoring_schema"]["scale"], "0-2")
        self.assertIn("Download JSON record", self.html)
        self.assertIn("score_main_point_recall", self.html)
        self.assertIn("save-draft", self.html)
        self.assertIn("restore-draft", self.html)
        self.assertIn("clear-draft", self.html)
        self.assertIn("stimulus pairs locked: **no**", self.markdown)
        self.assertIn("Status: **design complete, not run**", self.markdown)

    def test_validator_accepts_complete_synthetic_record_and_rejects_missing(self):
        record = {
            "record_type": "communication_job_listener_outcome_observation",
            "protocol_id": self.protocol["protocol_id"],
            "responses": {
                "participant_code": "synthetic", "date": "2026-09-18", "protocol_version": "test",
                "modality": "text", "stimulus_id": "synthetic-pair-01", "condition": "control",
                "scorer_id_or_blind_code": "blind-1", "consent": True,
                "accessibility_issue": "no",
            },
        }
        for task in self.protocol["listener_tasks"]:
            record["responses"][f"task_{task['task_id']}"] = "synthetic response"
            record["responses"][f"score_{task['task_id']}"] = 2
        self.assertTrue(any("stimulus pairs" in error for error in validate(record, self.protocol)))
        self.assertEqual(validate(record, self.protocol, allow_unlocked_synthetic=True), [])
        incomplete = copy.deepcopy(record)
        del incomplete["responses"]["task_main_point_recall"]
        self.assertTrue(any("main_point_recall" in error for error in validate(incomplete, self.protocol, allow_unlocked_synthetic=True)))


if __name__ == "__main__":
    unittest.main()
