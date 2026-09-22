#!/usr/bin/env python3
"""Create a portable, label-blinded first-batch reviewer archive."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "research/recovered-pattern-priority-review.json"
KEY_PATH = ROOT / "research/recovered-pattern-priority-review-key.json"
BROWSER_PATH = ROOT / "writeups/recovered-pattern-priority-review.html"
OUT = ROOT / "deliverables/recovered-pattern-priority-reviewer-pack.zip"


def instructions(packet: dict) -> str:
    return f"""# Independent review: presentation-pattern first batch

This review covers {packet['item_count']} excerpts drawn from 55 provisional
presentation-pattern ideas. Each item states the proposed move in plain words,
so you know what to check. The internal pattern name, category and card ID are
hidden. This is a first check of selected examples, not proof that a move is
common, useful or effective.

## Independence and blinding

Each reviewer must work independently, must not have created these ideas or
their labels, and must not have seen the internal mapping key or another
reviewer's decisions. Do not share completed reviews before both are returned.
In other words, do not have seen the internal mapping key or the other review
before you finish your own.
Use a reviewer code and honestly describe any connection to this project. The
browser records your statement; it cannot verify your independence.

## Review

Open `recovered-pattern-priority-review.html` in a browser. For each item,
compare the excerpt with the proposed move. Open the source and read more of the
surrounding transcript or video when possible. Record what the speaker is
doing, another plausible explanation, relevant context, any source or access
concern, and what remains uncertain. If the excerpt does not show the move,
say what it does instead. If you cannot tell, choose that option; do not guess.
You may leave items blank. A blank answer stays missing; it is never counted as
agreement.

The six choices mean: the excerpt shows the proposed move; the speaker is doing
something else; the context is too limited; you are unsure for another reason;
the speaker/source may be wrong; or the clip may be a duplicate or compilation.
Each item says whether its transcript came from the linked video, another
video source, or an outside transcript. Machine-made transcripts can be wrong,
so check the linked recording where possible.

Download the JSON export and return it unchanged. Do not add candidate labels or
merge it with another review. Keep your working copy private until both
independent reviews have been returned.

## Return validation (for the coordinator)

From the project repository, run:

```text
python3 scripts/validate_recovered_pattern_priority_review_export.py reviewer.json
```

After two independent returns validate, compare them and route observed
disagreements to adjudication using the commands in
`writeups/next-validation-runbook.md`. Preserve all exports, missing responses,
comparison, and adjudication as separate records. Review agreement or
adjudication does not establish recurrence, teachability, audience outcomes,
or effectiveness.
"""


def build(output: Path = OUT) -> dict:
    packet = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
    key = json.loads(KEY_PATH.read_text(encoding="utf-8"))
    browser = BROWSER_PATH.read_bytes()
    packet_bytes = (json.dumps(packet, ensure_ascii=False, indent=2) + "\n").encode()

    if packet.get("status") != "priority_launch_packet_no_human_records":
        raise ValueError("unexpected packet status")
    if packet.get("promotion_eligible") is not False:
        raise ValueError("packet must remain non-promotion eligible")
    if len(packet.get("items", [])) != packet.get("item_count"):
        raise ValueError("packet item count does not reconcile")
    if key.get("status") != "internal_priority_key_do_not_send_with_packet":
        raise ValueError("internal key status is not recognized")
    if {x["blind_item_id"] for x in packet["items"]} != {x["blind_item_id"] for x in key["items"]}:
        raise ValueError("packet and internal key IDs do not reconcile")
    forbidden = ("pattern_id", "candidate_form", "card_id", "category", "quality_flags", "quality_disposition")
    packet_text = packet_bytes.decode()
    if any(name in packet_text for name in forbidden):
        raise ValueError("blinded packet contains an internal label field")
    pattern_ids = {item["pattern_id"] for item in key["items"]}
    if any(pattern_id and pattern_id in packet_text for pattern_id in pattern_ids):
        raise ValueError("blinded packet contains a key label value")
    if KEY_PATH.name.encode() in browser:
        raise ValueError("browser unexpectedly references the private key")

    files = {
        "README-reviewer.md": instructions(packet).encode(),
        "recovered-pattern-priority-review.html": browser,
        "recovered-pattern-priority-review.json": packet_bytes,
    }
    checksums = "".join(
        f"{hashlib.sha256(data).hexdigest()}  {name}\n" for name, data in sorted(files.items())
    ).encode()
    files["SHA256SUMS"] = checksums

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 22, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)

    with zipfile.ZipFile(output) as archive:
        names = set(archive.namelist())
        if names != set(files) or any("key" in name.lower() for name in names):
            raise ValueError("archive members do not match the blinded payload")
        for name, expected in files.items():
            if archive.read(name) != expected:
                raise ValueError(f"archive verification failed for {name}")
        for line in archive.read("SHA256SUMS").decode().splitlines():
            digest, name = line.split("  ", 1)
            if hashlib.sha256(archive.read(name)).hexdigest() != digest:
                raise ValueError(f"checksum verification failed for {name}")

    return {
        "output": str(output),
        "item_count": packet["item_count"],
        "pattern_count": packet["pattern_count"],
        "members": sorted(files),
        "private_key_included": False,
        "checksums_verified": True,
    }


def main() -> int:
    print(json.dumps(build(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
