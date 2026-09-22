"""Authored lessons grounded in the indicated local full-context reviews.

Applications are invented teaching examples, explicitly distinguished from
the source speaker's account. Caption numbers are not playback timestamps.
"""

READING_ROUTES = [
    ("Make an idea understandable", "Start here when a term, system or large number is difficult to picture. Distinguish a clear explanation from evidence that its claim is true.",
     "definition_and_explanation analogy_metaphor_and_callback scale_shift cause_and_mechanism familiarity_to_scope unity_across_scale question_redefinition evidence_gap".split()),
    ("Tell a story that changes the point", "Use an event to show a decision, an unexpected result or a change in what matters. Keep the lesson within what the event can support.",
     "story_memory_and_scene contrast_and_reversal expectation_reversal story_to_thesis failure_to_reframe unfinished_work_to_commitment authenticity_vs_performance craft_process_over_outcome".split()),
    ("Answer a challenge precisely", "Notice what the question assumes, answer the real concern and stay within the evidence. Narrow a claim if it says more than the facts show.",
     "question_and_reframe qualification_and_boundary objection_and_response risk_safety_and_limit repair_and_self_correction premise_correction scope_repair technical_explanation_and_interruption register_shift".split()),
    ("Make shared work visible", "Show who contributes, who decides and what the next person needs. Distinguish credit for past work from authority and responsibility for future work.",
     "credit_and_collective_agency institution_system_and_policy reciprocal_learning hands_off credit_redirection recognition_to_specific_credit access_obstacle_to_support authority_to_service".split()),
    ("Handle status, emotion and belonging", "Consider the relationship your words create. Humor, vulnerability and moral claims need context; none automatically produces trust or agreement.",
     "identity_status_and_belonging value_and_moral_frame humor_rapport_and_self_undercut self_undercut grief_loss_and_continuation sorrow_and_continuation moral_to_memorial emotion_to_composure analogy_transfer".split()),
    ("Guide the audience toward a next step", "Give the presentation a route and the ending a usable next turn. Match the request to the audience's role and leave room for limits, choice and unfinished work.",
     "audience_invitation_and_next_turn future_hope_and_action choice_and_responsibility metrics_and_revaluation metric_revaluation orientation_and_roadmap purpose_attention_example selection_and_incentive optional_support invitation_to_low_barrier_entry difficulty_to_capability despair_to_hope audience_shift".split()),
]

LESSONS = {
    "story_memory_and_scene": {
        "title": "Use one scene to explain your point",
        "problem": "Your audience understands the words in your claim but cannot picture the judgment you are asking them to make. Adding more abstract praise—care, excellence, leadership—does little to show the choice.",
        "principle": "Build the story around a choice. First show what the person was trying to do. Then show what happened that their first measure of success missed. Only then name the larger idea. The audience can compare the intended result with the consequence. This is one possible reading of the story, not a measured audience effect.",
        "source_title": "Jeff Bezos: cleverness, kindness and a childhood calculation",
        "source_writeup": "writeups/full-context-address-72.md",
        "source_passages": "Caption numbers 0–25: travel with grandparents and the calculation; 26–43: the unexpected reaction; 44–51: the kindness/cleverness distinction and gifts/choices approach. These are caption positions, not seconds.",
        "source_reading": [
            "The setup makes the child's working definition of success understandable. He likes calculating. While travelling with his grandparents, he uses a remembered smoking advertisement to estimate years of life lost. He expects admiration for his arithmetic. The precision belongs to the anecdote; it is not a reliable medical estimate.",
            "The grandmother cries. That response interrupts the expected reward and creates the story's central question: what has the clever child failed to notice? The speaker then describes uncertainty about how his grandfather will respond. Delaying the explanation gives the reaction a place in the reasoning.",
            "The grandfather's distinction between kindness and cleverness gives the speaker a new way to judge the action. He later develops the difference between gifts and choices. The larger point grows from a specific mistake; it is not an unrelated slogan."
        ],
        "transfer": "Use the same order: show the decision, what happened and what you learned. Choose a small event from your work where a technically correct action did not help the person or decision. Explain what changed in your thinking. One event can illustrate a problem, but cannot show how common it is.",
        "worked_title": "A team presentation about support quality",
        "before": "We need to become more customer-centric and stop focusing only on efficiency.",
        "after": "In this hypothetical case, we closed a support ticket in four minutes. The dashboard called it fast. The customer wrote back because the answer explained the setting but never told her what to click. We had optimized the reply, not the resolution. For next week's pilot, let's track whether the customer can take the next step as well as how quickly we respond.",
        "worked_explanation": "The four-minute ticket gives one measure of success. The return message shows what that measure missed. The last sentence proposes a small test. The story does not claim to describe every ticket or prove that the proposed measure will work.",
        "variations": [
            "For an executive audience, compress the setup and spend the saved time on the decision and its cost: what should change, who owns it, and how you will check the result.",
            "For new team members, explain the original measure before introducing its blind spot. They may not share the assumptions that made the first action seem sensible.",
            "For a sensitive or private event, use a clearly labeled hypothetical case or obtain permission. The lesson depends on the judgment, not on exposing an identifiable person."
        ],
        "failure_case": "An invented teaching example: a presenter describes one grateful customer and concludes that a redesign made all customers happier. One person's story cannot show how common this is. Use the story to explain what to investigate, then show evidence from the wider customer group.",
        "exercise": "Choose a small, low-risk event. Write four sentences: what you wanted; what you did; what happened that you did not expect; what you would measure next time. Delete details that do not help explain the change. Add one claim the event supports and one it does not.",
        "self_check": "Can you name what you expected and what you would look at next time? Point to the exact change instead of calling it better or impressive. Does your recommendation follow from the event? If a listener is available, ask which detail changed their view. Otherwise, underline that detail yourself; if you cannot find one, revise."
    },
    "contrast_and_reversal": {
        "title": "Explain what changed and what stayed the same",
        "problem": "You want to explain a revised plan without sounding inconsistent, defeated or certain that everything about the earlier plan was wrong.",
        "principle": "Explain what the earlier plan was meant to achieve, what you learned and what you changed. Say which parts of the plan still make sense. These details let listeners compare the old and new decisions and judge your reasons. Announcing a dramatic change without explaining it leaves them guessing.",
        "source_title": "Mindy Kaling: the completed college checklist and the changed adult timetable",
        "source_writeup": "writeups/full-context-address-71.md",
        "source_passages": "Caption numbers 219–231: completed college checklist and delayed interpretation; 232–252: adult timetable and the parenthood account; 253–261: permission to revise, with a concession that plans can motivate. Caption positions are not playback timestamps.",
        "source_reading": [
            "Kaling first describes a college checklist that she completed. This is more precise than a generic story about plans failing: the opening establishes that structured ambition once served her. She asks the audience to keep listening before treating the list as boasting.",
            "The adult checklist then has a different outcome. Its ages and schedules matter. The contrast is not simply between doing something and never doing it; it includes doing it outside the order she once expected. The account of parenthood introduces a feared absence of the conventional support scene and then names support from family and friends.",
            "The interpretation leaves room for planning. She permits changing the order or dropping goals while acknowledging that structured ambition can motivate. Removing that concession would turn the passage into a simpler but less faithful message: abandon plans."
        ],
        "transfer": "Write three sentences: why the earlier plan made sense, what you learned and what you now propose. Say whether the goal, the method or only the date has changed. Check that someone who supported the earlier plan could recognize it in your account.",
        "worked_title": "Explaining a revised product launch",
        "before": "The old plan was unrealistic. We need to be agile and launch differently.",
        "after": "Our original plan put all three regions into the June launch because we expected one approval process. In this hypothetical example, the pilot showed that each region needed a separate review. The goal is still a consistent customer experience; the timetable changes. We propose launching the approved region first and setting the other dates after their reviews. Keeping the June date for all three would preserve the calendar while abandoning its assumption.",
        "worked_explanation": "The revision is supported by an explicit change in the assumed approval process. The speaker preserves the goal, changes the sequence, and states what determines the remaining dates. The original team is not made into a foolish opponent to make the new proposal look good.",
        "variations": [
            "For colleagues who built the old plan, begin with the information available when it was made. Show respect through an accurate account of the earlier reasoning.",
            "For an audience new to the project, reduce the history to one assumption and one observation. More chronology is useful only if it changes the decision.",
            "For a personal story, describe your own changed expectation without suggesting that everyone has the same support, resources or freedom to revise."
        ],
        "failure_case": "An invented teaching counterexample: a speaker calls a previous strategy reckless, then recommends almost the same strategy with a new name. There is no observable turning point or substantive change. Test the contrast by removing the adjectives and comparing the actual decisions.",
        "exercise": "Write two columns: what changes and what stays. Draft a one-minute explanation containing one earlier assumption, one new observation and one revised decision. Add a sentence describing when the earlier plan would still be appropriate.",
        "self_check": "Could someone who supported the old plan recognize it in your description? Can you distinguish the new observation from your interpretation? Does the audience know exactly what they are being asked to approve now?"
    }
}

LESSONS.update({
    "question_and_reframe": {
        "title": "Answer the decision behind the question",
        "problem": "A question gives you two options, but neither describes how the work actually happens. Picking one would sound decisive while giving the audience the wrong explanation.",
        "principle": "Check whether the question gives you enough room to answer accurately. If someone asks whether A or B comes first, the process may start with something else. Say what the question leaves out, explain the actual order and give an example. Then return to what the person wanted to know. Changing the question is useful only if it helps you answer their concern.",
        "source_title": "Taylor Swift: an idea or feeling before the music-versus-lyrics choice",
        "source_writeup": "writeups/full-context-interview-27.md",
        "source_passages": "Caption numbers 100–120: music-versus-lyrics question and the idea/feeling response; 193–212: a later account distinguishes initial inspiration from extended development. These are caption positions, not playback times.",
        "source_reading": [
            "The interviewer asks whether music or lyrics comes first. The offered alternatives are recognizable components of a song. Swift instead describes starting with an idea or feeling. This keeps the topic—how composition begins—while changing the categories used to explain it.",
            "She follows with an autobiographical composition example and an account of metaphor connecting an experience to something different. The example gives the revised explanation a particular case. We can inspect the structure without reproducing song lyrics or treating one artist's process as a rule for every songwriter.",
            "A later answer describes a song developing across years. That does not necessarily contradict an account of quick inspiration: beginning an idea and completing a work are different intervals. A careful presentation preserves that distinction instead of making speed the headline."
        ],
        "transfer": "Write the question as it was asked. Under it, name the detail or option it leaves out. Start your answer by explaining why that detail matters, then answer the original concern. If someone asked for a decision, state your decision after the explanation.",
        "worked_title": "A client asks whether design or engineering should start first",
        "before": "That is the wrong question. We need to think more strategically.",
        "after": "You are asking whether design or engineering should lead the first week. Before either team builds, we need to agree which customer task is failing. In this hypothetical project, users can find the report but cannot tell which version is current. Let's spend Monday confirming that problem together, then let design test the version label while engineering checks how reliably we can supply the date. So my recommendation is a shared first day followed by two specific tests.",
        "worked_explanation": "The answer retains the client's scheduling concern. It replaces a broad contest between disciplines with a dependency: agree on the problem, then test the relevant parts. The last sentence returns to an actual allocation of work, making it possible to disagree with the recommendation.",
        "variations": [
            "For a time-limited Q&A, use one distinction and one answer. A long explanation of why the question is imperfect can consume the time needed to address it.",
            "For an expert audience, state exactly which assumption you are changing. They may agree with the original framing for reasons you have not considered.",
            "For a beginner, use a concrete case before naming the abstraction. 'Finding the report and knowing it is current are different tasks' is easier to examine than a slogan about strategy."
        ],
        "failure_case": "Example of what can go wrong: asked whether a delivery will arrive Friday, a presenter discusses the company's commitment to quality without giving a date or uncertainty. The answer has changed the subject. State the known delivery status first; explain tradeoffs only as they bear on that status.",
        "exercise": "Write a question you expect to receive and underline what it assumes. Draft one answer using that assumption. Draft a second that names an important detail the question leaves out. Compare the answers: what changes once you include that detail? Finish with your decision or state what you still need to learn.",
        "self_check": "Can the questioner recognize their concern in the first sentence? Does the new distinction change the reasoning? Have you returned to the requested answer, or have you only supplied a more comfortable topic?"
    },
    "qualification_and_boundary": {
        "title": "State your point and its limits",
        "problem": "A sentence is easy to remember but too broad to apply safely. Listeners may carry a statement about one occasion into every occasion, or mistake a useful emphasis for the whole commitment.",
        "principle": "A claim may apply only at a certain time, to a certain group or in a certain situation. Say where it applies and where it does not. Attach that limit to the part of the claim it changes. A named condition tells the audience more than a general maybe.",
        "source_title": "Aishwarya Rai Bachchan: a commemorative date within ongoing work",
        "source_writeup": "writeups/full-context-address-73.md",
        "source_passages": "Caption numbers 40–68: family commemoration and the named day; 69–74: the date provides emphasis while every day deserves attention; 84–91: a milestone is revisited without imposing a cap on future work. Positions refer to transcript text, not seconds.",
        "source_reading": [
            "The speaker connects a named day to her account of honoring her late father. The date marks a time to pay attention and contribute. The speech does not test whether the day changed anyone's behavior.",
            "The next qualification expands the underlying commitment beyond that date. November 20 supplies emphasis while every day deserves to be a day of smiles. A listener who extracted only the named occasion could miss this distinction between a focal moment and continuing responsibility.",
            "The closing also revisits years and procedure totals as motivating milestones while rejecting a cap on the work. The speech allows a number to mark progress without allowing it to settle whether the wider task is finished. Procedure counts remain source claims, not independently verified patient outcomes."
        ],
        "transfer": "Underline the claim in your draft. Ask whether it depends on a date, a group, an assumption or a particular situation. Put that condition beside the claim: ‘This estimate assumes two people can work on the task,’ for example. If you announce a deadline or milestone, say what will be finished then and what work continues.",
        "worked_title": "Launching a documentation week",
        "before": "Next week we will solve our documentation problems.",
        "after": "Next week is our focused documentation cleanup. In this invented example, the goal is to update the five setup pages that new starters use most. That will not cover the entire handbook. Each page will have an owner who checks it after the cleanup, so the week starts a maintenance routine rather than closing the issue.",
        "worked_explanation": "The revision separates what the campaign covers from the work that continues afterward. Five setup pages is clear; solving documentation is not. The final ownership statement explains how the temporary event relates to ongoing work.",
        "variations": [
            "For a slide headline, put the essential limit beside the claim: 'Five setup pages updated' is clearer than 'Documentation fixed' with a footnote several slides later.",
            "For a technical audience, identify the assumption that would invalidate the conclusion. A specific condition is easier to test than a general appeal to caution.",
            "For a public announcement, repeat the limit where you ask people to act. Someone who only sees the invitation still needs to know what the offer includes."
        ],
        "failure_case": "Example of what can go wrong: 'This always works, though results may vary.' The qualification does not repair the absolute promise because it never says which results, for whom, or under what conditions. Replace the promise with the strongest claim your evidence supports.",
        "exercise": "Take one headline from your draft and write the broadest interpretation a reasonable listener might give it. If that interpretation exceeds your evidence, revise the headline itself. Name one condition that changes the conclusion and one practical consequence of that condition.",
        "self_check": "Does the audience still know your main point after you add the limit? Is the limit close enough to the claim to survive quotation? Does it tell the listener what changes in their decision?"
    },
    "credit_and_collective_agency": {
        "title": "Explain who helped produce the result",
        "problem": "The person giving the presentation becomes the apparent cause of the result. A generic thank-you leaves the audience unable to see who did what, how the contributions connected, or which capabilities must exist for the work to continue.",
        "principle": "Specific thanks can show how people contributed to a result. Name the work, connect it to the result and explain what another person's work made possible. Check that each person is credited accurately. A polished list does not prove who caused the result or whether it worked.",
        "source_title": "Aishwarya Rai Bachchan: widening credit from personal encounters to care, access and funding",
        "source_writeup": "writeups/full-context-address-73.md",
        "source_passages": "Caption numbers 11–18: personal encounters; 19–29: clinical and related workers; 30–39: outreach, geography, partners and donors; 75–83: the speaker's own contribution situated within the larger effort. These are caption numbers rather than playback times.",
        "source_reading": [
            "The address begins its account of significance with reported personal encounters. It then names doctors, nurses, speech therapists, orthodontists and other workers. The transition widens attention from the visible speaker to the people performing different parts of the work.",
            "Outreach personnel, people working in difficult geographies, government partners and donors extend the account. The review reads the sequence as spanning care, access and funding. A summary centered only on the celebrity's involvement would remove that distributed account.",
            "Later, the speaker places her foundation's contribution within the larger effort. That makes the relationship between personal testimony and collective work clearer. It does not independently verify the address's broad claims about access or every patient's experience."
        ],
        "transfer": "List the main pieces of work and who did each one. Beside each, write what it made possible for the next person. Choose a few connections to explain aloud and put fuller credits in the written material if needed. Check names and descriptions with the people concerned.",
        "worked_title": "Closing a project demonstration",
        "before": "I am proud of what we built. Thanks to everyone who helped.",
        "after": "In this fictional project, the demonstration rests on three kinds of work. Support colleagues identified the confusing setup step. Engineering made the new default reversible. The documentation team gave customers a way to check and change it themselves. Those contributions connect the discovery of the problem to a usable release; today's demo shows only the last few minutes of that work.",
        "worked_explanation": "The revised acknowledgment assigns concrete verbs and relationships. It gives the audience an account of the work that the demonstration alone cannot show. It also avoids claiming that the demonstration proves customer success after release.",
        "variations": [
            "For leadership, connect contributions to resources and continuing ownership. Knowing which work made the result possible helps clarify what must be maintained.",
            "For peers, include the planning and practical work, not only the people closest to the finished result.",
            "For an external audience, explain each contribution in ordinary language. Job titles alone may mean little to people outside the organization."
        ],
        "failure_case": "Example of what can go wrong: a presenter thanks many people, then says their own idea alone made the result possible. Those statements conflict. Another failure is blaming people for a decision they did not control. Be as careful when assigning responsibility as when giving credit.",
        "exercise": "Draw three boxes: discovery, doing the work and support. Add one specific contribution to each. Name a person or team only if you have checked who did it. Write a short thank-you that explains how two contributions fit together.",
        "self_check": "Are the verbs specific? Can someone understand the work without knowing the titles? Would the contributors recognize the account? Have you mistaken gratitude for evidence that the project achieved its intended effect?"
    }
})

