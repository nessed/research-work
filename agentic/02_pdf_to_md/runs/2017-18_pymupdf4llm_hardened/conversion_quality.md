# Conversion Quality

## Status

- Overall QA status: `PASS`
- Structural QA status: `PASS`
- Prose fidelity QA status: `PASS`
- Table/chart/numeric certification: `NOT_CERTIFIED`

## Scope

- Source folder: `datalab_master/Master Data/pakistan_economic_survey/2017-18`
- Run folder: `agentic/02_pdf_to_md/runs/2017-18_pymupdf4llm_hardened`
- Selected PDFs: all `*.pdf` files directly inside the source folder, sorted case-insensitively by filename
- PDFs converted: `29`
- Failed conversions: `0`
- Conversion log output hash mismatches: `0`

## Page Markers

Every converted Markdown file contains explicit page markers of the form:

```markdown
<!-- page 1 -->
```

QA found `0` page-marker mismatches against source PDF page counts.

## Prose Fidelity

Deterministic sampled prose fidelity used seed `20260607`.

- Samples checked: `29`
- PASS samples: `29`
- WARN samples: `0`
- FAIL samples: `0`

Sample details are recorded in `qa_results.json` and summarized in `qa_report.md`.

## Table, Chart, And Numeric Status

Tables, chart text, numeric values, rankings, totals, and footnotes in Markdown are `NOT_CERTIFIED`.

Markdown is working text only. Original PDFs remain source truth. Any table-derived,
chart-derived, numeric, ranking, total, or footnote claim must be separately QA'd
against the source PDFs before research use.

## Known Limitations

- PyMuPDF4LLM may reflow columns, tables, headers, image text, and footnotes.
- Some chart/image text appears as omitted-picture placeholder text or OCR-like extracted fragments.
- The QA prose-fidelity check is sampled, not exhaustive.
- Duplicate source content is preserved when duplicate PDFs are present in the raw folder; raw PDFs were not deduplicated or normalized.
