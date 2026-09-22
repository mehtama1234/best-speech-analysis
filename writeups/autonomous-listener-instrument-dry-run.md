# Autonomous listener-instrument dry run

Status: **instrument_export_validation_and_summary_passed**.

Synthetic instrument dry run only; no listener participated and no outcome claim is made.

Two slice condition records passed validation and summary generation; a separate synthetic run covers **18 jobs and 36 balanced condition records**. `promotion_eligible` remains `False`.

This is an instrument check, not listener evidence.

```text
python3 scripts/run_autonomous_listener_dry_run.py
```