LESSONS.update({
    "objection_and_response": {
        "title": "State the strongest objection fairly, then answer it",
        "problem": "You believe in a proposal, but the audience has a sensible reason to resist it. Calling that resistance fear or lack of ambition removes information the decision needs.",
        "principle": "State the concern fairly enough that the person raising it would recognize it. Say which part you accept and how it affects your proposal. You may need to answer a factual question, reduce the request or explain why you think a cost is worth accepting. If the cost remains, keep it clear in your recommendation.",
        "source_title": "Jeff Bezos: a respected boss's caution about leaving a good job",
        "source_writeup": "writeups/full-context-address-72.md",
        "source_passages": "Caption numbers 85–92: the boss's caution and time for reflection; 93–98: the speaker's anticipated-regret reasoning. Caption positions are not playback seconds.",
        "source_reading": [
            "The boss enters the story as an admired person who listens. His concern is specific: an entrepreneurial idea looks different when pursuing it requires leaving an already good job. The speaker acknowledges the logic. This matters because the account preserves a real opportunity cost instead of inventing an unimaginative opponent.",
            "Reflection separates receiving the objection from deciding. The reported choice is then explained through anticipated regret: the speaker weighs trying and failing against never trying. That changes the standard by which he evaluates the risk; it does not disprove the boss's observation about the attractive job.",
            "The passage explains a personal decision retrospectively. It does not supply the resources, obligations or alternative options needed to recommend the same decision to everyone. A presentation can borrow its fair treatment of a concern without borrowing its career choice or treating later success as evidence that the original risk was negligible."
        ],
        "transfer": "Complete this sentence: ‘Someone could reasonably oppose this proposal because ____.’ Take one concern at a time. Decide whether you can answer it with facts, change the plan or accept the remaining cost. Finish by stating your recommendation and the conditions it depends on.",
        "worked_title": "Asking for a limited internal training pilot",
        "before": "Some people will say we are too busy, but we need to invest in learning if we want to improve.",
        "after": "For this invented proposal, the operations team's objection is that training takes people away from the support queue. That cost is real. I am asking for one forty-five-minute session with four volunteers, scheduled outside our busiest hour—not a company-wide rollout. We will compare the time spent with the troubleshooting steps participants can perform afterward. If queue coverage cannot be maintained, we postpone. This pilot buys a small amount of information; it does not establish that a full program is worth the time.",
        "worked_explanation": "The revision names the resource at stake, reduces the initial commitment and supplies a stop condition. Its argument is narrower than the original appeal to improvement: the request is to learn whether training helps under a specific practical constraint. No benefit is reported before the pilot has happened.",
        "variations": [
            "In an executive recommendation, place the strongest objection beside the requested decision, with its cost and mitigation. Do not bury it in an appendix that the decision-maker may never reach.",
            "In a live question period, restate the concern briefly and check your understanding when necessary. Then say whether your answer changes the recommendation or what it covers.",
            "When the objection identifies a genuinely unacceptable consequence, withdraw or redesign the proposal. Fair hearing includes the possibility that the objection wins."
        ],
        "failure_case": "Example of what can go wrong: a presenter reduces a staffing concern to people being afraid of change, then tells an inspirational story. The story does not provide the missing staff. Another failure is conceding a concern verbally while leaving every part of the plan unchanged and unexplained.",
        "exercise": "Write your recommendation in one sentence and the strongest objection in another. Draft three possible responses: evidence that answers it, a smaller design that contains it, and an honest statement that accepts the remaining cost. Choose only the response your situation actually supports.",
        "self_check": "Would the person who raised the concern accept your version of it? Have you answered the actual constraint? Can the audience tell which cost remains and what would change your recommendation?"
    },
    "repair_and_self_correction": {
        "title": "Correct the exact claim that went too far",
        "problem": "In conversation, a broad word slips out: everyone, always, never, the whole team. Continuing smoothly can leave a more expansive claim in the listener's mind than your evidence supports.",
        "principle": "A useful correction replaces the exact part of a claim that was wrong. Name the mistaken word, give the accurate version and explain whether the change affects the decision. Match the correction to the error: a corrected pronoun needs little explanation; a changed number may require a new conclusion. Correcting an error is a responsibility, not a performance of humility.",
        "source_title": "Taylor Swift: narrowing a pronoun and softening an absolute",
        "source_writeup": "writeups/full-context-interview-27.md",
        "source_passages": "Caption numbers 285–304: a broad they formulation narrowed to him; 621–647: never-linear language softened to very rarely. These references identify transcript positions, not media times.",
        "source_reading": [
            "In the relationship-writing exchange, the movement from a broad pronoun to a singular one changes the number of people the anecdote appears to concern. An analyst who preserves only the first formulation can turn one account into an apparent pattern of repeated incidents. The repaired version must govern the summary.",
            "Later, a discussion of career development includes an absolute about a path never being linear, immediately softened to very rarely. The qualification leaves room for exceptions. It remains personal advice in an interview, not a measured frequency estimate about creative careers.",
            "Both moments show a speaker revising language while the exchange continues. The transcript supports identifying that revision. It does not establish whether listeners noticed it, trusted the speaker more, or retained the corrected claim. Those possible effects should not be promised as a technique's guaranteed reward."
        ],
        "transfer": "Listen for words that make your claim broader than your knowledge. Change only what needs correcting, then repeat the full accurate claim if it affects the decision. In a prepared presentation, correct the slide and notes too; do not leave the audience with a chart or quotation that still shows the error.",
        "worked_title": "Repairing a generalization during a product review",
        "before": "Every customer struggles with this step. Well, not literally every customer, but you get the point. We have to redesign it.",
        "after": "In this hypothetical review: I said every customer; I should have said three of the five people in this week's usability sessions. That is a reason to investigate the step, not an estimate of how often all customers struggle. My recommendation is to test a revised instruction in the next round before committing to a larger redesign.",
        "worked_explanation": "The correction identifies the original overstatement, supplies the actual observation and changes the strength of the recommendation. Three of five is a feature of this invented example, not a finding from the reviewed speeches. Naming the sample is useful because the decision depends on the difference between a local observation and a claim about a wider group.",
        "variations": [
            "For a small verbal slip with no downstream consequence, keep the repair short: Tuesday, not Thursday. Long apologies can obscure the replacement information.",
            "For an error in a distributed deck, circulate a corrected version with the changed claim and affected decision clearly identified. Editing silently may leave earlier readers using the old figure.",
            "When you do not know the replacement fact, say what you are withdrawing and what you need to check. A second confident guess is not a correction."
        ],
        "failure_case": "Example of what can go wrong: a speaker says all departments approved a launch, then retreats to most departments without checking either statement. The softer word still invents knowledge. Another failure is correcting a sample size but retaining a conclusion that depended on the inflated original.",
        "exercise": "Underline every absolute word and group label in a draft. For each, write down what supports how broadly you are using it. Practise a fifteen-second correction: the mistaken claim, the accurate replacement and what that changes in your recommendation.",
        "self_check": "Is the corrected statement true to the information you have? Is it clear which version supersedes the other? Did you revise any conclusion, slide or handout that depended on the error?"
    },
    "craft_process_over_outcome": {
        "title": "Show the steps between idea and finished work",
        "problem": "A finished piece looks inevitable. When you show only the result or describe a flash of inspiration, the audience has little to borrow for its own unfinished work.",
        "principle": "Show the steps between having an idea and finishing the work. Explain how you recorded the idea, developed it, chose what to keep and prepared it for use. At each step, name a decision and what helped you make it. Include any failed attempts or unresolved problems that matter. A reader can then try a specific step instead of being told only to work hard.",
        "source_title": "Taylor Swift: developing ideas over time and recording them while travelling",
        "source_writeup": "writeups/full-context-interview-27.md",
        "source_passages": "Caption numbers 193–212: extended development; 246–284: adapting to locations and imperfect phone recordings; 621–647: revisions, dead ends and obligations. Caption numbers are not timestamps.",
        "source_reading": [
            "The interview distinguishes an initial idea from a song's longer development. A rapid beginning and years of later work describe different parts of the process. Compressing them into one duration produces either a misleading myth of instant completion or a misleading claim that every idea requires years.",
            "Asked about writing locations, Swift describes adapting to travel rather than requiring a single ideal room. Capturing ideas on a phone is one practical response. The account also retains recordings that later sound like mumbling. Capture creates a trace, but the trace can fail to preserve enough information to develop the idea.",
            "The later advice includes revisions, dead ends and work outside the most visible creative activity. These details make the reported process less frictionless. They are not a controlled comparison of methods and do not establish that a particular device, location or routine will produce successful work for another person."
        ],
        "transfer": "Choose one piece of work you have permission to discuss. Show its first usable draft, one important change and why you made it. Include something you dropped or a try that failed. End with a next step someone else can try; do not present your personal routine as the only way to be creative.",
        "worked_title": "Explaining how a team developed a presentation opening",
        "before": "The opening came to us on a walk. Sometimes you just need to wait for inspiration.",
        "after": "In this invented example, the walk gave us a phrase: fewer clicks, less confusion. It did not give us an opening. We wrote the phrase down with the setup problem it referred to. In the first draft, we discovered that fewer clicks was the wrong promise: an extra confirmation step was useful. We changed the opening to a short example showing how a person could see what would happen before confirming. The next task is to test whether that example makes the decision clear. The phrase started the work; revision changed the claim.",
        "worked_explanation": "The example shows a saved fragment, a reason to reject part of it and a revised draft. It proposes a future test instead of pretending success has already been proved. A learner can try the same steps without taking the walk or copying the original wording.",
        "variations": [
            "For a workshop, bring two successive versions and ask participants to locate the decision between them. Reveal your reason afterward, allowing alternative revisions to remain possible.",
            "For leadership, compress the process into the consequential choice and the remaining uncertainty. A chronology of every draft may consume time without clarifying the decision.",
            "For beginners, provide a small starting task: capture one example and the point it might explain. An elaborate expert workflow may create more barriers than it removes."
        ],
        "failure_case": "Example of what can go wrong: a designer attributes a successful presentation to waking at five in the morning. The routine describes a circumstance, not evidence of what improved the presentation. Another failure is displaying many drafts without explaining why any revision was made.",
        "exercise": "Save a rough paragraph, then make one change to its meaning. Beside the two versions, write what you wanted to say, what was unclear and how the change addresses it. Leave a note naming the next part to work on so you can resume tomorrow.",
        "self_check": "Can a reader identify an action to try and a reason to revise? Have you separated the origin of an idea from its development? Does the account include uncertainty without pretending that unfinished work is already successful?"
    }
})

LESSONS.update({
    "access_obstacle_to_support": {
        "title": "Name the barrier before offering help",
        "problem": "A presentation praises generosity or promises access without explaining what prevents someone from taking the next step. The proposed help may sound admirable while missing the actual obstacle.",
        "principle": "Describe the steps: a person tries to take part, meets a specific barrier, gets help suited to that barrier and can move forward. Keep the larger conditions in view. Removing one obstacle may help someone continue, but it does not guarantee the final result or change later decisions controlled by other organizations.",
        "source_title": "Lucila Takjerad, as identified in the local review: a stranger helps a mother enter her name",
        "source_writeup": "writeups/full-context-address-66.md",
        "source_passages": "Caption numbers 25–50: the list, inability to write a name and the stranger's help; 49–65: migration, loss and retrospective alternatives; 103–125: modest actions and the responsibility to do more. Identity spelling varies in the available material; caption positions are not timestamps.",
        "source_reading": [
            "In the narrated market encounter, the mother wants to join a list associated with refuge in France but cannot write her name. A stranger notices and writes it for her. The help is concrete enough to explain why it matters: it addresses the task at the exact point where she cannot proceed.",
            "The family is said to immigrate months later. The sequence gives the gesture significance, but it does not establish that writing the name alone caused the move or every later opportunity. Eligibility, processing and other institutional conditions remain outside the brief incident. The speaker also retains sadness about people left behind, so opportunity does not erase loss.",
            "The closing turns toward ordinary help, including translation assistance and a ride. It asks graduates to do the most they can as well as the least they can. That qualification matters: the memorable small gesture is not an argument for substituting token kindness for larger responsibilities."
        ],
        "transfer": "For a service, product or community presentation, find the exact step where someone cannot continue. Check whether the problem is information, language, physical access, time, equipment or eligibility. Offer help for that problem, ask whether it is wanted and name later conditions you cannot change.",
        "worked_title": "Proposing a more accessible workshop registration process",
        "before": "We want everyone to feel welcome, so we will send a more enthusiastic invitation.",
        "after": "In this fictional workshop, a participant can read the invitation on a phone but cannot complete the registration form because it requires a desktop-only attachment. A warmer invitation will not change that step. We propose a mobile form and an optional assisted-registration slot. We still need to check venue access and available places; completing registration is the next step, not proof that everyone can attend.",
        "worked_explanation": "The revision points to a problem in the task instead of blaming the participant. It says what each change is meant to fix. The remaining limits make clear that one better form will not make the workshop accessible to everyone.",
        "variations": [
            "For a product team, walk through the journey at the point of failure and distinguish an observed barrier from a suspected one. A demonstration of one case does not establish how many people encounter it.",
            "For a volunteer audience, specify a modest action within the volunteer's competence and a route for needs beyond it. Good intentions do not authorize taking over another person's decisions.",
            "For a funding request, separate the immediate access measure from the continuing service capacity. More successful applications can expose a later bottleneck rather than solve it."
        ],
        "failure_case": "Example of what can go wrong: an organization offers application coaching when the real obstacle is a fee people cannot afford. The coaching may help with applications, but it does not remove the fee. Another failure is sharing the story of someone who received help without permission, to make the helper look generous.",
        "exercise": "List the steps someone must take to join an activity. Mark one step where you have seen people get stuck. Propose a change to that step and name two problems it would leave unresolved. Describe the proposal in four sentences, using the actual actions instead of words such as inclusive or empowering.",
        "self_check": "Can the reader see exactly what changes for the participant? Is the help appropriate and wanted? Have you separated removal of a barrier from achievement of the final outcome?"
    },
    "orientation_and_roadmap": {
        "title": "Tell listeners where the talk is going, then follow that plan",
        "problem": "Your material contains good points, but listeners cannot tell where they are, how the pieces relate or when you have answered the question you announced.",
        "principle": "Tell listeners which questions or parts you will cover. As you move through the talk, use the same names so they can follow the plan. At the end, show how the parts answer the opening question. Include only sections that help with the audience's task, and promise only what you have time to explain.",
        "source_title": "William McRaven: ten announced lessons, ten story units and a recap",
        "source_writeup": "writeups/full-context-address-67.md",
        "source_passages": "Caption numbers 44–62: the ten-lesson promise; 63–259: the ten story-and-lesson units; 260–276: the compressed closing return. Caption references are positions, not playback times.",
        "source_reading": [
            "The address explicitly promises ten lessons before delivering them. Bed inspection, coordinated paddling, a smaller crew and later training stories form successive units. A recurring change-the-world cue helps mark the movement from a particular story to its proposed broader lesson.",
            "The concrete objects differ while the larger frame recurs. The close compresses earlier stories into imperatives and returns to the institutional slogan. The structural promise is therefore observable at the beginning, through the sequence and in the ending; it is not just a list placed on an introductory slide and forgotten.",
            "Fulfilling the roadmap does not validate every lesson. Some claims in the address are more absolute than their examples warrant, and hazardous training accounts are not general practical instructions. Nor does the transcript show that listeners remembered ten items. Borrow the fulfilled structure without assuming that ten is an ideal number or that a tidy list proves its contents."
        ],
        "transfer": "Start from the audience's decision and choose the smallest set of sections needed to support it. Give each section a question, a contribution and a closing sentence. At the end, answer the announced questions in the same order. If the scope changes during discussion, say which section you are postponing instead of silently abandoning the promise.",
        "worked_title": "Structuring a short internal tool proposal",
        "before": "I will cover the background, a few numbers, the options, some screenshots and anything else we have time for.",
        "after": "For this invented proposal: we need to decide whether to run a two-week trial. I will answer three questions: where does the current handoff fail, what would the trial change, and what would make us stop? First, the handoff. Later transitions repeat the second and third questions. The closing returns to them: we have a specific handoff to test, a limited change and a stop condition. The decision today is whether to authorize that trial—not whether to adopt the tool permanently.",
        "worked_explanation": "The roadmap makes each section accountable to the decision. The closing distinguishes the narrow authorization from a larger commitment. The script describes a presentation structure; it intentionally does not invent evidence that the hypothetical tool performs well.",
        "variations": [
            "For a technical audience, use the governing questions as section headings and keep detailed derivations beneath them. The audience should be able to recover the argument after inspecting a detail.",
            "For a short pitch, two parts may suffice: the problem worth solving and the next test worth authorizing. A large numbered list can consume the time it is meant to organize.",
            "For a discussion-led session, announce the decision order rather than a rigid speaking order. Name which question a contribution addresses before moving to the next."
        ],
        "failure_case": "Example of what can go wrong: a presenter promises three lessons, introduces seven more ideas and ends with a motivational quote. The extra material may be interesting, but the audience has to reconstruct the promised route. Another failure is a beautifully completed roadmap whose sections never justify the requested decision.",
        "exercise": "Write your opening roadmap and closing recap on the same page. Draw a line from each promised question to the section that answers it and the sentence that summarizes the answer. Cut, move or label any material with no role in that route.",
        "self_check": "Did every promised part arrive? Do the transition labels match the opening? Does the recap carry answers rather than just repeat topic names? Is the list short enough for your available time?"
    },
    "analogy_metaphor_and_callback": {
        "title": "Return to an earlier image to add meaning",
        "problem": "Your opening story and closing message feel like separate pieces. A decorative metaphor may be memorable, but it does not show how the argument developed.",
        "principle": "Introduce an object, phrase or situation early in the talk, then return to it after you have explained something that changes its meaning. A locked door might first describe a problem and later stand for a choice about who gets access. Make that change clear. Repeating an image can connect two parts of a talk; the claims in those parts still need evidence.",
        "source_title": "Jennifer Aniston: the table moves from exclusion to a place for questions",
        "source_writeup": "writeups/full-context-address-68.md",
        "source_passages": "Caption numbers 21–30: dismissal from a childhood dinner conversation; 56–70: a child's question and the speaker's limit; 80–86: the inclusive table callback and redirected recognition. These are caption numbers, not timestamps.",
        "source_reading": [
            "The table first appears in a childhood account of being dismissed from a conversation for having nothing interesting to contribute. In that setting it represents conditional participation: a child's place in the exchange depends on an adult's judgment of the child's worth.",
            "Later, a child asks what cancer is, and the speaker describes not feeling equipped to answer. The transcript supplies no substantive medical explanation. The episode therefore introduces a question with value even though the adult lacks an answer; it does not portray expertise that the source never demonstrates.",
            "At the close, the table returns as a place every child deserves, and questions retain value even when adults cannot answer them. The image joins the earlier exclusion to the later limit of knowledge. The change is specific: participation need not require an impressive contribution, and respecting a question does not require pretending to know."
        ],
        "transfer": "Choose an opening image that already belongs to your actual subject. Ask what it means at first and what a reader should understand differently at the end. Write both appearances before adding ornament. If the final use merely repeats the opening phrase, add the missing reasoning or remove the callback.",
        "worked_title": "Opening and closing a proposal for clearer project handoffs",
        "before": "Communication is a bridge. We need to build bridges. Thank you, and let us keep building bridges.",
        "after": "In this hypothetical presentation, the opening shows an inbox message with the subject Done. Nobody knows whether that means drafted, reviewed or released. After explaining the proposed handoff fields and their limits, the closing returns to the message: Done should tell the next person what they can do. In our pilot, every completion message will include what changed, who checked it and the next owner. We will review whether those fields remove ambiguity before making them standard.",
        "worked_explanation": "The familiar word returns with a more specific meaning. The middle of the presentation must earn that change by explaining the handoff proposal; the callback cannot substitute for that explanation. The proposed pilot also leaves its effectiveness open to inspection.",
        "variations": [
            "For a leadership presentation, let the recurring object carry the decision standard: a dashboard cell, a queue or a handoff message. Keep practical details beside the image so it does not float free of the proposal.",
            "For a personal address, return to an object that genuinely belongs to the remembered event. Do not manufacture a quotation or add sensory details you cannot substantiate.",
            "For a technical explanation, state where a metaphor stops matching the system. A bridge can suggest connection; it cannot explain permissions, failure states or data ownership by itself."
        ],
        "failure_case": "Example of what can go wrong: a speaker opens with a locked door and closes by declaring all doors open, while the proposal leaves the admission rules unchanged. The symbolic resolution conceals an unresolved barrier. Another failure is choosing a vivid image that suggests properties the actual system does not have.",
        "exercise": "Write an opening image in two sentences. Under it, write what that image means. Draft a closing return and name exactly what has changed. Identify the paragraph in the middle that earns the change; if none does, revise the argument before polishing the ending.",
        "self_check": "Does the returning image mean something more precise than it did at the start? Is the change supported by the intervening material? Could the image make the audience infer a result or promise you have not established?"
    },
    "reciprocal_learning": {
        "title": "Invite learners to correct what you think you know",
        "problem": "An account of leadership or mentoring makes one person the permanent source of wisdom. The people receiving help appear only as evidence of the leader's generosity.",
        "principle": "Show what each person learned from the other. For example, a manager may teach a procedure while a new colleague points out a missing step in its instructions. Explain what changed because of that discovery. The manager may still be responsible for the procedure. Saying that everyone learned from everyone tells us little unless you name the learning.",
        "source_title": "Dwayne Johnson with Oprah: learning from a father, then from daughters",
        "source_writeup": "writeups/full-context-interview-24.md",
        "source_passages": "Caption numbers 0–44: parenting commitments and a concrete message; 45–66: the father's teaching followed by the daughters' teaching; 429–455: receiving support from an audience. Caption positions do not supply verified timing.",
        "source_reading": [
            "The opening discussion makes a parenting commitment concrete through a message that need not receive a reply. The account gives an example of what an absence of conditions could look like. It remains the guest's report, not independent evidence of the daughters' experience or of parenting quality.",
            "The interview then moves from what the father taught the guest to what his daughters taught him. The host's question is part of the structure: the change in direction is elicited in dialogue. A summary that credits the guest alone with every turn would erase the interviewer’s contribution.",
            "Near the end, the guest describes needing the audience's support after his father's death. That moment complements his earlier intention to create experiences for audiences. It shows the giver also describing a need to receive, without proving that every listener felt the same way or that the encounter produced a measured emotional benefit."
        ],
        "transfer": "In a leadership story, identify a concrete instance when a junior colleague, participant or customer changed your understanding. Explain what you did differently afterward. Keep responsibility with the right person: being open to learning does not remove a manager's duties to the people they supervise.",
        "worked_title": "Introducing a revised onboarding guide",
        "before": "We taught the new starters everything they needed, and they brought fresh energy to the team.",
        "after": "In this invented onboarding example, we taught new starters how to run the setup steps. They showed us where the guide assumed knowledge we had stopped noticing: it named the shared workspace without explaining how to request access. We have added the request route and its owner before the setup instructions. The next onboarding group will help us check whether that change is enough. Their questions changed our documentation; responsibility for maintaining it remains with us.",
        "worked_explanation": "The new starters point out a missing step. The experienced team changes the guide instead of merely praising fresh eyes. The final sentence keeps responsibility clear and says the change still needs to be checked.",
        "variations": [
            "For a mentoring account, name a question that changed your advice and explain why. Obtain permission before making another person's learning difficulty part of a public story.",
            "For a customer presentation, show what customer input changed and what remains unresolved. Listening language without a traceable change can become a ceremonial acknowledgment.",
            "For a manager speaking to staff, provide a usable channel for correction and explain who responds. An invitation to teach the manager has little substance if disagreement carries unaddressed costs."
        ],
        "failure_case": "Example of what can go wrong: a senior speaker says interns taught them everything, then describes only their own achievements. The reversal is flattering but empty. A different failure asks junior staff to repair a flawed process without giving them authority, time or support.",
        "exercise": "Write three sentences: what you helped someone understand, what their response helped you notice, and what you changed. Replace learned so much with a specific observation. Add the responsibility that remains yours even after the exchange.",
        "self_check": "Is the contribution in each direction concrete? Does the account give appropriate credit to questions and feedback? Have you confused learning from someone with making them responsible for your work?"
    }
})

LESSONS.update({
    "scale_shift": {
        "title": "Connect the total to one person's experience",
        "problem": "A large number communicates magnitude but leaves the lived problem indistinct. A single vivid story communicates experience but can conceal how common or varied that experience is.",
        "principle": "A total and one person's story answer different questions. A total shows how many cases there are. One example shows how a problem happens. Return to the total to show what that example can—and cannot—tell us. Say when you change from the group to one person. Do not let one vivid story stand in for the total, or imply that everyone has the same experience.",
        "source_title": "Shakira: a large estimate, the difficulty of seeing individuals and an audience's own children",
        "source_writeup": "writeups/full-context-address-65.md",
        "source_passages": "Caption numbers 19–24: the source-era estimate and country-sized comparison; 25–30: individuals and circumstances of birth; 31–44: shared future concerns and children. These are transcript positions, not playback times.",
        "source_reading": [
            "The address gives an estimate of 250 million children at risk and compares it with the number of people in a large country. That figure comes from the speech; this lesson does not verify it or present it as current. The speaker uses it to show size before changing perspective.",
            "The speaker says that as the number grows, it becomes harder to see each person. The passage then asks listeners to imagine that the children being discussed could be their own. This invites the audience to picture the people in the total; it does not show that their feelings changed.",
            "The next movement connects different groups of children with shared future problems and possible contributions. The sequence joins scale and identification. It also requires care in reuse: a person's value need not depend on their future productivity or on whether the audience finds their circumstances familiar."
        ],
        "transfer": "Decide what each part adds. Use a checked total to show how many cases there are. Use a sourced or clearly made-up example to show one person's experience. Then say how far that example can take you. If you do not have a reliable total, say so; do not use one story to guess how common the problem is.",
        "worked_title": "Explaining an onboarding problem without confusing cases and people",
        "before": "We have hundreds of onboarding failures. Imagine how frustrating that is for everyone.",
        "after": "For this invented dataset, last month's log contains 240 failed setup attempts, not 240 different people. For example, a user follows an expired invitation and reaches a screen with no way to request a new one. This shows one way setup can fail. We still need to sort the log to learn how many failed attempts involve expired invitations before deciding whether this is the most important fix.",
        "worked_explanation": "The opening explains what was counted. The example shows one way the problem can happen. Returning to the log shows that we still do not know how often it happens. The number and example are invented for practice, not facts about a real product.",
        "variations": [
            "For an executive briefing, show the total, what it counts and the example together. Say whether the example is typical, unusual or chosen to show how something happens rather than how often it happens.",
            "For a public-interest presentation, show that people have choices and different circumstances. Do not choose only examples that make people seem worthy because their story feels familiar or impressive to the audience.",
            "For a technical investigation, compare the total number of failures with one recorded example. The example can show how a failure happens; a separate count is needed to show how often it happens."
        ],
        "failure_case": "Example of what can go wrong: a presenter reports ten thousand failed attempts, describes one stranded customer, then says ten thousand customers were stranded. Some people may have tried more than once; others may have succeeded later. The presenter quietly changed the count from attempts to people.",
        "exercise": "Write one sentence giving a total and saying what it counts. Add three sentences describing one case, then return to what the total tells you. Say whether you observed the case, summarized someone's account or made it up. State whether you know how closely it resembles other cases.",
        "self_check": "Are you counting the same thing throughout, such as people or attempts? Does the case explain how a problem happens? Does the total show how many cases there are? Have you claimed that one experience is typical without evidence?"
    },
    "institution_system_and_policy": {
        "title": "Explain what this group can do within the larger system",
        "problem": "A presentation about a large problem ends with everyone needing to do something. The audience leaves with urgency but no clear authority, contribution or division of responsibility.",
        "principle": "Ask the group for something it can decide or do. Name the people, funding or permission needed from others, and say who remains responsible for each part. For example, a business may offer space while a public body decides eligibility. Explain how the roles fit together. One story of cooperation does not show that a whole program works.",
        "source_title": "Shakira: business capabilities, government responsibility and a local partnership account",
        "source_writeup": "writeups/full-context-address-65.md",
        "source_passages": "Caption numbers 45–54: business capabilities and government qualification; 55–73: the local program and reported partnership; 74–76: the action list. Caption numbers are not playback seconds.",
        "source_reading": [
            "The question of what listeners can do is answered with capabilities attributed to the business audience: strategy, assets, staff and organizational capacity. The audience is not merely asked to care. It is addressed as a group with resources and particular kinds of work it could undertake.",
            "The suggestion to act where government leaves gaps is qualified immediately: government should be reengaged rather than excused from responsibility. The later school-building account includes government as a strategic partner. Removing those sentences would turn a shared-responsibility argument into a replacement argument the transcript does not support.",
            "The local account combines schooling, early development, feeding and training, followed by claims about progress. Those bundled components prevent this reading from isolating the effect of any one intervention. The closing policy requests remain proposals rather than verified implementation. The useful speaking choice is the visible allocation of roles, not a demonstrated policy formula."
        ],
        "transfer": "List what must happen for the proposal to work. Beside each task, name who can approve it, who will do it and what they need. Use that list to write the request for this audience. If an essential decision belongs to someone outside the room, say who must be consulted before the plan can proceed.",
        "worked_title": "Requesting a cross-team pilot for faster application responses",
        "before": "We all need to take ownership and fix the application experience.",
        "after": "In this hypothetical organization, the product team can redesign the status page, but it cannot decide eligibility or promise response dates on behalf of the review team. I am asking product to prototype a page that shows the current stage, review operations to define the stage labels and an owner from each team to check the handoff weekly during a pilot. Policy changes remain with the policy group. Today's request is permission to test clearer status information, not a promise of faster decisions.",
        "worked_explanation": "The request assigns work according to authority and distinguishes communication improvements from decision speed. The dependencies remain visible. The speaker has a limited next step to propose without pretending that the audience controls the whole system.",
        "variations": [
            "For a single-team meeting, state the team's contribution and the external decision it depends on. Do not assign another team a deadline without its agreement.",
            "For a partnership proposal, distinguish who contributes resources, who delivers the service, who makes decisions and who remains accountable. These roles may belong to different parties.",
            "For a public address, give listeners an action within their actual role and name the institutional duty that remains. Individual goodwill should not be presented as a substitute for obligations held by an organization."
        ],
        "failure_case": "Example of what can go wrong: a speaker asks frontline staff to eliminate waiting times when they cannot change staffing, eligibility rules or appointment capacity. The appeal converts a system constraint into a personal demand. Another failure is praising collaboration while leaving every critical decision owner unnamed.",
        "exercise": "Choose a recommendation and write four lines: this audience can decide; this audience can contribute; these partners must agree; this responsibility remains elsewhere. Use those lines to draft a one-minute request with one explicit next handoff.",
        "self_check": "Can this audience approve the action? Have you named the help or permission needed from others? Is it clear who remains responsible for each task? Does the wording treat the result as a proposal to test rather than a guarantee?"
    }
})

