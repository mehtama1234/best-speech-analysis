# Language recovery works—but availability is not accuracy

Two explicit Hindi requests returned **502 timestamped caption records** from
videos whose original English-request responses had `transcript: null`.
Both original responses remain byte-for-byte unchanged. The new evidence is
stored separately and **neither candidate is promoted to the canonical corpus**.

The provider documents that a requested language unavailable for a video can
produce a null transcript. That supports testing listed languages; it does not
guarantee caption accuracy or explain every missing transcript.
[ScrapeCreators transcript API](https://docs.scrapecreators.com/v1/youtube/video/transcript/)

| Candidate | Listed track | Returned segments | Spot-check result |
| --- | --- | ---: | --- |
| `05RW7gx-gG4` | Hindi, ASR marker | 259 | Samples look largely like English expressions rendered phonetically in Devanagari, with uncertain or broken words. |
| `2rmRzAdLgWk` | Hindi, no ASR marker | 243 | Samples contain Hindi sentence structure but awkward wording; translation status and accuracy remain unverified. |

These are two purposive tests, not an estimate of recovery success across the
32 available-track cases. One HTTP request was made per case, without automatic
retries. Cached provider responses are kept in ignored local cache; sanitized
candidate transcripts and separate attempt records retain hashes and language
metadata without copying account balances or signed caption URLs into reports.

## Why automatic promotion would be a mistake

The first result has valid timestamp fields and nonempty text, yet those checks
do not establish a useful transcription. A translation pipeline treating its
phonetic Devanagari as ordinary Hindi could compound errors. Audio comparison
or independently reviewed original-language evidence is needed.

The second result is more sentence-like in Hindi, but absence of an ASR marker
does not prove human authorship or faithful translation. Opening and closing
samples also repeat closely related wording. This could be an edited teaser,
reused footage or genuine repetition; the collection-style title and text alone
do not settle it. Do not count it as a rhetorical return without inspecting
the source boundaries.

The assistant inspected ordinals 0–17, 120–127 and 249–258 of the first candidate,
and 0–17, 116–123 and 233–242 of the second: **36 records per candidate**.
It did not read all 502 records or listen to either source. Exact inspected
ordinals, source hashes, reasons and dispositions are in the
[quality spot-check ledger](../research/recovery-quality-reviews.json).

## Reproducible recovery without overwriting evidence

```bash
python3 scripts/recover_transcript_language.py 05RW7gx-gG4 --language hi
python3 scripts/recover_transcript_language.py 2rmRzAdLgWk --language hi
```

These commands now find their existing attempt records and make no new request.
`--retry` explicitly permits a new attempt, with a separate ID. A prepared or
interrupted attempt is not silently retried. Credentials are loaded through the
existing helper, never printed or saved in the attempt record. Each HTTP call
has a 45-second timeout. Timestamp validation checks shape and boundaries, not
speech quality, translation, word alignment or complete source coverage.

The original registry remains at 395 nonempty transcripts; recovery candidates
are a separate pool until language, quality and lineage requirements are met.
Next: compare candidate excerpts with source audio and translation evidence,
then define language-aware registry integration and review gates before scale-up.
