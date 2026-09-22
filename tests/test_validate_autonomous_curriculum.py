import unittest

from scripts.validate_autonomous_curriculum import validate


class ValidateAutonomousCurriculumTest(unittest.TestCase):
    def test_autonomous_curriculum_passes_adversarial_checks(self):
        self.assertEqual(validate(), [])


if __name__ == "__main__":
    unittest.main()
