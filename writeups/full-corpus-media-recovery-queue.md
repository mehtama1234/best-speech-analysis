# Full-corpus media recovery queue

Status: **recovery routing; not media validation**.

This queue identifies fixed-corpus videos without local raw A/V and preserves prior download outcomes. It does not prove availability, identity, alignment, delivery meaning or effectiveness, and it does not authorize bypassing access, licensing or platform restrictions.

Queued missing/derived items: **321**.

| Priority | Media state | Existing video status | Items |
|---|---|---|---:|
| `feature_backed_next_candidate` | `derived_features_only` | `failed:1` | 6 |
| `fixed_corpus_transcript_only` | `transcript_only_no_local_media` | `failed:1` | 4 |
| `fixed_corpus_transcript_only` | `transcript_only_no_local_media` | `not_attempted` | 310 |
| `fixed_corpus_transcript_only` | `video_only` | `downloaded` | 1 |

## Operating rule

1. Review access, licensing and source restrictions before any retry.
2. Recover only what is permitted and record the result in `data/media-status.jsonl`.
3. Rebuild the full-corpus availability audit after recovery.
4. Treat every recovered file as unverified until speaker/event identity, transcript alignment and delivery review are completed.
5. Keep transcript-derived lessons usable when media cannot be recovered; never infer nonverbal or vocal findings from absence.
