import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.package_recovered_pattern_priority_review import build


class PriorityReviewerPackTests(unittest.TestCase):
    def test_builds_verified_blinded_archive_without_private_key(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "reviewer-pack.zip"
            result = build(output)
            self.assertEqual(result["item_count"], 162)
            self.assertEqual(result["pattern_count"], 55)
            self.assertFalse(result["private_key_included"])
            self.assertTrue(result["checksums_verified"])
            with zipfile.ZipFile(output) as archive:
                names = set(archive.namelist())
                self.assertEqual(
                    names,
                    {
                        "README-reviewer.md",
                        "recovered-pattern-priority-review.html",
                        "recovered-pattern-priority-review.json",
                        "SHA256SUMS",
                    },
                )
                self.assertNotIn("recovered-pattern-priority-review-key.json", names)
                self.assertIn(b"must not have seen the internal mapping key", archive.read("README-reviewer.md"))


if __name__ == "__main__":
    unittest.main()
