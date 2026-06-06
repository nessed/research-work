# Commentary Schema Discovery

This task folder contains the PES commentary schema discovery work. It is a
schema and extraction-prompt design area, not a full extraction run.

## Active Folders

- `pattern_scan/`
  - High-level scan of recurring commentary patterns across the 29 converted
    PES 2015-16 Markdown files.
- `schema/`
  - Current draft JSON schema and frozen working `commentary_schema_v0.1.json`.
- `stress_tests/`
  - Random and hard-case extraction tests used to validate the schema.
- `extraction_pilots/`
  - Five-file random extraction pilot using frozen schema v0.1.
- `archive/`
  - Superseded or renamed material retained for provenance.

## Current Active Files

- `pattern_scan/commentary_pattern_scan.md`
- `schema/commentary_schema_draft.json`
- `schema/commentary_schema_v0.1.json`
- `stress_tests/schema_stress_test_claims.json`
- `stress_tests/schema_stress_test_review.md`
- `stress_tests/hard_case_claims.json`
- `stress_tests/hard_case_schema_validation.md`
- `extraction_pilots/extraction_pilot_claims.json`
- `extraction_pilots/extraction_pilot_review.md`

Original PDFs remain source truth. Markdown is only a working text layer, and
tables/charts/numeric values need separate PDF QA.
