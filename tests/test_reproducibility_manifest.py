import json
import unittest
from pathlib import Path

from scripts.build_reproducibility_manifest import build
from scripts.validate_reproducibility_manifest import validate

ROOT = Path(__file__).resolve().parents[1]


class ReproducibilityManifestTests(unittest.TestCase):
    def test_manifest_hashes_authoritative_artifacts(self):
        manifest = json.loads((ROOT / "research/reproducibility-manifest.json").read_text())
        # Other unit tests intentionally regenerate checked-in research reports.
        # Do not make the full suite order-dependent by requiring the checked-in
        # receipt to remain unchanged after those tests run. The release audit
        # validates the checked-in receipt at the end of its build sequence;
        # here, validate a freshly constructed manifest and separately verify
        # that the checked-in receipt has the expected shape.
        current = build()
        self.assertEqual(validate(current), [])
        self.assertEqual(manifest["manifest_id"], current["manifest_id"])
        self.assertEqual(manifest["coverage_snapshot"]["unique_inventory_videos"], 480)
        self.assertEqual(manifest["coverage_snapshot"]["nonempty_transcript_videos"], 395)
        self.assertEqual(manifest["coverage_snapshot"]["full_context_reviews"], 395)
        self.assertGreaterEqual(len(manifest["artifacts"]), 20)


if __name__ == "__main__":
    unittest.main()
