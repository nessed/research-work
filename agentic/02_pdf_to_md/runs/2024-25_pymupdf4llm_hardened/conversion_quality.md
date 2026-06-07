# Conversion Quality

## Run Reviewed

- Source folder:
  `datalab_master/Master Data/pakistan_economic_survey/2024-25`
- Active output folder:
  `agentic/02_pdf_to_md/runs/2024-25_pymupdf4llm_hardened/converted_md`
- Conversion method:
  page-by-page `pymupdf4llm.to_markdown(doc, pages=[page_index])` with explicit
  Markdown page markers
- Review evidence:
  `repro_manifest.json`, `conversion_log.json`, `qa_results.json`,
  `qa_report.md`

## Headless QA Result

PASS for the current working purpose: page-cited prose/commentary extraction.

- PDFs found: `28`
- Manifest entries: `28`
- Conversion log entries: `28`
- Failed conversions: `0`
- Missing Markdown outputs: `0`
- Zero-byte Markdown outputs: `0`
- Page-marker mismatches: `0`
- Output hash mismatches: `0`
- Deterministic prose fidelity sample: `27 PASS`, `1 SKIP`

The skipped prose sample was `Annex_Ii_Tax_Expenditure.pdf`, which did not have
a page with at least 60 extractable text tokens under the QA sampling rule.

## Limits

NOT CERTIFIED for:

- tables
- chart values
- image content
- exact numeric claims
- row/column structure
- totals, rankings, and footnotes

The QA run recorded `1212` omitted-picture placeholders. Any chart/image-based
claim requires source-PDF review.

## Research Use

The Markdown corpus is acceptable as a working text layer for commentary
extraction only when claims remain page-cited and quote-grounded. Original PDFs
remain source truth.
