#!/usr/bin/env python3
"""Join a validated blinded review export to its private key for adjudication."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from scripts.validate_blinded_review_export import validate


def reduce(export: dict, key: dict) -> dict:
    errors = validate(export)
    if errors:
        raise ValueError("invalid blinded export: " + "; ".join(errors[:5]))
    mapping = {item["blind_item_id"]: item for item in key.get("items", [])}
    records = []
    for number in range(1, sum(payload["item_count"] for payload in _packet_gates().values()) + 1):
        response = export["responses"]
        blind_id = _blind_id_for_number(number)
        source = mapping.get(blind_id)
        if source is None:
            raise ValueError(f"missing key entry for {blind_id}")
        records.append({
            "blind_item_id": blind_id,
            "gate": source["gate"],
            "source_review_item_id": source["source_review_item_id"],
            "internal_reference": {key: value for key, value in source.items() if key.startswith("internal_")},
            "reviewer_response": {field: response[f"item_{number}_{field}"] for field in ("decision", "primary_function", "alternate", "reason", "identity_note")},
        })
    return {
        "schema_version": "1.0",
        "record_type": "blinded_review_adjudication_input",
        "status": "joined_for_adjudication_not_final_judgment",
        "reviewer_metadata": {key: export["responses"][key] for key in ("reviewer_code", "reviewer_role", "review_date", "conflict_statement")},
        "claim_boundary": "This joins a validated independent review export to internal source references for adjudication. It does not decide disagreements, promote labels, establish recurrence, or establish effectiveness.",
        "items": records,
    }


def _packet_gates() -> dict:
    packet = json.loads((Path(__file__).resolve().parents[1] / "research/blinded-review-packet.json").read_text())
    return packet["gates"]


def _blind_id_for_number(number: int) -> str:
    all_items = []
    for gate in ("function", "recurrence", "phrase_form"):
        all_items.extend(_packet_gates()[gate]["items"])
    return all_items[number - 1]["blind_item_id"]


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("usage: reduce_blinded_review_export.py EXPORT_JSON [OUTPUT_JSON]", file=sys.stderr)
        return 2
    root = Path(__file__).resolve().parents[1]
    export = json.loads(Path(sys.argv[1]).read_text())
    key = json.loads((root / "research/blinded-review-packet-key.json").read_text())
    result = reduce(export, key)
    output = Path(sys.argv[2]) if len(sys.argv) == 3 else Path("blinded-review-adjudication-input.json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(f"wrote {output}: {len(result['items'])} adjudication inputs; no judgments promoted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
