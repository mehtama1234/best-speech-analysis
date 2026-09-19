# Full-corpus timing candidate atlas

Status: **full local feature proxy atlas; manual listening and independent review pending**.

This atlas routes transcript/audio feature candidates for navigation. Caption gaps may reflect editing, missing captions, music, turn changes or silence; density reflects retained caption segmentation. No row establishes an intentional pause, pace choice, vocal meaning, identity, alignment, effectiveness or listener outcome.

Aligned feature coverage: **357 videos / 97743 caption rows** · routed candidate records: **5557** across **357 videos**.

| Candidate reason | Routed records | Raw matches before density cap |
|---|---:|---:|
| `gap_before_captioned_unit` | 2079 | 2079 |
| `gap_after_captioned_unit` | 2079 | 2079 |
| `lower_caption_density_proxy` | 1032 | 32964 |
| `higher_caption_density_proxy` | 367 | 2999 |

## Review rule

Open the linked source interval and inspect the complete captioned unit. Decide whether the boundary or density comes from speech, silence, an edit, music, a turn change, caption segmentation or missing data. Preserve `indeterminate` when the source cannot establish the cause. The atlas is a navigation surface, not a best-practice ranking.
