# Commentary Schema Discovery

This task folder contains the PES commentary schema discovery work.

## Folder Map

- `pattern_scan/`
  - High-level scan of recurring commentary patterns across the 29 converted
    PES 2015-16 Markdown files.
- `schema/`
  - Current draft JSON schema and frozen `commentary_schema_v0.1.json`.
- `stress_test/`
  - Limited 3-file extraction test and review showing where the schema broke.
- `stress_test_hard_cases/`
  - Deliberate hard-case test using dense prose, programme-heavy policy, and
    table/indicator-heavy files.
- `extraction_pilot_5_random/`
  - Five-file random extraction pilot using frozen schema v0.1.
- `archive/`
  - Non-active copies kept for traceability.

## Current Active Files

- `pattern_scan/commentary_pattern_scan.md`
- `schema/commentary_schema_draft.json`
- `schema/commentary_schema_v0.1.json`
- `stress_test/schema_stress_test_claims.json`
- `stress_test/schema_stress_test_review.md`
- `stress_test_hard_cases/hard_case_claims.json`
- `stress_test_hard_cases/hard_case_schema_review.md`
- `extraction_pilot_5_random/extraction_pilot_claims.json`
- `extraction_pilot_5_random/extraction_pilot_review.md`

Original PDFs remain source truth. Markdown is only a working text layer, and
tables/charts/numeric values need separate QA.
