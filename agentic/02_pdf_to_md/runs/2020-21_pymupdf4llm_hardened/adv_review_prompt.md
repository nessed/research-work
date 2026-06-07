# Adversarial Review Prompt

You are a fresh-context, read-only adversarial reviewer for the PES `2020-21`
PDF-to-Markdown conversion run.

Do not edit, move, rename, normalize, deduplicate, or delete any source PDFs or
derived outputs. Review only.

## Review Inputs

- Source PDFs:
  `datalab_master/Master Data/pakistan_economic_survey/2020-21`
- Run folder:
  `agentic/02_pdf_to_md/runs/2020-21_pymupdf4llm_hardened`
- Converted Markdown:
  `agentic/02_pdf_to_md/runs/2020-21_pymupdf4llm_hardened/converted_md`
- Conversion script:
  `agentic/02_pdf_to_md/runs/2020-21_pymupdf4llm_hardened/convert_2020_21_pymupdf4llm.py`
- QA script:
  `agentic/02_pdf_to_md/runs/2020-21_pymupdf4llm_hardened/qa_2020_21_pymupdf4llm.py`
- Evidence:
  `repro_manifest.json`, `conversion_log.json`, `qa_results.json`,
  `qa_report.md`, `conversion_quality.md`, `how_to_reproduce.md`
- Base Step 02 guide:
  `agentic/02_pdf_to_md/README.md`

## Required Checks

1. Verify the run identifies the exact selected source PDFs by path, size,
   page count, and SHA256.
2. Verify every direct selected source PDF has exactly one Markdown output.
3. Verify `conversion_log.json` has one entry per selected PDF and no failed
   conversions.
4. Verify Markdown page markers exist and marker counts match source PDF page
   counts.
5. Verify output hashes are present and reproducible.
6. Verify original source PDFs were not modified by comparing current source
   paths, sizes, mtimes, and hashes to `repro_manifest.json`.
7. Verify sampled PDF-to-MD prose fidelity against original PDFs, not just
   against existing QA prose.
8. Verify numeric, table, chart, ranking, total, footnote, and image
   limitations are explicit and strong enough.
9. Verify `how_to_reproduce.md` points to
   `agentic/02_pdf_to_md/README.md` as the canonical Step 02 guide and does not
   redefine the stage.
10. Verify the run stops after Step 02 and does not section split, extract
    claims, normalize JSON, export, or process other years.

## Expected Output

Write findings ordered by severity. Include:

- PASS/FAIL summary
- evidence checked
- concrete issues, if any
- residual risks
- whether the run is acceptable for LUMS Data Lab commentary work

Do not edit files.
