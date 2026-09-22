#!/usr/bin/env python3
"""Build one machine-checked audit for the autonomous end-to-end slice."""

from __future__ import annotations

import json
from pathlib import Path

try:
    from .validate_autonomous_counterexample_screening import validate as validate_counterexamples
    from .validate_autonomous_delivery_reconciliation import validate as validate_delivery
    from .validate_autonomous_language_reconciliation import validate as validate_language
    from .validate_autonomous_review_gate_readiness import validate as validate_review_gates
    from .validate_autonomous_evidence_to_practice import validate as validate_evidence_practice
    from .validate_autonomous_multimodal_traceability import validate as validate_multimodal
    from .validate_autonomous_web_surface_integrity import validate as validate_web
    from .validate_autonomous_accessibility_privacy import validate as validate_accessibility
    from .validate_autonomous_claim_boundaries import validate as validate_claims
    from .validate_autonomous_media_recovery import validate as validate_media_recovery
    from .validate_shared_evidence_model import validate as validate_shared_model
    from .validate_native_client_contracts import validate as validate_native_clients
    from .validate_practice_record import validate as validate_practice_record, validate_all_lesson_links
    from .validate_expanded_pattern_practice_record import validate as validate_expanded_pattern_record
    from .validate_compound_triad_practice_record import validate as validate_compound_triad_record
    from .ingest_local_practice_records import ingest_records
    from .summarize_local_practice_ledger import summarize
except ImportError:
    from validate_autonomous_counterexample_screening import validate as validate_counterexamples
    from validate_autonomous_delivery_reconciliation import validate as validate_delivery
    from validate_autonomous_language_reconciliation import validate as validate_language
    from validate_autonomous_review_gate_readiness import validate as validate_review_gates
    from validate_autonomous_evidence_to_practice import validate as validate_evidence_practice
    from validate_autonomous_multimodal_traceability import validate as validate_multimodal
    from validate_autonomous_web_surface_integrity import validate as validate_web
    from validate_autonomous_accessibility_privacy import validate as validate_accessibility
    from validate_autonomous_claim_boundaries import validate as validate_claims
    from validate_autonomous_media_recovery import validate as validate_media_recovery
    from validate_shared_evidence_model import validate as validate_shared_model
    from validate_native_client_contracts import validate as validate_native_clients
    from validate_practice_record import validate as validate_practice_record, validate_all_lesson_links
    from validate_expanded_pattern_practice_record import validate as validate_expanded_pattern_record
    from validate_compound_triad_practice_record import validate as validate_compound_triad_record
    from ingest_local_practice_records import ingest_records
    from summarize_local_practice_ledger import summarize


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/autonomous-end-to-end-audit.json"
MD = ROOT / "writeups/autonomous-end-to-end-audit.md"


def read(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text())