LESSONS.update({
    "definition_and_explanation": {
        "title": "Define key words with a clear example",
        "problem": "Everyone uses the same term, but their examples point to different things. A presentation about empowerment, readiness or quality can sound agreeable while leaving the actual decision undefined.",
        "principle": "Say what a word means in this discussion. Give an example that fits and a similar example that does not. If ‘complete’ means the draft has been reviewed and approved, a draft that has merely been submitted is still unfinished. The definition tells listeners how you are using the word; you still need evidence before saying the work meets it.",
        "source_title": "Jennifer Aniston: defining power through a use of one's voice",
        "source_writeup": "writeups/full-context-address-68.md",
        "source_passages": "Caption numbers 8–20: power, strength and the use of a voice; 21–30: childhood exclusion; 80–86: participation, questions and shared power. These references are caption positions rather than playback seconds.",
        "source_reading": [
            "The address connects power with using a voice to support and connect people. It also distinguishes feeling strong from thinking of oneself as powerful. That distinction separates an internal description from a proposed relational use: what a person does with the opportunity to speak.",
            "The childhood dinner account supplies a concrete opposing case, in which a child's contribution is dismissed. The later table callback gives participation a more inclusive interpretation. These episodes help explain the speaker's chosen meaning of power; they are not independent proof of every contribution attributed to her platform.",
            "The closing redirects recognition toward the organization and shared power. The address therefore gives the definition consequences within its own argument. This is a personal and ethical framing, not a neutral classification that exhausts political, organizational or other meanings of power. A lesson should identify that scope instead of presenting the definition as settled fact."
        ],
        "transfer": "Find a word that listeners must understand to judge your recommendation. Write what it means here, one example that fits and one similar example that does not. Choose a difference someone could check. If the audience already uses a formal definition, state it and explain any more limited meaning you need for this discussion.",
        "worked_title": "Defining ready in a project handoff",
        "before": "We will send the work over when it is ready. Everyone should maintain a high standard of readiness.",
        "after": "For this invented handoff, ready means the next team can start its review: the draft is attached, unresolved questions are marked and a contact is named. It does not mean the draft is approved for publication. A polished file without its open questions is not ready for this handoff; a rougher file with the necessary review context may be. These standards are our proposed working agreement for the pilot.",
        "worked_explanation": "The definition changes how cases would be classified. It distinguishes readiness for review from readiness to publish and gives a near miss that exposes the difference. Calling the agreement proposed prevents the presenter from implying that everyone has already accepted it.",
        "variations": [
            "For a technical presentation, pair the definition with an input, an output or a test case. Avoid using three equally unfamiliar terms to explain the first.",
            "For a strategy discussion, identify which decision the definition serves. A broad aspiration such as quality may need separate working meanings for reliability, usability and editorial accuracy.",
            "For a mixed audience, invite a counterexample before proceeding. A disagreement about the definition is useful to surface before it becomes a disagreement about the recommendation."
        ],
        "failure_case": "Example of what can go wrong: a presenter defines collaboration as acting collaboratively and supplies only a photograph of smiling colleagues. Neither helps distinguish shared decision-making from people attending the same meeting. Another failure defines success so narrowly that every disappointing result is excluded by definition.",
        "exercise": "Complete three sentences: here, this term means; a concrete example is; a nearby thing it does not mean is. Test your definition against one awkward case and revise it if it cannot guide a decision.",
        "self_check": "Could two readers use your definition to agree whether an example fits? Is it clear where the definition applies? If you say your work meets it, have you shown the evidence?"
    },
    "question_redefinition": {
        "title": "Explain the question before answering it",
        "problem": "A question seems impossible or contradictory because a key term carries a meaning different from the one your argument uses. Answering immediately may concede an assumption you do not share.",
        "principle": "Check whether a word in the question has more than one meaning. State the meaning you are using, then answer the concern. For example, ‘finished’ could mean drafted or approved; those meanings lead to different answers about whether work is ready. Explain the difference openly. Do not quietly change a word's meaning to make a difficult question disappear.",
        "source_title": "The Vivekananda-labeled composite text: a book objection answered through a different account of Vedas",
        "source_writeup": "writeups/full-context-historical-01.md",
        "source_passages": "Caption numbers 35–51: the organizing question; 52–77: the term redefinition and gravity analogy. The available upload combines historical texts; these positions do not establish one continuous original speech, an original voice or playback timing.",
        "source_reading": [
            "The passage in the transcript anticipates an objection about a timeless book. Its response presents Vedas as accumulated spiritual laws rather than treating the objection solely as a question about a physical book's beginning. The change of meaning alters what would count as an answer.",
            "A gravity analogy accompanies the explanation. Within the argument, it helps distinguish the discovery or articulation of a law from the law's proposed existence. That analogy explains the kind of distinction being asserted; it does not verify the theological claim or make it equivalent to an established scientific law.",
            "This source requires unusually explicit attribution. The local review identifies a composite of historical texts and damaged captions, not a verified recording of the historical speaker. The lesson concerns the argument in the transcript's structure. It does not infer timing, confidence, audience agreement or a seamless transition from the upload."
        ],
        "transfer": "Write the question and circle the word that could have two meanings. State both meanings, say which one you are answering and give the answer. Check whether the other meaning raises a question you still owe an answer to. Keep any agreed or formal definition clear; do not change it to make your claim easier to defend.",
        "worked_title": "Answering whether a process can be standardized without identical steps",
        "before": "That is the wrong question. You misunderstand what standardization means.",
        "after": "In this hypothetical discussion, you are asking how we can call the process standardized if teams use different tools. By standardized here, I mean the same required handoff information, not identical software. Each team must supply a decision, an owner and unresolved questions. That answers the information-consistency question. It does not answer whether our different tools create unnecessary maintenance costs; we should examine that separately.",
        "worked_explanation": "The answer identifies the disputed meaning without treating the questioner as foolish. It preserves the remaining cost concern instead of using the narrower definition to declare the whole challenge resolved. The redefinition clarifies one claim and leaves another open.",
        "variations": [
            "For a product discussion, distinguish available, enabled and usable if a question conflates them. Explain the actual state rather than choosing the label that sounds most favorable.",
            "For a research talk, identify whether a question concerns a model's internal definition or an observable real-world property. A result about the former may not answer the latter.",
            "For a short answer, use one sentence for the distinction and one for the direct response. A long terminology lecture can bury the concern that prompted it."
        ],
        "failure_case": "Example of what can go wrong: asked why a promised delivery is late, a presenter redefines delivery to mean work has begun. The original commitment concerned receipt, so the new meaning evades the question. Legitimate clarification must not rewrite an inconvenient promise after the fact.",
        "exercise": "Choose a question with a word that could mean two different things. Write an answer for each meaning. Say which meaning you intended in your original claim, then answer any concern raised by the other meaning.",
        "self_check": "Does the word really have more than one meaning in this discussion? Have you explained which one you are using? Did you answer the concern and keep any promise you made under the earlier meaning?"
    },
    "evidence_gap": {
        "title": "Show where the explanation stops short of proof",
        "problem": "A comparison makes a claim feel understandable, and the presentation begins treating that feeling as verification. The audience may follow the analogy while the decisive factual step remains unsupported.",
        "principle": "Say exactly which part of the explanation still needs evidence. An example may show what could happen; a description may explain how it could happen. Neither alone shows that it did happen. Name the missing observation: for example, did people who used the revised instructions finish the task? This gives the audience a specific question to investigate.",
        "source_title": "The Vivekananda-labeled composite text: familiar-language recall and the claim about past lives",
        "source_writeup": "writeups/full-context-historical-01.md",
        "source_passages": "Caption numbers 184–208: the memory objection and familiar-language analogy; 209–256: a separate question whose answer retains an explicit unknown. The source is a composite text with caption damage, not verified original audio; ordinals are not timestamps.",
        "source_reading": [
            "The memory objection is answered with a comparison involving access to a familiar language. The comparison offers a way to think about something learned but not currently in awareness. That is the explanatory role visible in the argument in the transcript.",
            "The further claim concerns access to past lives. Showing that people can recall a language already learned does not independently establish that different claim. The missing bridge is not merely another vivid example of ordinary memory; it is evidence bearing on the proposed past-life access itself. The local review supplies no such demonstration.",
            "A later question about a perfect soul and an imperfect body retains an admission of not knowing. It also criticizes labels that only rename a difficulty. This gives a second, distinct lesson in the same source: identifying a phenomenon or giving it a name should not be mistaken for explaining how it occurs. These observations analyze an argument respectfully without treating religious conviction as measured science."
        ],
        "transfer": "For each important claim, ask what the evidence directly shows and what extra step your conclusion requires. Write the missing step in ordinary language. Decide whether to gather evidence, narrow the claim or present it explicitly as a proposal. Preserve the useful explanation while withdrawing any certainty it cannot support.",
        "worked_title": "Presenting a prototype without claiming an established time saving",
        "before": "The prototype worked in our demo, so it will save every team hours each week.",
        "after": "In this invented example, the demo shows that the prototype can complete one prepared workflow. It does not tell us how often teams encounter that workflow, how much correction is needed on ordinary inputs or whether setup time exceeds the saving. Our next test should use representative tasks and record total time, including corrections. Until then, we can claim a demonstrated path through the prototype, not a weekly saving for every team.",
        "worked_explanation": "The revision does not dismiss the demo. It assigns it a defensible role and names the observations needed for the broader claim. The proposed measurement follows from the gap rather than serving as a generic request for more validation.",
        "variations": [
            "For an executive briefing, place the supported result and unresolved inference next to each other. Separate the decision justified now from a larger decision that depends on the missing evidence.",
            "For a teaching analogy, say which relationship it illustrates and which real-world properties it leaves untested. A familiar example can aid explanation without carrying the burden of proof.",
            "For an early-stage proposal, label assumptions before calculating projections. Precise arithmetic does not make assumed inputs observed facts."
        ],
        "failure_case": "Example of what can go wrong: a presenter admits that a pilot is small but still describes its outcome as guaranteed at company scale. The disclaimer has not changed the claim. Another failure responds to a specific missing comparison by adding unrelated testimonials.",
        "exercise": "Draw a line from your evidence to your conclusion. Write every assumption needed to cross it. Choose the weakest assumption and name one observation that could support or challenge it. Rewrite the current claim without silently depending on that assumption.",
        "self_check": "What does the evidence show directly? What are you still assuming? Would your proposed check tell you whether that assumption is correct? Does the recommendation reflect what you know and what you still need to find out?"
    },
    "optional_support": {
        "title": "Offer help without requiring people to take it",
        "problem": "A tool or technique that helps some people is presented as something everyone must use. The aid becomes a ritual, and the underlying task disappears behind compliance with the method.",
        "principle": "Explain what the help is for and who might find it useful. Say whether people must use it or can choose another way. For example, a worksheet may help someone prepare without being required for participation. If you call something optional, make sure declining it does not quietly prevent people from taking part.",
        "source_title": "The Vivekananda-labeled composite text: images as aids, with an explicit noncompulsion qualification",
        "source_writeup": "writeups/full-context-historical-01.md",
        "source_passages": "Caption numbers 468–499: symbolic practices and aids to attention; 500–534: stages, the garment comparison and supports not required for everyone. The upload is a composite, and these are caption positions, not verified original delivery or timestamps.",
        "source_reading": [
            "The argument in the transcript defends material images by comparing symbolic practices across traditions and presenting images as aids to attention. The focus is the job the support is said to do, rather than the bare presence of an object.",
            "The following passage uses stages and a one-size-garment contrast, then explicitly states that these supports are not needed or compulsory for everyone. That qualification prevents a defense of one practice from automatically becoming a universal instruction to adopt it.",
            "The broader source also contains hierarchical language and tensions that should not be erased by a modern summary of inclusion. This lesson borrows the distinction between an aid and a requirement. It does not endorse ranking people by their practices or claim empirical proof of the support's effects."
        ],
        "transfer": "When introducing a template, checklist or rehearsal exercise, explain what problem it is intended to address. State what the person must accomplish and which other routes are acceptable. If the aid is actually mandatory for a necessary shared process, say that plainly and explain the reason rather than calling it optional.",
        "worked_title": "Introducing speaker notes in a presentation workshop",
        "before": "Good presenters use this exact note template. Fill every box before you can give your talk.",
        "after": "For this hypothetical workshop, the note template is available if it helps you keep the example, point and next step together. You may instead use an outline or your own notes. The shared requirement is that your practice talk makes those three elements identifiable. We will check the talk against that requirement, not score whether you filled the template. If the template makes your drafting harder, choose another route and tell us where the support failed.",
        "worked_explanation": "The revision states the template's intended function and moves assessment to the communication task. Its alternatives are explicit. It also creates a route for reporting a poor fit rather than treating difficulty with the aid as a deficit in the learner.",
        "variations": [
            "For a team workflow, distinguish optional drafting aids from required handoff information. People can work differently while still supplying what colleagues need.",
            "For a training session, introduce one aid at a time and explain its purpose. A large kit of supposedly optional tools can still feel compulsory if every demonstration assumes their use.",
            "For an accessibility support, avoid requiring someone to disclose private circumstances to choose an available alternative. Explain the choices without treating one as evidence of inferior ability."
        ],
        "failure_case": "Example of what can go wrong: a facilitator calls a worksheet optional but refuses feedback until it is complete. The process contradicts the presentation. Another failure makes essential safety or shared-format requirements sound optional when people must actually follow them.",
        "exercise": "Choose one tool you recommend. Write its intended job, a situation where it may help, a situation where it may hinder and an acceptable alternative. Then inspect the assessment or workflow to see whether declining the tool has a hidden penalty.",
        "self_check": "Can someone decline the tool and still take part? Can they tell what they must complete and which methods they may choose? Do the alternatives work in practice? If everyone must use the same tool, have you said so and explained why?"
    }
})

LESSONS.update({
    "humor_rapport_and_self_undercut": {
        "title": "Use brief humor, then return to the point",
        "problem": "You want a lighter moment before discussing a shared habit, but a joke about the audience can put you above the people you need to work with. The humor may also distract from the actual point.",
        "principle": "If you joke about a shared habit, include your own part in it. A speaker discussing confusing file names might admit to creating ‘Final Really Final.’ Then return to the naming problem the group needs to solve. Decide whether the joke fits the people and occasion; including yourself does not guarantee that others will find it funny.",
        "source_title": "Mindy Kaling: literal house names and the titles of her own shows",
        "source_writeup": "writeups/full-context-address-71.md",
        "source_passages": "Caption numbers 0–26: local references and comic exaggeration; 98–118: literal house names and the return to the speaker's own show titles. These are caption positions; laughter, delivery and audience agreement were not measured.",
        "source_reading": [
            "The opening uses alumni, regional and campus references to situate the address in a particular community. Its exaggerations are comic material, not factual reports about paid laughter, the weather or a medical procedure. A literal summary would distort the opening's function.",
            "Later, the speaker jokes about literal house names and then connects that criticism to the literal titles of her own shows. The same standard now applies to the teller. The turn changes the joke's direction: it is no longer only an outsider judging a local habit.",
            "The transcript makes that self-inclusion observable. It does not tell us whether the joke landed, how long a pause lasted or whether all listeners shared the references. This chapter addresses the broader relationship choice. The more specific self-undercut structure concerns reversing a claim about the speaker's own status, which need not begin with a joke about a shared habit."
        ],
        "transfer": "Choose a low-stakes behavior you genuinely share. Make the mismatch concrete, keep the joke brief and connect it to the next point. Avoid borrowing a comedian's personal references or treating disclosure of a serious mistake as a punchline. If the observation only works by making another group look foolish, find a different opening.",
        "worked_title": "Opening a meeting about clearer internal names",
        "before": "Other teams keep inventing ridiculous names. Nobody can understand what they are talking about.",
        "after": "In this invented opening: we named a folder Final, then added Final Two, and finally Final Really Final. I helped name the third one, so my campaign for clarity has a complicated origin. Today I want us to agree on one simple rule: the name should tell a new colleague what is inside and which version to use.",
        "worked_explanation": "The speaker participates in the naming problem and the joke points directly to the meeting's purpose. The proposed rule can stand without the joke, which matters if the room does not respond. This is a written teaching example, not a tested comic script.",
        "variations": [
            "For colleagues who know you, a small shared inconvenience may be enough. Check that your account does not expose a person's mistake or turn an unresolved conflict into entertainment.",
            "For an unfamiliar audience, explain the setting in ordinary language. A reference that requires institutional history can make belonging feel conditional on already being an insider.",
            "For a sensitive or high-stakes topic, omit the joke if it could trivialize the harm. Warmth can come from clarity, attention and respectful acknowledgment without a comic opening."
        ],
        "failure_case": "Example of what can go wrong: a manager jokes that everyone is bad at planning, including them, while only junior staff face penalties for delays. Self-inclusion in the wording does not equalize the consequences. Another failure repeats the joke after no response, making the audience responsible for reassuring the speaker.",
        "exercise": "Write a one-sentence observation about a harmless habit you share, one sentence that includes your own participation and one sentence connecting it to the actual topic. Remove the first two sentences and check that the presentation still makes sense.",
        "self_check": "Who is the joke's target? Are the consequences low-stakes for them? Is your participation genuine? Can you proceed naturally if nobody laughs, without explaining why they should have?"
    },
    "metric_revaluation": {
        "title": "Treat a milestone as progress, not completion",
        "problem": "A celebration turns a useful count into a finish line. After congratulating the team, you still need to explain what the number leaves unfinished without making the achievement seem meaningless.",
        "principle": "Keep the number, but explain what it does and does not show. Say what work it records, then name what remains to be done. The number may still be useful; it just does not prove that the whole job is finished. Recognize the work already done before describing what comes next.",
        "source_title": "Aishwarya Rai Bachchan: surgery totals return as motivation rather than a cap",
        "source_writeup": "writeups/full-context-address-73.md",
        "source_passages": "Caption numbers 0–10: the reported milestone and wordplay; 84–87: the figures as motivation; 88–91: rejection of a cap on future work. Caption numbers are not playback times; the totals and medical outcomes are not independently verified here.",
        "source_reading": [
            "The address opens by celebrating a reported 500,000 cleft surgeries over eighteen years. The source uses that count to establish an occasion for recognition. The count is not automatically a unique-patient total, a description of sustained benefit or evidence that every need has been met.",
            "Near the end, the years and totals return as sources of inspiration and motivation. The next passage calls them merely numbers and rejects a limit on future work. Read together, the passages change what the count authorizes: recognition of progress, not permission to stop.",
            "Summarizing this as numbers do not matter would discard the very milestone around which the address is organized. The more precise reading preserves two claims at once: the contribution merits acknowledgment, and the mission extends beyond this total. The transcript does not show whether that closing led to continued action."
        ],
        "transfer": "When closing a project phase or celebrating a target, name the unit and the completed work accurately. Then state the next need in its own terms. If the original milestone was genuinely the agreed endpoint, do not quietly convert celebration into an unapproved extension of people's commitments; present new work as a new decision.",
        "worked_title": "Celebrating a community archive's digitization milestone",
        "before": "We have scanned ten thousand pages. The archive is now accessible to everyone.",
        "after": "In this fictional archive project, ten thousand scanned pages mark a real achievement by our volunteers. They do not mean the collection is fully usable: some scans still need descriptive records, and readers need a way to find what they contain. Let us celebrate the scanning milestone and decide separately how to staff the next phase of cataloging. The completed count matters; it is not a measure of every reader's access.",
        "worked_explanation": "The revision recognizes the achievement without claiming that everyone can use the archive. It names the remaining work and makes staffing it a separate decision. The next phase is not treated as an automatic, unlimited demand on volunteers.",
        "variations": [
            "For a project retrospective, distinguish the agreed delivery target from continuing maintenance. Completing the first can be true even when the second remains necessary.",
            "For a fundraising report, say what was counted and what remains to be done. Do not imply that the milestone proves a result for every person receiving help.",
            "For a team celebration, give recognition enough space to be heard before discussing the next phase. An immediate expansion of the target can make every achievement feel provisional."
        ],
        "failure_case": "Example of what can go wrong: after staff meet a target, a leader says numbers are meaningless and doubles the requirement without discussion. That is changing the rules after the work is done, not explaining what the number means. Another failure uses a count of activities as proof of a result, even after admitting that the two are different.",
        "exercise": "Write a three-part closing: what this milestone proves we completed; what it does not establish; what decision about the next phase is now needed. Underline the sentence that gives genuine credit for the completed work.",
        "self_check": "Is the number's legitimate meaning preserved? Is the unfinished work specific? Have you separated completion of an agreed commitment from a proposal to take on more?"
    },
    "hands_off": {
        "title": "Say who should take the next step",
        "problem": "A presentation ends with a moving account of one person's work, but the next participants do not know what they can carry forward or how responsibility will pass to them.",
        "principle": "When work passes to someone else, say who will act next, what they need and which decisions they can make. Explain who will still help or remain responsible, and how to raise a problem. Check that the next person has agreed to the work. Naming them in a presentation does not mean they have accepted it.",
        "source_title": "Manushi Chhillar: a local project expands through partners and shared credit",
        "source_writeup": "writeups/full-context-address-119.md",
        "source_passages": "Caption numbers 120–149: the described local supply and participation chain; 150–195: teams, communities, organizations and wider ownership. The source's catalog label is hands_off; the lesson treats it as a platform handoff, not withdrawal of responsibility. Ordinals are not playback seconds.",
        "source_reading": [
            "The address describes an idea developing through family-supported awareness sessions and a wider local program. Women sourcing and selling sanitary pads, social barriers at the point of purchase and affordability concerns give the account a chain of actors and constraints. The review does not establish the program's safety, affordability, continued use or effects.",
            "The later passage distributes credit across teams, young women, students, local communities, organizations and public officials. This expands the account beyond the speaker's personal platform. The named roles suggest a wider network carrying the work rather than a solitary achiever acting everywhere.",
            "The closing imagines a condition in which the empowerment label would no longer be needed. That vision can orient a handoff, but it does not prove shared decision-making or specify every practical responsibility. The practical approach below makes ownership explicit as an adaptation; it is not a claim that every element already appears in the speech."
        ],
        "transfer": "At the end of an update or proposal, distinguish people you are thanking from people you are asking to act. For each proposed transfer, state the next action, its resources and the acceptance step. Keep unresolved risks and support needs visible. A handoff is complete only when the receiving party has the information and authority it needs, not when the speaker finishes talking.",
        "worked_title": "Handing a neighborhood event plan to volunteer leads",
        "before": "This event belongs to all of us now. Please take ownership and make it happen.",
        "after": "For this invented event plan, I am asking two volunteers to consider leading the welcome desk. The role covers a two-hour shift, the sign-in sheet and directing questions to the event coordinator. I will provide the briefing and remain responsible for unresolved scheduling issues. Please confirm by Friday whether the role and support are workable; until someone accepts, the desk remains unassigned. We are sharing a defined task, not transferring every event problem to the next person.",
        "worked_explanation": "The request specifies work, duration, support and acceptance. It names what does not transfer. The public statement cannot manufacture consent, so the role remains explicitly unfilled until someone agrees.",
        "variations": [
            "For a project transition, include the current state, pending decisions and known risks alongside the files. Access to a folder is not the same as understanding what must happen next.",
            "For a community initiative, agree roles with participants before presenting them as owners. Public recognition should not impose duties they did not choose.",
            "For a senior leader's closing, identify the next decision owner and the support the leader still owes. Delegation is incomplete if responsibility moves but authority and resources do not."
        ],
        "failure_case": "Example of what can go wrong: a presenter announces that local volunteers will maintain a service indefinitely, though nobody has asked them or funded the work. Naming a group does not create capacity or consent. Another failure hands over a plan without disclosing an unresolved dependency that blocks the first action.",
        "exercise": "Draft a handoff in five lines: who acts next, what they do, what resources they have, who remains responsible and how to check that the handoff is complete. Ask which missing line would stop the next person from starting.",
        "self_check": "Is this an accepted transfer or only a request? Can the receiver act with the authority and resources supplied? Is continuing responsibility clear, and is there a route to raise a problem after the presentation ends?"
    }
})

