import json
import unittest
from pathlib import Path

from scripts.build_full_delivery_proxy_index import main


ROOT = Path(__file__).resolve().parents[1]


class FullDeliveryProxyIndexTests(unittest.TestCase):
    def test_proxy_index_covers_local_reports_without_overclaiming(self):
        main()
        payload = json.loads((ROOT / "research/full-delivery-proxy-index.json").read_text())
        markdown = (ROOT / "writeups/full-delivery-proxy-index.md").read_text()
        self.assertEqual(payload["counts"]["feature_report_count"], 364)
        self.assertEqual(payload["counts"]["with_audio_windows"], 364)
        self.assertIn("not audiovisual validation", markdown)
        self.assertIn("do not establish gesture meaning", payload["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
