import unittest

from scripts.validate_autonomous_media_recovery import validate


class AutonomousMediaRecoveryTest(unittest.TestCase):
    def test_partial_recovery_is_routed_without_promotion(self):
        self.assertEqual(validate(), [])


if __name__ == "__main__":
    unittest.main()
