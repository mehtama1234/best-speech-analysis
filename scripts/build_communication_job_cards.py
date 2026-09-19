#!/usr/bin/env python3
"""Build provisional, evidence-linked cards for the shared job vocabulary."""

from __future__ import annotations

import html
import json
import math
import re
from collections import defaultdict
from pathlib import Path


CARD_CONTENT = {
    "opening": {
        "problem": "Give the listener a reason and orientation for the exchange.",
        "mechanism": "Hypothesis: an opening can reduce orientation cost by naming the situation, relationship or question before detail arrives.",
        "form": "Name the room or question; state why it matters; preview the route.",
        "practice": "Open the same two-minute explanation with context, then without it; ask a listener what they think the talk is for.",
        "self_check": "Can a listener state the situation and purpose without guessing?",
        "non_fit": "Do not force a formal opening into a fast response or an already shared conversation.",
    },
    "closing": {
        "problem": "End without leaving the main point or next step diffuse.",
        "mechanism": "Hypothesis: a bounded close can compress the route and give the listener a retrievable takeaway, but repetition alone is not evidence of understanding.",
        "form": "Return to the point; name the limit or next step; release the turn.",
        "practice": "Close a short explanation in one sentence, then ask a listener to restate the takeaway and what remains open.",
        "self_check": "Does the close add orientation rather than merely announce that the talk is ending?",
        "non_fit": "Do not close over a live objection that still needs an answer.",
    },
    "question": {
        "problem": "Invite inquiry, reflection or a useful next turn.",
        "mechanism": "Hypothesis: a question can allocate attention and make the next reasoning step visible, but its usefulness depends on answerability and consent.",
        "form": "Ask one specific question; give context; allow a genuine answer or opt-out.",
        "practice": "Replace a broad question with a specific, answerable one and compare the next turn.",
        "self_check": "Could the listener answer, decline or ask for clarification without penalty?",
        "non_fit": "Do not use a rhetorical question to disguise a demand or corner someone.",
    },
    "answer_or_response": {
        "problem": "Respond to the literal prompt while addressing the underlying need.",
        "mechanism": "Hypothesis: naming the frame and then answering can reduce mismatch between what was asked and what the listener needs, but reframing can also evade the question.",
        "form": "Answer the literal point; state a useful frame if needed; give the bounded answer.",
        "practice": "Give a direct answer, then a frame-corrected answer; ask which one remains responsive.",
        "self_check": "Can the listener identify both the direct answer and any justified reframing?",
        "non_fit": "Do not reframe merely to avoid an uncomfortable but legitimate question.",
    },
    "story_or_personal_experience": {
        "problem": "Make an idea concrete without turning one life into universal proof.",
        "mechanism": "Hypothesis: time, place and action can give an abstract point human and temporal scale; an explicit boundary can prevent overgeneralization.",
        "form": "Give a bounded scene; say what it changed or illustrates; state what it cannot prove.",
        "practice": "Tell a 45-second event, then name the narrow lesson and one limit.",
        "self_check": "Can the listener separate the event, the interpretation and the limit?",
        "non_fit": "Do not disclose another person’s private experience or use trauma as decorative evidence.",
    },
    "example_or_case": {
        "problem": "Give a general claim a concrete handle without presenting an illustration as proof.",
        "mechanism": "Hypothesis: a concrete case can make an abstract claim inspectable; returning to the claim helps distinguish illustration from evidence.",
        "form": "State the claim; give one representative case; return to the claim and its evidence boundary.",
        "practice": "Explain a principle with and without a case; ask which detail made the idea more inspectable.",
        "self_check": "Does the case clarify the claim without pretending to establish its prevalence or cause?",
        "non_fit": "Do not select a vivid outlier to imply a typical pattern without denominators.",
    },
    "contrast_or_disagreement": {
        "problem": "Make a distinction or change in reasoning visible without escalating disagreement.",
        "mechanism": "Hypothesis: naming both sides can reduce the listener’s need to infer the replacement claim, but contrast can oversimplify real alternatives.",
        "form": "Name the earlier view; identify what changed; state the present view and remaining overlap.",
        "practice": "Use ‘I used to think X; Y changed the question; now I think Z,’ then test whether the distinction is fair.",
        "self_check": "Can the listener state what changed without turning the other side into a caricature?",
        "non_fit": "Do not manufacture a false binary or treat a person as an argument to defeat.",
    },
    "correction_or_reframe": {
        "problem": "Move from an unhelpful starting frame to a more useful question or category.",
        "mechanism": "Hypothesis: an explicit frame correction can prevent downstream reasoning from inheriting a false premise, but it can feel evasive if the original concern is ignored.",
        "form": "Acknowledge the starting frame; explain the correction; answer the more useful question.",
        "practice": "Answer a difficult prompt twice: first literally, then with one transparent frame correction.",
        "self_check": "Did you preserve the valid concern inside the revised frame?",
        "non_fit": "Do not label a challenge a ‘bad question’ simply because it is inconvenient.",
    },
    "repair_or_self_correction": {
        "problem": "Restore accuracy or shared understanding after an error, interruption or unclear phrase.",
        "mechanism": "Hypothesis: a visible repair can update the listener’s model and reduce ambiguity, but excessive self-correction can interrupt the thought.",
        "form": "Mark the error; replace it plainly; continue without over-explaining.",
        "practice": "Record a short answer with one intentional error and repair it in one sentence.",
        "self_check": "Is the corrected version unmistakable, and can the listener continue with you?",
        "non_fit": "Do not use ‘repair’ theatrically to avoid responsibility for a substantive claim.",
    },
    "qualification_or_boundary": {
        "problem": "State a clear point while marking uncertainty, scope or conditions.",
        "mechanism": "Hypothesis: an explicit qualifier helps locate certainty and revision conditions, but vague hedging can hide the claim rather than calibrate it.",
        "form": "State the main claim; name its evidence status or condition; say what would change it.",
        "practice": "Convert one absolute sentence into a bounded claim with one observable condition.",
        "self_check": "Is the claim clearer and more honest, rather than simply weaker?",
        "non_fit": "Do not add ornamental uncertainty to a claim that should be checked directly.",
    },
    "definition_or_explanation": {
        "problem": "Make an unfamiliar idea usable without overextending it.",
        "mechanism": "Hypothesis: an operational definition reduces ambiguity; naming exclusions can prevent the listener from applying it outside its scope.",
        "form": "Name the term; give its plain meaning; show one example and one boundary.",
        "practice": "Define a technical term for a newcomer in 20 seconds, then ask them to use it in a new sentence.",
        "self_check": "Can the listener use the term and say what it does not mean?",
        "non_fit": "Do not substitute a slogan, metaphor or credential for a usable definition.",
    },
    "transition_or_structure": {
        "problem": "Help a listener follow a change of topic, scale, speaker or reasoning step.",
        "mechanism": "Hypothesis: a signposted transition lowers navigation cost by showing how the next section connects, but too many labels can make speech mechanical.",
        "form": "Close the current point; name the relationship; enter the next point.",
        "practice": "Add one spoken bridge between two unrelated ideas and ask a listener to describe the connection.",
        "self_check": "Can the listener say why the next point arrived here?",
        "non_fit": "Do not use a transition to imply a connection that the evidence does not support.",
    },
    "callback_or_repetition": {
        "problem": "Give a long exchange continuity or let an earlier image carry changed meaning.",
        "mechanism": "Hypothesis: a callback can bind distant parts of a talk and make a shift noticeable, but repetition can become empty emphasis.",
        "form": "Introduce a meaningful anchor; return to it with a new application; avoid merely repeating it.",
        "practice": "Use one image at the opening and return to it at the close with a changed implication.",
        "self_check": "What new work does the repeated phrase do the second time?",
        "non_fit": "Do not repeat a slogan to pressure agreement or simulate evidence.",
    },
    "humor_or_rapport": {
        "problem": "Create ease or relational room without making affected people the joke.",
        "mechanism": "Hypothesis: self-directed or situational humor may lower social pressure and make a difficult turn more approachable, but context and power determine risk.",
        "form": "Use lightness about your own situation or the shared setting; return clearly to the point.",
        "practice": "Try a self-directed release and a neutral transition after difficult material; check whether either targets someone else.",
        "self_check": "Who bears the cost of the joke, and can the listener opt out of laughing?",
        "non_fit": "Do not use humor to trivialize grief, vulnerability, identity or an unresolved harm.",
    },
    "credit_or_acknowledgment": {
        "problem": "Make contribution, support or dependence visible without turning praise into a status performance.",
        "mechanism": "Hypothesis: specific credit can widen the authorship frame and show the work behind an outcome, but lists can exclude or tokenize people.",
        "form": "Name the contribution; connect it to the result; state what remains owed or unfinished.",
        "practice": "Replace generic thanks with one observable contribution and its consequence.",
        "self_check": "Could the credited person recognize the description as accurate and specific?",
        "non_fit": "Do not claim to transfer authority through praise while retaining all control.",
    },
    "call_to_action_or_audience_role": {
        "problem": "Turn a broad aspiration into a voluntary, bounded next role.",
        "mechanism": "Hypothesis: naming action, owner, time horizon and limit can make a request evaluable, but a request is not proof that the action is feasible or effective.",
        "form": "Name the problem; offer a specific action and responsible actor; state the limit and consent path.",
        "practice": "Rewrite ‘we should care’ as one feasible action with an owner, timeframe and non-fit.",
        "self_check": "Can the listener say what they may do and what the action cannot solve?",
        "non_fit": "Do not assign risk, money or care labor without authority, consent or support.",
    },
    "persuasion_or_advocacy": {
        "problem": "Move a room toward judgment or action while showing evidence, tradeoffs and responsibility.",
        "mechanism": "Hypothesis: a visible chain from problem to mechanism to responsibility can make advocacy inspectable, but rhetorical force does not establish policy truth or outcomes.",
        "form": "State the stake; show the mechanism; name tradeoffs and accountable actors; invite a bounded choice.",
        "practice": "Make one advocacy claim with evidence status, opposing concern, responsible actor and review point.",
        "self_check": "Can a listener disagree with the proposal while accurately restating it?",
        "non_fit": "Do not use urgency, fear or moral identity to conceal missing evidence or coercion.",
    },
    "reflection_or_value_frame": {
        "problem": "Connect an event or decision to a value without pretending the value settles the facts.",
        "mechanism": "Hypothesis: an explicit value frame can help a listener understand why a detail matters, but moral language can overrule evidence or disagreement.",
        "form": "Describe the event; name the value it raises; distinguish interpretation from verified fact.",
        "practice": "Take one personal or public event and state the value interpretation plus one alternative reading.",
        "self_check": "Can the listener tell which part is observation, value judgment and open question?",
        "non_fit": "Do not use a value label to end inquiry or claim moral superiority.",
    },
}