LESSONS.update({
    "self_undercut": {
        "title": "Show your experience without claiming to be always right",
        "problem": "An introduction needs to show why you are worth hearing, but a list of achievements can make it sound as if your status makes your advice always right. Empty self-deprecation creates the opposite problem: the audience cannot tell what you know how to do.",
        "principle": "Name a limit, exception or mistake right beside a claim about yourself. This keeps the useful experience while correcting an inflated impression. The contrast can be funny, but it should not hide real skill or turn into a joke about a habit everyone shares.",
        "source_title": "Mindy Kaling: an alumni-success boast immediately meets an exception",
        "source_writeup": "writeups/full-context-address-71.md",
        "source_passages": "Caption numbers 27–48: career introduction, audience recognition and the Shonda Rhimes exception. These are caption positions, not playback seconds; actual laughter or changes in perceived status were not measured.",
        "source_reading": [
            "The identity introduction combines career credentials with jokes about representation and recognition. The speaker needs to establish a relationship with the graduating audience, but the wording does not maintain a uniformly elevated account of her own standing.",
            "A claim to singular alumni success is immediately undercut by the reference to Shonda Rhimes. The exception belongs beside the boast. Quoting or summarizing only the initial claim would turn a locally reversed comic move into a straightforward assertion of superiority.",
            "The sequence does not erase the speaker's career or supply evidence that modesty improves persuasion. It shows an introduction allowing its own inflated claim to be revised. The timing visible here is textual adjacency, not an inspected pause or measured comic beat."
        ],
        "transfer": "State the experience that qualifies you to address the topic, then remove a specific implication that would go too far. For example, practical experience with one setting does not make you an authority on every setting. Let the limit sharpen the contribution you can make. Do not invent an exaggerated credential merely to manufacture a charming correction.",
        "worked_title": "Introducing a guest session on running a small museum exhibition",
        "before": "I have curated several successful exhibitions, so I can show you the formula for a great exhibition.",
        "after": "For this invented guest introduction: I have helped run three small exhibitions, which gives me three sets of mistakes to organize into slides. More usefully, it gives me experience with limited space, borrowed objects and volunteer staffing. I can show you the planning decisions we faced in that setting. I cannot give you a formula for every museum or predict what your visitors will value.",
        "worked_explanation": "The light opening narrows the authority claim rather than removing it. The concrete experience remains useful, and the final boundary identifies where the advice stops. The count and background are part of a hypothetical teaching script, not a claim about an actual curator.",
        "variations": [
            "For a specialist audience, omit the joke if a direct scope statement is clearer. Name the cases you know and the cases outside your experience.",
            "For a ceremonial address, a brief exception to a status claim can sit naturally in the introduction. Avoid a long inventory of flaws that asks listeners to provide reassurance.",
            "For a speaker whose competence is routinely questioned, accurate authority may need no comic reduction. This structure is an option, not a requirement to make expertise more acceptable."
        ],
        "failure_case": "Example of what can go wrong: a qualified instructor repeatedly says they know nothing, then asks the audience to follow a complex method. The introduction makes the basis for trust unclear. Another failure disguises a further boast as a flaw, such as claiming that the only problem is caring too much.",
        "exercise": "Write three lines: the experience you bring, what that experience does not qualify you to claim and what you can help explain today. Try a direct introduction before adding humor. Keep the version that makes your experience and its limits clearest.",
        "self_check": "Can listeners still tell what you know? Is the limit accurate and specific? Does the introduction help them judge your contribution, or does it ask them to reassure you?"
    },
    "expectation_reversal": {
        "title": "Say what you expected before describing what happened",
        "problem": "A story announces a surprising outcome, but the audience never understood what the person expected or why. The surprise is then a fact without a useful change in interpretation.",
        "principle": "Say what you expected before revealing what happened. Then explain why the difference changed your view of the original action. If a quick reply was meant to help but left someone confused, show what you had overlooked. That makes the surprise relevant to your point. One surprise still cannot tell you how often the same problem occurs.",
        "source_title": "Jeff Bezos: anticipated praise gives way to a grandmother's tears",
        "source_writeup": "writeups/full-context-address-72.md",
        "source_passages": "Caption numbers 0–25: calculating and the recalled smoking advertisement; 26–43: expected praise, tears and uncertainty; 44–51: the revised standard. Ordinals identify transcript positions, not verified media times.",
        "source_reading": [
            "The childhood setup makes the expectation intelligible: the child likes calculating and works out a precise-sounding estimate using a remembered smoking advertisement. The source preserves uncertainty about the advertisement, and the calculation is not a valid individual lifespan estimate. Its role in the story is to make the child's anticipated achievement visible.",
            "The child expects praise for cleverness but reports the grandmother crying instead. That reaction creates the reversal. The following uncertainty about what the grandfather will do gives the unexplained outcome a place in the narrative before the interpretation arrives.",
            "The kindness-versus-cleverness distinction revises the standard by which the action is judged. This chapter isolates the expectation-and-outcome hinge. The broader scene lesson concerns building a concrete event around a decision standard; the story-to-thesis pattern concerns carrying the resulting interpretation into a larger argument. One passage can contain all three without making them identical."
        ],
        "transfer": "Choose an incident where your own prediction was wrong and the correction matters to the audience's decision. State the prediction and its reason before the result. Explain the changed understanding without adding reactions you did not observe or know. If the event is private, use a permitted account or clearly label a hypothetical example.",
        "worked_title": "Explaining why a workshop activity needed revision",
        "before": "Our new activity did not work as expected, so we made it better.",
        "after": "In this hypothetical workshop, I expected a blank worksheet to encourage original ideas because it imposed no categories. Instead, the first question was where to start. The freedom I had designed was also an absence of orientation. For the next session, I would keep the open space but add one optional example and a clear first prompt. That change addresses the obstacle in this scene; it still needs to be tried with participants.",
        "worked_explanation": "The original design has a reasonable purpose, so its failure is informative rather than merely foolish. The reaction reveals a missing condition, and the proposed revision preserves the purpose while addressing that condition. No learner result is invented for the untested revision.",
        "variations": [
            "For a project retrospective, state what information made the initial prediction reasonable. Hindsight that makes every failed choice look obviously foolish teaches little about decision-making.",
            "For a personal story, keep the other person's reaction within what you actually know. A visible action is not permission to invent their entire inner experience.",
            "For a demonstration, reveal the expected result before running the example, but disclose any staging. A constructed surprise is a teaching device, not a naturally observed failure."
        ],
        "failure_case": "Example of what can go wrong: a presenter withholds a known constraint and then reveals it as a surprise that makes a colleague's decision look absurd. The reversal depends on unfair narration. Another failure jumps from one unexpected reaction to a claim that an entire audience segment behaves that way.",
        "exercise": "Complete four sentences: ‘I expected ____. I expected that because ____. Instead, ____. Now I would check ____.’ Read the first three aloud. Can a listener explain why the result surprised you? If not, add the missing detail about what you expected.",
        "self_check": "Was the original prediction clear before the reversal? Is the outcome described accurately? Does the new interpretation follow? Have you avoided using one event to make a claim about a whole group?"
    },
    "audience_invitation_and_next_turn": {
        "title": "Return the question to the people who can act on it",
        "problem": "Your presentation ends at the speaker's conclusion. The audience knows what you believe but not what to consider, decide or do next in its own circumstances.",
        "principle": "Tell listeners what response you are asking for: a question, a discussion, a decision or a small action. Address the people who can give that response and leave room for disagreement or refusal. Asking someone to comment does not assign them the work. Check what they actually agree to before describing the next step as settled.",
        "source_title": "Mindy Kaling: a personal possibility question becomes a question for graduates",
        "source_writeup": "writeups/full-context-address-71.md",
        "source_passages": "Caption numbers 253–261: permission to revise plans with a planning qualification; 264–274: the recurring personal question turned toward graduates. These are caption positions, not playback times or verified audience response.",
        "source_reading": [
            "Before the close, the address permits changes to a planned order of life events while retaining the possibility that structured ambition can motivate. That context matters: the invitation does not require abandoning every plan or treating uncertainty as inherently preferable.",
            "The speaker then recalls a question about whether she could have such a life and turns the question toward the graduates. The change in addressee shifts the immediate work from following an autobiography to considering one's own possibilities. The audience is now grammatically inside the question.",
            "The invitation does not demonstrate equal opportunity, remove material barriers or guarantee that belief will produce a similar life. Its observable achievement is structural: the ending gives listeners a question to carry away. Whether they considered it, found it useful or acted remains outside this transcript reading."
        ],
        "transfer": "Choose the next turn before writing the ending. Ask whether the audience should think, speak, decide or act. Give enough specificity that the request can be understood and enough freedom that disagreement or nonparticipation remains possible. If a response needs time, information or a later channel, provide it.",
        "worked_title": "Closing a public workshop on family photographs",
        "before": "Photographs connect us to the past. I hope you leave inspired to preserve your memories.",
        "after": "For this invented workshop closing: choose one photograph you would like someone else to understand. What name, place or story would be lost if you were not there to explain it? If you want to try the exercise, write that context on a separate note tonight; do not write on the photograph itself. You may keep the note private. At our next session, we can discuss what made the context difficult to recover.",
        "worked_explanation": "The closing gives the listener a specific question, a small optional task and a future discussion route. It does not require public disclosure of family information or imply that every photograph has a recoverable story. The request follows directly from the workshop's subject.",
        "variations": [
            "For a decision meeting, state exactly what decision is requested and distinguish assent from a request for more evidence. Silence should not be treated as consent.",
            "For a reflective address, offer one question with enough room for a personal answer. Several rhetorical questions in succession may leave no clear next task.",
            "For a training session, give a short activity and a way to decline or adapt it. Public speaking, personal disclosure or physical participation should not be smuggled into a seemingly simple invitation."
        ],
        "failure_case": "Example of what can go wrong: a speaker asks what everyone will change tomorrow, then immediately supplies the only acceptable answer and moves on. The question performs openness without allowing a turn. Another failure requests a major commitment from people who have neither authority nor the information needed to make it.",
        "exercise": "Write three alternative endings to the same presentation: a reflection question, a discussion prompt and an action request. Choose the one that matches your purpose. Add the information, time or channel needed to make that next turn possible.",
        "self_check": "Can a listener say what you are asking them to do? Do they have the time, information and authority to respond? Can they disagree or decline? Have you kept the request separate from any claim that people have already accepted it?"
    }
})

LESSONS.update({
    "premise_correction": {
        "title": "Correct the assumption before supplying the detail",
        "problem": "A question asks for details of something that did not happen or a practice you do not follow. Answering inside that frame would quietly confirm the mistaken premise.",
        "principle": "When a question assumes something that did not happen, correct that fact before explaining anything else. If asked why a project was canceled when it was delayed, say so, then explain the delay. Answer the reasonable concern behind the question. A mistaken assumption does not by itself mean the person is trying to mislead anyone.",
        "source_title": "Taylor Swift: an assumed guitar-naming practice replaced by acquisition stories",
        "source_writeup": "writeups/full-context-interview-27.md",
        "source_passages": "Caption numbers 508–547: the host's guitar-naming assumption, its denial and replacement stories. Caption positions are not playback times; the local reading does not verify the reported biographical details.",
        "source_reading": [
            "The host introduces a question assuming that Swift names guitars. The answer explicitly denies that practice. The denial must remain attached to the exchange; extracting the question as though it described an established habit would reverse the evidence.",
            "Acquisition memories and a do-it-yourself decoration story then supply other material about the instruments. The reply therefore does more than reject the premise. It continues the broader subject while refusing the particular assumption that would make a literal answer inaccurate.",
            "This is not the same as the interview's music-versus-lyrics reframe. There, the answer changes the organizing account of composition. Here, a specific attributed behavior is denied. The transcript supports that distinction without proving whether the host felt corrected gracefully or whether listeners remembered the denial."
        ],
        "transfer": "Write down the fact the question assumes. Check whether you know it is true. If it is false, begin with the correction, then answer the concern the question raises. If you do not know, say what you can confirm and what still needs checking. Avoid guessing why the person asked.",
        "worked_title": "Answering a question about an assumed project cancellation",
        "before": "Why we canceled it is complicated. We had concerns about the timeline and staffing.",
        "after": "In this invented exchange: we have not canceled the exhibition. We have postponed the opening while the loan dates are confirmed. If your question is about what visitors should expect, the current booking notice remains paused until we can publish a reliable date. The distinction matters because the collection and planning work are still in progress.",
        "worked_explanation": "The answer corrects cancellation before explaining the current state. It offers a useful visitor-facing consequence without overstating when the uncertainty will be resolved. It also avoids accepting the premise just because the question requests reasons for it.",
        "variations": [
            "For an interview, correct the specific assumption and return to the subject. A lengthy account of how the mistake arose may be less useful than the replacement information.",
            "For a contentious meeting, distinguish a false premise from a legitimate concern. Correcting the cancellation claim does not make questions about delay unreasonable.",
            "For a written response, make the corrected fact easy to quote without its surrounding explanation. Do not let the first sentence repeat the false premise as an unqualified headline."
        ],
        "failure_case": "Example of what can go wrong: asked why every application was rejected, an organizer explains the selection standards without saying that several applications were accepted. The answer reinforces an incorrect total. Another failure accuses the questioner of bad faith when the mistake could be an ordinary misunderstanding.",
        "exercise": "Write a question containing one false assumption about a low-stakes project. Draft a response with three sentences: the correction, the confirmed situation and a useful answer to the broader concern. Remove any unnecessary judgment about the questioner.",
        "self_check": "Did you correct the assumption before elaborating? Is the replacement fact supported? Have you answered the relevant concern without treating the correction as a reason to avoid it?"
    },
    "cause_and_mechanism": {
        "title": "Explain the intermediate steps between action and outcome",
        "problem": "A proposal jumps from an action to a promised result: a new resource will make something easier to use, a training session will improve performance, or a campaign will change behavior. The listener cannot see how the change is supposed to work.",
        "principle": "Explain the steps between an action and the result you expect. For each step, say who acts, what they need and what could stop them. A new guide, for example, must reach people, make sense to them and help them complete the task before it can reduce support requests. Say which steps have been observed and which are still assumptions.",
        "source_title": "Manushi Chhillar: a project described through local supply, sellers and barriers",
        "source_writeup": "writeups/full-context-address-119.md",
        "source_passages": "Caption numbers 100–119: locating the issue; 120–149: the described sourcing, local sale and adoption barriers. These positions are not timestamps, and the project's health or economic effects are not independently established by this reading.",
        "source_reading": [
            "The address moves from the large term empowerment to a specific setting and a described local project. Women source sanitary pads and sell them locally. That gives the listener actors and actions to inspect rather than leaving change as an abstract aspiration.",
            "The account also describes taboo and discomfort buying from a male shopkeeper, followed by an affordability consideration. These details identify conditions that might affect use even when a product exists. The chain therefore contains more than supplying an object: it includes the circumstances of obtaining it.",
            "The speech's account does not independently verify affordability, safety, sustained use or impact. Nor does naming a plausible pathway isolate its causal effect from other changes. The source is useful for studying how a speaker makes an intervention concrete, while the outcome claims remain separate questions."
        ],
        "transfer": "Find a promise such as ‘this will improve service’ in your draft. Replace it with the steps that would have to happen. Under each step, note what you have observed, what someone else reported and what you are assuming. Name a way each step could fail. If the result might have another cause, explain that too.",
        "worked_title": "Explaining a proposal for a neighborhood tool library",
        "before": "A tool library will empower residents and reduce waste.",
        "after": "For this hypothetical proposal, residents would reserve an available tool, collect it during staffed hours and return it in usable condition. If the tool matches a task they would otherwise buy equipment for, a loan might avoid that purchase. Availability, collection hours and maintenance are therefore part of the proposal, not administrative details to solve later. We can test the lending process first; a reduction in purchases or waste would need separate evidence.",
        "worked_explanation": "The revision exposes several links between inventory and the proposed benefit. It identifies a condition under which a purchase might be avoided and does not assume that every loan replaces one. The pilot's practical question is distinct from the larger environmental claim.",
        "variations": [
            "For a technical explanation, show the intermediate state where a failure becomes possible. A diagram of components is not yet an explanation of how they interact.",
            "For a funding proposal, include the costs and capacity needed to sustain each link. A pathway that works once may not operate reliably at the proposed scale.",
            "For a retrospective, distinguish a plausible explanation from a comparison that rules out alternatives. Sequence in time alone does not establish cause."
        ],
        "failure_case": "Example of what can go wrong: a presenter installs a suggestion box and claims that staff now influence decisions. The missing steps include reviewing submissions, deciding which to act on and reporting back. The object is present, but the proposed process of influence may not be.",
        "exercise": "Write the steps between your recommended action and the result you expect. Under each step, add what must be in place and how you would recognize a failure. Rewrite the presentation to make the least certain step clear.",
        "self_check": "Can a reader explain how the action could lead to the result? Which steps have been checked? Could something else explain the result? Is it clear that describing a possible process does not prove it worked?"
    },
    "register_shift": {
        "title": "Translate the description into what it means for the listener",
        "problem": "An accurate technical explanation leaves the audience asking what difference it makes. More detail in the same style may not answer the practical question.",
        "principle": "Sometimes a talk needs to move from naming or describing something to explaining why it matters. Make the link clear: say what a listener can conclude or do, and do not claim more than the description supports. This is more than replacing hard words with easy ones; it connects the facts to the decision or idea they support.",
        "source_title": "A Terminator dialogue excerpt: technical classification turns into a practical warning",
        "source_writeup": "writeups/full-context-scene-09.md",
        "source_passages": "Caption numbers 0–13: the fictional machine's composition and identification difficulty; 25–30: unavailable responses and a threat warning. This is a fictional dialogue excerpt with mixed turns and damaged wording, not real engineering evidence or verified delivery.",
        "source_reading": [
            "The opening distinguishes a machine interior from a living exterior and compares older and newer units. Within the fiction, these details explain a claimed difficulty identifying the threat. They are world-building, not evidence about actual machines.",
            "The ending lists responses said to be unavailable, including bargaining and appeals to feeling, before describing a lethal threat. The language now concerns what ordinary responses will not accomplish. Technical classification has become action-relevant warning through repeated negative predicates.",
            "The excerpt does not show successful persuasion or justify applying the machine's characterization to people. Its repetition is visible in the text, but vocal pacing and physical interaction were not inspected. The transferable lesson is the change of explanatory job, not the threat language or dehumanizing description."
        ],
        "transfer": "After a technical statement, add a sentence beginning, for this decision, that means. Explain the relevant consequence and any exception. If you cannot explain the link, do not hide the gap behind a confident instruction. Match the urgency to the situation.",
        "worked_title": "Explaining a shared document's export behavior",
        "before": "The exported file is a static snapshot with no synchronization to the source document.",
        "after": "In this invented software demonstration, the export is a copy taken at the moment you download it. For this review, that means later edits in the shared document will not appear in the copy you already sent. Before distributing the final version, export again and include the version date. That instruction follows from this example's stated behavior; it is not a claim about every document tool.",
        "worked_explanation": "The first sentence explains the property in ordinary language. The next supplies its consequence for the review, and the last gives a limited action. Each step remains connected; the practical instruction does not arrive as an unrelated tip.",
        "variations": [
            "For specialists, retain the technical term and append the decision implication. Precision and practical relevance can coexist without replacing the terminology altogether.",
            "For a public explanation, include only the technical detail needed to understand the result. A long list of categories can distract from the audience's question.",
            "For a risk discussion, name the consequence and uncertainty without borrowing dramatic fictional language. A plain limitation may be enough to support a sensible precaution."
        ],
        "failure_case": "Example of what can go wrong: a presenter says a system is complex and concludes that nobody should question its recommendations. Complexity does not support that instruction. Another failure uses a dramatic warning to imply a level of danger for which the explanation provides no evidence.",
        "exercise": "Choose three technical sentences in your draft. After each, write: ‘For this decision, that means ____ because ____.’ If the added sentence relies on another fact, include the fact and its evidence. Remove advice that the explanation cannot support.",
        "self_check": "What does each style of explanation do? Does the practical advice follow from the explanation? Are the limits still clear? Have you made the advice sound more certain or urgent than the facts allow?"
    }
})

