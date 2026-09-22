import unittest

from scripts.validate_autonomous_counterexample_screening import validate


class ValidateAutonomousCounterexampleScreeningTest(unittest.TestCase):
    def test_screening_is_complete_and_unpromoted(self):
        self.assertEqual(validate(), [])


if __name__ == "__main__":
    unittest.main()
