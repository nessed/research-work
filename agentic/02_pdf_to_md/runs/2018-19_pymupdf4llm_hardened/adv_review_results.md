# Adversarial Review Results

Claude was attempted first for the fresh-context review. The local Claude CLI
wrapper was blocked by PowerShell execution policy; invoking the underlying
Claude executable directly worked for help output, but the escalated read-only
review request was rejected by policy because it would disclose private
workspace/source-derived content to an external Claude service. The review
therefore used the Codex fallback reviewer.

## Findings

No blocking findings.

Low severity residual scope risk: the run correctly converts all 27 direct PDFs
in the `2018-19` source folder, including `Supplement_2017_18.pdf`,
`Supplement_2019_20.pdf`, `Supplement_2020_21.pdf`, and
`Supplement_2021_22.pdf`. This is acceptable for Step 02, but downstream
section splitting must not treat folder year as source year automatically.

## PASS/FAIL Summary

PASS for Step 02 PDF-to-Markdown review.

The run is acceptable for downstream section splitting as a reviewed Markdown
text layer, with the caveat that the section stage must explicitly
include/exclude or label supplements by actual source year.

## Concrete Evidence Checked

- Read required context and run files, including `agentic/02_pdf_to_md/README.md`,
  `repro_manifest.json`, `conversion_log.json`, `qa_results.json`,
  `qa_report.md`, `conversion_quality.md`, and `how_to_reproduce.md`.
- Independently counted source and output files: 27 direct source PDFs and 27
  converted Markdown files.
- Independently verified all 27 manifest entries: current source PDF size/hash
  matched manifest, output Markdown size/hash matched manifest, and Markdown
  page-marker counts matched recorded PDF page counts.
- QA evidence reports: 27 manifest entries, 27 conversion log entries, 0 failed
  conversions, 0 missing outputs, 0 zero-byte outputs, 0 hash mismatches, and 0
  page-marker mismatches.
- Sampled prose fidelity independently against original PDFs using PyMuPDF on
  5 pages:
  - `Overview_Of_The_Economy.pdf` page 1: 1.000 overlap
  - `Growth.pdf` page 3: 1.000 overlap
  - `Education.pdf` page 7: 1.000 overlap
  - `Trade_And_Payments.pdf` page 1: 1.000 overlap
  - `Economic_Survey_2018_19.pdf` page 232: 0.995 overlap
- Raw PDFs appear unmodified by this run based on current SHA256 and size
  matching `repro_manifest.json`.
- Numeric/table/chart limitations are explicit: tables, chart values, image
  content, exact numeric claims, row/column structure, totals, rankings, and
  footnotes are not certified and require source-PDF QA.
- `how_to_reproduce.md` follows the Step 02 base guide: it records run scope,
  commands, environment pointers, QA command, result, and caveats; it does not
  redefine the stage.

## Residual Risks

Markdown is suitable for prose/commentary extraction, not source truth. Tables,
charts, images, footnotes, and exact numeric claims remain uncertified. The
large full survey and supplements duplicate or overlap chapter-level material,
so section splitting should manage duplication and source-year scope explicitly.