LESSONS.update({
    "technical_explanation_and_interruption": {
        "title": "Answer the interruption, then continue the explanation",
        "problem": "You are halfway through an explanation when a listener objects. Continuing from the next slide may leave the misunderstanding intact; abandoning the entire explanation may lose the useful structure you already built.",
        "principle": "Use a relevant question to find out what the listener needs explained. They may be unsure about a word, a starting assumption, a step or what the result means for them. Answer that part, then show where it fits in the explanation you were giving. If a question needs a longer discussion, say when you can address it and continue with the group.",
        "source_title": "A Terminator dialogue excerpt: a feasibility objection changes the explanatory frame",
        "source_writeup": "writeups/full-context-scene-09.md",
        "source_passages": "Caption numbers 0–13: technical description and interruptions; 14–20: present feasibility, future origin and qualifications. This is fictional dialogue with mixed turns and damaged captions, not engineering evidence or inspected performance timing.",
        "source_reading": [
            "The excerpt begins with the machine's internal and external composition. Other concerns interrupt, including uncertainty about what the speaker wants and the need to change cars. The exchange therefore contains competing practical and explanatory tasks rather than an uninterrupted technical lecture.",
            "The objection that such a machine cannot yet be made exposes a time-frame conflict. The answer moves to a future origin and then qualifies that future as one possibility from the listener's perspective. The speaker also disclaims technical knowledge. Those limits belong to the explanation instead of being discarded as incidental dialogue.",
            "The conversation shows the account changing after an objection. It does not show that the listener is persuaded, consents or understands everything that follows. Unlike the register-shift lesson, which concerns moving from description to implication, this lesson concerns using another person's contribution to decide what the explanation needs next."
        ],
        "transfer": "Pause long enough to identify the actual question. Restate it briefly when needed, answer the missing point and mark your return: with that distinction in place, the next step is. If you lack the answer, say what you cannot establish and whether the remaining explanation depends on it. Give unrelated questions a clear later route rather than pretending they were answered.",
        "worked_title": "Explaining a library reservation system to volunteers",
        "before": "I will come to questions at the end. For now, just follow the flowchart.",
        "after": "In this hypothetical briefing, a volunteer interrupts: does a reservation mean the book is already here? The presenter responds: no—the reservation records the request; the collection notice means the copy is ready. That distinction matters because we should not promise pickup when we only see a request. Now return to the flowchart: the next box is the check that triggers the collection notice.",
        "worked_explanation": "The interruption reveals a consequential confusion between two states. The answer repairs it and returns to a specific point in the explanation. The volunteer's question improves the order of the briefing without requiring the entire session to restart.",
        "variations": [
            "For a technical audience, ask which step fails to follow rather than repeating every preceding detail. A focused objection may reveal one missing assumption.",
            "For a large group, distinguish a clarification everyone needs from a case-specific discussion. Answer the first in the room and give the second a real follow-up route.",
            "For a time-limited presentation, acknowledge an unresolved dependency explicitly. If your recommendation requires an answer you cannot supply, narrow or defer that recommendation."
        ],
        "failure_case": "Example of what can go wrong: a trainer hears a question about permission and responds with more detail about how the button works. The technical answer leaves the authority question untouched. Another failure dismisses every interruption as ignorance, making it harder to discover a genuine error in the presentation.",
        "exercise": "Choose a difficult paragraph and invent three interruptions: what does the term mean, why does the step follow, and what should I do? Draft a two-sentence repair for each followed by a sentence reconnecting to your route.",
        "self_check": "Did you answer the question that was actually raised? Is the missing distinction now clear? Can the group find its place again, and have you left any essential uncertainty visible?"
    },
    "metrics_and_revaluation": {
        "title": "Choose a measure that answers the actual question",
        "problem": "A presentation moves between enjoyment, attention, activity and success as though they were interchangeable. A favorable signal becomes an answer to a different question without anyone noticing the substitution.",
        "principle": "Start with the question, then say what you observed that could help answer it. Name what was counted, what it was compared with and what the measure cannot tell you. Ask whether the measure fits the claim. This differs from the milestone lesson, which asks whether a count marks completion or progress.",
        "source_title": "Taylor Swift: favorite performances and greatest crowd response remain different questions",
        "source_writeup": "writeups/full-context-interview-27.md",
        "source_passages": "Caption numbers 431–454: enjoyment of making a video; 484–507: preferred performances followed by a question about crowd response. Caption positions are not verified timing; no audience measurement was conducted in this reading.",
        "source_reading": [
            "Asked about a favorite video, Swift emphasizes the experience of making it rather than supplying an objective ranking of the finished films. The answer's standard is therefore production experience. Treating that preference as evidence of the best finished product would change the question.",
            "Later, she names performances she enjoys. A follow-up asks whether these also produce the strongest crowd response. She does not provide a clear ranking, describing the crowd as consistently loud. The host's follow-up makes the distinction between performer enjoyment and audience response visible.",
            "Neither a personal preference nor a reported impression of loudness establishes comparative audience impact. Even measured volume would answer only a particular question about sound, not automatically one about comprehension, lasting appreciation or agreement. The exchange is useful because it leaves the requested equivalence unproven."
        ],
        "transfer": "Write the intended claim before selecting a statistic or testimonial. Ask what the measure actually records and which interpretation requires extra assumptions. If several outcomes matter, report them separately rather than compressing them into one flattering label. When the available measure answers only a narrower question, use the narrower wording.",
        "worked_title": "Reporting on a public workshop",
        "before": "The workshop was a success: every place was booked and the audience applauded.",
        "after": "For this invented workshop report, all thirty places were booked. That establishes demand for the available places, not attendance or learning. We recorded twenty-six attendees. To assess whether the explanation was usable, we would need to inspect participants' attempts at the task or another relevant check. Applause can be reported as a response, but it does not answer that learning question.",
        "worked_explanation": "The revised report separates booking, attendance and task performance. It does not discard the favorable counts; it stops them from claiming more than they record. The learning check remains a proposal, not an invented result.",
        "variations": [
            "For a product presentation, distinguish attempts, unique people, completed tasks and repeat use. Each may matter, but one cannot silently replace another.",
            "For a creative review, separate the maker's satisfaction, the audience's preference and performance against the brief. A disagreement may reflect different standards rather than a mistaken observation.",
            "For a leadership update, show the measure alongside the decision it informs. A familiar dashboard figure should not become mandatory evidence simply because it is easy to retrieve."
        ],
        "failure_case": "Example of what can go wrong: a presenter treats a high number of help-page visits as proof that the page solves users' problems. Visits may instead reflect repeated difficulty. Another failure treats positive comments from a few volunteers as a representative measure of the whole audience.",
        "exercise": "Create three columns: question, what you observed and what that observation cannot show. Put each headline number from your draft into the table. Rewrite any headline that claims more than the observation supports.",
        "self_check": "What exactly is counted or judged? Does it answer the question? Is it clear which group is included and what the result is compared with? Have you kept attention, preference, activity and outcome separate?"
    },
    "risk_safety_and_limit": {
        "title": "Keep the cost and stopping condition beside the invitation",
        "problem": "A successful risk story makes a bold action sound like a general rule. The memorable invitation survives while the conditions, costs and reasons to stop disappear.",
        "principle": "When asking people to try something, say what it could cost and when you would stop or review it. For a small project, that might mean a limit on hours or spending. Explain what must be in place before starting. One person's success cannot show that an attempt is safe for everyone. Serious safety decisions need the relevant expertise.",
        "source_title": "William McRaven: an acknowledged risky maneuver and an absolute persistence ending",
        "source_writeup": "writeups/full-context-address-67.md",
        "source_passages": "Caption numbers 162–181: obstacle technique and acknowledged injury risk; 251–259: the bell and categorical persistence instruction. Caption positions are not playback times; no tactical or physical practice instruction is offered here.",
        "source_reading": [
            "The obstacle story describes an alternative technique and a favorable outcome while acknowledging injury risk. The acknowledged downside must remain beside the result. A summary that retains only the successful maneuver would turn a selected account into a misleading recommendation.",
            "The final training story builds toward an instruction never to ring the bell signaling withdrawal. The passage in the transcript does not supply injury exceptions, changed goals or other stopping standards. Its categorical force is part of the speech, but the source does not establish that never stopping is appropriate across circumstances.",
            "Together these passages are useful for examining both an explicit limit and a missing one. The lesson does not prescribe the physical activities described. It asks how to prevent a presentation's motivational form from overruling the practical judgment its listeners still need to make."
        ],
        "transfer": "For a small, low-risk proposal, say what you are asking people to commit to, what could go wrong and when you will review the plan. For serious health, safety, financial or other specialist risks, follow the proper expert process; do not make up advice in a speech. Make it clear when people may stop or opt out.",
        "worked_title": "Proposing an experimental format for a community newsletter",
        "before": "We have to be bold. Let us change everything and commit to making it work no matter what.",
        "after": "In this hypothetical proposal, let us try the new format for one optional special issue, with no more than two volunteer evenings spent on layout. The regular edition stays unchanged. If the template still cannot be read comfortably on a phone after the first review, we pause and revise it rather than spend the second evening adding more content. We are testing a format within a time limit, not proving our commitment by continuing indefinitely.",
        "worked_explanation": "The invitation names a limited experiment, preserves the regular service and includes an observable reason to reconsider. The stop condition is tied to the purpose of the work rather than to embarrassment about changing course.",
        "variations": [
            "For an internal pilot, make the resource ceiling and review point visible on the decision slide. A verbal qualification is easy to lose when the slide is forwarded alone.",
            "For a personal retrospective, say which resources and support made the risk possible. An audience with different constraints may reasonably choose differently.",
            "For a motivational address, distinguish courage from compulsory persistence. A person can act responsibly by refusing, stopping or changing the goal."
        ],
        "failure_case": "Example of what can go wrong: a leader praises one team for working through the weekend and asks every team to show the same commitment. The story omits costs and makes refusal look like a character flaw. Another failure specifies a review date but offers no standard for changing course.",
        "exercise": "Choose a small proposal, such as testing a new meeting format. Write what people would try, the maximum time or money involved, when they would stop to review it and what they could do instead. Remove any sentence that treats stopping as a personal failing.",
        "self_check": "Is the downside visible? Are the limits practical and enforceable? Does the success story preserve its conditions? Can someone decline or stop for a valid reason without being misrepresented?"
    }
})

LESSONS.update({
    "choice_and_responsibility": {
        "title": "Name what people can actually choose",
        "problem": "A presentation celebrates talent, resources or status without explaining the choices those advantages make possible. Alternatively, it tells people that everything is a choice, overlooking constraints they cannot control.",
        "principle": "Say which decision a person can make, what resources they have and who their choice affects. Separate that choice from circumstances they cannot control. A volunteer may choose which available shift to take while having no say over the event date. Do not judge every result as a sign of character or assume that everyone has the same options.",
        "source_title": "Jeff Bezos: gifts, choices and a sequence of closing alternatives",
        "source_writeup": "writeups/full-context-address-72.md",
        "source_passages": "Caption numbers 46–68: gifts, choices and possibilities; 99–112: paired alternatives; 113–119: imagined later reflection. Caption positions are not verified playback times, and this is not a tested list of moral types.",
        "source_reading": [
            "After the childhood story, the speaker distinguishes gifts from choices. Praise of the students' abilities then leads to possibilities and questions about how those abilities will be used. The sequence changes the subject from possessing capability to exercising judgment with it.",
            "The closing pairs alternatives involving service, criticism, apology, relationships and persistence. The alternatives are morally weighted, not a complete decision tree. Their force depends partly on presenting one direction as preferable; they should not be mistaken for an exhaustive account of every listener's options.",
            "The imagined age-eighty perspective asks listeners to view current decisions as parts of a future life story. That is an invitation to reflect, not evidence that everyone will value the same choices later. The source also contains support and deliberation in the career story, so the broader account is not one of unconstrained individual will."
        ],
        "transfer": "Write one decision the audience can actually make. List the available options, the limits on those options and the people affected. If your speech offers only two choices, check whether others exist. Say when the decision could be reconsidered as new information arrives.",
        "worked_title": "Introducing responsibilities for a volunteer selection panel",
        "before": "You are talented people. Use your influence wisely and make the right choices.",
        "after": "In this invented panel briefing, our authority is limited but real: we choose which applications receive an interview. We cannot promise anyone a place today. We can apply the published standards consistently, record reasons and flag a conflict of interest before discussing an application. Those are the decisions for which this panel is responsible. If a standard cannot be applied fairly with the information supplied, we should raise that problem rather than improvise a private rule.",
        "worked_explanation": "The revision turns a broad appeal to character into clear decisions. It limits the panel's authority and gives a route for a flawed process. Responsibility attaches to what members can do, not to outcomes outside their control.",
        "variations": [
            "For a leadership address, distinguish a leader's power to allocate resources from staff members' power to carry out a task. Do not describe unequal authority as a shared choice without qualification.",
            "For a personal story, name the support and alternatives that made your decision possible. A listener may share your values while reasonably choosing another path.",
            "For a classroom discussion, ask which options are missing before evaluating the options presented. The act of framing a choice can itself determine which responsibilities become visible."
        ],
        "failure_case": "Example of what can go wrong: a speaker tells overextended volunteers that they can choose excellence or choose excuses, while leaving out the lack of time and resources. This turns a workload problem into a judgment about character. Another failure praises people for taking initiative but withholds the permission they need to act.",
        "exercise": "Write four lines: the resource available, the decision within reach, the people affected and the constraint that remains. Turn them into a short invitation without using always, anyone or simply.",
        "self_check": "Is the choice genuinely available? Who controls it? Are relevant alternatives missing? Does your account assign responsibility without pretending that circumstances and outcomes are fully under individual control?"
    },
    "value_and_moral_frame": {
        "title": "Name the standard by which you want the decision judged",
        "problem": "A proposal lists benefits but leaves its governing value unstated. People can agree on the facts and still disagree because they are judging the decision by different standards.",
        "principle": "Say what you consider a good or responsible outcome. Connect that standard to a specific decision and name any competing concern. Values help people judge a choice; they do not prove facts or remove the need to look at what happened. This differs from explaining who gets to choose: it asks what should guide the choice.",
        "source_title": "Jeff Bezos: kindness becomes a standard for evaluating cleverness",
        "source_writeup": "writeups/full-context-address-72.md",
        "source_passages": "Caption numbers 17–45: the calculation, unexpected hurt and kindness/cleverness distinction; 46–51: the broader interpretation; 99–112: later moral alternatives. These are transcript positions rather than playback times.",
        "source_reading": [
            "The child's calculation is presented as an attempt to display cleverness. The grandmother's reported tears reveal a consequence that the original success standard missed. The story does not need the calculation to be medically valid for that narrative contrast to be intelligible; indeed, it is not a reliable individual lifespan estimate.",
            "The grandfather's distinction introduces kindness as a different standard for judging the action. The rhetorical question is no longer just whether the child can calculate, but how the use of that ability affects another person. The larger gifts-and-choices frame develops that interpretation.",
            "This remains a moral reading of a narrated incident. It does not establish that kindness and cleverness are mutually exclusive or that one is universally harder. A responsible adaptation preserves the evaluative question without converting the speaker's formulation into a universal psychological law."
        ],
        "transfer": "State the value as a standard that can affect a decision. Explain what it would change in a concrete case and where it might conflict with another legitimate concern. Avoid using a value word as a substitute for the evidence needed to justify your proposal. People who dispute a method do not necessarily reject the value it is meant to serve.",
        "worked_title": "Discussing how to correct mistakes in a volunteer newsletter",
        "before": "We need a kinder culture, so we should stop criticizing each other's work.",
        "after": "For this hypothetical editorial team, kindness should shape how we correct an error, not whether we correct it. We owe readers accurate information and contributors a respectful process. Let us identify the passage, explain the issue privately where possible and agree on the correction without making the mistake a judgment about the writer's character. If the error has already reached readers, the public correction still needs to be clear.",
        "worked_explanation": "The revision puts two obligations beside each other and lets the value change the method. It does not use kindness to hide an error or accuracy to justify humiliation. The proposed process still requires judgment about the actual circumstances.",
        "variations": [
            "For a strategy discussion, name the trade-off between values rather than assuming one favorable word settles it. Speed, care, fairness and openness may require different choices in a particular case.",
            "For an ethical appeal, distinguish a factual claim about consequences from a value judgment about which consequences matter. Both may be needed, but they require different kinds of support.",
            "For a disagreement, ask which standard each side is using. A dispute about the means can become more tractable once the shared and competing values are explicit."
        ],
        "failure_case": "Example of what can go wrong: a presenter labels their proposal compassionate and treats every request for evidence as a lack of compassion. The frame immunizes the method from scrutiny. Another failure states a value prominently but recommends a process that contradicts it.",
        "exercise": "Choose a recommendation and write the value behind it without naming the recommendation. Add a rival proposal that could serve the same value. Explain what evidence or trade-off would help choose between them.",
        "self_check": "Have you said what you consider a good result? Does that belief affect the decision you propose? Could someone share the belief but prefer another method? Have you left room to check what the method actually does?"
    },
    "story_to_thesis": {
        "title": "Explain what the story shows—and what it does not",
        "problem": "A presentation tells a vivid story and then announces a broad lesson. The audience may remember the event without seeing why that lesson follows, or may mistake a single case for proof of a general rule.",
        "principle": "After a story, explain what the event helps you see, then make a broader claim that the evidence can support. Keep an example, a possible explanation and proof that something is common separate. This pattern is about moving from the story to the point; the scene pattern is about shaping the event, and expectation reversal is about a prediction that proves wrong.",
        "source_title": "Jeff Bezos: a grandfather's distinction leads into gifts and choices",
        "source_writeup": "writeups/full-context-address-72.md",
        "source_passages": "Caption numbers 26–45: reaction and interpretation; 46–51: gifts-versus-choices main point; 52–68: extension toward the graduates. Caption numbers are not playback timestamps or verified delivery cues.",
        "source_reading": [
            "The narrated reaction changes the meaning of the child's calculation. The grandfather's kindness/cleverness distinction gives that reaction an interpretation instead of leaving the audience with an unexplained painful moment.",
            "The next passage turns to gifts and choices. The link is simple: having an ability is different from deciding how to use it. The story gives one example to think about; it does not provide a complete list of human abilities or decisions.",
            "The address then turns to the graduates' capabilities and their possible uses. That extends the relevance beyond the childhood scene. The transfer is rhetorical and moral, not a demonstrated finding that every listener faces equivalent circumstances or will respond in the same way."
        ],
        "transfer": "After writing the story, add a sentence that says what changed in your understanding. Then write the main point and ask whether the story only illustrates it or gives enough evidence to support it. If you need broader evidence, add it or narrow the point. Do not tack on a slogan just to end the story.",
        "worked_title": "Turning a small event into a presentation about clear instructions",
        "before": "Someone could not find the meeting room. This proves that communication is the most important skill in life.",
        "after": "In this invented example, our invitation said to meet by the main entrance. The organizer meant the entrance used by staff; a first-time visitor waited at the public entrance. The instruction depended on knowledge we had not shared. That is the point I want to examine today: before sending directions, identify the assumptions a newcomer cannot be expected to supply. One incident does not tell us how often this happens, but it gives us a concrete instruction to revise.",
        "worked_explanation": "The bridge names the hidden assumption, and the main point stays close to what happened. It suggests a useful check without claiming that one visitor's experience ranks skills for everyone. The story helps make the point; it is not just decoration.",
        "variations": [
            "For a research presentation, use the story to introduce the question and then show the evidence addressing it. Do not let the opening case stand in for the study.",
            "For a personal address, say what the event led you to reconsider if that is all the evidence supports. A personal lesson can matter without being a rule for everyone.",
            "For a proposal, connect the main point to a small next test. A story can help identify a possible problem, even when you do not yet know how often it happens or which fix is best."
        ],
        "failure_case": "Example of what can go wrong: a presenter tells a story about a successful last-minute decision and concludes that planning is unnecessary. The main point claims more than the story shows and ignores what made improvisation possible. Another failure adds a lesson unrelated to the choice that drove the event.",
        "exercise": "Write the story's final event, a sentence explaining what it shows and the main point on separate lines. Underline the idea shared by all three. Mark whether the story is an illustration, evidence or a reason to investigate, then revise the main point to fit.",
        "self_check": "Does the bridge explain the lesson? Does the main point match the evidence? Can a reader tell what the story shows and what still needs support?"
    }
})

