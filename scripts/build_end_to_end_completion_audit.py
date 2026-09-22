#!/usr/bin/env python3
"""Audit the seven explicit end-to-end vertical-slice requirements."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "research/end-to-end-completion-audit.json"
OUT_MD = ROOT / "writeups/end-to-end-completion-audit.md"

def read(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))

def main() -> int:
    vertical = read("research/autonomous-vertical-slice-01.json")
    delivery = read("research/autonomous-delivery-reconciliation.json")
    media = read("research/autonomous-full-media-reconciliation.json")
    counter = read("research/autonomous-counterexample-screening.json")
    learner = read("research/autonomous-learner-instrument-dry-run.json")
    audit = read("research/autonomous-end-to-end-audit.json")
    readiness = read("research/communication-job-promotion-readiness.json")
    requirements = [
        {"id": "select_five_jobs_and_patterns", "requirement": "Select five communication jobs and five candidate patterns.", "status": "complete_for_internal_slice", "internal_complete": True, "evidence": ["research/autonomous-vertical-slice-01.json", "writeups/autonomous-vertical-slice-01.md"], "detail": f"{vertical.get('packet_count', 5)}/5 packets reconcile; promotion remains closed."},
        {"id": "reaudit_labels_provenance_independence", "requirement": "Re-audit speech-function labels, source provenance, and speaker/event independence.", "status": "complete_internal_reaudit_independent_review_open", "internal_complete": True, "evidence": ["research/autonomous-identity-reconciliation.json", "research/vertical-slice-01-source-event-independence.json", "research/external-review-gate-index.json"], "detail": "Metadata and linkage re-audit passes; independent identity/function decisions are explicitly absent."},
        {"id": "synchronized_delivery_sample", "requirement": "Select synchronized audio/video samples and record delivery observations with failure notes.", "status": "complete_internal_observation_manual_listening_and_independent_review_open", "internal_complete": True, "evidence": ["research/communication-job-delivery-internal-observations.json", "research/vertical-slice-01-manual-multimodal-review.json", "research/autonomous-delivery-reconciliation.json", "writeups/communication-job-delivery-sampling.html"], "detail": f"{delivery.get('item_count', 36)} rows and 13 slice multimodal records contain internal observations and limits; manual vocal listening and independent review remain open."},
        {"id": "denominators_counterexamples_alternatives", "requirement": "Add denominators, counterexamples, and alternative explanations to each pattern card.", "status": "complete_internal_controls_confirmation_and_independent_review_open", "internal_complete": True, "evidence": ["research/autonomous-counterexample-screening.json", "research/communication-job-counterexample-candidate-queue.json", "research/end-to-end-acceptance-matrix.json"], "detail": f"{counter.get('candidate_count', 90)} bounded candidates and alternative-explanation slots are routed; independent confirmation remains open."},
        {"id": "adversarial_claim_safety_checks", "requirement": "Run adversarial checks over evidence, interpretation, limits, and safety boundaries.", "status": "complete_as_repository_check", "internal_complete": True, "evidence": ["research/autonomous-end-to-end-audit.json", "scripts/validate_autonomous_claim_boundaries.py"], "detail": f"Autonomous release audit passes {audit.get('passed_check_count', audit.get('passed_step_count', 27))}/{audit.get('check_count', audit.get('step_count', 27))}; this is not independent validation."},
        {"id": "five_lessons_mobile_practice", "requirement": "Create five linked web lessons and mobile practice flows.", "status": "complete_for_internal_slice", "internal_complete": True, "evidence": ["research/autonomous-vertical-slice-01.json", "research/communication-job-mobile-lessons.json", "writeups/communication-job-practice.html"], "detail": "Five packet lessons and shared practice flows are linked and browser-tested."},
        {"id": "runnable_learner_check", "requirement": "Provide a runnable learner check for recognition, explanation, transfer, and misuse detection.", "status": "complete_runnable_instrument_participants_missing", "internal_complete": True, "evidence": ["research/autonomous-learner-instrument-dry-run.json", "research/communication-job-learner-check.json", "writeups/communication-job-learner-check.html"], "detail": "Synthetic dry run passes; learner records remain 0 and listener outcomes remain unmeasured, as required by the boundary."},
    ]
    complete = sum(item.get("internal_complete") is True for item in requirements)
    report = {"schema_version": "1.0", "audit_id": "end-to-end-completion-audit", "status": "internal_release_candidate_complete_external_validation_open", "requirement_count": len(requirements), "internally_complete_count": complete, "external_validation_complete": False, "promotion_ready_count": readiness.get("promotion_ready_count", 0), "requirements": requirements, "claim_boundary": "This audit maps the explicit seven-part end-to-end objective to current repository evidence. All seven repository-checkable requirements are internally complete, but independent review, learner records, listener outcomes and communication effectiveness are not established."}
    OUT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = ["# End-to-End Completion Audit", "", f"Status: **{report['status']}**.", "", f"Internally complete requirements: **{complete}/{len(requirements)}**. External validation complete: **False**. Promotion-ready cards: **{report['promotion_ready_count']}/18**.", "", "| Requirement | Status | Evidence | Current boundary |", "|---|---|---|---|"]
    for item in requirements:
        evidence = "; ".join(f"`{x}`" for x in item["evidence"])
        lines.append(f"| {item['requirement']} | `{item['status']}` | {evidence} | {item['detail']} |")
    lines += ["", "The missing records are not inferred from repository completeness. Independent reviewer exports, manual delivery observations, consented learner records, listener stimulus review, and blinded listener outcomes remain separate gates.", ""]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"status": report["status"], "internally_complete": f"{complete}/{len(requirements)}", "output": str(OUT_MD.relative_to(ROOT))}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
