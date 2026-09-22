from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ListenerStimulusAdjudicationBrowserSmokeTest(unittest.TestCase):
    def test_browser_smoke_script_exists(self):
        self.assertTrue((ROOT / "scripts/check_listener_stimulus_adjudication_browser.py").is_file())

    def test_export_feedback_is_announced(self):
        review = (ROOT / "writeups/communication-job-listener-stimulus-review-workbook.html").read_text()
        adjudication = (ROOT / "writeups/communication-job-listener-stimulus-adjudication.html").read_text()
        for source in (review, adjudication):
            self.assertIn('lang="en"', source)
            self.assertIn('id="export-status" aria-live="polite"', source)
            self.assertIn("downloaded locally", source)