LESSONS.update({
    "recognition_to_specific_credit": {
        "title": "Thank people by naming what they did",
        "problem": "An acknowledgment calls everyone amazing but gives the audience no account of what anyone did. The people doing less visible work may disappear behind the overall success.",
        "principle": "Name who did what and why it mattered. Check that the credit is accurate before sharing it. Unlike the broader lesson about shared work, this pattern focuses on thanking one person clearly without inventing results or sharing private details.",
        "source_title": "Aishwarya Rai Bachchan: recognition expands into named kinds of work",
        "source_writeup": "writeups/full-context-address-73.md",
        "source_passages": "Caption numbers 19–29: clinical roles; 30–39: outreach, government partners and donors; 92–96: repeated closing thanks. These are caption positions, not playback times; the reading does not independently verify institutional outcomes.",
        "source_reading": [
            "The address moves beyond the speaker's personal encounters to identify doctors, nurses, speech therapists, orthodontists and other workers. Naming different roles makes the recognition more concrete than a single statement that the team is wonderful.",
            "Outreach work, difficult geographies, government partners and donors extend the acknowledgment beyond the most visible clinical encounter. The speech thus makes several kinds of contribution available to notice. The local analysis does not establish every individual's responsibilities or the effects of each contribution.",
            "Repeated thanks close the address. The teaching adaptation below goes further by attaching an explicit action to each acknowledgment. That is a drafting method derived from the passage's specificity, not a claim that the transcript gives a complete contribution record or that the audience felt appreciated."
        ],
        "transfer": "Replace a general thank-you with a sentence naming what the person did: checked the figures, arranged the room or explained a missing step. Add why that work mattered. Check the name and role, ask before sharing private details and make sure the wording does not give one person credit for everyone else's work.",
        "worked_title": "Thanking contributors at a local exhibition opening",
        "before": "Thank you to our incredible volunteers. None of this would have been possible without you.",
        "after": "In this invented opening, the installation volunteers checked each label against the object list, the welcome team rehearsed the visitor route, and the records group tracked the loans and return dates. Those jobs made the exhibition ready to open and made its responsibilities visible. We will thank the named contributors in the program using the details they have approved.",
        "worked_explanation": "The acknowledgment describes three distinct contributions and avoids claiming that gratitude proves visitor satisfaction. Approval of names and details prevents public thanks from becoming unwanted disclosure. The phrasing recognizes preparation and recordkeeping alongside the visible installation.",
        "variations": [
            "For a project report, include the person who identified a problem or challenged an assumption, not only those associated with the final delivery. Verify what changed because of the contribution.",
            "For a public ceremony, use approved names and accessible descriptions of specialist roles. A job title alone may not explain the work to outsiders.",
            "For a private acknowledgment, be direct about what you noticed. Detailed praise should not become a request for the person to keep doing extra work without support."
        ],
        "failure_case": "Example of what can go wrong: a presenter thanks the team for working without complaint when several members raised valid concerns. The praise rewrites their experience. Another failure assigns a celebrated outcome to one prominent contributor while omitting the less visible people whose work enabled it.",
        "exercise": "Replace three adjectives in a thank-you paragraph with verified actions. For each action, add why it mattered and check whether the contributor would recognize the account. Remove unnecessary personal details.",
        "self_check": "Have you named the work and credited the right person? Did you include preparation or support that the audience may not have seen? Have you checked permission to share details? Does the praise leave room for other contributions and any unresolved concerns?"
    },
    "credit_redirection": {
        "title": "Share credit without denying your own contribution",
        "problem": "An award, introduction or personal story centers attention on the speaker. The closing needs to recognize the larger effort without sounding like ritual self-denial or immediately returning the spotlight to the speaker.",
        "principle": "When attention is on your achievement, use part of the occasion to show the work or people behind it. Accept your own contribution, then explain what else made it possible. End on the contribution you want listeners to notice. Giving someone credit does not assign them a new job or responsibility.",
        "source_title": "Jennifer Aniston: personal reflection closes with organizational recognition and shared power",
        "source_writeup": "writeups/full-context-address-68.md",
        "source_passages": "Caption numbers 8–20: the speaker's account of power; 80–83: the inclusive table callback; 84–86: recognition redirected to the organization and shared power. Caption positions are not verified media times or audience-response evidence.",
        "source_reading": [
            "Much of the address concerns the speaker's relationship with having a voice. Personal memories and reported encounters supply the route into the subject, but the ending does not simply certify her own transformation.",
            "The table callback places value on children's participation and questions even when adults lack answers. The final recognition then points toward the organization and power shared beyond the individual. The attention established by the personal narrative is used to make something larger visible.",
            "The source still contains advocacy claims that this reading does not independently verify. Redirecting praise to an institution cannot make those claims true by itself. Nor does the transcript show that listeners actually shifted their attention or support. The observable move is the changed focus of the closing language."
        ],
        "transfer": "When receiving recognition, acknowledge your actual contribution without inflating or erasing it. Identify the wider effort the occasion can make visible and end on a concrete feature of that effort. Do not claim to speak for everyone involved or use the recognition to promise what another group has not agreed to deliver.",
        "worked_title": "Accepting recognition for a community publication",
        "before": "I do not deserve this at all. It is really everyone else's award. But let me explain how I built the publication.",
        "after": "For this invented acceptance: thank you for recognizing my editing work. I would like this occasion to make the publication's continuing work visible too: contributors who report local events, people who check names and dates, and the delivery volunteers who bring each issue to readers. The finished issue carries an editor's name, but it rests on that recurring effort. That is what I hope we recognize tonight.",
        "worked_explanation": "The speaker accepts the relevant credit, then changes the closing focus to an identifiable shared effort. The final sentence stays there. It does not convert recognition into a request for unpaid expansion or deny the editor's real role.",
        "variations": [
            "For an award speech, keep the acceptance clear before broadening the focus. A long refusal of praise can make the audience work to reassure you instead of noticing others.",
            "For a project demonstration, direct attention to work the demo cannot show, such as maintenance or careful review. Explain its role rather than presenting a ceremonial list.",
            "For institutional advocacy, distinguish deserved recognition from claims about effectiveness. Praise and outcome evidence perform different jobs."
        ],
        "failure_case": "Example of what can go wrong: a speaker says the award belongs to the team, then uses every remaining sentence to recount personal sacrifices. The declared redirection never happens. Another failure redirects praise to an organization as though the praise itself settled questions about its performance.",
        "exercise": "Write a four-sentence acceptance: acknowledge the recognition, state your contribution, identify the wider effort and end on that effort. Underline the subject of each sentence to check where attention actually goes.",
        "self_check": "Did the ending genuinely change focus? Is your own contribution represented accurately? Are others visible as contributors rather than props in your story? Have you kept recognition separate from unverified impact claims?"
    },
    "authority_to_service": {
        "title": "Say what your role lets you do—and what it does not",
        "problem": "A speaker's title, fame or expertise creates attention, but the presentation never explains how that standing serves the task. Status may also be mistaken for competence outside the speaker's field.",
        "principle": "Explain what your role lets you contribute. You might arrange a meeting, provide equipment, explain a process or draw attention to a problem. Say which decisions belong to someone else. A well-known supporter may help people hear about a service while qualified staff decide how that service is provided.",
        "source_title": "Jennifer Aniston: a public voice used for connection while a knowledge limit remains visible",
        "source_writeup": "writeups/full-context-address-68.md",
        "source_passages": "Caption numbers 8–20: power through a voice; 34–51: reported viewer feedback and entry into philanthropy; 56–70: the child's question and lack of an answer. These are transcript positions, not playback times; no clinical benefit is established.",
        "source_reading": [
            "The speaker defines power through using a voice to support and connect people. Reported messages from viewers lead her to reconsider her platform's value. Those messages describe her interpretation of feedback, not independently measured health outcomes.",
            "An invitation gives the account a route into philanthropic participation. The story therefore connects a public platform with a particular setting and activity rather than leaving service as an abstract claim about being influential.",
            "The child's question exposes a limit: the speaker describes not feeling equipped to explain the medical term, and the transcript retains no substantive answer. Public visibility is not presented as all-purpose expertise. The teaching point is the coexistence of a possible contribution and a real knowledge boundary."
        ],
        "transfer": "Name the resource your role gives you and the task it can responsibly support. Identify what still requires someone else's expertise or decision. If you introduce specialists, give them a real opportunity to speak rather than treating their presence as endorsement of everything you say. Keep the people served visible as participants with their own perspectives.",
        "worked_title": "A festival host introducing an archive-preservation session",
        "before": "I have worked in the arts for years, so I can tell you how to preserve any old object you own.",
        "after": "In this hypothetical introduction: my role today is to bring this conversation to the festival audience and help collect your questions. The conservator will explain the preservation considerations within the session's scope. I can describe why these objects matter to our program, but I should not guess how to treat a damaged item. Where a question needs individual examination, we will say so rather than improvise an answer on stage.",
        "worked_explanation": "The host's platform has a defined use: convening and facilitating. Specialist judgment remains distinct. The introduction also describes how unanswered questions will be handled, so the boundary leads to a useful process rather than a dead end.",
        "variations": [
            "For a senior leader, explain which resource or obstacle you can address. A call for others to serve is less concrete than specifying what your own authority will provide.",
            "For a specialist speaking outside their field, distinguish transferable experience from subject expertise. A respected credential does not settle every adjacent question.",
            "For a public advocate, provide access to the people doing and experiencing the work. Avoid making their entire role the confirmation of your account."
        ],
        "failure_case": "Example of what can go wrong: a well-known host introduces a technical subject and then answers specialist questions from personal intuition. Visibility substitutes for evidence. Another failure claims to give people a voice while scripting every contribution they are allowed to make.",
        "exercise": "Complete four statements: my role gives me access to; I can use it to; I am not qualified or authorized to decide; the appropriate next person or process is. Build an introduction that includes all four without becoming a recital of disclaimers.",
        "self_check": "Is the contribution concrete? Does the platform serve the task rather than become the task? Are expertise and authority boundaries clear, with a useful route for questions beyond them?"
    }
})

LESSONS.update({
    "scope_repair": {
        "title": "Correct the broad claim wherever it appears",
        "problem": "You correct an overstatement in one sentence, but the slide, summary or recommendation still carries the broader claim. Readers taking away only those parts receive the error rather than the repair.",
        "principle": "When a claim is too broad, correct who it applies to, how many people it covers, where it applies or when it happened. Then check the rest of the argument for the same error. Correcting a claim means more than changing one word: any conclusion that relied on the broader version may need to change too.",
        "source_title": "Taylor Swift: a plural relationship formulation corrected to a singular account",
        "source_writeup": "writeups/full-context-interview-27.md",
        "source_passages": "Caption numbers 285–304: broad relationship wording narrowed to one him; 305–316: preference for known characters. These are caption positions, not verified playback times or independent biographical evidence.",
        "source_reading": [
            "The relationship-writing exchange contains a broad they formulation that is corrected to him. The change affects how many people the account appears to concern. A summary that keeps only the first wording can incorrectly turn a singular anecdote into a repeated pattern.",
            "Use the corrected wording in later summaries. The question is not whether the first version was fluent or memorable, but which version of the claim the speaker finally kept. This passage does not independently verify several incidents.",
            "The following answer explains a preference for writing about known characters. That preference does not independently establish the accuracy of every portrayal. Keeping the two claims separate prevents a nearby general statement from quietly expanding the repaired anecdote again."
        ],
        "transfer": "After correcting a broad claim, check the title, chart labels, summary and recommendation for the old version. Ask whether you changed from attempts to people, one group to everyone, or one time period to all time. Repeat the accurate version wherever a reader might copy it. Explain the correction if it changes a decision.",
        "worked_title": "Correcting a report about workshop participants",
        "before": "Participants found the instructions confusing. To clarify, one participant said this, but the overall conclusion remains that participants need a redesigned course.",
        "after": "In this invented report, one participant said the first instruction was unclear. We have corrected the summary heading from Participants found the course confusing to One participant identified an unclear opening instruction. That observation supports reviewing the instruction and checking it in the next session. It does not yet establish how many participants had the problem or whether the whole course needs redesign.",
        "worked_explanation": "The correction changes the report's headline and makes the recommendation more careful. It keeps the useful observation without claiming that the pattern is common. The revised wording still makes sense if copied out of the paragraph.",
        "variations": [
            "For a live presentation, restate the complete corrected claim rather than expecting listeners to mentally edit an earlier sentence. Update the distributed materials afterward when necessary.",
            "For a quantitative report, inspect denominators and units as well as adjectives. Narrowing a claim about people is incomplete if the chart still counts repeated attempts as distinct people.",
            "For a qualitative account, distinguish one person's experience from a theme observed across several accounts. A vivid example can illustrate a theme only when the wider evidence actually supports it."
        ],
        "failure_case": "Example of what can go wrong: an author adds a footnote saying the result concerns one branch but leaves a headline claiming company-wide improvement. The most visible claim remains wrong. Another failure narrows everyone to many without evidence for the replacement quantity.",
        "exercise": "Take a claim and narrow one part: who, where, when or under what conditions. Mark every sentence that relies on the broader version. Rewrite the headline and recommendation before polishing the correction.",
        "self_check": "Does the accurate version appear throughout the argument? Do the numbers and examples support it? Would a reader who sees only the title and summary still get the right claim?"
    },
    "selection_and_incentive": {
        "title": "Explain how these examples were chosen",
        "problem": "A presentation shows selected questions, enthusiastic participants or memorable behavior as though they speak for the whole audience. It leaves out how those examples were chosen and whether a reward or pressure affected what people said.",
        "principle": "Before drawing a broad conclusion from examples, say who could take part, how the examples were chosen and what people might gain. Those choices affect which observations reach the presenter and how people behave. They are different influences. Neither makes an example worthless, but both limit what it can show about people outside that setting.",
        "source_title": "Taylor Swift's interview: selected fan questions and a chance to meet her",
        "source_writeup": "writeups/full-context-interview-27.md",
        "source_passages": "Caption numbers 80–99: many submitted questions and few selected; 358–389: costumes within a possible meet-and-greet selection setting. Caption positions are not timestamps; no representative audience survey was inspected.",
        "source_reading": [
            "The host reports many submitted questions while acknowledging that only a few can be used. The questions heard in the event therefore pass through a selection process. Describing them as highly voted does not establish that they represent every fan's priorities or people who did not submit questions.",
            "Later costume stories occur in a setting where audience members can be selected for a surprise meet-and-greet. That possible reward matters when interpreting conspicuous behavior. It is one relevant condition, not proof that every participant dressed a certain way for the same reason.",
            "The two passages support different cautions: selection limits the questions visible in the interview, while an incentive may shape behavior at a performance. A careful presentation keeps both conditions in view without pretending it has measured the size of either effect."
        ],
        "transfer": "When you share audience examples, say who supplied them, how you chose them and whether a reward or pressure may have mattered. Tell listeners whether an example was chosen to make a point or to estimate what a larger group thinks. To learn about quieter or absent participants, gather information that includes them.",
        "worked_title": "Reporting questions from an optional public consultation",
        "before": "Residents want longer opening hours. All the questions we received were about access.",
        "after": "For this invented consultation, we received twelve questions through an optional evening session. Five were selected for the panel because they addressed opening hours; those five illustrate the access issue, not its share of all residents' concerns. People unable to attend are not represented by this set. Before claiming a community priority, we need a broader way to hear from them and a transparent account of all the submitted topics.",
        "worked_explanation": "The report says how people joined and how the presenter chose examples. It keeps the questions as useful examples but does not claim they represent the whole group. The next step seeks views from people who were missing.",
        "variations": [
            "For a workshop, state whether volunteers were rewarded, publicly praised or selected by confidence. Visible participation may not reveal the experience of quieter learners.",
            "For a customer presentation, disclose whether testimonials came from invited enthusiasts or a broader collection. A compelling endorsement is not automatically a representative outcome.",
            "For an internal meeting, consider whether status affects who speaks. A show of hands can record an observable response without establishing privately held agreement."
        ],
        "failure_case": "Example of what can go wrong: a presenter offers a prize for the most enthusiastic answer, then says the response proves everyone loves the proposal. The prize may have affected what people said. Another failure selects only complaints and treats them as the share of everyone who had a problem.",
        "exercise": "For three examples in your draft, write how each reached you, why you chose it and whose views are missing. Note any reward or pressure that may matter. Rewrite one sentence so the example stays useful without claiming too much.",
        "self_check": "Who had a chance to be included? Why did these examples stand out? Were rewards or pressure involved? Have you kept useful examples separate from estimates of what the whole group thinks?"
    },
    "purpose_attention_example": {
        "title": "Tell listeners what to pay attention to",
        "problem": "An opening, demonstration or audience activity is designed to attract attention, but the presentation never specifies what the audience should notice or understand as a result.",
        "principle": "Before choosing an opening image, question or activity, decide what you want listeners to notice. Choose an example that makes that feature clear, then explain why it matters. If you compare two labels, say whether people should look at their wording, size or placement. An example can be memorable while its intended point remains unclear.",
        "source_title": "Taylor Swift: intended expression, listener encounters and conspicuous audience behavior",
        "source_writeup": "writeups/full-context-interview-27.md",
        "source_passages": "Caption numbers 121–147: expressing an intended meaning and watching listeners encounter it; 358–389: costumes and selection context. These are transcript positions rather than playback times; comprehension was not independently tested.",
        "source_reading": [
            "The interview includes an account of satisfaction when a line conveys what the speaker means, followed by observing listeners encounter those lines. This places intended expression and listener experience near each other, but the transcript does not provide an independent comprehension test.",
            "The costume examples describe visibly distinctive behavior in a context that includes possible selection for a meet-and-greet. Such behavior can attract notice while leaving the audience member's purpose or understanding uncertain. The example therefore makes attention visible without establishing every meaning attached to it.",
            "Taken together, the passages help separate expression, notice and interpretation. The instructional approach here asks a presenter to connect those stages deliberately. It is an adaptation, not a claim that the interview demonstrates a validated method for controlling audience attention."
        ],
        "transfer": "Before adding a surprising image, question or activity, write what it should help the audience distinguish. Choose details that serve that purpose and remove those that compete with it. After the example, state the intended connection. If you need evidence of understanding, ask for an explanation or task response rather than assuming that visible excitement supplied it.",
        "worked_title": "Opening a presentation about useful object labels",
        "before": "We will begin with a spectacular photograph to grab attention, then explain why labels matter.",
        "after": "In this invented museum-training opening, show one ordinary object with two labels: an unfamiliar catalog code and a short description of its use. Ask what each label lets a first-time visitor understand and what each leaves out. The purpose is to distinguish identification from explanation. The object does not need to be spectacular; it needs to make that difference clear.",
        "worked_explanation": "The activity helps explain a specific idea. Both labels may be useful, so the talk does not need to say that one is better for everyone. The opening prepares listeners for the distinction the rest of the presentation will explain instead of relying on visual excitement alone.",
        "variations": [
            "For a technical demonstration, choose an input that reveals the behavior under discussion. A dazzling edge case may distract from the ordinary decision the audience needs to make.",
            "For a public talk, connect a surprising fact explicitly to the question ahead. Surprise without a bridge can become the only thing listeners remember.",
            "For an interactive session, make the task and its purpose clear without demanding personal disclosure. Participation should contribute to the lesson, not merely make the room look active."
        ],
        "failure_case": "Example of what can go wrong: a presenter uses an elaborate animation about a minor feature, then concludes that the audience understood the system because everyone watched. Looking at the animation does not establish the intended understanding. Another failure chooses a joke whose subject overwhelms the actual point.",
        "exercise": "For each image, opening question or activity in your talk, write what it helps the audience notice. Remove or replace it if you cannot name a useful purpose. Then write a question asking listeners to explain the idea in their own words.",
        "self_check": "What should attention accomplish here? Do the example's details serve that purpose? Can you distinguish interest from understanding, and have you given the audience a clear bridge to the main point?"
    }
})

LESSONS.update({
    "identity_status_and_belonging": {
        "title": "Show the role, the mismatch and the conditions for change",
        "problem": "A story about finding your voice becomes a slogan about being yourself. The audience cannot see which role constrained the speaker, what changed or who made the change possible.",
        "principle": "Describe what a person was expected to do, why that role did not fit and what allowed them to contribute differently. A new employee might need time to read a proposal before discussing it, for example. Explain any change in permission, preparation or support. Speaking more confidently alone does not show that someone is accepted or has a say in decisions.",
        "source_title": "Dwayne Johnson with Oprah: an imposed wrestling role and permission to speak differently",
        "source_writeup": "writeups/full-context-interview-24.md",
        "source_passages": "Caption numbers 269–305: name and performance instructions; 306–341: request for microphone time and granted permission; 362–410: renewed identity difficulty in another setting. Caption positions are not verified playback times or independent outcome evidence.",
        "source_reading": [
            "The guest describes an imposed name and instructions to smile as inconsistent with how he wanted to express himself. These concrete expectations make the conflict more specific than a general claim that he was not being authentic.",
            "A reported hostile crowd reaction precedes a request for live microphone time. Permission is granted in the story. The opportunity therefore includes another person's decision and institutional access; it is not produced solely by the speaker choosing to be confident.",
            "The later Hollywood account reopens the identity problem after the earlier breakthrough. That recurrence prevents the story from being read as a permanently solved transformation. Wrestling also involves constructed performance roles, so the account should not be treated as an unmediated revelation of private identity or a universal workplace model."
        ],
        "transfer": "Describe what people were expected to do and what made that expectation difficult for someone. Then name the change that helped them contribute: more preparation time, another way to respond or permission to question the plan. Explain any problem that remains. Ask for changes to the working conditions when needed; confidence alone may not solve the problem.",
        "worked_title": "Explaining a change in how new team members join discussions",
        "before": "People just need the confidence to speak up and bring their whole selves to meetings.",
        "after": "In this invented team account, new members were expected to comment immediately on proposals they had first seen during the meeting. The problem was not simply confidence. We proposed sending the material a day earlier and accepting written questions before discussion. That gives people another route to contribute; we still need to check whether their questions receive a serious response. A channel exists only in practice when participation can influence the discussion.",
        "worked_explanation": "The revised account identifies a role expectation, a barrier and a proposed change in conditions. It avoids diagnosing quieter members or treating the new process as proven inclusion before observing how it works.",
        "variations": [
            "For a career story, specify which aspects of the role changed and which obligations remained. Being more comfortable does not mean every constraint disappeared.",
            "For a leadership presentation, examine permission and consequences as well as invitations to speak. An open microphone alone does not establish that disagreement is safe or consequential.",
            "For a personal introduction, share only the identity details relevant to your contribution and comfortable for you to disclose. The audience does not require access to your whole private life."
        ],
        "failure_case": "Example of what can go wrong: a manager invites everyone to be authentic but penalizes disagreement with the preferred plan. The invitation and the consequences conflict. Another failure presents one person's successful departure from a role as proof that everyone can do the same without cost.",
        "exercise": "Write four lines: what someone was expected to do, why that was difficult for them, what help or change became available and what remains difficult. Use those facts to tell the story without relying on the phrase ‘be yourself.’",
        "self_check": "Does the story name a specific expectation and the person's choices? Can readers see what support changed? Have you blamed someone for conditions outside their control or treated sharing private details as proof that they belong?"
    },
    "authenticity_vs_performance": {
        "title": "Do not judge a whole person by their public style",
        "problem": "A polished speaker is described as fake, or an unpolished moment is treated as proof of sincerity. The presentation turns surface style into a judgment about someone's private identity.",
        "principle": "Describe the public behavior you can see and keep claims about the person within what you know. A carefully rehearsed talk may express a belief the speaker holds. An emotional or awkward moment may still leave the facts uncertain. Explain what preparation or a particular role helps the speaker do; style alone cannot establish honesty or character.",
        "source_title": "Sushant Singh Rajput: inhabiting a character and speaking as oneself serve different functions",
        "source_writeup": "writeups/full-context-address-70.md",
        "source_passages": "Caption numbers 0–19: self-reported difficulty and confidence through characters; 158–168: performance as absorbed attention and a revised success account. These are transcript positions, not verified delivery or clinical evidence. Nothing is inferred from later events in the speaker's life.",
        "source_reading": [
            "The opening distinguishes confidence gained through inhabiting a character from difficulty speaking as himself. The speaker asks permission to falter. These are self-reports and anticipatory remarks, not observed diagnoses or proof that every unscripted statement is more sincere.",
            "Later, performance returns as an example of interest and attention in the present. The activity now has a different explanatory role: it illustrates absorption rather than cover for self-expression. Collapsing both passages into one psychological process would lose that difference.",
            "The account therefore complicates a simple opposition between performance and authenticity. A performed role can be meaningful work while a personal address can be difficult. The transcript does not establish a test for genuine identity or show that the speaker's revised outlook caused later outcomes."
        ],
        "transfer": "Try your draft aloud and decide where notes or rehearsal would help you say it accurately. If you describe another speaker, separate what you observed from what you guessed about their character. ‘She read from notes’ is an observation. It does not tell you whether she believes what she said.",
        "worked_title": "Introducing a rehearsed personal account",
        "before": "I did not prepare anything because I wanted this to be completely authentic.",
        "after": "For this invented introduction: I have written this account down because the details matter and some of them involve other people. These are the parts of the experience I can responsibly share. The preparation helps me keep the sequence accurate; it does not mean I can speak for everyone who was there. I will distinguish what I remember from what I learned afterward.",
        "worked_explanation": "The introduction gives preparation an ethical and practical purpose. It does not equate spontaneity with truth or a script with deception. The boundaries protect other people's experiences and the distinction between memory and later information.",
        "variations": [
            "For a ceremonial speech, rehearsing a difficult passage can support accurate acknowledgment. Emotional expression need not be staged or demanded as evidence of care.",
            "For a professional presentation, explain the role you occupy and the commitments attached to it. A role can guide responsible conduct without claiming to express every private opinion.",
            "For an interview, do not infer honesty from hesitation, eye contact or apparent ease alone. Focus on the content, evidence and acknowledged limits of the answer."
        ],
        "failure_case": "Example of what can go wrong: a presenter insists that tears prove a story is true or polished wording proves it is false. Neither conclusion follows from what we can see. Another failure pressures participants to share painful details to make a workshop feel genuine.",
        "exercise": "Write why you chose your format: notes, slides, rehearsal or conversation. Replace any claim about looking authentic with the purpose that choice serves. Mark personal details that are unnecessary or not yours to share.",
        "self_check": "Have you described what the speaker did without guessing their character? Have you assumed that rehearsing makes someone insincere? Are you judging a claim by its evidence, or treating the speaker's visible emotion as proof?"
    },
    "failure_to_reframe": {
        "title": "Ask whether the goal itself was wrong",
        "problem": "A disappointment leads immediately to trying harder or choosing a new route to the same target. The presentation never considers whether the original success standard was the problem.",
        "principle": "Say what you tried to achieve and what actually happened. Then ask which part needs to change: the method, the target or the belief that reaching the target would help. Meeting an attendance target may still leave the audience's questions unanswered. Explain why you would change the measure, while keeping any missed commitments clear.",
        "source_title": "Sushant Singh Rajput: successive achievements do not resolve the original success equation",
        "source_writeup": "writeups/full-context-address-70.md",
        "source_passages": "Caption numbers 36–74: the initial equation and admission; 85–142: acting, recognition and reported dissatisfaction; 143–168: the revised standard. Caption positions are not playback times; this is the speaker's account, not a clinical finding or proof of what caused the change.",
        "source_reading": [
            "The account begins with money and recognition as ingredients of happiness and success. Admission and family celebration do not eliminate the reported sense of something missing. The disappointment concerns what the achievement was expected to deliver, not the absence of the achievement itself.",
            "A move into acting initially retains money and recognition as goals. Later success brings a reported high, costs and dissatisfaction. The sequence is therefore not simply a move from the wrong career into a passion that immediately solves everything; the old standard travels into the new setting.",
            "The later account emphasizes present experience and excitement while acknowledging continued money and fame. That revises their role rather than literally renouncing them. It does not prove that planning is harmful, that material constraints do not matter or that the revised outlook will produce happiness for others."
        ],
        "transfer": "Write the target and the benefit it was meant to produce. Record whether each happened. If you met the target but missed the benefit, explain why the target may have been the wrong measure. Propose what you would check next time. Keep the useful work, costs and missed promises from the first attempt clear.",
        "worked_title": "Reconsidering a reading group's participation target",
        "before": "Only a few people spoke, so next time we need twice as many attendees and more energetic promotion.",
        "after": "In this invented reading group, we filled every seat but still heard from only three people. Attendance was our target because we assumed a fuller room would produce a richer discussion. That assumption needs checking. For the next session, we propose shorter opening comments and an optional written response before discussion. We will examine whether more perspectives enter the conversation, not call a larger crowd the solution in advance.",
        "worked_explanation": "The original target was achieved, but its assumed benefit did not follow in this example. The revision changes both the standard and the proposed format. It does not label the earlier session worthless or promise that the new format will work.",
        "variations": [
            "For a retrospective, preserve the original aim in the record. Changing the standard should not conceal a missed commitment or erase costs already incurred.",
            "For a personal narrative, frame the change as your interpretation of the experience. Other people may have different constraints and legitimate reasons to retain the original target.",
            "For a proposal, compare a revised standard with improving the existing method. Reframing is one option, not an automatic response to every setback."
        ],
        "failure_case": "Example of what can go wrong: a project misses its promised delivery and the presenter declares that the real goal was team learning all along. That rewrites the commitment instead of examining it. Another failure rejects measurement entirely because one target was poorly chosen.",
        "exercise": "Write the target, the benefit it was supposed to produce and the assumption connecting them. State what actually happened without reinterpretation. Only then propose a revised question and identify what it would change in the next attempt.",
        "self_check": "Was the target missed, or was the promised benefit missing? Does the experience support the new standard? Have you kept responsibility for the original commitment clear and left the new approach open to testing?"
    }
})

