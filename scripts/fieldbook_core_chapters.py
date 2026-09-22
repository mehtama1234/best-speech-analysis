"""Job-first chapters for the public Speaking Patterns Fieldbook.

The 55 named patterns remain a research index. These chapters teach a smaller
set of reader problems using selected, paraphrased source cases.
"""

JOB_CHAPTERS = [
    {
        "id": "route",
        "title": "Help the audience know where they are going",
        "question": "What does the audience need to understand first, and what will you cover next?",
        "principle": (
            "Tell listeners what the talk is about, why it matters and what you "
            "will cover. Then cover what you promised. If the plan changes, say "
            "so. End by answering the opening question or stating what remains "
            "unknown."
        ),
        "method": [
            "Write the audience’s main question in one sentence.",
            "Name the result, decision or explanation the talk can actually provide.",
            "Preview only the sections you have time to deliver; signal a change of direction when it happens.",
            "Close by answering the opening question or naming what remains unresolved.",
        ],
        "example_keys": ["orientation_and_roadmap"],
        "boundary": (
            "The McRaven transcript supports a comparison between the announced "
            "ten lessons, the ten story units and the closing recap. It does not "
            "show that listeners remembered them or that ten is the right number. "
            "Several stories describe dangerous training; they are not practical "
            "instructions for ordinary situations."
        ),
        "failure_case": (
            "Invented failure: a speaker promises four decisions, discusses only "
            "two, then ends with a new request. Listeners cannot use the opening "
            "to follow a talk that breaks its own map. Fix the outline before "
            "adding more signposts."
        ),
        "exercise": (
            "Write a 30-second opening for your next talk. Underline the subject, "
            "the reason this audience should care, and the route. Mark where each "
            "promised part appears in your outline. Remove any promise with no "
            "place in the talk."
        ),
        "check": (
            "After hearing the opening, could someone say what the talk is about, "
            "why it matters, and what comes next? At the end, did the talk answer "
            "the question it raised?"
        ),
        "pattern_ids": [
            "orientation_and_roadmap", "purpose_attention_example",
            "audience_shift", "register_shift",
        ],
    },
    {
        "id": "explain",
        "title": "Make an unfamiliar idea easier to picture",
        "question": "What does the audience need to picture, compare or understand?",
        "principle": (
            "Explain the idea without making it seem simpler or more certain than "
            "it is. Define the term, give a specific example and say how it helps. "
            "If you use a comparison, state what is similar and where the "
            "comparison stops."
        ),
        "method": [
            "Name the idea in ordinary words.",
            "Give one example the audience can inspect.",
            "Say which part of the example illustrates the idea.",
            "State what the example cannot establish; add a second example if one case could mislead.",
        ],
        "example_keys": ["analogy_metaphor_and_callback"],
        "boundary": (
            "This account comes from one address and was not independently "
            "checked. It cannot tell us what the child or other listeners thought, "
            "or whether the image would help another speaker explain a difficult "
            "subject."
        ),
        "failure_case": (
            "Invented failure: comparing a complicated health system to a single "
            "machine and then treating every part of the comparison as fact. The "
            "image may be memorable while quietly adding claims the evidence "
            "does not support. State the one useful similarity and where it ends."
        ),
        "exercise": (
            "Explain one unfamiliar term to a person outside your field. Use a "
            "real example, then write: ‘This example shows ____. It does not show ____. ’ "
            "Replace the example if a listener could mistake it for proof of a broader claim."
        ),
        "check": (
            "Can a listener explain the idea without repeating your analogy as "
            "if it were literal? Can they say what the example leaves unanswered?"
        ),
        "pattern_ids": [
            "definition_and_explanation", "analogy_metaphor_and_callback",
            "scale_shift", "cause_and_mechanism", "familiarity_to_scope",
            "unity_across_scale", "analogy_transfer",
        ],
    },
    {
        "id": "change",
        "title": "Use a story to show what changed",
        "question": "What did someone expect, what happened, and what does that change mean now?",
        "principle": (
            "Use a story when it helps explain a choice, result or change in "
            "belief. Say what the person expected, what happened and what they "
            "learned. Keep the lesson within what this one account can show: it "
            "cannot tell us how often the same thing happens or what everyone "
            "should do."
        ),
        "method": [
            "Set the scene and the original expectation.",
            "Show the choice or event that interrupted it.",
            "Explain what changed—and what stayed true.",
            "Limit the lesson to this case unless other evidence supports a broader claim.",
        ],
        "example_keys": ["story_memory_and_scene", "contrast_and_reversal"],
        "boundary": (
            "Bezos’s commencement account describes a childhood calculation, "
            "an unexpected reaction from his grandmother, and a later distinction "
            "between cleverness and kindness. The story changes the standard by "
            "which the child judges his action. Mindy Kaling’s Dartmouth account "
            "adds a useful counter-reading: a checklist did not unfold on the "
            "expected timetable, but she also says plans can motivate. Neither "
            "account proves that risk-taking or planning has one right answer."
        ),
        "failure_case": (
            "Invented failure: presenting a changed plan as proof that planning "
            "is foolish. That leaves out what the original plan made possible, "
            "the support available, and the conditions that changed. Tell the "
            "change fairly before drawing a lesson from it."
        ),
        "exercise": (
            "Tell a short, non-private example using four lines: ‘I expected ____. "
            "Then ____. Now I think ____. This example does not prove ____. ’ "
            "If the story requires an unverified fact about another person, choose a different one."
        ),
        "check": (
            "Can a listener identify the expectation, the change and the lesson? "
            "Does the lesson claim more than this one story can support?"
        ),
        "pattern_ids": [
            "story_memory_and_scene", "contrast_and_reversal", "expectation_reversal",
            "story_to_thesis", "failure_to_reframe", "unfinished_work_to_commitment",
            "authenticity_vs_performance", "craft_process_over_outcome",
        ],
    },
    {
        "id": "answer",
        "title": "Answer hard questions without dodging them",
        "question": "What does the question assume, and what does the person asking need to decide?",
        "principle": (
            "Start by showing that you heard the question. Answer it directly "
            "when the facts allow. If the question leaves out a difference that "
            "matters, name it and explain why. Correct your own wording if it was "
            "too broad. Do not use a different question to avoid the one you were "
            "asked."
        ),
        "method": [
            "Restate the concern briefly and fairly.",
            "Give the clearest supported answer first.",
            "Name any condition, missing fact or distinction that changes the answer.",
            "If you overstated something, correct the exact phrase and continue.",
        ],
        "example_keys": ["question_and_reframe", "repair_and_self_correction"],
        "boundary": (
            "These moments come from one interview. They do not show that other "
            "songwriters work the same way, or that correcting a sentence changes "
            "what a listener thinks."
        ),
        "failure_case": (
            "Invented failure: someone asks for the confirmed launch date and the "
            "speaker launches into a story about why dates are difficult. The story "
            "may be relevant later, but first give the date—or say clearly that it "
            "is not known."
        ),
        "exercise": (
            "Write a real question someone might ask about your proposal. Draft "
            "one sentence that answers it. Add a second sentence for the condition "
            "or missing evidence. Ask a colleague whether your first sentence "
            "answers the question they heard."
        ),
        "check": (
            "Can the listener find the answer without searching through a long "
            "preface? Are uncertainty and corrections stated where they matter?"
        ),
        "pattern_ids": [
            "question_and_reframe", "question_redefinition", "qualification_and_boundary",
            "objection_and_response", "risk_safety_and_limit", "repair_and_self_correction",
            "premise_correction", "scope_repair", "technical_explanation_and_interruption",
            "evidence_gap",
        ],
    },
    {
        "id": "responsibility",
        "title": "Show who did the work and who owns the next step",
        "question": "Who contributed, who can decide, and what support or responsibility remains?",
        "principle": (
            "Credit and responsibility are related but different. Name the work "
            "people actually did. Say who can make the next decision and what "
            "help they need. A personal story is not a substitute for a service, "
            "policy or named person responsible for the work. If no one measured "
            "the result, say so."
        ),
        "method": [
            "Name specific contributions rather than praising an unnamed group.",
            "Separate what is already done from what is being requested.",
            "Say who decides, what help they need and who takes over any remaining work.",
            "Keep reported results separate from verified results.",
        ],
        "example_keys": ["credit_and_collective_agency", "hands_off"],
        "boundary": (
            "An Aishwarya Rai Bachchan address transcript widens recognition "
            "from individual encounters to clinical workers, outreach, partners "
            "and donors. A Manushi Chhillar address describes a local project "
            "through suppliers, sellers and participants. These readings make "
            "contributions and handoffs visible; they do not verify the reported "
            "medical or economic outcomes. The events and source claims were not "
            "independently checked."
        ),
        "failure_case": (
            "Invented failure: thanking a large team while leaving the next task "
            "with ‘someone’ and giving no time, authority or resources. Praise "
            "does not assign responsibility. Name the owner and what they need."
        ),
        "exercise": (
            "Choose one result in your talk. List the people and conditions that "
            "made it possible. Then write the next step, the person who can approve "
            "it, the support required and one thing the result does not yet prove."
        ),
        "check": (
            "Can a listener distinguish past contribution from the decision you "
            "are requesting? Is any claim of impact supported by a measure?"
        ),
        "pattern_ids": [
            "credit_and_collective_agency", "institution_system_and_policy",
            "reciprocal_learning", "hands_off", "credit_redirection",
            "recognition_to_specific_credit", "access_obstacle_to_support",
            "authority_to_service",
        ],
    },
    {
        "id": "relationship",
        "title": "Build connection without putting people on the spot",
        "question": "What relationship do your words create, and does the audience have a real choice?",
        "principle": (
            "A story, joke, identity or personal disclosure can help people see "
            "why a subject matters. It can also expose someone, reduce a group "
            "to a stereotype or pressure listeners to agree. Share only what is "
            "yours to share. Make your point without asking listeners to reveal "
            "private experiences or show a particular emotion."
        ),
        "method": [
            "State the point in words; do not make a gesture, identity or joke carry it alone.",
            "Use a personal example only with a clear reason and a fair boundary.",
            "Make participation optional and offer a way to pass or respond privately.",
            "Check who bears the risk if the joke or disclosure is misunderstood.",
        ],
        "example_keys": ["reciprocal_learning"],
        "boundary": (
            "This is one person's account. It cannot tell us what his daughters "
            "privately thought, how listeners responded or what is right for every "
            "family."
        ),
        "failure_case": (
            "Invented failure: asking everyone in a work meeting to tell a painful "
            "personal story to prove they care about a policy. A person should not "
            "have to disclose private information to count as engaged. Explain "
            "the issue with evidence and allow people to pass."
        ),
        "exercise": (
            "Read one personal example from your draft. Mark who owns the story, "
            "what the audience is being asked to feel or do, and whether someone "
            "can decline. Rewrite it so the point survives without demanding a "
            "private response."
        ),
        "check": (
            "Could a listener disagree, stay quiet or use another access mode "
            "without being treated as uncaring? Does the story belong in this talk?"
        ),
        "pattern_ids": [
            "identity_status_and_belonging", "value_and_moral_frame",
            "humor_rapport_and_self_undercut", "self_undercut",
            "grief_loss_and_continuation", "sorrow_and_continuation",
            "moral_to_memorial", "emotion_to_composure",
        ],
    },
    {
        "id": "next-step",
        "title": "Ask for a next step people can actually take",
        "question": "What action is possible for this audience, with the time, authority and support they have?",
        "principle": (
            "A useful request tells people what to do, who is responsible, what "
            "support is available and what happens if the condition is not met. "
            "Match the request to the audience’s actual role. Leave room to decline, "
            "ask for more information or choose another path. A strong closing "
            "can clarify a decision; it cannot prove that the decision was made "
            "or that the proposal worked."
        ),
        "method": [
            "Name one action, not a cloud of good intentions.",
            "Identify the person or group that can take it and the resources required.",
            "State the time limit, condition, opt-out or alternative path.",
            "Say how you will check what happened without treating attendance or applause as success.",
        ],
        "example_keys": ["institution_system_and_policy"],
        "boundary": (
            "A Shakira address transcript identifies capabilities of the business "
            "audience, qualifies the role of government, describes a reported local "
            "partnership and ends with policy requests. That gives the request a "
            "named audience and context. The transcript does not verify that the "
            "requests were adopted or that the described program caused the reported "
            "results. A speech’s proposal is not an outcome record."
        ),
        "failure_case": (
            "Invented failure: ending with ‘We all need to do more’ when listeners "
            "cannot tell what to do, who owns it or whether they have authority. "
            "Replace the slogan with one bounded request and a route for questions "
            "or refusal."
        ),
        "exercise": (
            "Draft the last 30 seconds of a proposal. State the decision, owner, "
            "time or resource limit, and what you will check afterward. Add one "
            "sentence that makes clear what approval does not commit the audience to."
        ),
        "check": (
            "Can the audience repeat the request, its limit and the next check? "
            "Is there a safe way to say no or ask for a different option?"
        ),
        "pattern_ids": [
            "audience_invitation_and_next_turn", "future_hope_and_action",
            "choice_and_responsibility", "metrics_and_revaluation", "metric_revaluation",
            "selection_and_incentive", "optional_support", "invitation_to_low_barrier_entry",
            "difficulty_to_capability", "despair_to_hope",
        ],
    },
]
