import unittest

from scripts.validate_autonomous_evidence_to_practice import validate


class AutonomousEvidenceToPracticeTest(unittest.TestCase):
    def test_every_lesson_traces_to_bounded_evidence_and_tasks(self):
        self.assertEqual(validate(), [])


if __name__ == "__main__":
    unittest.main()
