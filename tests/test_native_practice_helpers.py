import unittest
from pathlib import Path


class NativePracticeHelperTests(unittest.TestCase):
    def test_shared_typescript_helper_contains_builder_and_diff(self):
        path = Path(__file__).resolve().parents[1] / "clients/examples/practice_record_helpers.ts"
        source = path.read_text()
        self.assertIn("createPracticeRecord", source)
        self.assertIn("changedResponses", source)
        self.assertIn("not learner-validation evidence", source)
        self.assertIn("provisional_not_validated", source)
        self.assertIn("practice_hypothesis", source)
        self.assertIn("safety_boundary", source)


if __name__ == "__main__":
    unittest.main()
