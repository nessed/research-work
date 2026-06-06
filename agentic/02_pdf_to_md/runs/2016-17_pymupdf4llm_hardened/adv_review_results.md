# Adversarial Review Results

Status: PASS with low residual risk.

No blocking findings. The run is acceptable for page-cited prose/commentary
work, provided Markdown is treated only as a working text layer and all
numeric/table/chart claims are checked against the source PDFs.

## Findings

- Low: prose QA is sampled, not exhaustive. QA samples 30 pages, one per PDF,
  with PASS threshold at token overlap `>= 0.80`. Two samples were relatively
  low but still passing: `Health.pdf` p9 `0.8644`,
  `Annex_Vi_Tax_Expenditure.pdf` p1 `0.8704`. This is reasonable for
  prose/commentary triage, not a guarantee for every page.
- Low: current conversion manifest/log were produced in reuse mode.
  `repro_manifest.json` says `generation_mode: reuse_existing_outputs`, and
  `conversion_log.json` entries show `reused_existing_output: true`. The full
  conversion and reuse commands are documented and headless, but the reviewer
  did not rerun them because the review was explicitly read-only.

## Evidence Checked

- Direct source PDFs: `30`; manifest entries: `30`; conversion log entries:
  `30`; Markdown files: `30`.
- One-to-one PDF-to-MD mapping: PASS, no missing/extra Markdown files.
- Source evidence: all manifest source paths, sizes, SHA256 hashes, mtimes,
  and source URLs present; independent checks found `0` size/hash/mtime
  mismatches.
- Page counts: independent PyMuPDF check found `0` mismatches; total pages
  `1,815`; largest source `Pakistan_Es_2016_17_Pdf.pdf` has `462` pages.
- Page markers: `0` marker-count mismatches against PDF page counts.
- Source PDFs untouched: PASS by hash/size/mtime evidence; latest source mtime
  `2026-06-02T03:07:20+00:00`, before run artifacts.
- Derived paths: PASS; outputs are under
  `agentic/02_pdf_to_md/runs/2016-17_pymupdf4llm_hardened/converted_md`.
- QA: `qa_results.json` and `qa_report.md` report structural PASS and prose
  PASS.
- Limits: strong enough. QA policy says Markdown is `NOT_CERTIFIED` for table,
  chart, numeric, row/column, total, ranking, and footnote fidelity; `706`
  omitted-picture placeholders recorded.

## Residual Risks

- Tables in sampled Markdown show structural artifacts and repeated headers; do
  not use Markdown tables as source truth.
- Images/charts are explicitly omitted or uncertified.
- Exact numbers, rankings, totals, and footnotes require PDF-page verification.

## Verdict

Acceptable for LUMS Data Lab page-cited prose/commentary extraction. Not
acceptable as a source of truth for tables, charts, or numeric claims without
separate PDF evidence.
