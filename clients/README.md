# Shared client contracts

The generated files in `clients/generated/` are projections of
`research/shared-evidence-model.json`:

- `shared_evidence_contract.ts` is the web/TypeScript contract.
- `SharedEvidenceContract.kt` is the Android/Kotlin contract.
- `SharedEvidenceContract.swift` is the iOS/Swift contract.

`clients/examples/practice_record_helpers.ts` shows the shared record builder
and revision diff used by client integrations. It does not upload records or
score learner performance.

Regenerate and validate them with:

```text
python3 scripts/build_native_client_contracts.py
python3 scripts/validate_native_client_contracts.py
python3 scripts/build_native_practice_fixture.py
```

When the platform toolchains are installed, compile the generated files as
part of the client build. The TypeScript projection can be checked directly:

```text
npx --yes -p typescript@5.7.2 tsc --noEmit --target ES2020 --strict clients/generated/shared_evidence_contract.ts
npx --yes -p typescript@5.7.2 tsc --noEmit --target ES2020 --strict clients/examples/practice_record_helpers.ts
```

These types carry entity fields, provenance and claim-level structure. They do
not turn provisional research into validated evidence or participant outcomes.

Local practice records use the shared JSON schema at
`research/practice-record.schema.json` and are checked with
`python3 scripts/validate_practice_record.py PATH`. The schema requires exact
transcript and delivery sample IDs so a saved attempt remains linked to the
lesson evidence it used.

`clients/examples/practice_record_fixture.json` is a synthetic cross-client
fixture. The native contract validator checks it with the same practice-record
validator used for browser exports; it contains no participant evidence.

`clients/examples/mobile_lesson_fixture.json` is a current provisional lesson
payload. The native contract validator checks its required pattern, evidence,
step, safety and validation fields before client projections are accepted.
`clients/examples/mobile_lesson_fixtures.json` applies the same check to all 18
current communication-job lessons.

`clients/examples/mobile_lesson_helpers.ts` selects a bounded lesson step and
returns linked evidence IDs while enforcing the provisional claim and safety
boundary at the client boundary.

`clients/examples/MobileLessonHelpers.kt` and
`clients/examples/MobileLessonHelpers.swift` expose the same bounded step
selection and exact-evidence-link behavior for Android and iOS integrations.
They reject promoted or unbounded lesson payloads at the client boundary; they
do not score practice or imply learner validation. They also build the same
consent-bearing local practice record and response-diff shape used by the web
helper.

Run `python3 scripts/validate_practice_record.py --audit-lessons` to check all
18 provisional lessons' evidence links without creating participant records.
To honor withdrawal of one local record, run
`python3 scripts/ingest_local_practice_records.py --ledger PATH --forget-hash HASH`.
To produce a metadata-only research summary, run
`python3 scripts/summarize_local_practice_ledger.py PATH --output SUMMARY.json`.
