# How To Reproduce

This folder records commentary schema discovery for Pakistan Economic Survey
commentary extraction.

## Inputs

- Hardened Markdown corpus:
  `agentic/02_pdf_to_md/runs/2015-16_pymupdf4llm_hardened/converted_md`
- Source truth:
  `datalab_master/Master Data/pakistan_economic_survey/2015-16`

## Outputs

- Pattern scan:
  `pattern_scan/commentary_pattern_scan.md`
- Draft and frozen working schema:
  `schema/commentary_schema_draft.json`
  `schema/commentary_schema_v0.1.json`
- Stress-test records and reviews:
  `stress_tests/`
- Five-file extraction pilot:
  `extraction_pilots/`

## Method Summary

1. Scan the 29 converted Markdown files for recurring commentary patterns.
2. Draft a JSON schema for source-grounded claims.
3. Run a random stress test and revise the schema where needed.
4. Run hard-case stress tests against dense prose, programme-heavy prose, and
   indicator-heavy material.
5. Freeze working schema v0.1 after the schema holds.
6. Run a five-file random extraction pilot using schema v0.1.

## Constraints

- This is not full corpus extraction.
- Original PDFs remain source truth.
- Markdown page markers are used for working citations.
- Numeric/table/chart-sensitive claims must be flagged for separate PDF QA.
- No database import is performed here.

## Validation

Validate JSON files from repo root:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" -c "import json, pathlib; [json.load(open(p, encoding='utf-8')) for p in pathlib.Path(r'agentic\03_commentary_schema_discovery').rglob('*.json')]; print('json_ok')"
```

Expected five-file pilot count:

```text
25 records
```
