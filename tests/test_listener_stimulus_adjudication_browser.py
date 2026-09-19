from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ListenerStimulusAdjudicationBrowserSmokeTest(unittest.TestCase):
    def test_browser_smoke_script_exists(self):
        self.assertTrue((ROOT / "scripts/check_listener_stimulus_adjudication_browser.py").is_file())
