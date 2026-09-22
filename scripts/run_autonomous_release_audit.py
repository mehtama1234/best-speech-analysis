#!/usr/bin/env python3
"""Run the repository-checkable end-to-end release audit in one command."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/autonomous-release-audit.json"
MD = ROOT / "writeups/autonomous-release-audit.md"


def run_step(name: str, command: list[str]) -> dict:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    return {
        "name": name,
        "command": " ".join(command),
        "return_code": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def step_plan(include_full_tests: bool = False) -> list[tuple[str, list[str]]]:
    python = sys.executable
    steps = []
    if include_full_tests:
        # The suite contains a receipt-integrity test. Establish a current
        # passing core receipt before that test runs; the outer invocation
        # writes the authoritative full receipt after all steps finish.
        steps.append(("core release receipt preflight", [python, "scripts/run_autonomous_release_audit.py"]))
        # The suite validates the manifest as it exists at test start and also
        # regenerates several authoritative reports. Prebuild it for that
        # check, then rebuild again after the suite so the receipt hashes final
        # state.
        steps.append(("reproducibility manifest preflight build", [python, "scripts/build_reproducibility_manifest.py"]))
        steps.append(("full repository test suite", [python, "-m", "unittest", "discover", "-s", "tests", "-v"]))
    steps.extend([
        ("browser runtime smoke", [python, "scripts/run_autonomous_browser_smoke.py"]),
        ("compound triad practice browser smoke", [python, "scripts/check_compound_triad_browser.py"]),
        ("media recovery integrity", [python, "scripts/validate_autonomous_media_recovery.py"]),
        ("acceptance matrix build", [python, "scripts/build_end_to_end_acceptance_matrix.py"]),
        ("shared evidence model build", [python, "scripts/build_shared_evidence_model.py"]),
        ("native client contract build", [python, "scripts/build_native_client_contracts.py"]),
        ("native TypeScript compile", ["npx", "--yes", "-p", "typescript@5.7.2", "tsc", "--noEmit", "--target", "ES2020", "--strict", "clients/generated/shared_evidence_contract.ts", "clients/examples/practice_record_helpers.ts", "clients/examples/mobile_lesson_helpers.ts"]),
        ("cross-artifact consistency", [python, "scripts/validate_cross_artifact_consistency.py"]),
        ("fail-closed promotion readiness", [python, "scripts/check_promotion_readiness.py", "--allow-blocked"]),
        ("public claim-boundary wording", [python, "scripts/check_public_claim_boundaries.py"]),
        ("model-assisted gate readiness", [python, "scripts/run_model_assisted_gate_judge.py"]),
        ("aggregate end-to-end audit", [python, "scripts/build_autonomous_end_to_end_audit.py"]),
        ("reproducibility manifest build", [python, "scripts/build_reproducibility_manifest.py"]),
        ("reproducibility manifest validation", [python, "scripts/validate_reproducibility_manifest.py"]),
    ])
    return steps


def run(include_full_tests: bool = False) -> dict:
    steps = step_plan(include_full_tests)
    results = [run_step(name, command) for name, command in steps]
    failed = [step["name"] for step in results if step["return_code"] != 0]
    return {
        "schema_version": "1.0",
        "audit_id": "autonomous-release-audit",
        "status": "release_audit_passed" if not failed else "release_audit_failed",
        "step_count": len(results),
        "passed_step_count": len(results) - len(failed),
        "failed_steps": failed,
        "steps": results,
        "claim_boundary": "This command verifies repository-local artifact joins, browser behavior, recovery routing and manifest integrity. It does not establish independent review, learner outcomes, listener outcomes or communication effectiveness.",
    }


def render(report: dict) -> str:
    lines = ["# Autonomous release audit", "", f"Status: **{report['status']}**.", "", report["claim_boundary"], "", f"Steps passed: **{report['passed_step_count']}/{report['step_count']}**.", "", "| Step | Result | Command | Output |", "|---|---:|---|---|"]
    for step in report["steps"]:
        lines.append(f"| `{step['name']}` | `{step['return_code']}` | `{step['command']}` | {step['stdout'] or step['stderr']} |")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--full-tests", action="store_true", help="also run the complete unittest suite")
    args = parser.parse_args()
    report = run(include_full_tests=args.full_tests)
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    MD.write_text(render(report))
    print(f"autonomous release audit: {report['status']} ({report['passed_step_count']}/{report['step_count']})")
    raise SystemExit(0 if not report["failed_steps"] else 1)
