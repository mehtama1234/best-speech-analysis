# The Speaking Patterns Fieldbook: editorial handoff

## What this edition contains

This edition has seven chapters and 55 detailed pattern entries: 22 main themes, 18 smaller speaking moves and 15 more ideas to explore. Each entry has a short source summary, a separate made-up before-and-after example, practical guidance, adaptations, a check, a limit and a link to its source note. These 55 source summaries draw on 17 selected analyses; several entries examine different choices in the same source. The index links each main theme to one detailed entry. The other 33 entries remain separate because they can support more than one theme. The edition also has a complete sample presentation, source notes, an editable manuscript, a web page and a PDF.

The downloadable package now contains a companion book with 27 speaking approaches and 11 learning paths. It is built from a separate project covering ten YouTube channels; its first Charisma on Command set has 16 transcripts. The fieldbook includes an editorial map from each of the 27 approaches to related patterns among its 55, or says there is no direct match. This map is a guide for readers, not independent proof that two sources teach the same thing. The fieldbook's selected source notes do not represent a fresh review of all 395 transcript records.

- [Read the fieldbook](speaking-patterns-fieldbook.html)
- [Edit the manuscript](speaking-patterns-fieldbook.md)
- In the portable bundle, open `speaking-patterns-fieldbook.pdf` for the print edition. The companion HTML, CSS and PDF are in `writeups/companion/`. Keep that folder intact so its web page works.

## What the examples support

Source passages are paraphrases of local transcript analyses. Caption numbers identify text order, not playback time. They help a reader locate a passage in the cited analysis; they do not verify the event or establish the speaker's private intent. The chapter's explanation is an editorial interpretation, not a measured effect.

The 55 labels came from transcript searches and editorial grouping. The source examples in this book come from 17 selected transcript analyses; the larger project reviewed the full transcripts of 395 videos in a 480-video inventory. This edition is not an independent recheck of all 395. Search counts show how many videos returned a match, not how many examples reviewers confirmed. Labels may overlap: more than one can describe different steps in the same passage. Repeated labels do not show that a choice caused a result.

The practice presentation and failure cases are invented and marked. They help demonstrate the writing choices; they are not evidence from the source corpus. Named speakers and organizations are not presented as endorsers. The book does not include recordings, photographs, lyrics or full speech texts. These notes do not establish commercial rights clearance.

## What remains untested

No independent human review returns are included in this edition. A 162-item review packet is prepared, but preparation is not review. No learner study shows whether readers can use the ideas, and no audience study measures comprehension, trust or response. Do not describe the labels or chapter advice as independently verified, validated or proven to improve presentations.

The current files are an editorial draft, not a finished, validated curriculum or a commercially cleared publication. Further work requires independent review, recorded resolution of disagreements, then separate learner and listener studies with real participant records. Choosing a publisher, price or sales channel is also outside this handoff.

## Local checks

From the repository root, with the companion project in the neighboring `speaking-humor-and-communication-concepts-research` folder:

```sh
python3 scripts/build_professional_pattern_fieldbook.py
python3 -m unittest discover -s tests -p 'test_professional_pattern_fieldbook*.py'
python3 scripts/export_speaking_fieldbook.py
python3 scripts/check_professional_pattern_fieldbook_browser.py
python3 scripts/check_fieldbook_delivery.py
```

The export step copies the current companion HTML, CSS and PDF into this package. The checks cover the seven fieldbook chapters, 55 patterns, all 27 comparison entries, the companion's 27 chapters and 11 learning paths, local links, browser behavior, print content and offline package. A passing check does not show that the advice helps every speaker or audience. Review both books as a reader before sharing them.
