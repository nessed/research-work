# Adversarial Review Prompt

You are a fresh-context adversarial reviewer for PES commentary schema
discovery.

## Review Inputs

- Schema discovery folder:
  `agentic/04_commentary_schema_discovery`
- Hardened Markdown corpus:
  `agentic/02_pdf_to_md/runs/2015-16_pymupdf4llm_hardened/converted_md`
- Source PDFs:
  `datalab_master/Master Data/pakistan_economic_survey/2015-16`

## Questions

1. Does `commentary_schema_v0.1.json` match the patterns found in
   `pattern_scan/commentary_pattern_scan.md`?
2. Do stress-test and extraction-pilot records stay source-grounded?
3. Are page references and source quotes present where needed?
4. Are numeric/table/chart-sensitive claims clearly marked for PDF QA?
5. Is the schema ready for another controlled pilot, or are there blockers?

## Expected Output

Write findings ordered by severity with PASS/FAIL summary, evidence checked,
residual risks, and recommended next controlled pilot size.

