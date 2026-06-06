# Step 02: PDF To Markdown

This is the canonical instruction document for the PDF -> MD stage. Follow this
file first for every year. Use each run folder's `how_to_reproduce.md` only for
that run's exact paths, commands, observed environment, and results.

## Purpose

Convert selected Pakistan Economic Survey PDFs into Markdown working text with
explicit page markers, while preserving enough evidence to reproduce and review
the conversion.

## Source Truth

- Raw PDFs under `datalab_master/Master Data/` are source truth.
- Do not modify, move, rename, normalize, or delete raw PDFs.
- Markdown is a working text layer for page-cited prose/commentary work.
- Markdown tables, chart text, numeric values, rankings, totals, and footnotes
  are not source truth unless separately QA'd against the PDFs.

## Required Run Layout

Create one run folder under:

```text
agentic/02_pdf_to_md/runs/<year>_<tool>_<label>/
```

Each run folder must contain:

- `converted_md/`
- `repro_manifest.json`
- `conversion_log.json`
- `qa_results.json`
- `qa_report.md`
- `conversion_quality.md`
- `how_to_reproduce.md`
- `adv_review_prompt.md`
- `adv_review_results.md`
- retained conversion and QA scripts when code was used

## Required Conversion Rules

- Select source PDFs explicitly and record the exact input folder/files.
- Convert only selected PDFs for the intended run.
- Keep deterministic file naming and stable ordering.
- Add explicit Markdown page markers, such as `<!-- page 1 -->`.
- Record source PDF paths, sizes, hashes, and page counts where practical.
- Record output Markdown paths and hashes.
- Log every conversion success/failure.

## Required QA

Every run must check:

- File counts reconcile with selected PDFs.
- Source paths are recorded.
- Every Markdown output has page markers.
- Page-marker counts match source PDF page counts, or exceptions are documented.
- Output hashes are recorded.
- Sampled prose fidelity is checked against source PDF text.
- Table/chart/numeric limitations are stated clearly.

## Review Gate

Before downstream use, a fresh-context/read-only reviewer must verify:

- manifests, logs, counts, hashes, and page markers
- sampled PDF-to-MD prose fidelity
- raw-PDF non-mutation
- numeric/table/chart limitations
- reproducibility instructions for the specific run

## Run-Level Reproducibility

Run-level `how_to_reproduce.md` files should not redefine this stage. They
should only state:

- year and source input scope
- output folder
- exact script commands
- observed tool versions/environment
- QA command
- run result
- any run-specific caveats
