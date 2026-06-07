# Adversarial Review Prompt

You are a fresh-context, read-only adversarial reviewer. Review only Step 02 PDF-to-Markdown for Pakistan Economic Survey year 2023-24.

Run folder:

`agentic/02_pdf_to_md/runs/2023-24_pymupdf4llm_hardened`

Source folder:

`datalab_master/Master Data/pakistan_economic_survey/2023-24`

Do not modify, move, rename, delete, normalize, or deduplicate any raw source PDFs. Do not edit run outputs. Do not run downstream section splitting, claim extraction, JSON normalization, export, or any other year.

Verify:

1. Selected scope: all and only direct `*.pdf` files inside the 2023-24 source folder are represented, in deterministic filename order. Non-PDF files are excluded.
2. Counts: source PDF count, converted Markdown count, manifest entries, and conversion log entries reconcile.
3. Source protection: raw PDFs were not modified by this run; source paths, sizes, mtimes, hashes, and page counts are recorded.
4. Hashes: source PDF hashes and output Markdown hashes in `repro_manifest.json` match files on disk.
5. Page markers: every Markdown output contains explicit `<!-- page N -->` markers and marker counts match PDF page counts.
6. Conversion log: every selected PDF has a success/failure record in `conversion_log.json`; failures, if any, are explicit.
7. Prose fidelity: independently sample PDF pages and compare extractable prose against the corresponding Markdown page sections.
8. Numeric/table/chart warnings: verify `qa_report.md`, `qa_results.json`, `conversion_quality.md`, and `how_to_reproduce.md` state that Markdown numeric, table, chart, ranking, total, and footnote content is NOT_CERTIFIED unless separately QA'd against source PDFs.
9. Reproducibility: verify retained scripts and `how_to_reproduce.md` are sufficient to reproduce conversion and QA.
10. Scope boundary: confirm no section splitting, claim extraction, JSON normalization, export, or other-year processing was performed as part of this run.

Write findings to:

`agentic/02_pdf_to_md/runs/2023-24_pymupdf4llm_hardened/adv_review_results.md`

Required result format:

- Overall verdict: PASS, PASS_WITH_NOTES, or FAIL
- Checks performed
- Findings, ordered by severity
- Evidence with file paths and key counts/hashes/page-marker results
- Any residual risks or caveats

