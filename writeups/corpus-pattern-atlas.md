# Corpus pattern atlas

This is a transcript retrieval and coverage artifact, not a set of validated universal rules.

- Eligible videos: **394**
- Eligible caption segments: **102351**
- Videos with prior contextual/manual annotations: **25**
- Exact evidence IDs in prior reviewed cards: **86**
- Boundary: transcript-only; phrase hits and candidate labels require manual review.
- Counts below are retrieval denominators (caption-segment and video hits), not validated speech-function or effectiveness findings.
- The train/holdout counts use a stable video-level split; they are not a statistical performance evaluation.
- The recurrence-review queue is stratified by phrase family and event split; queued items still require contextual, audiovisual and independent review.

## Phrase-form families

- `contrast_or_disagreement` — **380** videos / **5515** caption segments; event holdout **66** videos / **933** segments; `\bbut\b` (4938), `\bhowever\b` (69), `\binstead\b` (118), `\brather than\b` (58), `\bon the other hand\b` (7), `\bused to\b` (210), `\bnow I\b` (151)
- `example` — **76** videos / **129** caption segments; event holdout **12** videos / **17** segments; `\bfor example\b` (67), `\bfor instance\b` (18), `\bsuch as\b` (36), `\bone example\b` (8)
- `story_or_personal_experience` — **311** videos / **2514** caption segments; event holdout **52** videos / **343** segments; `\bwhen I\b` (747), `\bI remember\b` (125), `\byears ago\b` (175), `\bone day\b` (107), `\bI was\b` (1527), `\bmy first\b` (94), `\bgrowing up\b` (40)
- `uncertainty_or_qualification` — **279** videos / **1882** caption segments; event holdout **47** videos / **301** segments; `\bmaybe\b` (364), `\bperhaps\b` (90), `\bI think\b` (1405), `\bI'm not sure\b` (16), `\bit depends\b` (12), `\bto some extent\b` (2), `\bnot necessarily\b` (5)
- `conclusion_or_summary` — **105** videos / **193** caption segments; event holdout **16** videos / **38** segments; `\bthe point is\b` (13), `\bwhat matters\b` (13), `\bin conclusion\b` (3), `\bultimately\b` (47), `\bin short\b` (9), `\bso the\b` (105), `\bthe lesson\b` (5)
- `question` — **358** videos / **4951** caption segments; event holdout **61** videos / **801** segments; `\bwhy\b` (858), `\bhow\b` (1812), `\bwhat if\b` (29), `\bcan we\b` (63), `\?` (2655)
- `definition` — **74** videos / **95** caption segments; event holdout **13** videos / **14** segments; `\bin other words\b` (18), `\bmeans that\b` (23), `\bdefined as\b` (1), `\bis when\b` (32), `\bwhat I mean\b` (14), `\bthe definition\b` (7)
- `call_to_action` — **371** videos / **3542** caption segments; event holdout **65** videos / **584** segments; `\bwe need to\b` (145), `\byou can\b` (678), `\blet's\b` (393), `\bdo not\b` (156), `\bdon't\b` (2153), `\bjoin us\b` (29), `\btake action\b` (9)

## Candidate speech-function inventory

These labels are transcript retrieval aids, not validated semantic annotations.

- `call_to_action` — **247** videos / **827** segments; reviewed segments: **11**
- `conclusion_or_summary` — **33** videos / **39** segments; reviewed segments: **5**
- `contrast_or_disagreement` — **276** videos / **851** segments; reviewed segments: **8**
- `definition` — **162** videos / **372** segments; reviewed segments: **9**
- `example` — **144** videos / **260** segments; reviewed segments: **10**
- `question` — **383** videos / **6181** segments; reviewed segments: **10**
- `story_or_personal_experience` — **265** videos / **1063** segments; reviewed segments: **13**
- `uncertainty_or_qualification` — **339** videos / **3343** segments; reviewed segments: **10**
- `unclassified` — **394** videos / **89980** segments; reviewed segments: **14**

The candidate-function review queue contains **187** stratified intervals for non-`unclassified` labels (up to 12 train and 12 holdout videos per label).

## How to use this atlas

Use the JSON to select cross-speaker, cross-event samples for manual review. Preserve the exact evidence ID and timestamp, inspect surrounding context, then add audiovisual evidence, counterexamples, and practice only after the candidate survives review.

A phrase hit is not proof that the speaker performed the associated function; the same words can serve different jobs.

The generated recurrence-review queue contains **192** balanced candidate intervals (up to 12 train and 12 holdout videos per phrase family).
