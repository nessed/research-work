# Adversarial Review Prompt

You are a fresh-context, read-only adversarial reviewer for the PES `2019-20`
PDF-to-Markdown Step 02 run.

## Review Inputs

- Canonical Step 02 guide:
  `agentic/02_pdf_to_md/README.md`
- Source PDFs:
  `datalab_master/Master Data/pakistan_economic_survey/2019-20`
- Run folder:
  `agentic/02_pdf_to_md/runs/2019-20_pymupdf4llm_hardened`
- Converted Markdown:
  `agentic/02_pdf_to_md/runs/2019-20_pymupdf4llm_hardened/converted_md`
- Conversion script:
  `convert_2019_20_pymupdf4llm.py`
- QA script:
  `qa_2019_20_pymupdf4llm.py`
- Evidence:
  `repro_manifest.json`, `conversion_log.json`, `qa_results.json`,
  `qa_report.md`, `conversion_quality.md`, `how_to_reproduce.md`

## Read-Only Rule

Do not edit, move, rename, delete, normalize, or deduplicate any raw PDFs or run
artifacts. Inspect only.

## Required Checks

1. Verify the selected PDF list against direct `*.pdf` files in the source
   folder and confirm deterministic ordering.
2. Verify source PDF paths, file sizes, SHA256 hashes, page counts, and output
   Markdown paths in `repro_manifest.json`.
3. Verify `conversion_log.json` has one entry per selected PDF, no failed
   conversions, page counts, output hashes, and internally consistent paths.
4. Verify every Markdown output exists and has explicit page markers.
5. Verify page marker counts match source PDF page counts.
6. Verify output hashes in the manifest/log match current Markdown files.
7. Sample source PDFs against Markdown outputs for prose fidelity using original
   PDFs as source truth.
8. Verify raw PDFs were not modified by checking source hashes against the
   manifest.
9. Verify table, chart, numeric, ranking, total, and footnote limitations are
   explicit and remain NOT_CERTIFIED.
10. Verify `how_to_reproduce.md` follows
    `agentic/02_pdf_to_md/README.md`, records only this `2019-20` run's exact
    scope/commands/environment/QA/results/caveats, and does not redefine the
    stage.
11. Confirm no section splitting, claims extraction, JSON normalization, or
    export was run as part of this task.

## Expected Output

Write findings ordered by severity. Include:

- PASS/FAIL summary
- exact evidence checked
- any mismatches or residual risks
- whether this run is acceptable as Step 02 working text for LUMS Data Lab
  commentary work
