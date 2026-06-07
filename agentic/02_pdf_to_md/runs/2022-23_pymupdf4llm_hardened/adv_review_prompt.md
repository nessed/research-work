# Adversarial Review Prompt

You are a fresh-context, read-only adversarial reviewer for Step 02
PDF-to-Markdown conversion.

Review only this run:

`agentic/02_pdf_to_md/runs/2022-23_pymupdf4llm_hardened/`

Source folder:

`datalab_master/Master Data/pakistan_economic_survey/2022-23`

## Required Context To Read

1. `PROJECT_CONTEXT.md`
2. `agentic/PIPELINE_PLANNING_REPORT.md`
3. `agentic/WORKSPACE_STRUCTURE.md`
4. `agentic/02_pdf_to_md/README.md`
5. This run's `repro_manifest.json`
6. This run's `conversion_log.json`
7. This run's `qa_results.json`
8. This run's `qa_report.md`
9. This run's `conversion_quality.md`
10. This run's `how_to_reproduce.md`

## Review Tasks

Verify, independently and read-only:

- The source folder contains exactly the selected direct PDFs listed in
  `repro_manifest.json`, in deterministic filename order.
- No other year or nested folder was processed.
- `converted_md/` contains one Markdown output per selected PDF, with
  deterministic output names.
- `conversion_log.json` records every selected PDF and every conversion has
  success/failure evidence.
- Current source PDF sizes and SHA256 hashes match `repro_manifest.json`.
- Current output Markdown sizes and SHA256 hashes match `repro_manifest.json`.
- Current PDF page counts match recorded page counts.
- Markdown page markers use explicit markers like `<!-- page 1 -->`.
- Page marker counts and marker sequences match source PDF page counts.
- Sample prose fidelity against the original PDFs on several pages, including
  at least one large PDF and one supplement.
- Raw PDFs were not moved, renamed, edited, deleted, normalized, or
  deduplicated.
- The run files clearly state that Markdown is working text only and that
  table/chart/numeric/ranking/footnote content remains `NOT_CERTIFIED` unless
  separately QA'd against PDFs.
- Reproduction instructions are complete enough to rerun conversion and QA.

## Output Format

Write findings into `adv_review_results.md` with:

- PASS/FAIL summary
- Blocking findings first, if any
- Non-blocking risks or caveats
- Concrete evidence checked
- Any commands or scripts used
- Final recommendation for whether this Step 02 run can feed Step 03 section
  splitting

Do not section split. Do not extract claims. Do not normalize JSON. Do not
export. Do not process another year.
