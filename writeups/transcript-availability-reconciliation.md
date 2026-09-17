# Successful requests are not necessarily usable transcripts

The saved corpus has **395 videos with nonempty transcript lists out of 480**.
The earlier headline “474 successes, 395 nonempty and 82 empty” mixed request-log
and cache counts. A revised [coverage audit](../data/metadata/transcript-coverage.json)
now exposes their intersection, video-level states and input hashes.

| Latest corpus-log state | Cache evidence | Videos |
| --- | --- | ---: |
| Success | Nonempty transcript list | 392 |
| Success | `transcript: null` | 79 |
| Success | `notFound: true`, no transcript field | 3 |
| No corpus-log record | Nonempty cached pilot transcript | 3 |
| Failed | No cached response | 3 |
| **Total** | | **480** |

Thus 474 logged successes comprise 392 usable-list responses plus 82 responses
without segments. The three separately cached pilot videos bring nonempty
coverage to 395 and total cached responses to 477. There are no actual empty
transcript lists and no malformed payloads under the audit's shape checks.
The three cached `notFound` IDs are `tWhHf7IeFmo`, `y0oWA2yVB3s` and
`oMZZGzPg254`; these are different from the three HTTP-failure IDs.

The current corpus status file records a latest result for 477 videos. It is
not a complete request/retry ledger, so do not label 477 as the total number of
API calls. Cached pilots `5i0u4jFmE78`, `fBnAMUkNM2k` and `qOwYULOPuPs` must not
be described as unrequested simply because this particular status file lacks
their records. Original responses and logs remain unchanged.

## A concrete recovery lead

Of the 82 cached responses without segments, **32 list caption tracks**. None
of their listed track language codes is English: observed codes are Arabic,
Hindi, Indonesian, Portuguese, Punjabi, Spanish and Vietnamese; nine listed
Hindi tracks are marked automatic speech recognition. These are metadata about
available tracks, **not verified identification of the spoken language**.
All 82 lack alternate `transcript_only_text` content.

The corpus downloader requests English by default and skips any video with an
existing cache file. Together, these facts identify a recovery path to test:
inspect language availability and try supported track acquisition explicitly,
preserving original-language evidence and marking any later translation.
They do not yet prove that the language request caused every null response or
that the listed track URLs are currently usable. No tracks were fetched in
this audit; language support and source accuracy remain unverified.

Before recovery, preserve the current response, record the selected language
and retrieval attempt separately, and compare the new result with the old
state. A null response should not be an eternal “already complete” cache hit.
The remaining 47 null responses without listed tracks, three cached notFound
responses and three failed requests require separate availability checks.

## Meaning and compatibility of the counts

`successful_transcript_count` remains the count of latest logged `success`
states for compatibility, not a semantic availability measure.
`empty_transcript_count` now strictly means an empty list; the old report
collapsed null and missing-field responses into that label. Use
`cached_without_segments_count` for that historical 82-file category.
The audit's schema version is now 0.2. A nonempty list still does not prove
correct words, reliable timestamps, complete source coverage or deep review.

Rebuild with `python3 scripts/audit_transcript_coverage.py`. This is a read-only
inspection of source files followed by a derived-report write; it makes no API
calls and changes no source transcripts, features or annotations.
