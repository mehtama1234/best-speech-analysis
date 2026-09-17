# Caption timing quality audit

stored multimodal features, not full transcript corpus or listening review.

Videos: 36; segments: 5059; captions overlapping their predecessor: 3741; no audio windows: 0; excluded caption rates: 1.

## Excluded rates

Raw records are preserved; no timestamps are silently repaired.

- AwA0Jnfj3ao:00238: 3 words / 0.004000s = 750.0 words/s; caption_duration_below_provisional_0.25_second_floor.

## Method and limits

0.25-second minimum is a provisional quality guard, not a biological speech-rate rule. Rates above 8 are review flags, not automatic exclusions. Overlap is flagged, not repaired.

Caption display intervals are not exact spoken-word boundaries. An audio-window overlap only proves that a window intersects the caption interval, not that the words were spoken throughout it. Overlapping captions reuse acoustic windows; segment counts are not independent audio observations. Mean caption rates weight captions equally, not speech duration.

The shared screening helper is applied to current delivery summaries, baselines, individual cards and the disjoint comparison. Raw feature files remain unchanged. Screening an obvious artifact does not validate the remaining timing or pitch proxies.

[Machine-readable counts, per-video means, flags and source hashes](../research/timing-quality-audit.json).
