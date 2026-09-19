import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CommunicationJobDeliveryBrowserSmokeTests(unittest.TestCase):
    def test_smoke_script_is_present(self):
        self.assertTrue((ROOT / "scripts/check_communication_job_delivery_browser.py").exists())


if __name__ == "__main__":
    unittest.main()
