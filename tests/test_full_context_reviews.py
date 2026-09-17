import json
import unittest
from pathlib import Path
from scripts.review_evidence import context_digest

ROOT = Path(__file__).resolve().parents[1]


class FullContextReviewTests(unittest.TestCase):
    def test_complete_retained_context_and_relation_provenance(self):
        reviews = json.loads((ROOT / 'research/full-context-reviews.json').read_text())['reviews']
        wanted = {r['video_id'] for r in reviews}
        source = {v: [] for v in wanted}
        with (ROOT / 'research/segment-registry.jsonl').open() as stream:
            for line in stream:
                # Cheap prefilter only; parsed video ID remains authoritative.
                if any(v in line for v in wanted):
                    row = json.loads(line)
                    if row['video_id'] in source:
                        source[row['video_id']].append(row)
        prior = {r['review_id']: r for name in ['passage-context-reviews.json', 'contextual-label-reviews.json']
                 for r in json.loads((ROOT / 'research' / name).read_text())['reviews']}
        for review in reviews:
            rows = source[review['video_id']]
            ids = [r['evidence_id'] for r in rows]
            self.assertEqual(review['context_evidence_ids'], ids)
            self.assertEqual(review['context_sha256'], context_digest(rows))
            self.assertEqual(review['modality'], 'transcript_only')
            if 'extends_review_id' in review:
                self.assertTrue(set(prior[review['extends_review_id']]['context_evidence_ids']) <= set(ids))
            episodes = [e for episode in review['episode_map'] for e in episode['evidence_ids']]
            self.assertEqual(episodes, ids)
            for relation in review['relations']:
                for field in ['from_evidence_ids', 'to_evidence_ids', 'intervening_evidence_ids']:
                    self.assertTrue(set(relation.get(field, [])) <= set(ids))
            for boundary in review['boundary_cases']:
                self.assertTrue(set(boundary['evidence_ids']) <= set(ids))
            self.assertTrue((ROOT / review['writeup']).is_file())