DELIVERY_PATTERN_JOBS = {
    "candidate-question": ["question"],
    "candidate-question-or-qualification": ["question", "qualification_or_boundary"],
    "candidate-uncertainty-or-qualification": ["qualification_or_boundary"],
    "candidate-story-or-personal-experience": ["story_or_personal_experience"],
    "candidate-call-to-action": ["call_to_action_or_audience_role"],
    "candidate-example": ["example_or_case"],
}


def load_delivery_items(root: Path) -> dict[str, list[dict]]:
    by_job = defaultdict(list)
    inventory_path = root / "research/communication-job-delivery-inventory.json"
    if inventory_path.exists():
        inventory = json.loads(inventory_path.read_text())
        for job in inventory["jobs"]:
            for sample in job["samples"]:
                by_job[job["canonical_job"]].append({
                    "evidence_id": sample["evidence_id"],
                    "video_id": sample["video_id"],
                    "title": sample["title"],
                    "pattern_id": f"delivery-sample-{job['canonical_job']}",
                    "sampled_time_seconds": round((sample["start_seconds"] + sample["end_seconds"]) / 2, 3),
                    "source_url": sample["source_url"],
                    "transcript_text": sample["transcript_excerpt"],
                    "frame_observation": " ".join(filter(None, (sample.get("visual_observation"), sample.get("setting_editing_music_observation")))),
                    "alignment_decision": sample.get("transcript_alignment"),
                    "measured_audio_proxy": sample.get("audio_measurements", {}),
                    "nearest_frame_measurement": sample.get("nearest_sampled_frame") or {},
                    "feature_limit": "Proxy measurements and a single internal midpoint-frame note are inspection aids, not vocal meaning, nonverbal intent or effectiveness evidence.",
                    "review_status": "internal_midpoint_frame_observation_not_independent",
                    "delivery_evidence_status": "internal_bounded_review_not_independent",
                })
        return by_job
    for filename in ("research/multimodal-expansion-manual-review.json", "research/multimodal-expansion-manual-review-02.json"):
        report = json.loads((root / filename).read_text())
        for item in report["items"]:
            for job in DELIVERY_PATTERN_JOBS.get(item.get("pattern_id"), []):
                video_url = f"https://www.youtube.com/watch?v={item['video_id']}&t={math.floor(item['sampled_time_seconds'])}s"
                by_job[job].append({
                    "evidence_id": item["evidence_id"],
                    "video_id": item["video_id"],
                    "title": item["title"],
                    "pattern_id": item.get("pattern_id"),
                    "sampled_time_seconds": item.get("sampled_time_seconds"),
                    "source_url": video_url,
                    "transcript_text": item.get("transcript_text", ""),
                    "frame_observation": item.get("frame_observation", ""),
                    "alignment_decision": item.get("alignment_decision"),
                    "measured_audio_proxy": item.get("measured_audio_proxy", {}),
                    "nearest_frame_measurement": item.get("nearest_frame_measurement", {}),
                    "feature_limit": item.get("feature_limit", ""),
                    "review_status": item.get("review_status"),
                    "delivery_evidence_status": "internal_bounded_review_not_independent",
                })
    return by_job


