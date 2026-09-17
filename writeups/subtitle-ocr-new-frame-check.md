# New frames expose false text, not just spelling errors

The frozen OCR method matched **four of five visible subtitles**, misread one,
and produced **false text on all three frames without subtitles in its region**.
It should not become an unattended transcript builder on this evidence.

Eight timestamps were fixed before recognition or viewing: 0, 20, 160, 300,
440, 580, 720 and 843 seconds. Six span the interior at 140-second spacing;
the other two probe opening/ending material. Settings, pilot script, runtime
and source hashes were checked before processing. No failed frame was removed
and no OCR setting was changed after these results.

| Requested time | Subtitle inside fixed region? | Observed outcome |
| ---: | --- | --- |
| 0 s | No | Background/clothing produces false tokens. |
| 20 s | Yes | Exact text match, but the surrounding label marks a preview. |
| 160 s | Yes | Exact visible-subtitle match. |
| 300 s | Yes | First line matches; second line is corrupted. Scene shows an attendee. |
| 440 s | No | Scene texture produces false tokens; speaker label is outside the region. |
| 580 s | Yes | Exact visible-subtitle match. |
| 720 s | Yes | Exact match across two visible lines. |
| 843 s | No | End-card graphics produce false tokens. Promotional text exists elsewhere in the frame. |

The [machine report](../research/subtitle-ocr-new-frames.json) retains all outputs,
word boxes, engine scores, exact decoded timestamps and PNG hashes. The separate
[assistant review](../research/subtitle-ocr-new-frame-review.json) records direct
inspection of all eight frames. This is a new-frame check on the **same upload**,
not a random sample, independent reviewer assessment or corpus-wide accuracy
estimate. Images were inspected after the OCR results were seen.

## Three separate decisions

1. **Is there subtitle text?** A recognizer can invent word-like output from
   clothing or background lines. Nonempty OCR output does not answer this.
2. **Was the visible text recognized correctly?** A frame can contain subtitles
   while one of its lines is corrupted. Correct neighboring words do not repair it.
3. **Whose material is it?** A preview subtitle can be read perfectly and still
   not belong to the featured speech. A speaker label can persist over an
   attendee shot, so visible faces must not inherit the caption's attribution.

These decisions precede treating text as language evidence. Frame timestamps
still do not establish subtitle intervals, spoken-word boundaries or a pause.
No psychological state is inferred from the attendee image; no audio was heard.

## Why not immediately add a confidence cutoff?

On these eight frames, the false detections and corrupted line have lower OCR
scores than the correctly read material. That is a useful development lead,
not a validated threshold. Choosing a cutoff after seeing these labels and
then reporting accuracy on the same frames would overstate the evidence.

Freeze any proposed gate first, then evaluate new timestamps and other layouts,
including previews, promotional cards and subtitle-free intervals. Preserve
the present failures as development cases. Until those checks pass, maintain
reviewed editorial-text observations separately from the canonical transcript
corpus. Both language-recovery candidates remain unpromoted.
