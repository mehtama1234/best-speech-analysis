# Reviewed speech-pattern cards

These cards are reviewed examples, not universal findings. The text function was reviewed from the transcript; delivery fields are directly measured audio summaries when pilot media exists.

## review-001: `personal_story_setup`

Evidence: `-54zUwySKCg:00035`  
Candidate labels: story_or_personal_experience  
Supported by review: **True**  
Confidence: **high**

Direct observation: First-person past-tense account with a named place and age.

Interpretation: The speaker is beginning a personal anecdote.

Limitation: One caption is not enough to establish the full story boundary.

Delivery measurements: RMS None; speech-activity proxy None; zero-crossing rate None; spectral centroid None Hz; overlapping audio windows None.

## review-002: `personal_story_transition`

Evidence: `-54zUwySKCg:00059`  
Candidate labels: contrast_or_disagreement, story_or_personal_experience  
Supported by review: **True**  
Confidence: **high**

Direct observation: First-person past-tense account includes a contrastive 'but'.

Interpretation: The speaker is narrating a decision or turning point.

Limitation: The contrast marker does not by itself indicate disagreement.

Delivery measurements: RMS None; speech-activity proxy None; zero-crossing rate None; spectral centroid None Hz; overlapping audio windows None.

## review-003: `rhetorical_question`

Evidence: `-54zUwySKCg:00122`  
Candidate labels: question, uncertainty_or_qualification  
Supported by review: **True**  
Confidence: **high**

Direct observation: Caption ends with a question mark and asks what the speaker could do.

Interpretation: The question appears to transition from another person's example to the speaker's own reflection.

Limitation: The transcript does not establish audience response.

Delivery measurements: RMS None; speech-activity proxy None; zero-crossing rate None; spectral centroid None Hz; overlapping audio windows None.

## review-004: `emotional_opening`

Evidence: `-54zUwySKCg:00015`  
Candidate labels: question  
Supported by review: **False**  
Confidence: **high**

Direct observation: The caption contains the word 'consider' but is not a question.

Interpretation: The question keyword heuristic is a false positive here.

Limitation: Caption punctuation and segmentation may be incomplete.

Delivery measurements: RMS None; speech-activity proxy None; zero-crossing rate None; spectral centroid None Hz; overlapping audio windows None.

## review-005: `conclusion_or_charge`

Evidence: `-54zUwySKCg:00196`  
Candidate labels: conclusion_or_summary  
Supported by review: **True**  
Confidence: **high**

Direct observation: The phrase 'The point is' explicitly marks a central takeaway.

Interpretation: The speaker is foregrounding a conclusion or charge to the audience.

Limitation: The surrounding paragraph is needed to distinguish summary from a new claim.

Delivery measurements: RMS None; speech-activity proxy None; zero-crossing rate None; spectral centroid None Hz; overlapping audio windows None.

## review-006: `definition_or_reformulation`

Evidence: `-6qN3bm2RYo:00068`  
Candidate labels: definition  
Supported by review: **True**  
Confidence: **medium**

Direct observation: The phrase contains 'this means'.

Interpretation: The speaker is likely reformulating or defining the preceding idea.

Limitation: The caption is fragmented; preceding context is required.

Delivery measurements: RMS None; speech-activity proxy None; zero-crossing rate None; spectral centroid None Hz; overlapping audio windows None.

## review-007: `example_introduction`

Evidence: `-6qN3bm2RYo:00079`  
Candidate labels: example  
Supported by review: **True**  
Confidence: **high**

Direct observation: The phrase 'such as' introduces a class of concrete cases.

Interpretation: The speaker is moving from a general issue to examples.

Limitation: This is an example marker, not evidence that the example improved comprehension.

Delivery measurements: RMS None; speech-activity proxy None; zero-crossing rate None; spectral centroid None Hz; overlapping audio windows None.

## review-008: `institutional_call_to_action`

Evidence: `-6qN3bm2RYo:00276`  
Candidate labels: call_to_action  
Supported by review: **True**  
Confidence: **high**

Direct observation: The speaker says 'we need to create' followed by a proposed action.

Interpretation: The speaker is presenting a collective action or policy recommendation.

Limitation: The transcript does not reveal whether the audience accepted it.

Delivery measurements: RMS None; speech-activity proxy None; zero-crossing rate None; spectral centroid None Hz; overlapping audio windows None.

## review-009: `collective_appeal`

Evidence: `-6qN3bm2RYo:00343`  
Candidate labels: call_to_action  
Supported by review: **True**  
Confidence: **high**

Direct observation: The phrase 'let us strive' directly addresses collective action.

Interpretation: The speaker is closing or intensifying an appeal.

Limitation: The caption is a fragment and should be reviewed with adjacent captions.

Delivery measurements: RMS None; speech-activity proxy None; zero-crossing rate None; spectral centroid None Hz; overlapping audio windows None.

## review-010: `summary_transition`

Evidence: `-URn1fARvts:00119`  
Candidate labels: conclusion_or_summary  
Supported by review: **True**  
Confidence: **high**

Direct observation: The phrase 'In short' explicitly announces compression or summary.

Interpretation: The speaker is summarizing a preceding idea.

Limitation: The summary's effectiveness cannot be inferred from the phrase alone.

Delivery measurements: RMS None; speech-activity proxy None; zero-crossing rate None; spectral centroid None Hz; overlapping audio windows None.

## review-011: `urgent_collective_call`

