#!/usr/bin/env python3
"""Build draft matched listener stimuli for the 18 provisional job cards.

These are newly authored study materials, not quotations or reconstructions of
the source speeches. They are drafts until readability, accessibility, safety
and proposition matching are independently checked.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


STIMULI = {
    "opening": {
        "topic": "community library hours",
        "proposition": "The library will change weekend hours next month and visitors need the new schedule.",
        "control": "Next month, the library will change its weekend hours. The new schedule will be posted at the entrance and online. Visitors should check it before coming.",
        "pattern_informed": "Next month, the library will change its weekend hours. I will explain what is changing, why visitors need to know, and where to check the schedule before coming.",
        "safety_note": "No personal disclosure or pressure; orientation is the manipulation target.",
    },
    "closing": {
        "topic": "community garden watering",
        "proposition": "The garden needs a watering rota and volunteers should sign up for a slot.",
        "control": "The garden needs a watering rota. Volunteers can sign up for a morning or evening slot on the shared sheet. The rota will be reviewed next Friday.",
        "pattern_informed": "The garden needs a watering rota. Volunteers can sign up for a morning or evening slot on the shared sheet, and we will review it next Friday. The takeaway is simple: choose one slot only if you can keep it.",
        "safety_note": "The request remains voluntary and does not assume unpaid capacity.",
    },
    "question": {
        "topic": "meeting agenda",
        "proposition": "The team needs to choose one priority before the next meeting.",
        "control": "The team needs to choose one priority before the next meeting. We will review the three proposals and select one.",
        "pattern_informed": "The team needs to choose one priority before the next meeting. Which of the three proposals best fits the time and people we actually have? You may ask for more information before choosing.",
        "safety_note": "The question permits clarification and does not demand agreement.",
    },
    "answer_or_response": {
        "topic": "project deadline",
        "proposition": "The report can be delivered Friday if the data arrives Wednesday.",
        "control": "Yes, the report can be delivered Friday if the data arrives Wednesday. If the data arrives later, the delivery date will move.",
        "pattern_informed": "The short answer is yes: the report can be delivered Friday if the data arrives Wednesday. The useful question is whether that data date is confirmed; if it is not, the delivery date may move.",
        "safety_note": "The frame correction does not avoid the direct answer.",
    },
    "story_or_personal_experience": {
        "topic": "handoff checklist",
        "proposition": "A checklist can prevent a missed handoff, but one experience is not universal proof.",
        "control": "A handoff checklist can prevent a missed item. Teams should list the owner, deadline and next action before work changes hands.",
        "pattern_informed": "During one handoff, I missed a file because I had not named the next owner. A checklist would have caught it. That event illustrates the value of naming an owner, but it does not prove one checklist fits every team.",
        "safety_note": "The stimulus uses a fictional or anonymous event and does not require personal disclosure.",
    },
    "example_or_case": {
        "topic": "appointment reminders",
        "proposition": "A reminder may reduce missed appointments, but one case does not prove general causality.",
        "control": "A clear reminder may reduce missed appointments. The service should test reminders against its own attendance records before changing the whole process.",
        "pattern_informed": "A clear reminder may reduce missed appointments. For example, one clinic sent a reminder the day before and recorded fewer missed visits that month. The case illustrates a possibility, but it does not prove the reminder caused the change everywhere.",
        "safety_note": "No medical advice or identifiable patient information is used.",
    },
    "contrast_or_disagreement": {
        "topic": "delivery estimate",
        "proposition": "An order expected in two days arrived in five because a supplier delay changed the schedule.",
        "control": "The order arrived in five days. The supplier delay changed the schedule, so the original estimate did not hold. We need to check the next delivery before promising two days.",
        "pattern_informed": "We expected the order in two days, but it arrived in five after a supplier delay. The change explains why the estimate did not hold; it does not by itself show that anyone acted carelessly. For the next order, we should check the supplier date first.",
        "safety_note": "The contrast does not infer motive or turn disagreement into a personal attack.",
    },
    "correction_or_reframe": {
        "topic": "training attendance",
        "proposition": "The useful question is whether the training is accessible and relevant, not simply whether attendance is high.",
        "control": "Attendance was low at the last training. We should improve attendance by sending reminders and choosing a better time.",
        "pattern_informed": "Attendance was low at the last training. The more useful question is whether the session was accessible and relevant before we treat attendance as the problem. We should check the barriers and then decide what to change.",
        "safety_note": "The reframe retains the attendance concern instead of dismissing it.",
    },
    "repair_or_self_correction": {
        "topic": "report status",
        "proposition": "The report is nearly finished, with one review step remaining.",
        "control": "The report is finished except for one review step. It is ready to send after that review.",
        "pattern_informed": "The report is finished—sorry, I mean nearly finished—with one review step remaining. It is ready to send after that review.",
        "safety_note": "The correction is small and observable; it does not perform accountability theatrically.",
    },
    "qualification_or_boundary": {
        "topic": "pilot delays",
        "proposition": "Early records suggest a pilot may reduce delays, but more records are needed.",
        "control": "The pilot reduces delays. We should use it for the whole service next month.",
        "pattern_informed": "Early records suggest the pilot may reduce delays, but the sample is small and we need another month of records before recommending it for the whole service.",
        "safety_note": "The boundary distinguishes an observation from a recommendation.",
    },
    "definition_or_explanation": {
        "topic": "service handoff",
        "proposition": "A handoff means naming who owns the next action and when it is due.",
        "control": "A good handoff improves coordination. The sender should include the relevant details and the receiver should follow up.",
        "pattern_informed": "By a handoff, I mean naming who owns the next action and when it is due. It is not simply forwarding information; the next responsibility must be visible.",
        "safety_note": "The definition is operational and does not imply a universal process.",
    },
    "transition_or_structure": {
        "topic": "budget meeting",
        "proposition": "The group must move from describing the problem to choosing a feasible option.",
        "control": "The budget is smaller than expected. Option A costs less, Option B serves more people, and the group must choose one.",
        "pattern_informed": "We have described the budget problem; now we can move to the choice it creates. Option A costs less, Option B serves more people, and the group must choose one.",
        "safety_note": "The bridge signals structure without pretending the tradeoff is resolved.",
    },
    "callback_or_repetition": {
        "topic": "safety checklist",
        "proposition": "A checklist introduced at the start should guide the final decision.",
        "control": "The team will review three safety items before deciding. The final decision should consider the risks and the available evidence.",
        "pattern_informed": "At the start we called this the three-item safety check: risk, evidence and owner. We have reviewed the options, so return to that check before deciding what is safe to do.",
        "safety_note": "The repeated anchor adds structure and does not substitute for evidence.",
    },
    "humor_or_rapport": {
        "topic": "presentation nerves",
        "proposition": "A speaker can acknowledge nerves and still present the main point clearly.",
        "control": "I am nervous about presenting this material, but I have prepared the main point and the evidence. I will begin with the recommendation.",
        "pattern_informed": "I am nervous about presenting this material; my internal stage manager is requesting a fire exit. I have prepared the main point and evidence, so I will begin with the recommendation.",
        "safety_note": "The humor is self-directed and does not target a listener or affected group.",
    },
    "credit_or_acknowledgment": {
        "topic": "community survey",
        "proposition": "The survey result depended on residents who collected responses and checked translations.",
        "control": "Thank you to everyone who helped with the survey. The result will guide the next meeting and the report will be shared online.",
        "pattern_informed": "Residents collected responses at three sites and checked the translations, which made the survey usable across the neighborhood. Their work shaped the result; the report will be shared online and the next decision remains open.",
        "safety_note": "Credit is specific without claiming to transfer authority or naming people without consent.",
    },
    "call_to_action_or_audience_role": {
        "topic": "meeting accessibility",
        "proposition": "People who need captions can request them before the meeting, but one request cannot solve every access barrier.",
        "control": "Accessibility matters for the meeting. We should try to make the meeting accessible and ask people to share what they need.",
        "pattern_informed": "If you need captions for Thursday's meeting, request them by Tuesday through the access form; the coordinator will confirm what can be provided. This step helps with captions but cannot solve every access barrier, so other requests remain welcome.",
        "safety_note": "The action is optional, names an owner and does not shift all access labor to attendees.",
    },
    "persuasion_or_advocacy": {
        "topic": "tree planting budget",
        "proposition": "The council should fund a tree-planting pilot and review survival after one year.",
        "control": "The council should fund a tree-planting pilot because trees benefit the neighborhood. The council should approve the proposal.",
        "pattern_informed": "Hot streets and limited shade need a test. A one-year tree-planting pilot lets the council measure watering, survival and cost before expanding it. The parks team reports; the council may revise or stop it if the evidence is poor.",
        "safety_note": "The advocacy names mechanism, owner, review and reversal rather than hiding tradeoffs.",
    },
    "reflection_or_value_frame": {
        "topic": "school timetable",
        "proposition": "A timetable decision should consider both measured travel time and the value of predictable access.",
        "control": "The new timetable adds ten minutes to the trip for some students. The committee will compare the routes and decide whether to keep it.",
        "pattern_informed": "The new timetable adds ten minutes to the trip for some students. The measured delay matters, and so does the value of predictable access for students who rely on the route. Those are interpretations to weigh alongside the route data, not a substitute for checking it.",
        "safety_note": "The value frame is separated from the observed travel-time claim.",
    },
}


def words(text: str) -> int:
    return len(re.findall(r"\b[\w’'-]+\b", text))


def build(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    cards = json.loads((root / "research/communication-job-cards.json").read_text())["cards"]
    records = []
    for card in cards:
        job = card["canonical_job"]
        item = STIMULI[job]
        control_words = words(item["control"])
        pattern_words = words(item["pattern_informed"])
        records.append({
            "stimulus_id": f"draft-{job}-01",
            "card_id": card["card_id"],
            "canonical_job": job,
            "topic": item["topic"],
            "proposition": item["proposition"],
            "control_text": item["control"],
            "pattern_informed_text": item["pattern_informed"],
            "control_word_count": control_words,
            "pattern_informed_word_count": pattern_words,
            "word_count_delta": pattern_words - control_words,
            "same_proposition_statement": "Draft author assertion; requires independent content and readability review.",
            "source_boundary": "Newly authored study material; not copied from corpus speakers.",
            "safety_note": item["safety_note"],
            "status": "draft_requires_matching_readability_accessibility_and_safety_review",
        })
    return {
        "schema_version": "1.0",
        "stimulus_bank_id": "communication-job-listener-stimuli-draft",
        "status": "draft_not_locked",
        "claim_boundary": "These are newly authored draft stimuli for a future listener study. They are not corpus evidence and do not demonstrate that a pattern works.",
        "source": "research/communication-job-cards.json",
        "stimulus_count": len(records),
        "pair_count": len(records),
        "records": records,
        "review_requirements": [
            "independent content-equivalence review",
            "readability and vocabulary matching",
            "caption/audio accessibility review",
            "safety, privacy and coercion review",
            "pilot comprehension review before locking",
            "holdout split and randomization lock",
        ],
    }


def write_outputs(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    result = build(root)
    (root / "research/communication-job-listener-stimuli-draft.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    lines = ["# Draft communication-job listener stimuli", "", "Status: **draft, not locked**.", "", result["claim_boundary"], "", f"Matched-pair drafts: **{result['pair_count']}**.", "", "| Job | Topic | Control words | Pattern words | Delta | Status |", "|---|---|---:|---:|---:|---|"]
    lines += [f"| `{r['canonical_job']}` | {r['topic']} | {r['control_word_count']} | {r['pattern_informed_word_count']} | {r['word_count_delta']:+d} | `{r['status']}` |" for r in result["records"]]
    (root / "writeups/communication-job-listener-stimuli-draft.md").write_text("\n".join(lines) + "\n")
    return result


if __name__ == "__main__":
    result = write_outputs()
    print(json.dumps({"pair_count": result["pair_count"], "status": result["status"]}, indent=2))
