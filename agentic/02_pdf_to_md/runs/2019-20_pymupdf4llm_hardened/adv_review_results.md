# Adversarial Review Results

## Reviewer Path

- Claude-first review attempt: failed because the sub-agent returned a usage
  limit error before completing review.
- Fallback reviewer: Codex sub-agent `019e9fc9-ff18-7f51-b884-4dd17b17dc76`
  completed a fresh-context, read-only adversarial review.

## Summary

PASS on conversion integrity after this file was created and the Python command
path in `how_to_reproduce.md` was aligned with `repro_manifest.json`.

The fallback reviewer initially reported one material layout-completeness
failure: `adv_review_results.md` was missing. This file resolves that required
artifact gap. The reviewer also reported a low-severity Python path mismatch in
`how_to_reproduce.md`; that path has been updated to match the Python executable
recorded in `repro_manifest.json`.

## Findings Ordered By Severity

1. RESOLVED: Missing required review artifact.
   - Reviewer evidence: `adv_review_results.md` was absent from the run folder.
   - Resolution: this file was created from the completed read-only review.

2. RESOLVED: Python command path inconsistency.
   - Reviewer evidence: `repro_manifest.json` recorded
     `C:\Users\Ali\AppData\Local\Python\pythoncore-3.14-64\python.exe`, while
     `how_to_reproduce.md` used `C:\Users\Ali\AppData\Local\Python\bin\python.exe`.
   - Resolution: `how_to_reproduce.md` now uses the executable path recorded in
     `repro_manifest.json`.

## Checks Passed By Reviewer

- Selected direct PDFs: PASS. Source folder has 29 direct `*.pdf` files;
  manifest `selected_pdfs` has 29; case-insensitive sorted order matches.
- Manifest/log counts: PASS. `repro_manifest.json` totals show 29 found, 29
  converted, 0 failures. `conversion_log.json` has 29 entries, 29 successes,
  and 0 failures.
- Conversion methods: PASS. Reviewer observed 22
  `pymupdf4llm_layout_page_chunks` entries and 7
  `pymupdf_text_long_pdf_fallback` entries.
- Source sizes/hashes: PASS. Reviewer independently recalculated all 29 source
  PDF sizes and SHA256 hashes with 0 mismatches.
- Page counts: PASS. Reviewer independently opened all 29 PDFs with PyMuPDF
  and found 0 page-count mismatches against the manifest.
- Markdown outputs: PASS. All 29 output `.md` files exist, are nonzero, and
  match manifest sizes/hashes.
- Page markers: PASS. All outputs contain explicit `<!-- page n -->` markers;
  marker count equals PDF page count for all 29.
- Output hashes: PASS. Reviewer independently recalculated all 29 output
  hashes with 0 mismatches.
- Prose fidelity: PASS for commentary use. Existing QA reports 27 PASS and
  2 SKIP from 29 samples. Reviewer spot checks showed high token overlap:
  `Agriculture.pdf` p18 1.0000, `Fiscal_Development.pdf` p8 0.9500,
  `Pes_2019_20.pdf` p325 1.0000,
  `Transport_And_Communication.pdf` p1 0.9812,
  `Annex_Iii_Covid_19_Advent_And_Impact_Assesment.pdf` p3 0.9938.
- Numeric/table/chart caveats: PASS. `qa_report.md`,
  `conversion_quality.md`, `how_to_reproduce.md`, and `repro_manifest.json`
  explicitly mark tables/charts/numbers as `NOT_CERTIFIED`.
- Reproduce scope: PASS. `how_to_reproduce.md` follows the Step 02 guide's
  run-level scope and only records this 2019-20 PDF-to-Markdown run.
- No downstream processing: PASS. Reviewer found no 2019-20 section splitting,
  claims extraction, JSON normalization, or export artifacts for this run.

## Residual Risks

Markdown should be used only for page-cited prose/commentary. Tables, chart
values, exact numbers, totals, rankings, and footnotes remain explicitly
NOT_CERTIFIED and must be checked against source PDFs before research use.

## Acceptability

Acceptable as a complete Step 02 working-text run for LUMS Data Lab commentary
work, with the explicit limitation that original PDFs remain source truth and
numeric/table/chart material is not certified from Markdown.