def build() -> dict:
    curriculum = read("research/autonomous-curriculum-audit.json")
    delivery = read("research/autonomous-delivery-reconciliation.json")
    media = read("research/autonomous-full-media-reconciliation.json")
    language = read("research/autonomous-language-reconciliation.json")
    packet = read("research/autonomous-vertical-slice-01.json")
    learner_dry_run = read("research/autonomous-learner-instrument-dry-run.json")
    full_curriculum = read("research/autonomous-full-curriculum-audit.json")
    listener_dry_run = read("research/autonomous-listener-instrument-dry-run.json")
    identity = read("research/autonomous-identity-reconciliation.json")
    acceptance = read("research/end-to-end-acceptance-matrix.json")
    local_llm = read("research/local-llm-lesson-judge.json")
    expanded_llm = read("research/local-llm-expanded-pattern-judge.json")
    gate_llm = read("research/local-llm-gate-judge.json")
    draft_llm = read("research/local-llm-draft-judge.json")
    expanded_browser = read("research/expanded-pattern-browser-smoke.json")
    triad_browser = read("research/compound-triad-browser-smoke.json")
    priority_review = read("research/recovered-pattern-priority-review.json")
    checks: list[dict] = []

    def check(name: str, status: str, evidence: list[str], detail: str) -> None:
        missing = [path for path in evidence if not (ROOT / path).exists()]
        checks.append({
            "layer": name,
            "status": "pass" if status == "pass" and not missing else "fail",
            "evidence": evidence,
            "detail": detail if not missing else f"missing artifacts: {', '.join(missing)}",
        })

    check(
        "fixed corpus and curriculum",
        "pass" if curriculum.get("coverage", {}).get("fixed_corpus_videos") == 395 and curriculum.get("coverage", {}).get("full_context_reviews") == 395 and curriculum.get("coverage", {}).get("communication_jobs") == 18 else "fail",
        ["research/autonomous-curriculum-audit.json", "writeups/autonomous-curriculum-audit.md"],
        "395 fixed-corpus videos, 395 full-context reviews and 18 communication jobs reconcile.",
    )
    check(
        "five-packet vertical slice",
        "pass" if packet.get("status") == "autonomous_reconciliation_complete" and packet.get("packets_reconciled") == 5 else "fail",
        ["research/autonomous-vertical-slice-01.json", "writeups/autonomous-vertical-slice-01.md"],
        "Five lesson packets have examples, controls, media-proxy caveats, lesson links and safety fields.",
    )
    check(
        "delivery proxy layer",
        "pass" if delivery.get("item_count") == 36 and "effectiveness" in delivery.get("claim_boundary", "").lower() else "fail",
        ["research/autonomous-delivery-reconciliation.json", "writeups/autonomous-delivery-reconciliation.md"],
        "36 job-linked delivery rows reconcile to local timing/audio proxies without semantic or effectiveness claims.",
    )
    check(
        "full media coverage",
        "pass" if media.get("coverage", {}).get("fixed_corpus_videos", media.get("video_count")) == 395 or media.get("video_count") == 395 else "fail",
        ["research/autonomous-full-media-reconciliation.json", "writeups/autonomous-full-media-reconciliation.md"],
        "Every fixed-corpus video has an explicit local media/proxy availability state.",
    )
    check(
        "language and recurrence layer",
        "pass" if "not_validation" in language.get("status", "") else "fail",
        ["research/autonomous-language-reconciliation.json", "writeups/autonomous-language-reconciliation.md"],
        "Exact forms and recurrence candidates reconcile while remaining provisional.",
    )
    counter_errors = validate_counterexamples()
    check(
        "counterexample screening",
        "pass" if not counter_errors else "fail",
        ["research/autonomous-counterexample-screening.json", "scripts/validate_autonomous_counterexample_screening.py"],
        "90 bounded candidates cover 18 jobs at five types per job; none is promoted.",
    )
    practice_row = next((row for row in acceptance.get("rows", []) if row.get("requirement_id") == "practice_and_shared_curriculum"), {})
    check(
        "acceptance-matrix integration",
        "pass" if "research/autonomous-vertical-slice-01.json" in practice_row.get("evidence", []) else "fail",
        ["research/end-to-end-acceptance-matrix.json", "scripts/build_end_to_end_acceptance_matrix.py"],
        "The project-level acceptance matrix links the autonomous vertical slice.",
    )
    check(
        "learner instrument dry run",
        "pass" if learner_dry_run.get("status") == "instrument_export_validation_and_scoring_passed" and learner_dry_run.get("pattern_count") == 5 and learner_dry_run.get("full_curriculum", {}).get("status") == "full_18_job_synthetic_export_validated" and learner_dry_run.get("full_curriculum", {}).get("job_count") == 18 and learner_dry_run.get("full_curriculum", {}).get("task_count") == 72 else "fail",
        ["research/autonomous-learner-instrument-dry-run.json", "writeups/autonomous-learner-instrument-dry-run.md", "scripts/run_autonomous_learner_dry_run.py"],
        "The five-section slice and full 18-job/72-task learner export paths validate on synthetic records explicitly excluded from learner evidence.",
    )
    check(
        "full 18-job curriculum surface",
        "pass" if full_curriculum.get("status") == "full_18_job_surface_reconciled_not_validated" and full_curriculum.get("job_count") == 18 else "fail",
        ["research/autonomous-full-curriculum-audit.json", "writeups/autonomous-full-curriculum-audit.md", "scripts/build_autonomous_full_curriculum_audit.py"],
        "All 18 jobs join across canonical cards, mobile lessons, learner protocol and web surfaces.",
    )
    check(
        "listener instrument dry run",
        "pass" if listener_dry_run.get("status") == "instrument_export_validation_and_summary_passed" and listener_dry_run.get("record_count") == 2 and listener_dry_run.get("summary", {}).get("promotion_eligible") is False and listener_dry_run.get("full_curriculum", {}).get("status") == "full_18_job_synthetic_export_validated" and listener_dry_run.get("full_curriculum", {}).get("job_count") == 18 and listener_dry_run.get("full_curriculum", {}).get("record_count") == 36 else "fail",
        ["research/autonomous-listener-instrument-dry-run.json", "writeups/autonomous-listener-instrument-dry-run.md", "scripts/run_autonomous_listener_dry_run.py"],
        "The listener record validator and summary path pass on slice fixtures plus 36 synthetic records covering both conditions across all 18 jobs, without promotion.",
    )
    check(
        "identity metadata preflight",
        "pass" if identity.get("status") == "metadata_reconciliation_complete_identity_not_proven" and identity.get("video_count") == 395 and identity.get("issue_count") == 0 else "fail",
        ["research/autonomous-identity-reconciliation.json", "writeups/autonomous-identity-reconciliation.md", "scripts/build_autonomous_identity_reconciliation.py"],
        "All 395 fixed-corpus rows have consistent metadata, URL linkage, review linkage and identity-workbook coverage; identity decisions remain blank.",
    )
    delivery_errors = validate_delivery()
    check(
        "delivery lineage validator",
        "pass" if not delivery_errors and delivery.get("item_count") == 36 else "fail",
        ["research/autonomous-delivery-reconciliation.json", "research/communication-job-delivery-measurement-preflight.json", "scripts/validate_autonomous_delivery_reconciliation.py"],
        "The 36 delivery rows have local feature, frame, transcript and bounded observation lineage checks.",
    )
    language_errors = validate_language()
    check(
        "language recurrence validator",
        "pass" if not language_errors else "fail",
        ["research/autonomous-language-reconciliation.json", "research/corpus-recurrence-independent-review-workbook.json", "scripts/validate_autonomous_language_reconciliation.py"],
        "The 50 phrase forms and 192 recurrence candidates preserve a 96/96 split, event-level separation and explicit non-independence boundaries.",
    )
    review_gate_errors = validate_review_gates()
    check(
        "external review gate readiness",
        "pass" if not review_gate_errors else "fail",
        ["research/external-review-gate-index.json", "research/blinded-review-packet.json", "scripts/validate_autonomous_review_gate_readiness.py"],
        "All 10 independent-review and participant-data gates have runnable forms, validators and boundaries; 429 blinded items remain unanswered.",
    )
    check(
        "recovered pattern priority review readiness",
        "pass" if priority_review.get("pattern_count") == 55 and priority_review.get("item_count") == 162 and priority_review.get("promotion_eligible") is False else "fail",
        ["research/recovered-pattern-priority-review.json", "research/recovered-pattern-priority-review-key.json", "writeups/recovered-pattern-priority-review.html", "scripts/validate_recovered_pattern_priority_review_export.py", "scripts/check_recovered_pattern_priority_review_browser.py", "scripts/compare_recovered_pattern_priority_reviews.py", "scripts/build_recovered_pattern_priority_adjudication.py"],
        "The 162-item label-blinded launch packet spans all 55 recovered presentation patterns, has a separate internal key, a runtime browser path and a fail-closed export validator; no human review is implied.",
    )
    evidence_practice_errors = validate_evidence_practice()
    check(
        "evidence-to-practice traceability",
        "pass" if not evidence_practice_errors else "fail",
        ["research/shared-lesson-cards.json", "research/communication-job-mobile-lessons.json", "research/communication-job-learner-check.json", "research/expanded-pattern-candidate-cards.json", "research/presentation-sequence-library.json", "scripts/validate_autonomous_evidence_to_practice.py"],
        "All 18 production jobs trace eight distinct-video examples, exact transcript evidence, counterexample slots, delivery links and four learner task phases; six expanded candidate talk architectures retain links to their source cards.",
    )
    multimodal_errors = validate_multimodal()
    check(
        "multimodal traceability",
        "pass" if not multimodal_errors else "fail",
        ["research/communication-job-delivery-sampling.json", "research/communication-job-delivery-measurement-preflight.json", "scripts/validate_autonomous_multimodal_traceability.py"],
        "All 36 delivery samples trace to matched transcript intervals, local feature files, aligned IDs, nearest frames and proxy limits.",
    )
    web_errors = validate_web()
    check(
        "web surface integrity",
        "pass" if not web_errors else "fail",
        ["writeups/communication-job-curriculum.html", "writeups/communication-job-practice.html", "writeups/communication-job-learner-check.html", "writeups/shared-provisional-curriculum.html", "writeups/shared-lesson-cards.html", "scripts/validate_autonomous_web_surface_integrity.py"],
        "The five local web surfaces expose all 18 jobs, resolve local links and retain provisional boundaries and task/card payloads.",
    )
    browser_smoke = read("research/autonomous-browser-smoke.json")
    check(
        "browser runtime smoke",
        "pass" if browser_smoke.get("status") == "core_browser_smoke_passed" and browser_smoke.get("check_count") == browser_smoke.get("passed_check_count") else "fail",
        ["research/autonomous-browser-smoke.json", "writeups/autonomous-browser-smoke.md", "scripts/run_autonomous_browser_smoke.py", "scripts/check_practice_pwa_browser.py", "scripts/check_recovered_pattern_priority_review_browser.py", "scripts/check_unified_pattern_library_browser.py", "research/unified-pattern-library-browser-smoke.json", "writeups/unified-pattern-library.html", "writeups/recovered-pattern-priority-review.html"],
        f"{browser_smoke.get('check_count', 0)} browser paths render, navigate, export and validate locally, including the blinded recovered-pattern priority review; the receipt remains a runtime check rather than outcome evidence.",
    )
    accessibility_errors = validate_accessibility()
    check(
        "accessibility and privacy boundary",
        "pass" if not accessibility_errors else "fail",
        ["writeups/communication-job-practice.html", "writeups/communication-job-learner-check.html", "writeups/communication-job-listener-record.html", "writeups/blinded-review-packet.html", "scripts/validate_autonomous_accessibility_privacy.py"],
        "Seven user surfaces declare responsive structure, labelled controls, consent/local-data boundaries and no network submission primitive.",
    )
    claim_errors = validate_claims()
    if local_llm.get("promotion_eligible") is not False or local_llm.get("status") != "local_model_judgment_recorded_human_validation_open":
        claim_errors.append("local LLM lesson judgment must remain non-promotional while human validation is open")
    if expanded_llm.get("promotion_eligible") is not False or expanded_llm.get("status") != "local_model_candidate_screen_recorded_review_open":
        claim_errors.append("expanded-pattern LLM screen must remain non-promotional while review is open")
    if gate_llm.get("promotion_eligible") is not False or gate_llm.get("status") != "local_model_gate_prioritization_recorded_human_gates_open" or gate_llm.get("judgment", {}).get("overall") != "prioritized_not_completed":
        claim_errors.append("local LLM gate prioritization must remain non-promotional and incomplete")
    if draft_llm.get("promotion_eligible") is not False or draft_llm.get("status") != "local_model_draft_screen_recorded_not_effectiveness_evidence" or draft_llm.get("parsed_judgment_count") != 1:
        claim_errors.append("local LLM draft screen must remain parsed and non-promotional")
    if expanded_browser.get("status") != "expanded_pattern_browser_smoke_passed" or expanded_browser.get("card_count") != 33:
        claim_errors.append("expanded pattern browser smoke must cover all 33 cards")
    if triad_browser.get("status") != "compound_triad_browser_smoke_passed" or triad_browser.get("triad_count") != 24:
        claim_errors.append("compound triad browser smoke must cover all 24 practice triads")
    expanded_record_errors = validate_expanded_pattern_record(read("research/expanded-pattern-practice-record.example.json"))
    claim_errors.extend(f"expanded practice record: {error}" for error in expanded_record_errors)
    triad_example = {
        "record_type": "local_compound_triad_practice_record",
        "triad_id": read("research/compound-pattern-triads.json")["triads"][0]["triad_id"],
        "source_review_ids": ["synthetic-review"],
        "source_evidence_ids": ["synthetic-evidence"],
        "draft": "Move one. Move two. Move three.",
        "reflections": {"listener": "clear", "unclear": "none", "nonfit": "none", "revision": "shorten bridge"},
        "claim_boundary": "Local triad practice record; not effectiveness evidence.",
        "saved_at": "2026-09-19T00:00:00Z",
    }
    claim_errors.extend(f"triad practice record: {error}" for error in validate_compound_triad_record(triad_example))
    check(
        "claim-boundary integrity",
        "pass" if not claim_errors else "fail",
        ["research/shared-lesson-cards.json", "research/communication-job-mobile-lessons.json", "research/communication-job-learner-check.json", "research/communication-job-listener-outcome-protocol.json", "research/local-llm-lesson-judge.json", "research/expanded-pattern-candidate-cards.json", "research/local-llm-expanded-pattern-judge.json", "research/local-llm-gate-judge.json", "research/local-llm-draft-judge.json", "research/expanded-pattern-practice-record.example.json", "research/expanded-pattern-browser-smoke.json", "research/compound-pattern-triads.json", "research/compound-triad-browser-smoke.json", "scripts/validate_autonomous_claim_boundaries.py", "scripts/run_local_llm_lesson_judge.py", "scripts/run_local_llm_expanded_pattern_judge.py", "scripts/run_local_llm_gate_judge.py", "scripts/run_local_llm_draft_judge.py", "scripts/validate_expanded_pattern_practice_record.py", "scripts/validate_compound_triad_practice_record.py", "scripts/check_expanded_pattern_browser.py", "scripts/check_compound_triad_browser.py"],
        "All 18 production cards, 33 expanded candidate cards and 24 triad practice candidates remain explicitly provisional; local LLM screens, browser smoke, and both practice-record validators remain non-promotional.",
    )
    media_recovery_errors = validate_media_recovery()
    check(
        "media recovery integrity",
        "pass" if not media_recovery_errors else "fail",
        ["research/full-corpus-media-coverage.json", "research/full-corpus-media-recovery-queue.json", "data/full-corpus-media-recovery.jsonl", "scripts/validate_autonomous_media_recovery.py"],
        "The 41 unavailable or partial media records remain routed with file-state consistency; a partial download cannot silently become raw A/V coverage.",
    )
    shared_model_errors = validate_shared_model(read("research/shared-evidence-model.json"))
    check(
        "shared web/mobile evidence contract",
        "pass" if not shared_model_errors else "fail",
        ["research/shared-evidence-model.json", "research/shared-lesson-cards.json", "research/communication-job-mobile-lessons.json", "scripts/validate_shared_evidence_model.py"],
        "The shared evidence contract, current manifest and web/mobile lesson payload remain synchronized with explicit missingness and claim-level rules.",
    )
    native_client_errors = validate_native_clients()
    check(
        "native client contract outputs",
        "pass" if not native_client_errors else "fail",
        ["clients/generated/shared_evidence_contract.ts", "clients/generated/SharedEvidenceContract.kt", "clients/generated/SharedEvidenceContract.swift", "clients/examples/mobile_lesson_helpers.ts", "clients/examples/MobileLessonHelpers.kt", "clients/examples/MobileLessonHelpers.swift", "clients/examples/practice_record_fixture.json", "scripts/validate_native_client_contracts.py"],
        "Generated TypeScript, Kotlin and Swift types plus matching lesson helpers enforce the shared evidence boundary, and a synthetic practice record crosses the same validator; these artifacts carry the schema and client guardrails, not research validation claims.",
    )
    synthetic_practice_record = {
        "record_type": "local_communication_practice_record",
        "schema_version": "1.0",
        "lesson_id": "mobile:provisional-job-opening",
        "pattern_id": "provisional-job-opening",
        "canonical_job": "opening",
        "source_evidence_ids": ["dgkxN6RASpg:00000"],
        "delivery_sample_ids": ["delivery:opening:01"],
        "participant_code": "synthetic-local-user",
        "consent": True,
        "accessibility_or_modality": "typed",
        "step_responses": {"rehearse": "synthetic response"},
        "claim_boundary": "Local practice log only; not learner-validation evidence or effectiveness evidence.",
        "saved_at": "2026-09-19T00:00:00Z",
    }
    practice_record_errors = validate_practice_record(synthetic_practice_record) + validate_all_lesson_links()
    check(
        "practice record contract",
        "pass" if not practice_record_errors else "fail",
        ["research/shared-evidence-model.json", "research/practice-record.schema.json", "scripts/validate_practice_record.py", "tests/test_practice_record_contract.py"],
        "Synthetic browser/native records for the 18 lessons validate consent, exact evidence links and the non-effectiveness boundary; no participant evidence is inferred.",
    )
    ingestion_report = ingest_records([synthetic_practice_record], dry_run=True)
    check(
        "practice record ingestion",
        "pass" if ingestion_report.get("accepted") == 1 and not ingestion_report.get("rejected") else "fail",
        ["scripts/ingest_local_practice_records.py", "scripts/validate_practice_record.py", "tests/test_ingest_local_practice_records.py"],
        "A validated practice record can enter a local append-only ledger with deduplication and an explicit non-evidence boundary; no participant data is written by the audit.",
    )
    summary = summarize([synthetic_practice_record])
    check(
        "practice ledger summary",
        "pass" if summary.get("record_count") == 1 and summary.get("invalid_record_count") == 0 and "does not score" in summary.get("claim_boundary", "") else "fail",
        ["scripts/summarize_local_practice_ledger.py", "scripts/validate_practice_record.py", "tests/test_summarize_local_practice_ledger.py"],
        "A bounded metadata summary returns job, modality and response-count metadata, detects tampered ingested rows, and never scores outcomes or effectiveness.",
    )
    failed = [row["layer"] for row in checks if row["status"] != "pass"]
    return {
        "schema_version": "1.0",
        "audit_id": "autonomous-end-to-end-audit",
        "status": "autonomous_release_candidate_reconciled_not_promotion_validated" if not failed else "needs_repair",
        "check_count": len(checks),
        "passed_check_count": len(checks) - len(failed),
        "failed_layers": failed,
        "checks": checks,
        "claim_boundary": "This audit proves that local autonomous artifacts join into a reproducible end-to-end release candidate. It does not establish independent agreement, speaker identity or intent, learner observations or teachability, listener outcomes, communication effectiveness or universal best practice.",
        "open_outcome_gates": ["independent review", "learner observations", "listener outcomes", "effectiveness and causal evidence"],
    }


def render(report: dict) -> str:
    lines = [
        "# Autonomous end-to-end audit",
        "",
        f"Status: **{report['status']}**.",
        "",
        report["claim_boundary"],
        "",
        f"Checks passed: **{report['passed_check_count']}/{report['check_count']}**.",
        "",
        "| Layer | Status | Evidence | Detail |",
        "|---|---|---|---|",
    ]
    for row in report["checks"]:
        lines.append(f"| `{row['layer']}` | `{row['status']}` | {', '.join(f'`{x}`' for x in row['evidence'])} | {row['detail']} |")
    lines += [
        "",
        "## Open outcome gates",
        "",
        "The autonomous release candidate is usable as a bounded research and practice surface. The following remain explicitly open: independent review, learner observations, listener outcomes, and effectiveness or causal evidence.",
        "",
        "## Machine command",
        "",
        "```text",
        "python3 scripts/build_autonomous_end_to_end_audit.py",
        "```",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    report = build()
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    MD.write_text(render(report))
    print(f"autonomous end-to-end audit: {report['status']} ({report['passed_check_count']}/{report['check_count']})")
    if report["failed_layers"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
