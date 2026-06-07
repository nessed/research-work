# Adversarial Review Results

## Overall Verdict

PASS_WITH_NOTES

Claude was called first as requested, but the local `claude` command was blocked by PowerShell execution policy:

`claude.ps1 cannot be loaded because running scripts is disabled on this system`

Codex fallback review was then performed read-only.

## Checks Performed

- Recounted direct source PDFs in `datalab_master/Master Data/pakistan_economic_survey/2023-24`.
- Recounted Markdown outputs in `converted_md/`.
- Compared selected PDF order in `repro_manifest.json` against case-insensitive filesystem order.
- Verified manifest entry count and conversion log entry count.
- Verified all conversion log records are successful.
- Recomputed source PDF SHA-256 hashes and output Markdown SHA-256 hashes.
- Recomputed PDF page counts with PyMuPDF and compared them to Markdown page-marker counts.
- Reviewed QA status in `qa_results.json` and `qa_report.md`.
- Independently sampled prose fidelity for five PDF/page pairs, including the page-specific override page.
- Checked documentation for raw-PDF source-truth rules and numeric/table/chart warning language.
- Checked that this run did not create section, claims, normalization, or export artifacts.

## Evidence

Structural checks:

- Source PDFs found: 29
- Converted Markdown files found: 29
- Manifest entries: 29
- Conversion log entries: 29
- Conversion failures: 0
- Source/output hash mismatches: 0
- Page-marker mismatches: 0
- Total PDF pages checked against markers: 2,024
- First selected PDF: `Agriculture.pdf`
- Last selected PDF: `Transport.pdf`
- Direct non-PDF files excluded: `Statistical_Supplement.zip`, `manifest.csv`

Retained QA evidence:

- `qa_results.json` overall status: PASS
- Retained QA prose sample counts: `{'PASS': 29}`
- `qa_report.md` states table/numeric certification is NOT_CERTIFIED.

Independent prose spot-checks:

| PDF | Page | Token overlap | Source tokens | Markdown tokens |
| --- | ---: | ---: | ---: | ---: |
| `Economic_Survey_2023_24.pdf` | 174 | 0.9889 | 722 | 756 |
| `Highlights.pdf` | 25 | 1.0 | 183 | 183 |
| `Trade_And_Payments.pdf` | 2 | 0.9655 | 551 | 593 |
| `Supplement_2021_22.pdf` | 155 | 1.0 | 500 | 686 |
| `Agriculture.pdf` | 25 | 1.0 | 197 | 197 |

## Findings

No blocking findings.

Notes:

- `Economic_Survey_2023_24.pdf` page 174 required a documented page-specific `pymupdf4llm` override after default table detection caused a native process exit during conversion isolation. The override is recorded in `convert_2023_24_pymupdf4llm.py`, `repro_manifest.json`, and `conversion_quality.md`.
- `conversion_log.json` was regenerated in `--reuse-existing` mode after the long conversion completed in interrupted passes. This is documented in `how_to_reproduce.md`; output hashes and page markers were independently verified.
- Markdown table, chart, numeric, ranking, total, and footnote content remains NOT_CERTIFIED. This limitation is stated in `qa_report.md`, `qa_results.json`, `conversion_quality.md`, and `how_to_reproduce.md`.

## Raw PDF Protection

No raw PDF edits were performed during this review. Source paths, sizes, mtimes, hashes, and page counts are recorded in `repro_manifest.json`; recomputed source hashes matched the manifest.

## Scope Boundary

Review found only Step 02 artifacts in the 2023-24 run folder. No section splitting, claim extraction, JSON normalization, export, or other-year processing was performed as part of this run.

