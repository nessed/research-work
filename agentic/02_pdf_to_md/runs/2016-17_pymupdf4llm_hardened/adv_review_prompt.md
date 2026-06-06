# Adversarial Review Prompt

You are a fresh-context adversarial reviewer for the hardened PES `2016-17`
PDF-to-Markdown conversion run.

## Review Inputs

- Source PDFs:
  `datalab_master/Master Data/pakistan_economic_survey/2016-17`
- Hardened run:
  `agentic/02_pdf_to_md/runs/2016-17_pymupdf4llm_hardened`
- Converted Markdown:
  `agentic/02_pdf_to_md/runs/2016-17_pymupdf4llm_hardened/converted_md`
- Conversion script:
  `convert_2016_17_pymupdf4llm.py`
- QA script:
  `qa_2016_17_pymupdf4llm.py`
- Evidence:
  `repro_manifest.json`, `conversion_log.json`, `qa_results.json`,
  `qa_report.md`, `conversion_quality.md`

## Questions

1. Does the run identify the exact source PDFs by path, size, URL, page count,
   and SHA256?
2. Does every direct source PDF have exactly one Markdown output?
3. Do Markdown page markers match source PDF page counts?
4. Are original source PDFs left untouched?
5. Are path references internally consistent and rooted under `agentic/` for
   derived outputs?
6. Can the conversion and QA be rerun headlessly?
7. Is Markdown acceptable for page-cited prose/commentary extraction?
8. Are table, chart, image, and numeric limitations stated strongly enough?
9. Does the review avoid treating Markdown tables/charts/numeric values as
   source truth?

## Expected Output

Write findings ordered by severity. Include a PASS/FAIL summary, concrete
evidence checked, residual risks, and whether the run is acceptable for LUMS
Data Lab commentary work.
