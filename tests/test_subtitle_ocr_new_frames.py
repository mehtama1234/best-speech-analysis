import json
import unittest
from pathlib import Path
from scripts.ocr_language_verification_frames import digest

ROOT = Path(__file__).resolve().parents[1]


class NewFrameOCRTests(unittest.TestCase):
    def test_frozen_inputs_and_complete_review(self):
        report = json.loads((ROOT / 'research/subtitle-ocr-new-frames.json').read_text())
        review = json.loads((ROOT / 'research/subtitle-ocr-new-frame-review.json').read_text())
        self.assertEqual(digest(ROOT / review['report_path']), review['report_sha256'])
        self.assertEqual([f['requested_seek_seconds'] for f in report['frames']], report['requested_times'])
        self.assertEqual([f['requested_seek_seconds'] for f in review['comparisons']], report['requested_times'])
        self.assertEqual(len(set(report['requested_times'])), 8)
        self.assertFalse(review['preprocessing_changed_after_results'])
        self.assertFalse(review['independent_reviewer'])
        for path, expected in report['source_sha256'].items():
            if path.startswith('data/video/') and not (ROOT / path).exists():
                continue
            self.assertEqual(digest(ROOT / path), expected)
        self.assertEqual(report['frozen_pilot_sha256'], digest(ROOT / 'scripts/ocr_language_verification_frames.py'))

    def test_counts_include_absent_subtitle_false_positives(self):
        review = json.loads((ROOT / 'research/subtitle-ocr-new-frame-review.json').read_text())
        rows, counts = review['comparisons'], review['counts']
        self.assertEqual(counts['frames'], len(rows))
        self.assertEqual(counts['subtitle_present'], sum(r['visible_subtitle_in_region'] for r in rows))
        self.assertEqual(counts['subtitle_absent'], sum(not r['visible_subtitle_in_region'] for r in rows))
        self.assertEqual(counts['exact_subtitle_matches'], sum(r['classification'] == 'exact_visible_subtitle' for r in rows))
        self.assertEqual(counts['false_text_detections_on_absent_frames'], sum(not r['visible_subtitle_in_region'] and r['classification'] == 'false_text_detection' for r in rows))
        self.assertFalse(review['promoted_to_corpus'])

    def test_cached_pixels_when_available(self):
        report = json.loads((ROOT / 'research/subtitle-ocr-new-frames.json').read_text())
        available = [f for f in report['frames'] if (ROOT / f['frame_path']).exists()]
        if not available:
            self.skipTest('Ignored frame cache absent')
        for frame in available:
            self.assertEqual(digest(ROOT / frame['frame_path']), frame['frame_sha256'])
