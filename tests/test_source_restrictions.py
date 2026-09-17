import json
import unittest
from collections import Counter
from pathlib import Path
from scripts.source_restrictions import restrictions_by_video

ROOT = Path(__file__).resolve().parents[1]


class SourceRestrictionTests(unittest.TestCase):
    def test_flags_accumulate_and_unreviewed_is_not_certified(self):
        self.assertEqual(restrictions_by_video([
            {'video_id': 'v', 'evidence_restrictions': ['timing']},
            {'video_id': 'v', 'evidence_restrictions': ['pairing', 'timing']},
            {'video_id': 'w'}]), {'v': ['pairing', 'timing']})

    def test_saved_aggregates_honor_known_restriction(self):
        vid = 'bV5uKHsWQtY'
        overview = json.loads((ROOT / 'research/corpus-overview.json').read_text())
        row = next(r for r in overview['videos'] if r['video_id'] == vid)
        self.assertEqual(row['segment_count'], 465)
        self.assertIsNone(row['approx_words_per_minute'])
        self.assertEqual(row['rate_status'], 'withheld_source_restriction')
        candidates = json.loads((ROOT / 'research/candidate-patterns.json').read_text())
        self.assertEqual(candidates['excluded_source_segments'][vid], 465)
        for pattern in candidates['patterns'].values():
            self.assertFalse(any(e['video_id'] == vid for e in pattern['examples']))

    def test_candidate_counts_exclude_all_restricted_rows(self):
        report = json.loads((ROOT / 'research/candidate-patterns.json').read_text())
        counts = Counter()
        with (ROOT / 'research/segment-registry.jsonl').open() as stream:
            for line in stream:
                row = json.loads(line)
                if row['video_id'] not in report['source_restrictions']:
                    counts.update(row['candidate_speech_functions'])
        self.assertEqual(dict(counts), {k: v['segment_count'] for k, v in report['patterns'].items()})
