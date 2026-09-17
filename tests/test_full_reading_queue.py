import json
import unittest
from pathlib import Path
from scripts.build_full_reading_queue import coverage, digest

ROOT = Path(__file__).resolve().parents[1]


class FullReadingQueueTests(unittest.TestCase):
    def test_reading_does_not_clear_source_restriction(self):
        videos = {'v': {'title': 'mismatch', 'evidence_ids': ['v:1'], 'word_count': 1}}
        reviews = [{'video_id': 'v', 'context_evidence_ids': ['v:1'],
                    'evidence_restrictions': ['video_transcript_pairing_unverified']}]
        row = coverage(videos, reviews, {'v'})[0]
        self.assertTrue(row['has_full_context_analytic_review'])
        self.assertEqual(row['reading_action'], 'resolve_source_restrictions')
        self.assertEqual(row['evidence_restrictions'], ['video_transcript_pairing_unverified'])

    def test_union_is_not_single_review_or_analytic_completion(self):
        videos = {'v': {'title': 'test', 'evidence_ids': ['v:1', 'v:2'], 'word_count': 2},
                  'w': {'title': 'test2', 'evidence_ids': ['w:1'], 'word_count': 1}}
        reviews = [{'context_evidence_ids': ['v:1']}, {'context_evidence_ids': ['v:2']}]
        rows = coverage(videos, reviews, set())
        row = next(r for r in rows if r['video_id'] == 'v')
        self.assertEqual(row['captions_in_inspected_contexts'], 2)
        self.assertFalse(row['all_captions_in_one_review'])
        self.assertFalse(row['has_full_context_analytic_review'])
        self.assertEqual(rows, coverage(dict(reversed(list(videos.items()))), reviews, set()))

    def test_saved_counts_and_provenance(self):
        report = json.loads((ROOT / 'research/full-reading-queue.json').read_text())
        rows = report['videos']
        self.assertEqual(report['video_count'], len(rows))
        self.assertEqual(report['caption_count'], sum(r['caption_count'] for r in rows))
        self.assertEqual(report['captions_in_inspected_contexts'], sum(r['captions_in_inspected_contexts'] for r in rows))
        self.assertEqual(report['full_context_analytic_review_count'], sum(r['has_full_context_analytic_review'] for r in rows))
        for r in rows:
            self.assertEqual(r['caption_count'], r['captions_in_inspected_contexts'] + r['captions_outside_inspected_contexts'])
        for path, expected in report['source_sha256'].items():
            self.assertEqual(digest(ROOT / path), expected)
