# Conversion Quality

## Run Reviewed

- Source folder:
  `datalab_master/Master Data/pakistan_economic_survey/2019-20`
- Active output folder:
  `agentic/02_pdf_to_md/runs/2019-20_pymupdf4llm_hardened/converted_md`
- Selected source scope:
  all `*.pdf` files directly inside the source folder, sorted
  case-insensitively by filename
- Conversion evidence:
  `repro_manifest.json`, `conversion_log.json`, `qa_results.json`,
  `qa_report.md`

## Conversion Method

The retained conversion script is `convert_2019_20_pymupdf4llm.py`.

- PDFs with 100 pages or fewer used
  `pymupdf4llm.to_markdown(str(pdf_path), page_chunks=True)`.
- PDFs over 100 pages used PyMuPDF page text extraction as a long-PDF fallback
  after PyMuPDF4LLM layout conversion exceeded practical runtime for the
  516-page full survey PDF.
- Every Markdown output has explicit page markers of the form
  `<!-- page 1 -->`.

## Headless QA Result

PASS for the current working purpose: page-cited prose/commentary extraction.

- PDFs found: `29`
- Manifest entries: `29`
- Conversion log entries: `29`
- Failed conversions: `0`
- Missing Markdown outputs: `0`
- Zero-byte Markdown outputs: `0`
- Page-marker mismatches: `0`
- Output hash mismatches: `0`
- Missing conversion log output hashes: `0`
- Conversion log hash mismatches: `0`
- Deterministic prose fidelity sample: `27 PASS`, `2 SKIP`
- Prose-sample skips:
  `Annex_Ii_Tax_Expenditure.pdf`, `Economic_Indicators.pdf`

## Limits

NOT_CERTIFIED for:

- tables
- chart text and chart values
- image content
- exact numeric claims
- row/column structure
- totals, rankings, and footnotes

The QA run recorded `110` omitted-picture placeholders. Any chart, image,
table, footnote, ranking, total, or numeric claim requires separate source-PDF
review before research use.

## Caveats

- `Inflation.pdf` and `Inflation(1).pdf` were both converted because both are
  direct PDFs in the source folder. They were not deduplicated or modified.
- Direct supplements from other years inside the `2019-20` source folder were
  converted because Step 02 converts selected direct PDFs only. Later section
  splitting must decide inclusion/exclusion for a source-year-specific section
  layer.
- Markdown is a working text layer only. Original PDFs remain source truth.
