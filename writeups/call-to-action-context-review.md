# Calls to action: what is requested, and whose request is it?

17 September 2026. Ten remaining candidates received assistant transcript-only
contextual review. All eleven selected call-to-action candidates now have
explicit decisions, including the earlier rejected advice embedded in a story.
The review does not establish audience compliance or improved persuasion.

## Evidence and distinctions

| Target with saved caption timestamp | Contextual decision |
| --- | --- |
| [-6qN3bm2RYo:00276](https://www.youtube.com/watch?v=-6qN3bm2RYo&t=792) | Supported: collective institutional proposal following an invitation to member states |
| [-6qN3bm2RYo:00343](https://www.youtube.com/watch?v=-6qN3bm2RYo&t=988) | Supported: broad closing aspiration, completed in following captions |
| [-HA8kSdsf_M:00079](https://www.youtube.com/watch?v=-HA8kSdsf_M&t=217) | Supported: repeated collective appeals; no literal combat or effectiveness inference |
| [2fWJh-_UG5s:00401](https://www.youtube.com/watch?v=2fWJh-_UG5s&t=954) | Supported: policy-necessity sequence, with unclear target wording preserved |
| [aXmM0VZv810:00179](https://www.youtube.com/watch?v=aXmM0VZv810&t=446) | Rejected: a moderator invites named interlocutors to answer |
| [AwA0Jnfj3ao:00002](https://www.youtube.com/watch?v=AwA0Jnfj3ao&t=17) | Rejected: interviewer story prompt |
| [jxY2-YgAgm0:00125](https://www.youtube.com/watch?v=jxY2-YgAgm0&t=370) | Supported as an upload-level action appeal, but part of a promotional outro |
| [pmAL79dnvu0:00116](https://www.youtube.com/watch?v=pmAL79dnvu0&t=393) | Supported: civic-participation appeal spanning captions |
| [qOwYULOPuPs:00348](https://www.youtube.com/watch?v=qOwYULOPuPs&t=902) | Supported: broad closing encouragement to continue |
| [aXmM0VZv810:00003](https://www.youtube.com/watch?v=aXmM0VZv810&t=7) | Rejected: procedural event management |

Links are navigation aids using provider caption starts rounded down, not
validated spoken-word onsets. Exact context IDs and hashes are stored in the
[contextual ledger](../research/contextual-label-reviews.json). Windows cover
four captions either side except review-011 (75–90, to finish the appeal) and
review-049 (108–126, to inspect the transition into promotion).

## Important attribution correction

The English-practice invitation follows the featured speech's closing thanks.
The expanded context then promotes a learning community, transcripts, courses
and classes. Its language supports a call to action, but not attribution of
that action to the featured speaker. The review records
`promotional_outro_text_not_featured_speaker_verified` explicitly.

This is a corpus-design issue: an upload can contain multiple speakers,
introductions, excerpts and channel promotions. Video-level identity is not
enough for speaker-level pattern claims. Future segmentation must mark these
boundaries and isolate promotional material before estimating recurrence
across featured speakers. The present decision does not silently delete the
outro or pretend the corpus-wide segmentation is complete.

The generated individual reader cards now display current contextual reasons
and attribution alongside clearly labelled historical observations. Previously
those current decisions were present in JSON and the aggregate delivery report,
but not explained in the individual-card Markdown.

## Action appeal versus conversational procedure

Imperative grammar alone is insufficient. Inviting a guest to answer and
moving an event forward are procedural requests, while a collective proposal
asks for substantive action. Broad aspirations and encouragement remain
supported under the broad label, but are not detailed instructions. The rubric
now makes this scope explicit and retains the earlier rejection of reported
advice to a story character.

One policy caption contains unclear wording about schools. The repeated
necessity construction and surrounding proposals support the discourse label;
they do not authorize silently reconstructing the exact policy. Similarly,
the civic appeal's verb falls in the next caption. Reading across that clause
boundary is necessary, whereas transferring a label from an unrelated nearby
sentence would be unjustified.

## Practice implication and checkpoint

A useful proposed exercise is to mark an appeal's addressee, requested action,
specificity and location in the speech. Then distinguish it from turn-taking
and promotional material. This exercise is not an experimentally supported
claim that more forceful appeals improve audience outcomes.

Support remains 7/11 for this selected queue, including the promotional outro.
No call-to-action practice card is promoted. Contextual review now covers
77/87 rows; ten remain (seven pauses and three unclassified). Sixty rows have
at least one supported label, and five provisional cards remain admitted.
No raw media, transcripts or original annotations were changed. The full
playlist-scale research and multimodal validation remain unfinished.

Verification: six builders succeeded and 27 tests passed in 15.085 seconds.
Whitespace checks passed; original annotations, transcripts and raw feature
files have no diff. These checks establish artifact consistency, not independent
semantic validation. The new regression checks ensure the outro attribution
reaches individual reader cards and procedural requests remain distinguished.
