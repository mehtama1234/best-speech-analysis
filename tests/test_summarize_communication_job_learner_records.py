import json
import unittest
from pathlib import Path

from scripts.summarize_communication_job_learner_records import summarize

ROOT = Path(__file__).resolve().parents[1]


class SummarizeCommunicationJobLearnerRecordsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.protocol = json.loads((ROOT / "research/communication-job-learner-check.json").read_text())

    def synthetic(self, participant: str, score: str = "2"):
        responses = {"participant_code": participant, "date": "2026-09-18", "lesson_version": "test", "consent": True}
        for card in self.protocol["cards"]:
            tasks = [task["task_id"] for task in self.protocol["tasks"] if task["card_id"] == card["card_id"]]
            responses[f"{card['card_id']}_task_ids"] = ",".join(tasks)
            for task_id in tasks: responses[task_id] = "synthetic response"
            for suffix in ("listener_restatement", "revision", "boundary_note"): responses[f"{card['card_id']}_{suffix}"] = "synthetic note"
            for dimension in card["scoring_dimensions"]: responses[f"{card['card_id']}_score_{dimension}"] = score
            responses[f"{card['card_id']}_safety_issue"] = "no"
        return {"record_type": "communication_job_learner_observation", "protocol_id": self.protocol["protocol_id"], "claim_boundary": self.protocol["claim_boundary"], "task_bank_ids": [task["task_id"] for task in self.protocol["tasks"]], "responses": responses}

    def test_summary_preserves_per_job_scores_and_boundary(self):
        report = summarize([self.synthetic("p1"), self.synthetic("p2", "1")], self.protocol)
        self.assertEqual(report["record_count"], 2)
        self.assertEqual(len(report["by_card"]), 18)
        self.assertEqual(report["by_card"][0]["scores"]["recognition"]["mean"], 1.5)
        self.assertIn("does not establish", report["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
