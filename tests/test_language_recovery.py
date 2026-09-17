import unittest
import json
import hashlib
from pathlib import Path
from scripts.recover_transcript_language import inspect_segments


class LanguageRecoveryTests(unittest.TestCase):
    def test_saved_candidates_and_reviews_preserve_lineage(self):
        root = Path(__file__).resolve().parents[1]
        reviews = json.loads((root / 'research/recovery-quality-reviews.json').read_text())['reviews']
        for review in reviews:
            path = root / review['candidate_path']
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), review['candidate_sha256'])
            payload = json.loads(path.read_text())
            self.assertEqual(len(payload['transcript']), review['segment_count'])
            self.assertTrue(all(0 <= i < review['segment_count'] for i in review['inspected_ordinals']))
            self.assertEqual(len(review['inspected_ordinals']), len(set(review['inspected_ordinals'])))
            attempt = json.loads((root / 'research/transcript-recovery-attempts' / (review['attempt_id'] + '.json')).read_text())
            self.assertEqual(attempt['candidate_sha256'], review['candidate_sha256'])
            self.assertEqual(hashlib.sha256((root / attempt['original_path']).read_bytes()).hexdigest(), attempt['original_sha256'])
            self.assertFalse(attempt['promoted_to_corpus'])
            self.assertEqual(inspect_segments(payload)['state'], attempt['state'])

    def test_null_and_empty_are_not_successful_recovery(self):
        for payload in [{'success': True, 'transcript': None}, {'transcript': []}, {'notFound': True}]:
            self.assertEqual(inspect_segments(payload)['state'], 'no_segments')

    def test_timestamped_text_is_only_a_candidate(self):
        r = inspect_segments({'transcript': [{'startMs': '100', 'endMs': '250', 'text': 'नमस्ते'}]})
        self.assertEqual(r['state'], 'timestamped_candidate')
        self.assertEqual(r['segment_count'], 1)

    def test_bad_boundaries_and_missing_text_are_flagged(self):
        rows = [{'startMs': 20, 'endMs': 10, 'text': 'x'}, {'startMs': 'nan', 'endMs': 30, 'text': 'x'},
                {'startMs': 0, 'endMs': 10, 'text': ''}, None]
        r = inspect_segments({'transcript': rows})
        self.assertEqual(r['state'], 'segments_need_repair')
        self.assertEqual(r['invalid_ordinals'], [0, 1, 2, 3])
