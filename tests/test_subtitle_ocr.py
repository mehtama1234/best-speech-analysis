import unittest
import json
from pathlib import Path
from scripts.ocr_language_verification_frames import digest
from scripts.ocr_language_verification_frames import select_words


HEADER = 'level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext\n'


class SubtitleOCRTests(unittest.TestCase):
    def test_saved_provenance_and_review_scope(self):
        root = Path(__file__).resolve().parents[1]
        report = json.loads((root / 'research/subtitle-ocr-pilot.json').read_text())
        review = json.loads((root / 'research/subtitle-ocr-review.json').read_text())
        self.assertEqual(digest(root / review['report_path']), review['report_sha256'])
        self.assertFalse(review['held_out'])
        self.assertFalse(review['promoted_to_corpus'])
        self.assertEqual({c['decoded_pts_seconds'] for c in review['comparisons']}, {f['decoded_pts_seconds'] for f in report['frames']})
        for path, expected in report['source_sha256'].items():
            if path.startswith('data/cache/') and not (root / path).exists():
                continue
            self.assertEqual(digest(root / path), expected, path)
        for frame in report['frames']:
            self.assertIn('whole_frame_then_filter_baseline', frame)
            self.assertTrue(frame['text'])
            if (root / frame['frame_path']).exists():
                self.assertEqual(digest(root / frame['frame_path']), frame['frame_sha256'])
            for word in frame['words']:
                self.assertGreaterEqual(word['top'], report['roi_pixels']['top'])
                self.assertLessEqual(word['top'] + word['height'], report['roi_pixels']['bottom'])

    def test_roi_excludes_labels_and_clipped_tokens(self):
        rows = ['5\t1\t1\t1\t1\t1\t5\t200\t50\t20\t95\tLabel',
                '5\t1\t2\t1\t1\t1\t5\t250\t50\t20\t90\tword',
                '5\t1\t2\t1\t1\t2\t630\t250\t50\t20\t95\tclipped']
        result = select_words(HEADER + '\n'.join(rows), {'left': 0, 'top': 245, 'right': 640, 'bottom': 360})
        self.assertEqual(result['text'], 'word')
        self.assertEqual(result['words'][0]['ocr_confidence'], 90)

    def test_line_order_does_not_sort_individual_word_heights(self):
        rows = ['5\t1\t1\t1\t1\t1\t5\t252\t20\t20\t90\tfirst',
                '5\t1\t1\t1\t1\t2\t40\t250\t20\t20\t90\tsecond',
                '5\t1\t2\t1\t1\t1\t5\t300\t20\t20\t90\tthird']
        result = select_words(HEADER + '\n'.join(rows), {'left': 0, 'top': 245, 'right': 640, 'bottom': 360})
        self.assertEqual(result['text'], 'first second\nthird')
