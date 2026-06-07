# Conversion Quality

## Run Reviewed

- Source folder:
  `datalab_master/Master Data/pakistan_economic_survey/2021-22`
- Active output folder:
  `agentic/02_pdf_to_md/runs/2021-22_pymupdf4llm_hardened/converted_md`
- Conversion method:
  deterministic PyMuPDF `page.get_text("text")` with explicit Markdown page
  markers
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

The skipped prose sample had no page with at least 60 extractable tokens under
the QA script's deterministic sampling rule.

## Method Caveat

The requested run folder name follows the existing `pymupdf4llm_hardened`
pattern. In this environment, whole-document and page-wise `pymupdf4llm`
conversion attempts timed out on `Economic_Survey_2021_22.pdf`, the 548-page
combined survey PDF. The retained completed script records this and uses PyMuPDF
text extraction to produce deterministic page-marked Markdown for all selected
PDFs.

## Limits

NOT CERTIFIED for:

- tables
- chart values
- image content
- exact numeric claims
- row/column structure
- totals, rankings, and footnotes

The QA run recorded `0` omitted-picture placeholders because this conversion
uses text extraction rather than image placeholder emission. That does not
certify images or charts. Any chart/image/table/numeric claim requires source-PDF
review.

## Research Use

The Markdown corpus is acceptable as a working text layer for commentary
extraction only when claims remain page-cited and quote-grounded. Original PDFs
remain source truth.
