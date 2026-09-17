import json
import unittest
from pathlib import Path
from scripts.audit_transcript_coverage import summarize, classify_payload


class TranscriptCoveragePartitions(unittest.TestCase):
    def test_response_success_is_not_transcript_availability(self):
        self.assertEqual(classify_payload({'success': True, 'transcript': None}), ('null_transcript', []))
        self.assertEqual(classify_payload({'success': True, 'notFound': True}), ('provider_not_found', []))
        self.assertEqual(classify_payload({'success': True, 'transcript': []}), ('empty', []))
        self.assertEqual(classify_payload({'transcript': 'malformed'}), ('invalid', []))

    def test_cached_unlogged_is_not_missing_or_failed(self):
        rows = [dict(video_id='pilot', transcript_file=True, transcript_status='unlogged', cache_state='nonempty', segment_count=2),
                dict(video_id='empty', transcript_file=True, transcript_status='success', cache_state='empty', segment_count=0),
                dict(video_id='failed', transcript_file=False, transcript_status='failed', cache_state='missing', segment_count=0),
                dict(video_id='bad', transcript_file=True, transcript_status='success', cache_state='invalid', segment_count=0)]
        report = summarize(rows)
        self.assertEqual(report['transcript_file_count'], 3)
        self.assertEqual(report['successful_transcript_count'], 2)
        self.assertEqual(report['cached_unlogged_video_ids'], ['pilot'])
        self.assertEqual(report['empty_transcript_count'], 1)
        self.assertEqual(report['invalid_transcript_count'], 1)
        self.assertEqual(report['missing_transcript_count'], 1)

    def test_saved_partition_consistency(self):
        root = Path(__file__).resolve().parents[1]
        report = json.loads((root / 'data/metadata/transcript-coverage.json').read_text())
        for key, value in summarize(report['videos']).items():
            self.assertEqual(report[key], value, key)
        self.assertEqual(sum(r['video_count'] for r in report['status_cache_cross_tab']), report['unique_video_count'])
        self.assertEqual(report['transcript_file_count'], report['nonempty_transcript_count'] + report['empty_transcript_count'] + report['invalid_transcript_count'] + report['null_transcript_count'] + report['provider_not_found_count'])
        self.assertEqual(report['unique_video_count'], report['transcript_file_count'] + report['missing_transcript_count'])
