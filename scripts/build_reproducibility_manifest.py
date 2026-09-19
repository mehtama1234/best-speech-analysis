#!/usr/bin/env python3
"""Build hashes and coverage counts for the authoritative speech-analysis artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/reproducibility-manifest.json"
ARTIFACTS = [
    ("research/full-reading-queue.json", "fixed source inventory"),
    ("research/full-context-reviews.json", "full-context transcript reviews"),
    ("research/corpus-evidence-bank.json", "timestamped evidence bank"),
    ("research/corpus-pattern-atlas.json", "heuristic retrieval atlas"),
    ("research/corpus-phrase-form-inventory.json", "heuristic exact phrase forms"),
    ("research/communication-job-cards.json", "provisional communication-job cards"),
    ("research/communication-job-curriculum-index.json", "integrated provisional curriculum"),
    ("research/communication-job-mobile-lessons.json", "mobile lesson payload"),
    ("research/communication-job-delivery-sampling.json", "delivery observation queue"),
    ("research/communication-job-counterexample-workbook.json", "counterexample review queue"),
    ("research/corpus-identity-review-workbook.json", "identity review queue"),
    ("research/corpus-function-independent-review-workbook.json", "function review queue"),
    ("research/corpus-recurrence-independent-review-workbook.json", "recurrence review queue"),
    ("research/corpus-phrase-form-independent-review-workbook.json", "phrase-form review queue"),
    ("research/multimodal-independent-review-workbook.json", "multimodal review queue"),
    ("research/communication-job-learner-check.json", "learner protocol"),
    ("research/communication-job-listener-outcome-protocol.json", "listener protocol"),
    ("research/shared-evidence-model.json", "shared web/mobile evidence contract"),
    ("research/end-to-end-status.json", "live status dashboard"),
    ("research/end-to-end-acceptance-matrix.json", "requirement acceptance matrix"),
    ("research/external-review-gate-index.json", "external review/data-collection routing index"),
    ("research/communication-job-promotion-readiness.json", "per-job promotion readiness audit"),
    ("research/shared-provisional-curriculum.json", "shared 18-job web curriculum index"),
    ("research/shared-lesson-cards.json", "shared 18-job web/mobile lesson cards"),
    ("research/communication-job-delivery-internal-observations.json", "internal midpoint-frame delivery observations"),
    ("research/communication-job-delivery-inventory.json", "job-level delivery inspection inventory"),
    ("research/validation-handoff.json", "human validation gate handoff"),
    ("research/communication-job-counterexample-candidate-queue.json", "counterexample candidate routing queue"),
    ("writeups/communication-job-practice.html", "local 18-job practice surface"),
    ("writeups/end-to-end-goal.md", "end-to-end goal and definition of done"),
    ("writeups/master-speech-learning-system.md", "master speech-learning system goal"),
    ("research/corpus-findings-catalog.json", "evidence-linked corpus findings catalog"),
    ("writeups/corpus-findings-catalog.md", "usable corpus findings and examples"),
    ("scripts/build_corpus_findings_catalog.py", "corpus findings catalog builder"),
    ("writeups/repeatable-communication-patterns.md", "cross-talk repeatable communication synthesis"),
    ("writeups/vertical-slice-01-reviewer-start-here.md", "vertical-slice reviewer execution handoff"),
    ("scripts/check_communication_job_delivery_browser.py", "delivery-review browser smoke test"),
    ("scripts/check_communication_job_listener_browser.py", "listener-outcome browser smoke test"),
    ("scripts/check_communication_job_learner_browser.py", "18-job learner browser smoke test"),
    ("scripts/check_communication_job_practice_browser.py", "18-job practice-surface browser smoke test"),
    ("scripts/check_listener_stimulus_adjudication_browser.py", "listener-stimulus adjudication browser smoke test"),
    ("scripts/validate_listener_stimulus_adjudication.py", "listener-stimulus adjudication validator"),
    ("scripts/lock_listener_stimuli.py", "listener-stimulus lock reducer"),
    ("writeups/communication-job-listener-stimulus-adjudication.html", "listener-stimulus adjudication form"),
    ("scripts/check_independent_review_forms_browser.py", "independent-review browser smoke test"),
    ("scripts/check_vertical_slice_lesson_browser.py", "vertical-slice learner browser smoke test"),
    ("scripts/check_vertical_slice_02_learner_browser.py", "vertical-slice 02 learner browser smoke test"),
    ("writeups/learner-field-guide.md", "learner-facing 18-job field guide"),
    ("research/full-corpus-media-coverage.json", "full transcript-corpus media availability audit"),
    ("research/full-corpus-media-recovery-queue.json", "full transcript-corpus media recovery routing queue"),
    ("scripts/recover_full_corpus_media.py", "resumable fixed-queue media recovery tool"),
    ("data/full-corpus-media-recovery.jsonl", "fixed-queue media recovery attempt ledger"),
    ("research/multimodal-pattern-comparison.json", "heuristic multimodal feature comparison"),
    ("writeups/multimodal-pattern-comparison.md", "heuristic multimodal comparison report"),
    ("scripts/compare_multimodal_patterns.py", "multimodal comparison builder"),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build() -> dict:
    queue = json.loads((ROOT / "research/full-reading-queue.json").read_text())
    reviews = json.loads((ROOT / "research/full-context-reviews.json").read_text())
    artifacts = []
    for relative, role in ARTIFACTS:
        path = ROOT / relative
        if not path.exists():
            raise FileNotFoundError(relative)
        artifacts.append({"path": relative, "role": role, "sha256": sha256(path), "bytes": path.stat().st_size})
    return {
        "schema_version": "1.0",
        "manifest_id": "best-speech-analysis-reproducibility",
        "status": "checkpoint_reproducible_artifacts_hashed_research_incomplete",
        "claim_boundary": "Hashes prove which local artifacts were checked at manifest generation. They do not prove independent review, delivery meaning, teachability, listener outcomes or effectiveness.",
        "coverage_snapshot": {"unique_inventory_videos": queue["video_count"], "full_context_reviews": len(reviews["reviews"]), "inspected_captions": queue["caption_count"]},
        "verification_commands": ["python3 -m unittest discover -s tests -p 'test_*.py'", "python3 scripts/validate_end_to_end_status.py", "python3 scripts/validate_cross_artifact_consistency.py", "python3 scripts/validate_communication_job_cards.py", "python3 scripts/validate_communication_job_curriculum.py"],
        "artifacts": artifacts,
    }


def main() -> int:
    result = build()
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "artifact_count": len(result["artifacts"]), "coverage": result["coverage_snapshot"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
