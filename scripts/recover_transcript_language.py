#!/usr/bin/env python3
"""One explicit language recovery attempt; never replace original evidence."""
import argparse
import hashlib
import json
import math
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

if __package__:
    from .download_transcripts import load_key, ENDPOINT
else:
    from download_transcripts import load_key, ENDPOINT

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect_segments(payload):
    if not isinstance(payload, dict):
        return {'state': 'invalid_payload', 'segment_count': 0, 'invalid_ordinals': []}
    rows = payload.get('transcript')
    if not isinstance(rows, list) or not rows:
        return {'state': 'no_segments', 'segment_count': 0, 'invalid_ordinals': []}
    invalid = []
    for i, row in enumerate(rows):
        try:
            start, end = float(row['startMs']), float(row['endMs'])
            valid = math.isfinite(start) and math.isfinite(end) and 0 <= start <= end
            valid = valid and isinstance(row['text'], str) and bool(row['text'].strip())
        except (TypeError, KeyError, ValueError, OverflowError):
            valid = False
        if not valid:
            invalid.append(i)
    return {'state': 'timestamped_candidate' if not invalid else 'segments_need_repair',
            'segment_count': len(rows), 'invalid_ordinals': invalid}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('video_id')
    parser.add_argument('--language', required=True)
    parser.add_argument('--retry', action='store_true', help='Explicitly permit a new attempt after an earlier one')
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]{11}', args.video_id) or not re.fullmatch(r'[a-z]{2}', args.language):
        parser.error('Expected an 11-character video ID and a two-letter language code')
    original = ROOT / f'data/transcripts/{args.video_id}.json'
    source = json.loads(original.read_text())
    if source.get('transcript'):
        parser.error('Original already contains segments; recovery would require a separate comparison scope')
    tracks = [t for t in source.get('captionTracks', []) if t.get('languageCode') == args.language]
    if not tracks:
        parser.error('Requested language is not listed in the saved response')
    attempts = ROOT / 'research/transcript-recovery-attempts'
    attempts.mkdir(parents=True, exist_ok=True)
    if not args.retry:
        previous = sorted(attempts.glob(f'{args.video_id}-{args.language}-*.json'))
        if previous:
            print(json.dumps({'state': 'existing_attempt_no_request_made', 'attempt': str(previous[-1].relative_to(ROOT))}))
            return
    attempt_id = f'{args.video_id}-{args.language}-{uuid.uuid4().hex[:12]}'
    record_path = attempts / f'{attempt_id}.json'
    record = {'schema_version': '1.0', 'attempt_id': attempt_id, 'video_id': args.video_id,
              'requested_language': args.language, 'requested_at': datetime.now(timezone.utc).isoformat(),
              'original_path': str(original.relative_to(ROOT)), 'original_sha256': digest(original),
              'script_sha256': digest(Path(__file__).resolve()),
              'selected_track_metadata': [{'language_code': t.get('languageCode'), 'kind': t.get('kind')} for t in tracks],
              'endpoint': ENDPOINT, 'cache_max_age': '1d', 'request_count': 0,
              'documentation': 'https://docs.scrapecreators.com/v1/youtube/video/transcript/',
              'state': 'prepared', 'promoted_to_corpus': False,
              'interpretation': 'Requested caption language is not independently verified spoken language. ASR/translation status and source accuracy require review. No automatic English translation or corpus replacement.'}
    # Persist intent before making the request; an interrupted attempt is not silently retried.
    record_path.write_text(json.dumps(record, indent=2) + '\n')
    query = urlencode({'url': f'https://www.youtube.com/watch?v={args.video_id}', 'language': args.language, 'cache_max_age': '1d'})
    request = Request(ENDPOINT + '?' + query, headers={'x-api-key': load_key(None), 'Accept': 'application/json'})
    try:
        record['request_count'] = 1
        record['state'] = 'request_started'
        record_path.write_text(json.dumps(record, indent=2) + '\n')
        with urlopen(request, timeout=45) as response:
            raw = response.read()
            record['http_status'] = response.status
        cache = ROOT / f'data/cache/transcript-recovery/{attempt_id}.json'
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_bytes(raw)
        record['raw_response_path'], record['raw_response_sha256'] = str(cache.relative_to(ROOT)), digest(cache)
        payload = json.loads(raw)
        record.update(inspect_segments(payload))
        if isinstance(payload, dict):
            record['provider_language'] = payload.get('language')
            record['provider_success'] = payload.get('success')
            record['provider_cached'] = payload.get('cached')
        if record['segment_count']:
            artifact = ROOT / f'data/transcript-recovery/{attempt_id}.json'
            artifact.parent.mkdir(parents=True, exist_ok=True)
            clean = {'schema_version': '1.0', 'video_id': args.video_id, 'requested_language': args.language,
                     'provider_language': payload.get('language'), 'attempt_id': attempt_id,
                     'raw_response_sha256': record['raw_response_sha256'], 'transcript': payload['transcript'],
                     'quality_status': record['state'], 'review_status': 'not_contextually_reviewed',
                     'translation_status': 'not_independently_verified'}
            artifact.write_text(json.dumps(clean, ensure_ascii=False, indent=2) + '\n')
            record['candidate_path'], record['candidate_sha256'] = str(artifact.relative_to(ROOT)), digest(artifact)
    except HTTPError as exc:
        record.update(state='http_error', http_status=exc.code)
    except (URLError, TimeoutError, ValueError, OSError) as exc:
        record.update(state='request_or_decode_error', error_type=type(exc).__name__)
    finally:
        record['finished_at'] = datetime.now(timezone.utc).isoformat()
        record['original_preserved'] = digest(original) == record['original_sha256']
        record_path.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({k: record[k] for k in ['attempt_id', 'state', 'request_count', 'original_preserved', 'segment_count', 'candidate_path'] if k in record}))


if __name__ == '__main__':
    main()
