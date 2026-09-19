import json
import unittest
from pathlib import Path

from scripts.validate_reproducibility_manifest import validate

ROOT = Path(__file__).resolve().parents[1]


class ReproducibilityManifestTests(unittest.TestCase):
    def test_manifest_hashes_authoritative_artifacts(self):
        manifest = json.loads((ROOT / "research/reproducibility-manifest.json").read_text())
        self.assertEqual(validate(manifest), [])
        self.assertEqual(manifest["coverage_snapshot"]["full_context_reviews"], 395)
        self.assertGreaterEqual(len(manifest["artifacts"]), 20)


if __name__ == "__main__":
    unittest.main()
