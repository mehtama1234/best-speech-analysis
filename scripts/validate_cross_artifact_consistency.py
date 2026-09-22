#!/usr/bin/env python3
"""Check that the primary status and handoff artifacts agree on scope."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_HANDOFF = ROOT / "research/external-source-candidate-handoff.json"
DRY_BAR_EXTERNAL_HANDOFF = ROOT / "research/external-source-candidate-handoff-dry-bar.json"
TED_EXTERNAL_HANDOFF = ROOT / "research/external-source-candidate-handoff-ted.json"


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text())


def validate() -> list[str]:
    status = load("research/end-to-end-status.json")
    matrix = load("research/end-to-end-acceptance-matrix.json")
    readiness = load("research/communication-job-promotion-readiness.json")
    gates = load("research/external-review-gate-index.json")
    browser_smoke = load("research/autonomous-browser-smoke.json")
    errors = []
    if not EXTERNAL_HANDOFF.is_file():
        errors.append("missing external source candidate handoff")
    else:
        external = json.loads(EXTERNAL_HANDOFF.read_text())
        if external.get("status") != "candidate_source_visible_not_in_fixed_corpus":
            errors.append("external source handoff must remain outside fixed corpus")
        if external.get("candidate_count") != 7 or external.get("fixed_corpus_inclusion") is not False:
            errors.append("external source handoff candidate count or inclusion boundary is stale")
        for path in external.get("candidate_artifacts", []):
            if not (ROOT / path).resolve().is_file():
                errors.append(f"external source handoff artifact missing: {path}")
    if not DRY_BAR_EXTERNAL_HANDOFF.is_file():
        errors.append("missing Dry Bar external source candidate handoff")
    else:
        dry_bar = json.loads(DRY_BAR_EXTERNAL_HANDOFF.read_text())
        if dry_bar.get("status") != "candidate_source_visible_not_in_fixed_corpus" or dry_bar.get("candidate_count") != 6:
            errors.append("Dry Bar external source handoff status or candidate count is stale")
        if dry_bar.get("fixed_corpus_inclusion") is not False:
            errors.append("Dry Bar external source handoff must remain outside fixed corpus")
        for path in dry_bar.get("candidate_artifacts", []):
            if not (ROOT / path).resolve().is_file():
                errors.append(f"Dry Bar external handoff artifact missing: {path}")
    if not TED_EXTERNAL_HANDOFF.is_file():
        errors.append("missing TED external source candidate handoff")
    else:
        ted = json.loads(TED_EXTERNAL_HANDOFF.read_text())
        if ted.get("status") != "candidate_source_visible_not_in_fixed_corpus" or ted.get("candidate_count") != 6 or ted.get("fixed_corpus_inclusion") is not False:
            errors.append("TED external source handoff status, candidate count, or inclusion boundary is stale")
        for path in ted.get("candidate_artifacts", []):
            if not (ROOT / path).resolve().is_file(): errors.append(f"TED external handoff artifact missing: {path}")
    stages = status["stages"]

    expected = {
        "transcript_reviews": (stages["transcript_context"]["video_count"], 395),
        "cards": (stages["communication_job_cards"]["card_count"], readiness["card_count"]),
        "delivery_samples": (stages["communication_job_delivery_sampling"]["queued_sample_count"], 36),
        "learner_tasks": (stages["communication_job_learner_check"]["task_count"], 72),
        "listener_jobs": (stages["communication_job_listener_outcomes"]["pattern_count"], 18),
        "listener_tasks": (stages["communication_job_listener_outcomes"]["listener_task_count"], 6),
    }
    for label, (actual, required) in expected.items():
        if actual != required:
            errors.append(f"{label}: expected {required}, found {actual}")

    media = stages["full_corpus_media_coverage"]
    media_total = sum(media.get(key, 0) for key in ("raw_audio_video_present", "audio_only", "video_only", "derived_features_only", "transcript_only_no_local_media"))
    if media_total != media["video_count"]:
        errors.append(f"full-corpus media states sum to {media_total}, not {media['video_count']}")
    if matrix["open_requirement_count"] != sum(row["status"] not in {"complete_for_fixed_corpus", "contract_and_validators_ready"} for row in matrix["rows"]):
        errors.append("acceptance matrix open_requirement_count is stale")
    if readiness["promotion_ready_count"] != 0 or len(readiness["cards"]) != readiness["card_count"]:
        errors.append("promotion readiness count or card rows is inconsistent")
    readiness_stage = status["stages"].get("promotion_readiness", {})
    if readiness_stage.get("card_count") != readiness["card_count"] or readiness_stage.get("promotion_ready_count") != readiness["promotion_ready_count"]:
        errors.append("end-to-end promotion readiness stage is stale")

    gate_counts = {gate["gate_id"]: gate["item_count"] for gate in gates["gates"]}
    for gate_id, count in {"identity": 395, "delivery": 36, "learner": 72, "listener_stimuli": 18, "listener_outcomes": 18}.items():
        if gate_counts.get(gate_id) != count:
            errors.append(f"gate {gate_id}: expected {count}, found {gate_counts.get(gate_id)}")

    # Keep the maintainer-facing handoff synchronized with the receipts. These
    # checks prevent a passing audit from being paired with stale instructions
    # or an outdated browser-path count.
    handoff_paths = [
        ROOT / "README.md",
        ROOT / "writeups/start-here.md",
        ROOT / "writeups/validation-handoff.md",
        ROOT / "PROJECT_STATUS.md",
    ]
    browser_count = f"{browser_smoke['passed_check_count']}/{browser_smoke['check_count']}"
    required_phrases = {
        "python3 scripts/run_autonomous_release_audit.py": "release audit command",
        "27/27": "aggregate audit count",
        browser_count: "browser smoke count",
    }
    for path in handoff_paths:
        text = path.read_text()
        for phrase, label in required_phrases.items():
            if phrase not in text:
                errors.append(f"{path.relative_to(ROOT)} missing current {label} ({phrase})")
    audit_text = (ROOT / "writeups/autonomous-end-to-end-audit.md").read_text().lower()
    if "not_promotion_validated" not in audit_text and "without promotion" not in audit_text:
        errors.append("autonomous end-to-end audit missing non-promotion boundary")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("cross-artifact consistency invalid:\n" + "\n".join(f"- {error}" for error in errors))
        return 1
    print("cross-artifact consistency valid: status, acceptance, readiness and gates reconcile")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
