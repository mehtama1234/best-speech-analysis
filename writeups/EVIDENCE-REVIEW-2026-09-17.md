# Resumption evidence review — 17 September 2026

This is a code/provenance audit by the assistant, not a new human annotation,
audio listening session, visual review or effectiveness study.

## Corrected evidence loss

The delivery-report builder obtained transcript text and timestamps from the
smaller media-feature sample rather than the full segment registry. Eleven of
62 supported annotation examples consequently appeared without transcript text
or timestamped links, even though their source segments were present.

The builder now obtains text, start/end time and source-transcript path from
the segment registry independently of audio feature availability. All 62
examples now resolve to text and timestamps; the 11 without aligned features
retain null measurements and an explicit status. No measurements were invented.
The delivery and provisional-practice JSON/Markdown reports were regenerated.

Regression tests cover absent media, conflicting cached feature text/time,
zero timestamps, missing registry segments and published example provenance.

## Interpretation gaps exposed, not resolved

- Practice-card eligibility counts reviewed transcript-label support, not
  successful delivery or audience outcomes. The six-card count is unchanged.
- Audio summaries use smaller, metric-specific samples. Cards now disclose
  those counts and baseline example/video denominators.
- The existing baseline includes all usable segments, including the target
  examples. It is not a disjoint control or a matched speech-function control.
  Its arithmetic was not changed in this pass; its description is now explicit.
- Videos and uploaders are not verified distinct speakers. Cross-speaker
  recurrence remains unestablished.
- Legacy annotations have a single support boolean for potentially multiple
  candidate labels. Support for one label must not automatically validate all
  labels. Contextual per-label re-review is needed before stronger findings.
- Legacy records say “reviewed” but lack reviewer identity, review modality and
  review date. This audit cannot establish that a human, rather than an assistant,
  produced those judgments. Preserve the records without upgrading their provenance.
- Sparse visual samples cannot establish timed gesture or facial-expression
  semantics. No new video/voice claims have been made.

## Next research work

Introduce an explicit per-label contextual review record with reviewer type,
modality, source versions, context bounds and independent judgments. Re-review
multi-label records first, then balance further sampling across known formats
and verified speaker metadata. Preserve historical judgments and report changed
eligibility rather than targeting a desired card count. After language evidence
is sound, use localized audio/video review and disjoint matched controls to test
delivery hypotheses. The full saved research goal remains unfinished.