LESSONS.update({
    "future_hope_and_action": {
        "title": "Give hope a next action, not a guaranteed ending",
        "problem": "An encouraging closing describes a better future but leaves the listener with no manageable action. Or it promises that effort will certainly produce the desired result, making uncertainty sound like a failure of belief.",
        "principle": "Describe the result you hope for, then name one step someone can take now. Say who can do it, what it requires and why it may help. Keep uncertainty clear: agreeing to test an idea does not tell you whether it will work. The next step should be small enough to describe and assign.",
        "source_title": "William McRaven: collective singing and a closing return to change",
        "source_writeup": "writeups/full-context-address-67.md",
        "source_passages": "Caption numbers 220–250: one singer becomes a group; 260–276: difficulty, recalled lessons and a future-facing close. These positions are not playback times; the training conditions and audience effects were not independently verified.",
        "source_reading": [
            "The mud-flat account describes one person singing and others joining. Conditions reportedly seem less harsh. The narrated change concerns experience and collective participation; it is not a measured change in temperature or evidence of a treatment effect.",
            "The example also depends on other people taking up the action. Removing their contribution would turn a shared event into a misleading account of one person accomplishing everything alone. The story supplies a visible action through which the speech discusses hope.",
            "The closing acknowledges difficulty, compresses earlier lessons and returns to changing the world. Its future promise remains exhortation. A practical adaptation should preserve an actionable next step without copying the address's more absolute claims or its hazardous training context."
        ],
        "transfer": "Name what you hope will improve and one step this audience can take. Say what that step could change or help you learn, who would do it and what help they need. If the work continues after the talk, include a time to review progress before making a larger commitment.",
        "worked_title": "Closing a proposal for a neighborhood reading corner",
        "before": "Together we will transform reading in this community. We just have to believe it is possible.",
        "after": "In this hypothetical proposal, we hope to make it easier for neighbors to find and discuss books. Our next step is one Saturday trial with a borrowed table, an agreed host and a small set of books. We will record what visitors ask for and what prevents them from taking part. That will not establish a lasting program, but it can tell us whether this version is useful enough to develop.",
        "worked_explanation": "The future remains an aspiration, while the next action has a concrete form. The trial produces information rather than a promised transformation. Borrowed resources and an agreed host make support part of the proposal instead of an invisible assumption.",
        "variations": [
            "For a team under pressure, name the support accompanying the request. Encouragement without resources can become another demand placed on already stretched people.",
            "For a public campaign, separate the long-term vision from the immediate contribution. Explain how people can participate without claiming that each small action guarantees the whole outcome.",
            "For a personal address, describe a possibility rather than prescribing a life path. Listeners may reasonably choose different next steps under different constraints."
        ],
        "failure_case": "Example of what can go wrong: an organizer promises that a single event will restore community trust, then interprets modest attendance as a lack of commitment. The claim outruns the action and blames participants for an unrealistic promise. Another failure supplies an inspiring future with no identifiable first step.",
        "exercise": "Write a closing in four sentences: desired future, next action, available support and what remains uncertain. Remove any guarantee that the action cannot establish. Check that the immediate contribution still sounds worthwhile.",
        "self_check": "Is the next step clear and feasible? Does hope remain distinct from prediction? Are support and uncertainty visible, and can the action be useful without promising a transformed future?"
    },
    "difficulty_to_capability": {
        "title": "Name the skill or support a hard moment calls for",
        "problem": "A hard experience is presented as inherently character-building. The audience hears that difficulty is good for them without learning which skill, support or decision could actually help.",
        "principle": "Name what a hard task requires: preparation, coordination, deciding what comes first or asking for help. Explain how someone could obtain that skill or support. Do not assume that going through a difficult experience automatically teaches it, or that people should have to face avoidable hardship to learn.",
        "source_title": "William McRaven: composure in a narrated diving task, alongside coordination and support",
        "source_writeup": "writeups/full-context-address-67.md",
        "source_passages": "Caption numbers 83–97: coordinated paddling and help; 139–161: fatigue and a claimed training benefit; 200–219: darkness during a diving task and composure. These are caption positions, not practical training instructions or verified safety findings.",
        "source_reading": [
            "The underwater-task passage transfers a description of darkness and danger into advice about composure in difficult moments. The named capability is more specific than simply being tough. The lesson analyzes that transfer without endorsing the literal activity or tactical account.",
            "Elsewhere, coordinated paddling emphasizes assistance and combined contribution. That context matters when interpreting the address's individual imperatives: support is present in the broader argument and should not disappear from a summary of capability.",
            "The extra-training story describes accumulating fatigue before claiming improved strength. The selected account does not establish that punitive exertion benefits everyone or that harmful conditions should be recreated. A responsible adaptation asks what capability is needed and how it can be supported without treating suffering as the method."
        ],
        "transfer": "Describe the task someone has to complete, then list the preparation, equipment or help it requires. Ask whether any unnecessary difficulty can be removed. For the speaking exercise, choose an ordinary task you can discuss without asking anyone to repeat dangerous activities described in a source.",
        "worked_title": "Preparing a team for a busy public information desk",
        "before": "The opening weekend will be chaos, but pressure makes people stronger. Stay calm and push through.",
        "after": "For this invented briefing, the difficult moment is likely to be several visitors asking different questions at once. The capability we need is orderly triage: acknowledge the queue, answer the short routing question and refer the specialist question to the named coordinator. We will rehearse that sequence and agree when to call for another volunteer. If the desk remains overloaded, staffing and process need review; endurance alone is not the plan.",
        "worked_explanation": "The revision identifies a concrete demand, a rehearsable response and a support route. It treats overload as information about the setup rather than proof that volunteers need more grit. Calm is not demanded as an unexplained personality trait.",
        "variations": [
            "For a project presentation, distinguish a skill gap from insufficient resources. Training cannot by itself solve every capacity problem.",
            "For a retrospective, explain which preparation or assistance helped and what remained costly. A favorable outcome does not make the original conditions desirable.",
            "For a workshop, practise the capability at a manageable scale. Learners do not need to experience the source story's danger or distress to inspect its communication structure."
        ],
        "failure_case": "Example of what can go wrong: a supervisor withholds instructions so newcomers can learn resilience, then blames them for predictable mistakes. The imposed difficulty does not constitute a teaching method. Another failure names confidence as the solution when the missing ingredient is access to information.",
        "exercise": "Replace a sentence praising toughness with three details: what someone must do, the skill they need and the help that makes the task possible. Add one situation in which you would change the task instead of asking people to keep struggling.",
        "self_check": "Have you named a skill someone could practise or demonstrate? Is there a reason to think the task teaches that skill? Have you included the equipment and help needed, and considered removing unnecessary difficulty?"
    },
    "unfinished_work_to_commitment": {
        "title": "Name what is unfinished and what you will do next",
        "problem": "A success story ends as though the problem has been solved permanently. When the issue returns in a new setting, the speaker either hides the recurrence or treats it as evidence that all earlier progress was false.",
        "principle": "Say what improved, what remains difficult and what you will do next. A successful first attempt may need more preparation when the setting changes. Name that continuing work instead of promising that the problem is solved forever. Make the commitment specific enough for someone to ask later whether you carried it out.",
        "source_title": "Dwayne Johnson with Oprah: an identity breakthrough followed by renewed difficulty in Hollywood",
        "source_writeup": "writeups/full-context-interview-24.md",
        "source_passages": "Caption numbers 306–341: the reported wrestling breakthrough; 362–410: renewed pressure, uncertainty, work and a new ability to act. Caption positions are not playback times, and later results are not independently checked here.",
        "source_reading": [
            "The wrestling account presents a consequential opportunity to speak differently after permission for microphone time is granted. The guest describes a breakthrough, but that part of the interview is not the end of the identity narrative.",
            "The later Hollywood passage says that pressure to change returned and that he spent years figuring out his identity again. The recurrence complicates the earlier never-looking-back formulation. A faithful account preserves the new difficulty instead of editing the story into a single irreversible transformation.",
            "The guest describes uncertainty about achieving his vision, willingness to work and a change of agency. These are elements of his reported response, not proof that the same response will work elsewhere. The host's affirmation also does not independently validate the causal account."
        ],
        "transfer": "Write what is working now and whether it would keep working if the people, workload or setting changed. Name the remaining task, who will do it and when they will check the result. Explain how this task builds on the earlier achievement. Keep the promise limited to work you can actually commit to.",
        "worked_title": "Explaining why a successful event process needs another revision",
        "before": "We solved registration last year. Any problems now are just people not following the process.",
        "after": "In this hypothetical update, last year's single-session registration worked for that event. This year, visitors can attend several sessions, and the old form does not show conflicting choices. The earlier work still gives us a useful contact list and confirmation route. Our next commitment is to test how the form handles two overlapping sessions before opening registration. We solved one version of the problem, not every future version.",
        "worked_explanation": "The update retains what remains useful while identifying the changed condition. The commitment addresses the new failure mode and supplies a concrete check. It avoids treating recurrence as either personal blame or proof that last year's work had no value.",
        "variations": [
            "For a personal narrative, allow a lesson to require relearning. Acknowledging recurrence can make the account more accurate without requiring a dramatic confession of failure.",
            "For a project handoff, document which conditions the solution assumes. The next owner needs to know what would make the earlier success insufficient.",
            "For a long-running initiative, name continuing maintenance separately from new development. A commitment should not hide unlimited work inside the word finished."
        ],
        "failure_case": "Example of what can go wrong: a presenter announces a problem permanently solved after one pilot, then dismisses later failures as exceptions that do not count. The completion claim has become impossible to challenge. Another failure uses unfinished work as a reason to avoid ever stating an accountable commitment.",
        "exercise": "Write three columns: what is solved here, what remains uncertain and what now needs doing. Choose one unfinished task. Name who will do it, when they will review it and what they will check. Keep one sentence recognizing the work already completed.",
        "self_check": "What exactly was resolved? What changed? Is the next commitment specific and reviewable? Have you avoided both permanent-success language and the dismissal of genuine earlier progress?"
    }
})

LESSONS.update({
    "invitation_to_low_barrier_entry": {
        "title": "Make the first step clear and limited",
        "problem": "People may be interested in a cause or activity but cannot tell what joining requires. A broad invitation to get involved hides the time, knowledge or commitment expected of them.",
        "principle": "Make the first step easy to understand: what happens, how long it takes, what preparation is needed and what people are agreeing to. State any later commitment separately. Before calling participation easy, check what it requires from the person being invited, including time, travel, equipment or help.",
        "source_title": "Jennifer Aniston: a personal invitation provides a route into participation",
        "source_writeup": "writeups/full-context-address-68.md",
        "source_passages": "Caption numbers 41–51: the Marlo Thomas invitation and gala experience; 52–55: later participation described as both rewarding and difficult. These are caption positions, not playback times; the account does not show that everyone could take part.",
        "source_reading": [
            "The address gives a particular invitation a place in the speaker's route into philanthropy. Rather than describing involvement as a spontaneous moral transformation, it names an encounter through which participation became concrete.",
            "A gala film reportedly contributes to a desire to become involved. This remains the speaker's retrospective account, not a measured conversion effect. Access to a named person's invitation and a gala also depends on circumstances that cannot be assumed for a general audience.",
            "The later encounter is described as both the best and hardest day of the year. Entry does not make the continuing activity effortless. The teaching adaptation therefore focuses on making a first step explicit; it does not claim that this particular invitation was accessible to everyone or that subsequent participation had no costs."
        ],
        "transfer": "Describe the first action separately from any ongoing role. List practical requirements and possible barriers, including time, location, equipment and social expectations. Offer a way to ask questions or decline. Do not use a small initial request to conceal a larger obligation that participants will discover only after accepting.",
        "worked_title": "Inviting newcomers to help with a community newsletter",
        "before": "Join our amazing team and help us change the community. No experience needed—just commitment.",
        "after": "In this hypothetical invitation, you can join one thirty-minute online orientation to see how the newsletter is made. You do not need to bring an article or accept a regular role. We will explain the available tasks and their time requirements, and you can decide afterward whether any fit. If the meeting time does not work, we can provide the same information in writing. This is an introduction, not a sign-up for ongoing work.",
        "worked_explanation": "The invitation gives the first step a duration, purpose and boundary. It provides an alternative route and postpones the larger decision until participants have the information needed to make it. The organizer still needs to deliver those promised conditions.",
        "variations": [
            "For a workshop, state what materials and prior knowledge are required. Calling a session beginner-friendly does not remove an unexplained prerequisite.",
            "For a volunteer role, distinguish an observation visit from training and responsibility. Participants should know when expectations change.",
            "For a professional network, offer a useful first interaction without demanding personal disclosure, a public introduction or an immediate reciprocal favor."
        ],
        "failure_case": "Example of what can go wrong: an organizer advertises a casual introduction and then assigns attendees recurring shifts before they leave. The small invitation concealed the actual commitment. Another failure calls an event accessible while ignoring a fee, travel requirement or unavailable equipment.",
        "exercise": "Write an invitation stating what to do first, how long it takes, what preparation is needed, another way to take part and any later commitment. Ask which requirement could still keep someone from joining and what you could change.",
        "self_check": "Can a newcomer understand the first step? Is the commitment honestly limited? Are hidden costs visible, and can someone decline further involvement without being misrepresented?"
    },
    "familiarity_to_scope": {
        "title": "Use a familiar example to explain, not to prove",
        "problem": "An abstract system feels remote. Listing recognizable places can make it tangible, but the audience may mistake recognition of the examples for evidence that the entire claim is true.",
        "principle": "Move from familiar examples to a clear statement of what your claim covers. Explain what the examples have in common and what they help explain. They do not show how common the pattern is. Unlike the pattern that moves between a total and one person, this one uses several everyday settings to explain an idea's range.",
        "source_title": "A Matrix dialogue excerpt: ordinary settings carry a sweeping account",
        "source_writeup": "writeups/full-context-scene-07.md",
        "source_passages": "Caption numbers 31–44: naming unease; 45–58: familiar settings; 59–65: the broader metaphor. This is scripted fiction with transcript limits, not evidence of real-world control, performer beliefs or successful persuasion.",
        "source_reading": [
            "The dialogue first gives a name to an inarticulate feeling. The reply identifies the Matrix, but that textual response does not establish independent confirmation or full understanding of the account offered.",
            "The explanation then names the room, window, television, work, church and taxes. These settings connect a sweeping assertion to recognizable parts of ordinary life. Their familiarity makes the scope easier to picture without logically validating the assertion.",
            "A later metaphor extends the fictional account. The scene also contains an authority frame and asymmetrically valued choices, so its explanatory vividness should not be confused with neutral options or informed consent. The safe transfer is making scope clear, not borrowing manufactured urgency or an unsupported totalizing claim."
        ],
        "transfer": "Choose a few familiar situations that truly fit the idea you are explaining. Say what they have in common and what your claim does not cover. Use other evidence before saying the pattern is common or caused by something. Do not assume that recognizing an example means the audience agrees with your explanation.",
        "worked_title": "Introducing the idea of a handoff in a community organization",
        "before": "Handoffs are everywhere, and poor handoffs explain all our problems.",
        "after": "In this invented briefing, a handoff occurs when a booking becomes a room setup, when a submitted article becomes an editing task, and when a returned key becomes the next host's responsibility. These situations share a transfer of information or ownership. They illustrate what we mean by a handoff; they do not show that every delay has that cause. Today we will examine the room-setup transfer, where we have a specific missing-information example.",
        "worked_explanation": "The familiar settings establish a useful category, then the presentation narrows to one clear example. The shared connection is stated directly. The examples do not prove a general cause of organizational problems.",
        "variations": [
            "For a technical topic, choose contexts the audience actually knows and explain the common relationship. A familiar object with an unfamiliar process may still need explanation.",
            "For a public talk, include a boundary example showing where the concept does not apply. This prevents a broad idea from absorbing every experience by definition.",
            "For a mixed audience, avoid treating one cultural or institutional routine as universal. Offer more than one route into the concept without assuming shared experience."
        ],
        "failure_case": "Example of what can go wrong: a speaker lists several everyday frustrations and declares that all are evidence for one hidden cause. Recognition of the frustrations does not establish the explanation. Another failure chooses examples connected only by mood rather than a meaningful common relationship.",
        "exercise": "List three familiar examples of your idea and say what they have in common. Add a similar example that does not fit, explaining why. Write the sentence that connects the examples to the idea without using ‘everywhere’ or ‘always.’",
        "self_check": "Have you named what the examples share? Do they all fit your explanation? Have you used their familiarity to claim, without evidence, that something is common, caused by the same thing or accepted by everyone?"
    }
})

