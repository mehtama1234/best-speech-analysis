import unittest

from scripts.validate_cross_artifact_consistency import validate


class CrossArtifactConsistencyTests(unittest.TestCase):
    def test_primary_reports_reconcile(self):
        self.assertEqual(validate(), [])


if __name__ == "__main__":
    unittest.main()
