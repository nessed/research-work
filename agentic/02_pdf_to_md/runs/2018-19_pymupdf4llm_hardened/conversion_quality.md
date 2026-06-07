# Conversion Quality

## Run Reviewed

- Source folder:
  `datalab_master/Master Data/pakistan_economic_survey/2018-19`
- Active output folder:
  `agentic/02_pdf_to_md/runs/2018-19_pymupdf4llm_hardened/converted_md`
- Conversion method:
  direct `pymupdf4llm.to_markdown(str(pdf_path), page_chunks=True)`
- Review evidence:
  `repro_manifest.json`, `conversion_log.json`, `qa_results.json`,
  `qa_report.md`

## Headless QA Result

PASS for the current working purpose: page-cited prose/commentary extraction.

- PDFs found: `27`
- Manifest entries: `27`
- Conversion log entries: `27`
- Failed conversions: `0`
- Missing Markdown outputs: `0`
- Zero-byte Markdown outputs: `0`
- Page-marker mismatches: `0`
- Output hash mismatches: `0`
- Deterministic prose fidelity sample: `27 PASS`

## Limits

NOT CERTIFIED for:

- tables
- chart values
- image content
- exact numeric claims
- row/column structure
- totals, rankings, and footnotes

The QA run recorded `2152` omitted-picture placeholders. Any chart/image-based
claim requires source-PDF review.

## Research Use

The Markdown corpus is acceptable as a working text layer for commentary
extraction only when claims remain page-cited and quote-grounded. Original PDFs
remain source truth.
