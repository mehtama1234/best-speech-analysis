# Presentation pattern atlas

Status: **corpus_mined_candidate_system_indexed_for_practice**.

This atlas indexes transcript-derived candidate patterns and local practice surfaces. It does not establish speaker intent, universal effectiveness, learner improvement, listener outcomes, causality, or independent human validation.

## Corpus coverage

- **480** unique inventory videos; **395** have non-empty canonical transcripts
- **395** full-context reviews
- **102816** inspected captions
- **50380** episode records
- **33330** relation records

## Discovery layers

- **22** broad themes + **18** relation architectures + **15** unmatched clusters
- **33** source-linked expanded cards
- **136** recurring compound pairings; top **24** surfaced for rehearsal
- **160** recurring three-move triads; top **24** retained as practice candidates
- **6** presentation sequences
- **2** local-LLM-prioritized cards

## Start a presentation

1. Choose a sequence in the [sequence library](presentation-sequence-library.md): explain, propose, report, lead, answer, or tell a story.
2. Use the [presentation builder](presentation-builder.html) to enter a topic, audience and outcome, then combine one architecture with up to three pattern moves.
3. Use the [expanded pattern browser](expanded-pattern-candidate-cards.html) to select moves and draft each sentence-level step.
4. Use the [compound bundle browser](compound-pattern-bundles.html) when two recurring moves need to be rehearsed together.
5. Record the listener restatement, uncertainty, non-fit and next revision before exporting the local practice record.

For the complete human-readable catalog of themes, subthemes, source-linked examples and presentation uses, read the [amazing presentation patterns guide](amazing-presentation-patterns.md).

## Sequence IDs

- `explain_an_unfamiliar_idea`
- `make_a_proposal`
- `report_an_incident`
- `lead_a_room`
- `answer_a_hard_question`
- `tell_a_story_with_a_point`

## Runtime evidence

- `expanded_pattern_browser` — `writeups/expanded-pattern-candidate-cards.html` — **expanded_pattern_browser_smoke_passed**
- `compound_pattern_browser` — `writeups/compound-pattern-bundles.html` — **compound_pattern_browser_smoke_passed**
- `compound_triad_browser` — `writeups/compound-pattern-triads.html` — **compound_triad_browser_smoke_passed**
- `sequence_library` — `writeups/presentation-sequence-library.md` — **source_linked_library_generated**
- `cli_speech_worksheet` — `scripts/build_speech_draft.py` — **sequence_stems_and_boundaries_tested**
- `local_llm_draft_judge` — `writeups/local-llm-draft-judge.md` — **local_model_draft_screen_recorded_not_effectiveness_evidence**

The local LLM screen is a prioritization aid. It does not promote a pattern or replace independent review.
