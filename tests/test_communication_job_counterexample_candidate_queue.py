import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CommunicationJobCounterexampleCandidateQueueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.queue = json.loads((ROOT / "research/communication-job-counterexample-candidate-queue.json").read_text())

    def test_routes_all_slots_without_confirming_any(self):
        self.assertEqual(self.queue["job_count"], 18)
        self.assertEqual(self.queue["candidate_count"], 90)
        self.assertEqual(self.queue["source_linked_candidate_count"], 54)
        self.assertEqual(self.queue["confirmed_counterexample_count"], 0)
        self.assertEqual(self.queue["status"], "candidate_queue_not_independently_reviewed")
        self.assertTrue(all(item["candidate_status"] == "candidate_requires_check" for item in self.queue["items"]))


if __name__ == "__main__":
    unittest.main()
