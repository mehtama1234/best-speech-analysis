import json
import unittest
from pathlib import Path

from scripts.summarize_communication_job_listener_records import summarize

ROOT = Path(__file__).resolve().parents[1]


class SummarizeCommunicationJobListenerRecordsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.protocol = json.loads((ROOT / "research/communication-job-listener-outcome-protocol.json").read_text())

    def synthetic(self, participant: str, score=2):
        responses = {
            "participant_code": participant, "date": "2026-09-18", "protocol_version": "test",
            "modality": "text", "stimulus_id": self.protocol["patterns"][0]["draft_stimulus_id"],
            "condition": "control", "scorer_id_or_blind_code": "blind-1", "consent": True,
            "accessibility_issue": "no",
        }
        for task in self.protocol["listener_tasks"]:
            responses[f"task_{task['task_id']}"] = "synthetic response"
            responses[f"score_{task['task_id']}"] = score
        return {"record_type": "communication_job_listener_outcome_observation", "protocol_id": self.protocol["protocol_id"], "responses": responses}

    def test_summary_preserves_task_scores_and_boundary(self):
        report = summarize([self.synthetic("p1"), self.synthetic("p2", 1)], self.protocol, allow_unlocked_synthetic=True)
        self.assertEqual(report["record_count"], 2)
        self.assertEqual(report["by_job_and_condition"][0]["task_scores"]["main_point_recall"]["mean"], 1.5)
        self.assertFalse(report["promotion_eligible"])
        self.assertIn("does not establish", report["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
