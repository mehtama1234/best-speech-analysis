import json
import unittest
from pathlib import Path

from scripts.build_delivery_proxy_candidate_atlas import main


ROOT = Path(__file__).resolve().parents[1]


class DeliveryProxyCandidateAtlasTests(unittest.TestCase):
    def test_proxy_candidates_link_transcript_jobs_to_local_measurements(self):
        main()
        payload = json.loads((ROOT / "research/delivery-proxy-candidate-atlas.json").read_text())
        markdown = (ROOT / "writeups/delivery-proxy-candidate-atlas.md").read_text()
        browser = (ROOT / "writeups/delivery-proxy-candidate-atlas.html").read_text()
        self.assertEqual(payload["counts"]["candidate_record_count"], 1505)
        self.assertEqual(payload["counts"]["candidate_video_count"], 188)
        self.assertIn("not delivery validation", markdown)
        self.assertIn("proxy candidates", browser)
        self.assertIn("Human delivery review required", browser)
        self.assertIn("proxy_backed_clip_requires_human_delivery_review", {x["candidate_status"] for x in payload["candidates"]})


if __name__ == "__main__":
    unittest.main()
