# Conversion Quality

## Result

Status: PASS for Step 02 PDF-to-Markdown conversion QA.

This run converted 29 selected PDFs directly inside:

`datalab_master/Master Data/pakistan_economic_survey/2023-24`

Outputs were written to:

`agentic/02_pdf_to_md/runs/2023-24_pymupdf4llm_hardened/converted_md`

## Scope

Selected input rule: all `*.pdf` files directly inside the 2023-24 source folder, sorted case-insensitively by filename.

Non-PDF files were not converted. `manifest.csv` and `Statistical_Supplement.zip` remained outside conversion scope.

## QA Summary

See `qa_results.json` and `qa_report.md` for machine-readable and human-readable QA evidence.

Observed QA result:

- PDFs found: 29
- Manifest entries: 29
- Conversion log entries: 29
- Failed conversions: 0
- Missing outputs: 0
- Zero-byte outputs: 0
- Hash mismatches: 0
- Page-marker mismatches: 0
- Prose fidelity samples: 29 PASS

## Conversion Method Note

The retained conversion script uses `pymupdf4llm.to_markdown` page-by-page and inserts explicit markers in the form:

`<!-- page N -->`

During isolation, default `pymupdf4llm` table detection caused a native process exit on `Economic_Survey_2023_24.pdf` page 174. The retained script applies a documented page-specific override for that page only:

- `ignore_images=True`
- `ignore_graphics=True`
- `table_strategy="text"`

This is recorded in `repro_manifest.json`.

## Research Use Limitations

Markdown is working text only. Original PDFs remain source truth.

Tables, charts, numeric values, rankings, totals, row/column structure, and footnotes are NOT_CERTIFIED in this Markdown layer. Any numeric, table-derived, chart-derived, ranking, or footnote claim must be separately QA'd against the original PDF before research use.