Evidence: `-HA8kSdsf_M:00079`  
Candidate labels: call_to_action  
Supported by review: **True**  
Confidence: **high**

Direct observation: The phrase 'let us fight' is an explicit collective imperative.

Interpretation: The speaker is escalating toward a call to action.

Limitation: The historical and rhetorical context matters; this is not a general best practice.

Delivery measurements: RMS None; speech-activity proxy None; zero-crossing rate None; spectral centroid None Hz; overlapping audio windows None.

## review-012: `qualification_or_contrast`

Evidence: `-54zUwySKCg:00028`  
Candidate labels: contrast_or_disagreement  
Supported by review: **True**  
Confidence: **high**

Direct observation: The phrase 'But then I realized' marks a change in reasoning, not necessarily interpersonal disagreement.

Interpretation: The speaker is introducing a personal reconsideration.

Limitation: Contrast markers should not automatically be treated as disagreement.

Delivery measurements: RMS None; speech-activity proxy None; zero-crossing rate None; spectral centroid None Hz; overlapping audio windows None.

## review-013: `story_recall`

Evidence: `S43F1BZfQKY:00002`  
Candidate labels: story_or_personal_experience  
Supported by review: **True**  
Confidence: **high**

Direct observation: The speaker explicitly says 'I remember that day'.

Interpretation: The speaker is opening a personal story.

Limitation: A story label does not imply emotional state.

Delivery measurements: RMS -24.076; speech-activity proxy 1.0; zero-crossing rate 0.11111; spectral centroid 466.09 Hz; overlapping audio windows 3.

## review-014: `story_event_with_embedded_advice`

Evidence: `S43F1BZfQKY:00011`  
Candidate labels: call_to_action, story_or_personal_experience  
Supported by review: **False**  
Confidence: **high**

Direct observation: 'Maybe you should' occurs inside a narrated event and is advice quoted from another person, not the speaker's call to the audience.

Interpretation: The story marker is supported; the call-to-action heuristic is a false positive.

Limitation: Speaker attribution within quoted dialogue requires broader context.

Delivery measurements: RMS -39.485; speech-activity proxy 0.444; zero-crossing rate 0.0955; spectral centroid 434.722 Hz; overlapping audio windows 18.

## review-015: `story_action`

Evidence: `S43F1BZfQKY:00036`  
Candidate labels: story_or_personal_experience  
Supported by review: **True**  
Confidence: **high**

Direct observation: The speaker narrates a first-person past action: 'I went for it'.

Interpretation: The speaker is advancing a personal narrative.

Limitation: Caption-level boundaries may split one narrative unit.

Delivery measurements: RMS -20.403; speech-activity proxy 1.0; zero-crossing rate 0.16655; spectral centroid 1136.106 Hz; overlapping audio windows 20.

## review-016: `causal_transition`

Evidence: `3AIoHLr8nTI:00003`  
Candidate labels: conclusion_or_summary  
Supported by review: **False**  
Confidence: **high**

Direct observation: 'Therefore' links a preceding idea to a consequence but does not by itself summarize or conclude the speech.

Interpretation: The conclusion keyword heuristic is a false positive for this transition.

Limitation: The surrounding speech may establish a larger conclusion.

Delivery measurements: RMS -19.439; speech-activity proxy 1.0; zero-crossing rate 0.11621; spectral centroid 673.143 Hz; overlapping audio windows 10.

## review-017: `conclusion_marker`

Evidence: `aXmM0VZv810:00483`  
Candidate labels: conclusion_or_summary  
Supported by review: **True**  
Confidence: **medium**

Direct observation: The phrase 'what matters' explicitly foregrounds a criterion or takeaway.

Interpretation: The speaker is emphasizing a concluding or prioritizing point.

Limitation: The segment is short and should be read with neighboring captions.

Delivery measurements: RMS -15.764; speech-activity proxy 1.0; zero-crossing rate 0.17077; spectral centroid 638.521 Hz; overlapping audio windows 6.

## review-018: `example_marker`

Evidence: `aXmM0VZv810:00274`  
Candidate labels: example  
Supported by review: **True**  
Confidence: **high**

Direct observation: The phrase 'for example' introduces a concrete case.

Interpretation: The speaker is moving from an abstract claim to an example.

Limitation: This does not establish whether the example was effective.

Delivery measurements: RMS -15.101; speech-activity proxy 1.0; zero-crossing rate 0.12568; spectral centroid 491.947 Hz; overlapping audio windows 7.

## review-019: `audience_question_or_rhetorical_question`

Evidence: `m92yvNscIAo:00004`  
Candidate labels: question  
Supported by review: **True**  
Confidence: **medium**

Direct observation: The segment asks 'how many different ways'.

Interpretation: The speaker is posing a question to orient the audience.

Limitation: It is unclear whether the audience was expected to answer aloud.

Delivery measurements: RMS -43.174; speech-activity proxy 0.6; zero-crossing rate 0.16535; spectral centroid 791.795 Hz; overlapping audio windows 5.

## review-020: `narrative_detail`

Evidence: `S43F1BZfQKY:00021`  
Candidate labels: question  
Supported by review: **False**  
Confidence: **high**

Direct observation: The segment contains no interrogative structure; the question heuristic fired on an ordinary word match.

Interpretation: This is another question-detector false positive.

Limitation: Transcript punctuation may be imperfect.

Delivery measurements: RMS -13.346; speech-activity proxy 1.0; zero-crossing rate 0.10697; spectral centroid 466.106 Hz; overlapping audio windows 5.
