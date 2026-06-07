# Adversarial Review Prompt

You are a fresh-context, read-only adversarial reviewer for the hardened PES
`2024-25` PDF-to-Markdown conversion run.

## Review Inputs

- Source PDFs:
  `datalab_master/Master Data/pakistan_economic_survey/2024-25`
- Hardened run:
  `agentic/02_pdf_to_md/runs/2024-25_pymupdf4llm_hardened`
- Converted Markdown:
  `agentic/02_pdf_to_md/runs/2024-25_pymupdf4llm_hardened/converted_md`
- Conversion script:
  `convert_2024_25_pymupdf4llm.py`
- QA script:
  `qa_2024_25_pymupdf4llm.py`
- Evidence:
  `repro_manifest.json`, `conversion_log.json`, `qa_results.json`,
  `qa_report.md`, `conversion_quality.md`, `how_to_reproduce.md`
- Base stage guide:
  `agentic/02_pdf_to_md/README.md`

## Questions

1. Does the run identify the exact source PDFs by path, size, page count, and
   SHA256?
2. Does every direct source PDF have exactly one Markdown output?
3. Do Markdown page markers match source PDF page counts?
4. Are output hashes present and reproducible?
5. Are original source PDFs left untouched?
6. Are path references internally consistent and rooted under `agentic/` for
   derived outputs?
7. Can the conversion and QA be rerun headlessly?
8. Does sampled PDF-to-MD prose fidelity check against original PDFs?
9. Are table, chart, image, footnote, and numeric limitations explicit and
   strong enough?
10. Does `how_to_reproduce.md` follow the base Step 02 guide without
    redefining the pipeline stage?

## Expected Output

Write findings ordered by severity. Include a PASS/FAIL summary, concrete
evidence checked, residual risks, and whether the run is acceptable for LUMS
Data Lab commentary work. Do not edit files.
