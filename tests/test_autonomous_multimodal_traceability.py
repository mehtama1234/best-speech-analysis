import unittest

from scripts.validate_autonomous_multimodal_traceability import validate


class AutonomousMultimodalTraceabilityTest(unittest.TestCase):
    def test_delivery_samples_trace_to_local_measurements_and_limits(self):
        self.assertEqual(validate(), [])


if __name__ == "__main__":
    unittest.main()
