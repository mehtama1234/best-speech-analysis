#!/usr/bin/env python3
"""Audit recorded reading coverage and retain a stable full-corpus work order."""
import hashlib
import json
import random
from pathlib import Path
if __package__:
    from .review_evidence import context_digest
else:
    from review_evidence import context_digest

ROOT = Path(__file__).resolve().parents[1]
SEED = 20260918


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def coverage(videos, reviews, analytic_video_ids):
    inspected = set().union(*(set(r['context_evidence_ids']) for r in reviews))
    single = [set(r['context_evidence_ids']) for r in reviews]
    order = sorted(videos)
    random.Random(SEED).shuffle(order)
    rows = []
    for rank, vid in enumerate(order, 1):
        source = videos[vid]
        ids = set(source['evidence_ids'])
        covered = len(ids & inspected)
        restrictions = sorted({flag for review in reviews
                               if review.get('video_id') == vid
                               for flag in review.get('evidence_restrictions', [])})
        rows.append({'video_id': vid, 'order': rank, 'title': source['title'],
                     'evidence_restrictions': restrictions,
                     'caption_count': len(ids), 'word_count': source['word_count'],
                     'captions_in_inspected_contexts': covered,
                     'captions_outside_inspected_contexts': len(ids) - covered,
                     'all_captions_in_one_review': any(ids <= context for context in single),
                     'has_full_context_analytic_review': vid in analytic_video_ids,
                     'reading_action': ('resolve_source_restrictions' if restrictions else
                                        'extend_to_full_context_analysis' if vid not in analytic_video_ids else
                                        'analysis_recorded_not_independently_validated')})
    return rows


def main():
    names = ['research/contextual-label-reviews.json', 'research/passage-context-reviews.json', 'research/full-context-reviews.json']
    reviews = [r for name in names for r in json.loads((ROOT / name).read_text())['reviews']]
    analytic = {r['video_id'] for r in json.loads((ROOT / names[-1]).read_text())['reviews']}
    needed = {e for r in reviews for e in r['context_evidence_ids']}
    source_rows, videos = {}, {}
    registry = ROOT / 'research/segment-registry.jsonl'
    with registry.open() as stream:
        for line in stream:
            row = json.loads(line)
            vid, eid = row['video_id'], row['evidence_id']
            video = videos.setdefault(vid, {'title': row.get('title', vid), 'evidence_ids': [], 'word_count': 0})
            video['evidence_ids'].append(eid)
            video['word_count'] += row.get('word_count', len(row['text'].split()))
            if eid in needed:
                source_rows[eid] = row
    for review in reviews:
        if context_digest([source_rows[e] for e in review['context_evidence_ids']]) != review['context_sha256']:
            raise ValueError('Stale source context: ' + review['review_id'])
    rows = coverage(videos, reviews, analytic)
    inputs = [ROOT / n for n in names] + [registry, Path(__file__).resolve(), ROOT / 'scripts/review_evidence.py']
    report = {'schema_version': '1.0', 'seed': SEED,
              'scope': 'All currently nonempty canonical transcript videos, not the whole availability inventory. Unavailable sources and unpromoted recovery candidates remain separate work, not excluded from the project goal.',
              'order_policy': 'Sorted full video-ID frame shuffled once with fixed seed, then retained. Never prioritize short transcripts or keyword hits. Completed analytic reviews stay in the order; next work is the first row without one.',
              'coverage_policy': 'Membership in an assistant-inspected source context is not deep annotation, independent agreement, full original-event coverage or audiovisual review. A full-context analytic record is a separate milestone.',
              'source_sha256': {str(p.relative_to(ROOT)): digest(p) for p in inputs},
              'video_count': len(rows), 'caption_count': sum(r['caption_count'] for r in rows),
              'captions_in_inspected_contexts': sum(r['captions_in_inspected_contexts'] for r in rows),
              'videos_with_all_captions_in_one_review': sum(r['all_captions_in_one_review'] for r in rows),
              'full_context_analytic_review_count': len(analytic),
              'restricted_source_count': sum(bool(r['evidence_restrictions']) for r in rows),
              'restricted_sources': [r['video_id'] for r in rows if r['evidence_restrictions']],
              'videos': rows}
    output = ROOT / 'research/full-reading-queue.json'
    output.write_text(json.dumps(report, indent=2) + '\n')
    pending = [r for r in rows if not r['has_full_context_analytic_review']]
    print(json.dumps({k: report[k] for k in ['video_count', 'caption_count', 'captions_in_inspected_contexts', 'videos_with_all_captions_in_one_review', 'full_context_analytic_review_count']}))
    print(json.dumps({'next': pending[:3]}))


if __name__ == '__main__':
    main()