LESSONS.update({
    "emotion_to_composure": {
        "title": "Tell a personal story, then return to the shared task",
        "problem": "A personal account carries emotional weight, and you need to continue without pretending the feeling has disappeared or making the audience responsible for restoring your composure.",
        "principle": "Decide which part of a personal memory helps with the subject of the talk. After telling it, explain that connection and return to the shared task. Allow yourself to pause or leave out details you do not want to share. A planned sentence can help you find your place; it cannot guarantee how you will feel.",
        "source_title": "Taylor Swift: reported old feelings on stage and a shift toward the audience",
        "source_writeup": "writeups/full-context-interview-27.md",
        "source_passages": "Caption numbers 317–338: the reported onstage experience and crowd response; 339–357: evolving craft and hopes for listeners. Caption positions are not playback times; no performance or emotional state was independently observed.",
        "source_reading": [
            "A fan's question elicits an account of experiencing old feelings during performance. The answer describes a subsequent shift when the crowd responds. The sequence is the speaker's report of her experience, not an observation of every performance.",
            "The audience therefore appears in the account as part of the immediate setting rather than only a distant recipient of a finished song. That does not establish that audience response reliably changes emotional experience or that performers should depend on applause to continue.",
            "The following discussion turns toward artistic choices and hopes that listeners will grow with the work. The interview moves from remembered feeling into an account of ongoing craft. The teaching adaptation below provides a textual transition; it does not infer an unobserved technique for controlling emotion."
        ],
        "transfer": "Decide how much personal detail the talk needs. Write a simple way back to the subject and keep another version without the sensitive part. You can pause, use notes or change course; you do not need to share something private to prove you are being sincere. Protect other people's privacy as carefully as your own.",
        "worked_title": "Returning from a personal memory during an archive talk",
        "before": "This is very emotional, so please bear with me. I am not sure I can get through all the details.",
        "after": "In this invented script: this photograph matters to me because it is the only image we have of that gathering. I will leave the private parts of the story there. For today's archive discussion, the useful detail is the note on the back: it preserves a name we could not have recovered from the image alone. That is why the next section concerns recording context alongside photographs.",
        "worked_explanation": "The bridge identifies the relevant detail and sets a privacy boundary. It makes continuation possible at the level of the script without promising that the speaker will feel composed. A shorter alternative could simply introduce the note without the personal memory.",
        "variations": [
            "For a ceremonial address, agree the scope of personal details in advance where others are involved. The occasion does not grant unrestricted permission to tell their stories.",
            "For a professional presentation, include a personal account only when it serves the topic. Emotional intensity is not a substitute for the evidence behind a recommendation.",
            "For a rehearsal, practise the transition and the alternative version. The aim is a usable route through the material, not a requirement to reproduce a particular emotional display."
        ],
        "failure_case": "Example of what can go wrong: a facilitator insists that participants share painful experiences and then praises those who appear calm. The activity imposes disclosure and judges an internal state from outward behavior. Another failure uses a moving story to make questioning the proposal seem insensitive.",
        "exercise": "Mark the personal passage in a draft. Write its purpose, the private details you will omit and one sentence returning to the shared task. Prepare a version that reaches the same point without the personal passage.",
        "self_check": "Is the material necessary and yours to share? Is there a clear transition and an alternative? Have you avoided making emotional display a credibility test or demanding reassurance from the audience?"
    },
    "despair_to_hope": {
        "title": "Name what is hard and what can still be done",
        "problem": "A description of helplessness leaves no room for a person's choices, but a sudden optimistic ending can erase the seriousness of what came before. The audience is asked to feel differently before being given a reason to reconsider.",
        "principle": "After describing a difficulty, give a concrete reason that the situation may allow more than it first seemed: help is available, an option remains or a condition has changed. Explain what this new information leaves unresolved. Offer the audience a reason to reconsider without telling them how they should feel.",
        "source_title": "The Vivekananda-labeled composite text: helplessness followed by spiritual affirmation",
        "source_writeup": "writeups/full-context-historical-01.md",
        "source_passages": "Caption numbers 257–316: storm, boat and crushing-force images followed by an affirming spiritual identity. The upload combines historical texts with damaged captions; it is not verified original delivery or evidence of listener relief.",
        "source_reading": [
            "The passage uses images of forces acting on a person to describe helplessness. The person seems to have few choices or ways to act.",
            "An affirming spiritual identity follows. Within the argument, this supplies a different way to understand the person's relation to those conditions. The sequence changes the evaluative and theological frame rather than documenting an external problem disappearing.",
            "These religious beliefs belong to the source and should be described respectfully. The transcript does not show that listeners felt better or agreed, and it does not prove the religious claims. A nonreligious lesson can examine the change in the passage without presenting this belief as an answer for everyone."
        ],
        "transfer": "State what is difficult without exaggerating it for dramatic effect. Offer a concrete reason the initial interpretation may be incomplete: available help, a remaining option or a changed constraint. Preserve what that reason does not solve. If you have no basis for reassurance, honest acknowledgment may be more appropriate than manufacturing a hopeful turn.",
        "worked_title": "Addressing disappointment after a venue becomes unavailable",
        "before": "Losing the venue is a disaster, but everything happens for a reason and this will turn out better.",
        "after": "In this hypothetical update, losing the venue means the planned exhibition cannot open on that date. The preparation is not all lost: the object list, captions and contributor permissions remain useful. We have not secured a replacement space, so I cannot promise a new opening. We can now assess a smaller display or a later date using work already completed. The setback changes the plan without erasing every available option.",
        "worked_explanation": "The revised frame rests on identifiable work and options, not a claim that disappointment guarantees a better outcome. It names the unresolved venue problem plainly. The hopeful element is a narrower interpretation of what has been lost.",
        "variations": [
            "For a team update, distinguish remaining options from approved plans. Possibility can support discussion without being announced as a commitment.",
            "For a personal address, offer your interpretation as your own. Other people may not share the same meaning or be ready to adopt it.",
            "For a sensitive situation, avoid forced silver linings. Acknowledging difficulty and offering practical support can be sufficient without narrating a transformation."
        ],
        "failure_case": "Example of what can go wrong: a leader responds to lost resources by insisting that constraints are always blessings. The claim denies costs and discourages realistic planning. Another failure invents a reassuring outcome because the presentation seems to need an uplifting close.",
        "exercise": "Write the difficult fact, the interpretation it initially suggests and one evidence-based reason that interpretation may be incomplete. Add a sentence preserving what remains unresolved. Remove any prediction you cannot support.",
        "self_check": "What justifies the hopeful turn? Does it change the interpretation without denying the facts? Are listeners free to respond differently, and is uncertainty still explicit?"
    },
    "unity_across_scale": {
        "title": "Name what groups share without hiding their differences",
        "problem": "A presentation needs to connect people or activities at different scales, but unity language can imply that their needs, beliefs or responsibilities are identical.",
        "principle": "Name exactly what different groups share: a purpose, a question or work that depends on each other. Then explain where their needs and responsibilities differ. Hosts and visitors may both want a useful workshop while needing different information to take part. Check the shared purpose with the people concerned; saying ‘we all agree’ does not make it true.",
        "source_title": "The Vivekananda-labeled composite text: individuality, universal consciousness and connecting imagery",
        "source_writeup": "writeups/full-context-historical-01.md",
        "source_passages": "Caption numbers 404–467: individuality, universal consciousness and an appeal to scientific unity; 553–599: colored-glass and thread imagery. These are transcript positions in a composite text, not verified original delivery or current scientific consensus.",
        "source_reading": [
            "The argument responds to an objection about lost individuality by expanding toward universal consciousness and invoking scientific unity. This is the source's philosophical and theological claim; the invocation of science does not establish an independently verified convergence.",
            "Later imagery involving colored glass and a connecting thread returns to the question of apparent contradictions. The images offer a way to understand plurality through a common approach. They do not independently record agreement among the traditions being discussed.",
            "The broader source also retains hierarchical and demeaning classifications, so a summary of uncomplicated inclusion would be incomplete. The teaching adaptation borrows the need to specify a shared relation while rejecting the inference that a unifying account makes all differences disappear."
        ],
        "transfer": "List what each group wants, what it can decide and what it needs from the others. Use those details to write one specific statement of what they share. Check that statement with the groups before speaking for them. Include a difference that still matters to the proposal.",
        "worked_title": "Opening a meeting between an exhibition's contributors",
        "before": "We are all one team, so we all want the same thing and should work the same way.",
        "after": "For this invented meeting, lenders, writers and volunteers share the aim of a clear exhibition that treats the objects responsibly. Their obligations differ: lenders need return conditions respected, writers need accurate information, and volunteers need workable shifts. The shared purpose connects these roles; it does not cancel their constraints. Today we will identify where one role's needs affect another's plan.",
        "worked_explanation": "The opening makes unity a specific shared aim rather than a claim of identical interests. It names distinct responsibilities and turns the connection into a practical discussion. Agreement on the purpose would still need to be checked with the participants.",
        "variations": [
            "For a cross-team project, describe the common outcome and the separate decisions needed to pursue it. Do not use shared ownership to leave actual ownership undefined.",
            "For a public address, distinguish shared stakes from shared beliefs. People can be affected by the same issue while disagreeing about its causes or remedies.",
            "For a conceptual explanation, state which relationship repeats across scales and where the analogy breaks. Similarity at one level does not imply identical behavior at another."
        ],
        "failure_case": "Example of what can go wrong: an organizer invokes unity to silence a contributor's concern about workload. The shared purpose becomes a reason to erase a real difference. Another failure uses a single metaphor to claim that individuals, teams and institutions operate by the same rules.",
        "exercise": "Write one purpose the groups in a project share and a different task for each of three groups. Show two places where one group's work needs another's. Draft an opening that explains the shared purpose and these different jobs before asking for cooperation.",
        "self_check": "What exactly do the groups share, and have they agreed to it? Can listeners still see the different needs and responsibilities? Does the shared purpose help explain the work while leaving people free to disagree?"
    }
})

LESSONS.update({
    "analogy_transfer": {
        "title": "Use one part of an analogy, not the whole story",
        "problem": "An analogy joins two situations, but the audience may carry over more than the comparison supports. A familiar example becomes an implied claim that the experiences are equivalent.",
        "principle": "Say exactly what two things have in common, then say where the comparison ends. An analogy explains one idea by comparing it with another. A callback returns to an image or phrase used earlier. A comparison can help explain an idea, but it cannot prove that the two things work the same way.",
        "source_title": "Erika Kirk's memorial address transcript: a flight interval used in a support story",
        "source_writeup": "writeups/full-context-memorial-01.md",
        "source_passages": "Caption numbers 97–123: a reported comparison with the last fifteen minutes of a difficult flight. These are caption positions, not verified media times. The account establishes neither a clinical method nor an obligation for others to respond similarly.",
        "source_reading": [
            "The address transcript reports a support story that compares getting through another short interval with the last fifteen minutes of a difficult flight. The shared feature is the limited interval, not equivalence between travel discomfort and bereavement.",
            "The speaker says the words helped her. That is a report of personal helpfulness within her account. It does not demonstrate that the comparison will help other people or establish a general method for responding to grief.",
            "The broader address includes religious and organizational claims that remain attributed rather than independently verified. This lesson isolates the analogy's structure without endorsing those claims, inferring recovery or presenting the analogy as treatment. Its practice example uses an ordinary drafting task instead."
        ],
        "transfer": "Write the source situation, the target situation and the exact relationship they share. Explain the target using that relationship, then state one important difference. If the analogy concerns another person's painful experience, do not presume it is welcome or equivalent to your chosen comparison. Often the more respectful choice is not to use it.",
        "worked_title": "Explaining how to review a long exhibition text",
        "before": "Editing is like a marathon, so just keep pushing until you finish.",
        "after": "In this invented workshop, reviewing a long text can be organized like checking a route one section at a time: first confirm the opening's direction, then inspect each transition, then check the destination. The comparison concerns the order of inspection. It does not mean writing has one correct path or that you should work without breaks. For this exercise, review just the transition between the first two sections.",
        "worked_explanation": "The analogy transfers a sequence of checks and immediately limits the comparison. The limited task makes the relationship usable. It does not import endurance, competition or a single finish line merely because the image involves a route.",
        "variations": [
            "For a technical explanation, map the components explicitly and name properties that do not transfer. Familiar machinery can otherwise suggest false capabilities or failure modes.",
            "For a workshop, ask participants where the comparison breaks. This can reveal whether they understood the intended relation rather than memorized the image.",
            "For a personal account, describe why a comparison mattered to you without prescribing it to others. Reported meaning and general effectiveness remain different claims."
        ],
        "failure_case": "Example of what can go wrong: a presenter compares a team to a family and then treats disagreement or leaving as betrayal. The analogy imports obligations that were never agreed. Another failure uses a familiar physical process as proof that a social process must behave identically.",
        "exercise": "Make a three-column map: a feature of the familiar situation, the matching feature in your topic, and a feature that does not match. Write the comparison using only the parts that truly match, then add a sentence explaining where it stops being useful.",
        "self_check": "What exactly transfers? What does not? Does the comparison explain rather than prove? Could it trivialize an experience or import an obligation the audience has not accepted?"
    },
    "moral_to_memorial": {
        "title": "Move from judging a decision to remembering a person",
        "problem": "A tribute follows a contested decision, and commemoration is mistaken for proof that the decision was right. Conversely, a remembrance can be overtaken by argument when the occasion has a different immediate purpose.",
        "principle": "Say what this part is for: judging a decision, reviewing the facts or remembering someone. A memorial can honor a relationship or contribution without settling every question about the person's choices. Keep those purposes separate; do not use a moving tribute to shut down fair questions elsewhere.",
        "source_title": "A Star Trek II excerpt: moral rationale gives way to commemoration",
        "source_writeup": "writeups/full-context-scene-11.md",
        "source_passages": "Caption numbers 24–33: a many/few/one rationale; 44–54: memorial language and a decision not to debate wisdom; 55–59: personal tribute. This is fictional dialogue with damaged captions and unverified speaker assignments, not an ethical proof or practical instruction.",
        "source_reading": [
            "The practical exchange compares many, few and one to explain why the characters act. The damaged captions do not let us reconstruct every action or the full reasoning from memory of the film.",
            "The clearer memorial passage acknowledges sorrow and treats the sacrifice as meaningful. It also says the proceedings will not debate the deceased's wisdom. That sentence marks a commemorative stance rather than supplying an argument that resolves the ethical question.",
            "The personal tribute that follows belongs to that changed purpose. The excerpt can illustrate a transition between kinds of speech, but scripted commemoration cannot establish that self-sacrifice is generally right, that every listener agrees or that grief has ended."
        ],
        "transfer": "Before writing a tribute, choose the contribution or relationship you can describe accurately. Check which memories you have permission to share. If there are unresolved questions about someone's decisions, explain where those questions will be addressed when that is relevant. Do not use the tribute to claim that everyone agrees or that further questions are unwelcome.",
        "worked_title": "Separating a volunteer tribute from a project review",
        "before": "Because we admire the founder, there is no reason to question the decisions made during the project.",
        "after": "In this invented commemoration, today's short tribute recognizes the founder's years of organizing local reading sessions and the relationships people formed through them. It is not the review of the project's finances or future structure; those questions have their own meeting and records. We can remember a contribution accurately without asking this tribute to settle every decision associated with it.",
        "worked_explanation": "The passage defines the tribute's scope and retains an explicit place for review. It neither converts affection into proof nor uses the review to erase the contribution being remembered. The distinction depends on the promised review genuinely remaining available.",
        "variations": [
            "For a ceremonial address, choose specific, supportable contributions rather than claims of flawless character. A tribute need not become an exhaustive verdict on a life.",
            "For an organization, keep records and review of responsibilities separate from the memorial. Respect does not require hiding facts.",
            "For a mixed audience, avoid assuming that everyone had the same relationship with the person. Leave room for private and differing responses."
        ],
        "failure_case": "Example of what can go wrong: an organization invokes a memorial whenever someone asks about unresolved obligations, while never scheduling the promised review. The distinction becomes an evasion. Another failure treats a moving tribute as evidence that a disputed choice was justified.",
        "exercise": "Write two separate openings: one for a tribute and one for a factual review. Identify what each can establish and what belongs elsewhere. Add a transition that preserves both purposes without making one silence the other.",
        "self_check": "Is the passage's purpose explicit? Are factual claims supportable? Does remembrance remain distinct from ethical proof, and are legitimate questions still allowed an appropriate route?"
    }
})

LESSONS.update({
    "grief_loss_and_continuation": {
        "title": "Leave room for loss when speaking about what continues",
        "problem": "A remembrance turns too quickly into a message about moving forward. The speaker's account of meaning or continuing work can sound like an instruction that others should have reached the same conclusion.",
        "principle": "Acknowledge the loss before discussing any work that continues. If you describe what the loss means to you, speak for yourself and leave room for others to feel differently. Say which commitments you can make without assigning them to everyone else. Continuing a project or responsibility does not mean that grief has ended.",
        "source_title": "Erika Kirk's memorial address transcript: continuing work beside the pain of absence",
        "source_writeup": "writeups/full-context-memorial-01.md",
        "source_passages": "Caption numbers 199–216: incomplete work distinguished from unfinished personal business; 378–414: organizational intentions; 454–456: return to personal address. These are transcript positions, not verified media times, current leadership facts or evidence of recovery.",
        "source_reading": [
            "The address distinguishes incomplete work from unfinished personal business while retaining the pain of missing a spouse. The coexistence matters: a statement about the relationship's meaning does not erase the stated loss.",
            "Later, the speech turns to organizational leadership, events and expansion intentions. Those are attributed plans in the source, not verified achievements or current facts. They show a move into ongoing responsibility without supplying evidence that mourning has ended.",
            "The closing returns to direct address to the deceased. The full structure therefore includes both organizational continuation and personal relationship. This lesson analyzes that arrangement without endorsing the political or religious program, inferring private feelings or imposing its model on other bereaved people."
        ],
        "transfer": "If an occasion requires both remembrance and practical information, give each a clear place. Use specific, approved memories and state practical arrangements without presenting them as a cure or a duty to feel differently. Check whose experience you are speaking for. Some occasions need only remembrance; continuation need not be forced into every tribute.",
        "worked_title": "A community group's remembrance and practical notice",
        "before": "The best way to honor our colleague is to stop being sad and carry on exactly as before.",
        "after": "In this invented address: we remember the care our colleague brought to welcoming new members. People here will have different memories and different ways of experiencing this loss. The group has agreed to keep next month's gathering on the calendar, with another volunteer handling the welcome. That arrangement is practical information, not a request to feel ready or to attend. Today there is also room simply to remember.",
        "worked_explanation": "The passage separates a contribution being remembered from an agreed logistical arrangement. It does not claim the event will provide healing or make participation a test of respect. The speaker avoids assigning a shared internal state to everyone present.",
        "variations": [
            "For an organizational notice, distinguish essential arrangements from optional commemorative activities. People should not need to disclose private feelings to decline an activity.",
            "For a personal tribute, say what the person meant to you rather than claiming to summarize every relationship they had. Confirm sensitive details before sharing them.",
            "For a mixed audience, avoid assuming shared beliefs about loss or its meaning. A specific remembrance can be offered without requiring everyone to adopt the same interpretation."
        ],
        "failure_case": "Example of what can go wrong: a leader says that anyone who cared about the deceased will volunteer for a new initiative. The tribute turns grief into leverage for a commitment. Another failure announces that the group has found closure because an event has been scheduled.",
        "exercise": "Use a fictional or public, non-sensitive scenario rather than requiring a personal loss. Write one sentence of remembrance, one acknowledging different responses and one practical notice. Remove any sentence that tells people how they must feel or makes participation a moral test.",
        "self_check": "Whose experience can you speak about accurately? Have you kept practical tasks separate from expectations about how people should feel? Are private details protected, and can people choose whether to take part?"
    },
    "sorrow_and_continuation": {
        "title": "Name what continues without erasing the loss",
        "problem": "A narrative includes loss and subsequent activity, but the transition makes the second seem to cancel the first. Continuing work is presented as if it demonstrates emotional resolution.",
        "principle": "Put two facts side by side: something has been lost, and some activity or responsibility continues. Do not say one caused or resolved the other unless the account supports that. This small pattern looks at how neighboring passages relate; the larger lesson is about speaking to people after a loss.",
        "source_title": "A Star Trek II excerpt: memorial loss followed by a new layer of mission narration",
        "source_writeup": "writeups/full-context-scene-11.md",
        "source_passages": "Caption numbers 44–59: sorrow and personal tribute; 60–75: music markers and mission narration. This is fictional material with damaged captions and unverified edit continuity, not evidence that grief ends or that a musical transition causes an audience response.",
        "source_reading": [
            "The memorial passage acknowledges sorrow while connecting the death to protected new life. It treats the sacrifice as meaningful within the fictional account, but that interpretation does not establish an obligation for real people to find equivalent meaning in loss.",
            "The personal tribute is followed by music markers and continuing exploration in mission narration. The latter is a new narrative layer. The available text supports identifying its place after the memorial, not reconstructing the exact edit, performance or musical effect.",
            "The sequence therefore puts loss and continuation alongside one another. Nothing in the transcript text proves that the characters' grief has ended or that viewers experienced consolation. The lesson concerns avoiding that unsupported inference when writing or summarizing a transition."
        ],
        "transfer": "Check the words linking a passage about loss to one about what continues. Words such as therefore, finally or now can claim more than you know. Choose words that show the real link: afterward, alongside, or simply say that both are true. Do not invent a tidy ending just to make the story feel complete.",
        "worked_title": "Closing an account of a beloved venue's final season",
        "before": "The old hall closed, but we found a new space, so everyone moved on and the story ended happily.",
        "after": "In this invented account, the old hall closed after its final season. Members still speak about what they miss: the stage, the familiar entrance and the place where they met after rehearsals. The group now rehearses in a different room. That lets the work continue; it does not make the rooms interchangeable or tell us how every member feels about the move.",
        "worked_explanation": "The revision uses a change of place, not a comparison with bereavement. It keeps the continuing activity and the reported loss as separate facts. It does not claim that everyone reaches the same emotional ending.",
        "variations": [
            "For a documentary account, distinguish chronological sequence from a claim about emotional change. A later scene of activity cannot by itself establish recovery.",
            "For an organizational history, record what was preserved and what was not. Continuity of a name or activity does not mean every relationship or resource survived.",
            "For a tribute, end with a particular memory when a future-facing message would be premature or inappropriate. A closing need not resolve everything it has acknowledged."
        ],
        "failure_case": "Example of what can go wrong: a writer describes people returning to work and concludes that they are no longer affected by a loss. The visible action does not establish that internal state. Another failure treats a replacement as equivalent without asking what mattered about the original.",
        "exercise": "Write two short paragraphs: one about an ordinary loss or ending, and one about an activity that continues. Try three ways to connect them. For each, ask what it says about cause or feeling. Keep only what your facts support.",
        "self_check": "Does the passage allow work to continue while people still feel the loss? Have you assumed how someone feels just because they resumed an activity? Does the ending leave unresolved feelings or questions open?"
    },
    "audience_shift": {
        "title": "Name who you are addressing when the request changes",
        "problem": "A speaker moves from one person or group to another without signaling the change. Responsibilities become blurred, or a broader audience is recruited to distract from an unanswered challenge.",
        "principle": "Say when you turn from one person or group to another, and why the new group matters. Be clear about what you are asking of each group. Turning to a larger audience does not answer an earlier objection; keep unanswered questions visible. This differs from a general invitation because it is about changing who is being addressed.",
        "source_title": "A Scarface excerpt: interpersonal criticism becomes an accusation against observers",
        "source_writeup": "writeups/full-context-scene-06.md",
        "source_passages": "Caption numbers 59–79: a reply challenging conduct and responsibility; 89–107: the speaker turns to the people watching and criticizes them. This is scripted fiction with damaged captions and uncertain speaker turns. The scene has not been checked against the video and is not a model of respectful conduct.",
        "source_reading": [
            "The earlier reply challenges supposed moral superiority and asks about practical responsibilities. Those criticisms remain part of the exchange and matter when interpreting the later speech.",
            "A plural address broadens the rhetorical audience and accuses observers of needing someone to label as bad. The speaker redirects moral scrutiny toward those judging him. The textual shift is visible even though exact on-screen addressees and scene blocking were not verified.",
            "The redirection does not answer the preceding criticisms. A memorable counteraccusation is not proof of a successful rebuttal, and the excerpt contains abusive conduct that should not be taught as a presentation technique. It is a useful negative case: an audience shift can conceal unfinished argumentative work."
        ],
        "transfer": "Before turning to another group, answer the current question or say when you will return to it. Then name the next group and what you need from them: ‘For the hosts, the next task is to confirm the room.’ If someone belongs to both groups, explain how the two requests fit together. Check that the change has not left a concern unanswered.",
        "worked_title": "Addressing hosts and participants at the start of a workshop",
        "before": "Everyone should make sure this runs smoothly. If anyone has concerns, remember that we are all doing our best.",
        "after": "In this hypothetical opening: to participants, please tell the host if an instruction is unclear; you do not need to solve the process yourself. To the hosts, record the question and check whether the rest of the group needs the clarification. The concern raised earlier about the room layout is still open, and the coordinator will review it before the activity starts. Different roles carry different tasks, and naming them does not close the unresolved issue.",
        "worked_explanation": "The opening identifies two audiences and gives each a limited role. It keeps the earlier concern visible instead of replacing it with an appeal to goodwill. The shift supports coordination rather than recruiting one group against another.",
        "variations": [
            "For a public address, distinguish people directly affected from people able to provide resources. Do not place the same request on groups with unequal authority or capacity.",
            "For a panel answer, address the questioner first before broadening to the room. Make clear what has been answered and what remains uncertain.",
            "For a written presentation, use role labels at the transition. Pronouns such as we and you can become ambiguous when the audience changes within a paragraph."
        ],
        "failure_case": "Example of what can go wrong: asked about a missed commitment, a presenter turns to the wider room and praises everyone's dedication without answering. The new audience supplies a distraction, not a response. Another failure publicly assigns duties to a group without checking its authority or consent.",
        "exercise": "Mark every you, we and they in a draft that addresses several groups. Replace ambiguous cases with the relevant role. At each audience shift, write the unresolved question from the preceding passage and decide where it will be answered.",
        "self_check": "Can listeners tell who is being addressed? Are requests matched to each role? Does the shift clarify the work without evading an objection, assigning unaccepted duties or turning people into targets?"
    }
})
