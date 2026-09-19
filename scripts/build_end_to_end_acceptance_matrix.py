#!/usr/bin/env python3
"""Build a requirement-level acceptance matrix for the speech-learning system."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text())


def build() -> dict:
    status = load("research/end-to-end-status.json")
    queue = load("research/full-reading-queue.json")
    reviews = load("research/full-context-reviews.json")
    cards = load("research/communication-job-cards.json")
    curriculum = load("research/communication-job-curriculum-index.json")
    delivery = load("research/multimodal-coverage-audit.json")
    counterexamples = load("research/communication-job-counterexample-workbook.json")
    learner = load("research/communication-job-learner-check.json")
    listener = load("research/communication-job-listener-outcome-protocol.json")
    independent = load("research/corpus-function-independent-review-workbook.json")
    recurrence = load("research/corpus-recurrence-independent-review-workbook.json")
    rows = [
        {"requirement_id": "inventory_and_provenance", "requirement": "Every eligible source has an auditable identity, provenance and review state.", "status": "complete_for_fixed_corpus", "evidence": ["research/full-reading-queue.json", "research/corpus-identity-review-workbook.json"], "basis": f"{queue['video_count']} queued videos; identity review remains an independent gate.", "remaining": "Complete independent identity/duplication decisions before promotion."},
        {"requirement_id": "full_context_transcript", "requirement": "Retained captions are read in full context with source boundaries visible.", "status": "complete_for_fixed_corpus", "evidence": ["research/full-context-reviews.json", "research/corpus-evidence-bank.json"], "basis": f"{len(reviews['reviews'])} full-context reviews and {queue['caption_count']} captions.", "remaining": "Transcript evidence does not establish delivery or outcomes."},
        {"requirement_id": "exact_language_and_forms", "requirement": "Lessons expose exact words, phrases and repeatable speech forms in context.", "status": "provisional_transcript_evidence", "evidence": ["research/communication-job-cards.json", "research/corpus-phrase-form-inventory.json", "writeups/communication-job-curriculum.html", "writeups/repeatable-communication-patterns.md"], "basis": f"{cards['card_count']} cards with exact examples; {load('research/corpus-phrase-form-inventory.json')['form_count']} heuristic phrase forms; cross-job forms are synthesized with explicit claim boundaries.", "remaining": "Complete independent phrase-form review and adjudication."},
        {"requirement_id": "function_and_mechanism", "requirement": "Each pattern names the communication job and labels why it might help as a hypothesis.", "status": "provisional_transcript_interpretation", "evidence": ["research/communication-job-cards.json", "scripts/validate_communication_job_cards.py"], "basis": f"{cards['card_count']} evidence-linked cards pass structural validation.", "remaining": f"Independently review {independent['item_count']} candidate function items."},
        {"requirement_id": "verbal_vocal_nonverbal_setting", "requirement": "Verbal, vocal, pause, nonverbal, visual and setting evidence remain distinct with measurement limits.", "status": "partial_internal_coverage", "evidence": ["research/multimodal-coverage-audit.json", "research/communication-job-delivery-sampling.json", "research/communication-job-delivery-measurement-preflight.json"], "basis": f"{delivery['raw_audio_video_present_count']} selected videos have raw A/V; internal observations are bounded and non-independent.", "remaining": "Complete manual observation and independent multimodal review; missing media remains explicit."},
        {"requirement_id": "cross_talk_recurrence", "requirement": "Candidate patterns are compared across speakers, events, topics and formats with denominators and holdouts.", "status": "provisional_transcript_comparison", "evidence": ["research/communication-job-cross-comparison.json", "research/corpus-recurrence-independent-review-workbook.json"], "basis": f"Cross-job comparison has {status['stages']['cross_job_comparison']['pair_count']} pairs and an eligible-video denominator.", "remaining": f"Independently review {recurrence['item_count']} recurrence candidates and identity splits."},
        {"requirement_id": "counterexamples_and_limits", "requirement": "Every major job has absent, failed, alternate-function, confound and misuse-limit slots.", "status": "queued_not_completed", "evidence": ["research/communication-job-counterexample-workbook.json", "writeups/communication-job-counterexample-workbook.html"], "basis": f"{counterexamples['job_count']} jobs and {counterexamples['item_count']} blank slots are queued.", "remaining": "Populate, independently review and adjudicate the slots; do not force candidates."},
        {"requirement_id": "practice_and_shared_curriculum", "requirement": "Evidence becomes bounded practice with self-checks, non-fit warnings and linked web/mobile lessons.", "status": "provisional_constructed", "evidence": ["research/communication-job-curriculum-index.json", "research/communication-job-mobile-lessons.json", "writeups/repeatable-communication-patterns.md", "scripts/validate_communication_job_curriculum.py"], "basis": f"{curriculum['lesson_count']} lessons and mobile payloads pass join validation; the cross-job guide adds adaptation and delivery-inspection prompts.", "remaining": "Promotion depends on independent evidence and learner observations."},
        {"requirement_id": "independent_review", "requirement": "A second reviewer checks important examples, interpretations, limits and safety boundaries.", "status": "not_started", "evidence": ["research/corpus-function-independent-review-workbook.json", "research/corpus-recurrence-independent-review-workbook.json", "research/multimodal-independent-review-workbook.json"], "basis": "Review workbooks and disagreement-preserving validators exist; no independent exports are present.", "remaining": "Obtain and adjudicate independent exports."},
        {"requirement_id": "learner_validation", "requirement": "Learners are tested for recognition, explanation, transfer, non-fit and revision.", "status": "protocol_ready_not_run", "evidence": ["research/communication-job-learner-check.json", "scripts/summarize_communication_job_learner_records.py"], "basis": f"{learner['card_count']} cards and {learner['task_count']} fixed tasks; zero records.", "remaining": "Run the consented learner protocol and validate exports."},
        {"requirement_id": "listener_outcome_separation", "requirement": "Listener comprehension/recall is tested separately from corpus observations and learner teachability.", "status": "protocol_ready_not_run", "evidence": ["research/communication-job-listener-outcome-protocol.json", "scripts/summarize_communication_job_listener_records.py"], "basis": f"{len(listener['patterns'])} jobs and {len(listener['listener_tasks'])} scored tasks; stimuli are not locked and records are zero.", "remaining": "Complete independent stimulus review, lock pairs, then run the blinded study."},
        {"requirement_id": "claim_boundary_and_missingness", "requirement": "The product preserves uncertainty, missing modalities, disagreement and non-causal claim language.", "status": "contract_and_validators_ready", "evidence": ["research/shared-evidence-model.json", "research/end-to-end-status.json", "scripts/validate_end_to_end_status.py"], "basis": "Shared entity/status contract and dashboard validators pass.", "remaining": "Recheck these boundaries whenever evidence is promoted."},
    ]
    return {"schema_version": "1.0", "matrix_id": "best-speech-analysis-end-to-end-acceptance", "status": "research_checkpoint_not_complete", "claim_boundary": "This matrix audits requirements and evidence status; it is not proof that pending human reviews or outcome studies have occurred.", "rows": rows, "open_requirement_count": sum(row["status"] not in {"complete_for_fixed_corpus", "contract_and_validators_ready"} for row in rows)}


def write_outputs() -> dict:
    matrix = build()
    (ROOT / "research/end-to-end-acceptance-matrix.json").write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + "\n")
    lines = ["# End-to-end acceptance matrix", "", "Status: **research checkpoint not complete**.", "", matrix["claim_boundary"], "", "| Requirement | Status | Evidence | Remaining |", "|---|---|---|---|"]
    for row in matrix["rows"]:
        lines.append(f"| `{row['requirement_id']}` | `{row['status']}` | {', '.join(f'`{path}`' for path in row['evidence'])} | {row['remaining']} |")
    lines += ["", f"Open requirements: **{matrix['open_requirement_count']}**. A protocol, workbook or passing validator is not counted as completed human evidence.", ""]
    (ROOT / "writeups/end-to-end-acceptance-matrix.md").write_text("\n".join(lines))
    print(json.dumps({"output": "research/end-to-end-acceptance-matrix.json", "open_requirement_count": matrix["open_requirement_count"]}, indent=2))
    return matrix


if __name__ == "__main__":
    write_outputs()