NON_SPEECH_MARKER = re.compile(r"^\s*\[[^\]]+\]\s*$")


def example_quality(record: dict) -> tuple[int, int, int]:
    """Rank examples for teaching usefulness without changing source text."""
    segments = record["segments"][:3]
    lexical = [segment for segment in segments if segment.get("text", "").strip() and not NON_SPEECH_MARKER.match(segment["text"])]
    word_count = sum(len(re.findall(r"[A-Za-zÀ-ÿ]+", segment.get("text", ""))) for segment in lexical)
    contamination = sum(1 for segment in segments if NON_SPEECH_MARKER.match(segment.get("text", "")))
    # Prefer lexical speech, then more words, then fewer non-speech cues.
    return (1 if lexical else 0, word_count, -contamination)


def build(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    bank = json.loads((root / "research/corpus-evidence-bank.json").read_text())
    learner = json.loads((root / "research/communication-job-learner-check.json").read_text())
    learner_by_job = {row["canonical_job"]: row for row in learner["cards"]}
    delivery_by_job = load_delivery_items(root)
    by_job = defaultdict(list)
    for record in bank["records"]:
        if record["canonical_job"] in CARD_CONTENT and record["segments"]:
            by_job[record["canonical_job"]].append(record)
    cards = []
    for job, content in CARD_CONTENT.items():
        records = sorted(by_job[job], key=lambda item: (-example_quality(item)[0], -example_quality(item)[1], example_quality(item)[2], item["record_id"]))
        selected = []
        seen_videos = set()
        for record in records:
            if record["video_id"] in seen_videos:
                continue
            seen_videos.add(record["video_id"])
            # Keep exact, readable sample context while linking to the full
            # function span in the evidence bank.
            sample = record["segments"][:3]
            selected.append({
                "record_id": record["record_id"],
                "video_id": record["video_id"],
                "title": record["title"],
                "raw_function_label": record["raw_function_label"],
                "source_url": record["source_url"],
                "full_function_segment_count": len(record["segments"]),
                "sample_scope": "first_three_retained_segments_of_function_span",
                "example_quality": {
                    "lexical_speech_present": bool(example_quality(record)[0]),
                    "lexical_word_count": example_quality(record)[1],
                    "non_speech_marker_count": -example_quality(record)[2],
                    "selection_note": "ranked for lexical speech and low non-speech-marker contamination; transcript wording remains unrepaired",
                },
                "exact_segments": sample,
            })
            if len(selected) >= 8:
                break
        cards.append({
            "card_id": f"provisional-job-{job}",
            "canonical_job": job,
            "status": "provisional_transcript_inventory_not_independently_validated",
            **content,
            "recurrence": {
                "function_record_count": len(by_job[job]),
                "video_count": len({record["video_id"] for record in by_job[job]}),
                "denominator_status": "inventory_counts_not_effectiveness_denominators",
            },
            "exact_examples": selected,
            "phrase_forms": learner_by_job[job]["phrase_forms"],
            "phrase_form_coverage_status": learner_by_job[job]["phrase_form_coverage_status"],
            "delivery_evidence_status": "internal_bounded_review_not_independent" if delivery_by_job[job] else "no_aligned_internal_sample_for_this_job",
            "delivery_observations": delivery_by_job[job],
            "validation": {
                "independent_function_review": "pending",
                "independent_recurrence_review": "pending",
                "delivery_review": "pending_or_not_available_for_most_records",
                "learner_check": "not_run",
                "listener_outcome": "not_run",
            },
        })
    return {
        "schema_version": "1.0",
        "card_set_id": "provisional-communication-job-cards",
        "status": "provisional_transcript_cards_not_validated",
        "claim_boundary": "These cards organize transcript-derived observations into practice hypotheses. They do not establish that a form works, recurs independently, improves delivery or changes listener outcomes.",
        "sources": ["research/corpus-evidence-bank.json", "research/corpus-function-taxonomy.json"],
        "card_count": len(cards),
        "cards": cards,
    }


def write_outputs(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    result = build(root)
    (root / "research/communication-job-cards.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    lines = ["# Provisional communication-job cards", "", "Status: **transcript-derived practice hypotheses; not validated**.", "", result["claim_boundary"], ""]
    for card in result["cards"]:
        forms = ", ".join(form["phrase_form"] for form in card["phrase_forms"]) or "No direct exact-form family match indexed."
        lines += [f"## `{card['canonical_job']}`", "", f"**Problem:** {card['problem']}", "", f"**Mechanism hypothesis:** {card['mechanism']}", "", f"**Repeatable form:** {card['form']}", "", f"**Indexed exact forms:** {forms} (`{card['phrase_form_coverage_status']}`)", "", f"**Recurrence inventory:** {card['recurrence']['function_record_count']} records across {card['recurrence']['video_count']} videos.", "", f"**Practice:** {card['practice']}", "", f"**Self-check:** {card['self_check']}", "", f"**When not to use:** {card['non_fit']}", "", f"**Delivery evidence:** {len(card['delivery_observations'])} internally reviewed sample(s); status `{card['delivery_evidence_status']}`.", ""]
    (root / "writeups/communication-job-cards.md").write_text("\n".join(lines))
    cards_html = []
    for card in result["cards"]:
        examples = "".join(
            f"<li><a href='{html.escape(example['source_url'] or '', quote=True)}'>{html.escape(example['title'])}</a> — <code>{html.escape(example['raw_function_label'] or '[unlabeled]')}</code><blockquote>{html.escape(' '.join(segment['text'] for segment in example['exact_segments']))}</blockquote></li>"
            for example in card["exact_examples"]
        )
        delivery = "".join(f"<li><a href='{html.escape(item['source_url'], quote=True)}'>{html.escape(item['title'])}</a> — {html.escape(item['transcript_text'])}<br><small>{html.escape(item['frame_observation'])} Alignment: {html.escape(str(item['alignment_decision']))}. Audio/visual fields are bounded proxies; no intent or effect inferred.</small></li>" for item in card['delivery_observations'])
        forms = ", ".join(html.escape(form["phrase_form"]) for form in card["phrase_forms"]) or "No direct exact-form family match indexed."
        cards_html.append(f"<article class='card' data-search='{html.escape((card['canonical_job']+' '+card['problem']).lower(), quote=True)}'><h2>{html.escape(card['canonical_job'])}</h2><p><strong>Problem:</strong> {html.escape(card['problem'])}</p><p><strong>Mechanism hypothesis:</strong> {html.escape(card['mechanism'])}</p><p><strong>Repeatable form:</strong> {html.escape(card['form'])}</p><p><strong>Indexed exact forms:</strong> {forms} <small>({html.escape(card['phrase_form_coverage_status'])})</small></p><p><strong>Inventory:</strong> {card['recurrence']['function_record_count']} records / {card['recurrence']['video_count']} videos</p><p><strong>Practice:</strong> {html.escape(card['practice'])}</p><p><strong>Self-check:</strong> {html.escape(card['self_check'])}</p><p><strong>When not to use:</strong> {html.escape(card['non_fit'])}</p><details><summary>Exact examples</summary><ol>{examples}</ol></details><details><summary>Internal delivery observations ({len(card['delivery_observations'])})</summary><ul>{delivery or '<li>No aligned internal sample.</li>'}</ul></details></article>")
    browser = """<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Communication job cards</title><style>body{font:16px system-ui,sans-serif;max-width:1050px;margin:2rem auto;padding:0 1rem;color:#17202a}input{width:100%;box-sizing:border-box;padding:.7rem;font:inherit;margin:1rem 0 1.5rem}.notice{background:#fff4ce;padding:1rem;border-left:4px solid #b8860b}.card{border:1px solid #ccd3da;border-radius:8px;padding:1rem;margin:1rem 0}.card h2{margin:.1rem 0}blockquote{background:#f5f7f9;padding:.7rem;margin:.5rem 0}code{overflow-wrap:anywhere}</style><main><h1>Provisional communication-job cards</h1><div class="notice"><strong>Practice hypotheses, not proven best practices.</strong> All examples are transcript-derived; delivery, independent review, learner and listener gates remain visible.</div><label for="search">Search cards</label><input id="search" type="search" placeholder="e.g. question, contrast, story"><p id="count" aria-live="polite"></p>""" + "\n".join(cards_html) + """</main><script>const i=document.querySelector('#search'),c=[...document.querySelectorAll('.card')],n=document.querySelector('#count');function f(){let q=i.value.toLowerCase(),x=0;c.forEach(a=>{let s=!q||a.dataset.search.includes(q);a.hidden=!s;if(s)x++});n.textContent=`Showing ${x} of ${c.length} cards`}i.oninput=f;f()</script>"""
    (root / "writeups/communication-job-cards.html").write_text(browser)
    return result


if __name__ == "__main__":
    result = write_outputs()
    print(json.dumps({"card_count": result["card_count"], "status": result["status"]}, indent=2))
