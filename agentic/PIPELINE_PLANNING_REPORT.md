# Pipeline Planning Report

This document defines the timeless workflow for Pakistan Economic Survey
commentary work. Live status, blockers, review queues, git state, and next
actions belong in `CURRENT_PROGRESS.md`, not here.

## 1. Final Pipeline Outline

The active workflow is:

```text
PDF
  ↓
MD
  ↓
Sections
  ↓
Claims JSON
  ↓
Normalize
  ↓
Export
```

Schema discovery and hardening are completed design/provenance work. They are
not recurring active pipeline stages unless Claims JSON extraction exposes a
specific schema failure that requires a justified revision.

## 2. Ground Rules

- Raw source truth lives under `datalab_master/Master Data/`.
- Do not modify, move, rename, normalize, or delete raw PDFs.
- Original PDFs remain source truth.
- Markdown is a working text layer for commentary work.
- Markdown tables, chart text, numeric values, rankings, totals, and footnotes
  are not source truth unless separately QA'd against PDFs.
- Every derived output must be traceable to source files and reproducible from
  retained manifests, scripts, logs, QA reports, and review files.
- Reviewers must be fresh-context, read-only, and explicit about what they
  verified.

## 3. Stage Workflow

### PDF

Purpose:

- Inventory and select source PDFs without modifying raw data.
- Record paths, counts, file sizes, source-folder structure, and source-scope
  decisions.

Expected output:

- Folder/file inventory.
- Source selection manifest.
- `how_to_reproduce.md`
- `adv_review_prompt.md`
- `adv_review_results.md`

Review gate:

- Recount folders/files and verify paths, counts, sizes, and source-scope
  decisions against the filesystem.

### MD

Purpose:

- Convert selected source PDFs into Markdown with explicit page markers.
- Preserve enough provenance to reproduce the conversion and QA it against PDFs.

Expected output:

- `converted_md/`
- `repro_manifest.json`
- `conversion_log.json`
- `qa_results.json`
- `qa_report.md`
- `conversion_quality.md`
- `how_to_reproduce.md`
- `adv_review_prompt.md`
- `adv_review_results.md`

QA requirements:

- File counts reconcile with selected PDFs.
- Source paths are recorded.
- Source PDF hashes/sizes/page counts are recorded where practical.
- Every converted Markdown file has page markers.
- Page-marker counts match source PDF page counts.
- Output hashes are recorded.
- Sampled prose fidelity is checked against source PDF text.
- Table/chart/numeric limitations are stated clearly.

Review gate:

- Fresh reviewer verifies manifests, logs, counts, hashes, page markers,
  sampled PDF-to-MD fidelity, raw-PDF non-mutation, and numeric/table limits.

### Sections

Purpose:

- Convert reviewed Markdown into smaller source-tagged sections.
- Create sections only: no summaries, interpretations, claim extraction,
  normalized facts, or database-ready data.

Important invariant:

- Folder year is not automatically source year.
- Before section splitting, decide which converted Markdown files are valid
  inputs for the intended `source_year`.
- If a file says a different year, such as `Supplement_2020_21` inside a
  `2016-17` folder, exclude it from that year's section layer or label it
  separately.

Expected output:

- `sections.jsonl`
- `section_manifest.json`
- `section_split_report.md`
- `how_to_reproduce.md`
- `adv_review_prompt.md`
- `adv_review_results.md`

The section manifest/report must include:

- Included input Markdown files.
- Excluded input Markdown files.
- Reason for each exclusion.
- Source PDF path for each included input.
- Source year decision used by the run.

Section QA requirements:

- Unique `section_id`.
- Valid `source_year`.
- Valid `source_md_path`.
- Valid `source_pdf_path`.
- Valid `start_page` and `end_page`.
- Heading text and sector preserved where available.
- `numeric_or_table_sensitive` populated.
- `markdown_quality_flags` populated.
- No claim, summary, interpretation, outlook, risk, sentiment, or normalized
  data fields are created.

Review gate:

- Fresh reviewer verifies the manifest, included/excluded inputs, source scope,
  page spans, source Markdown traceability, flags, and no-extraction invariant.

### Claims JSON

Purpose:

- Extract source-grounded commentary records from reviewed sections.
- Track what the survey commentary said at a given time: summaries, narratives,
  cause-effect claims, policy/programme explanations, constraints, risks, and
  outlooks.
- Start with a small reviewed pilot inside this stage, then scale only after
  pilot QA/review passes.

Schema reference:

- Use the archived schema discovery/hardening work as the current extraction
  schema reference.
- Do not repeat schema hardening as a separate stage unless extraction reveals
  a concrete schema failure.

Expected output:

- Claims input manifest.
- Extraction prompt/rules.
- Pilot Claims JSON/JSONL and QA report.
- Full-batch Claims JSON/JSONL only after pilot approval.
- Extraction logs.
- `how_to_reproduce.md`
- `adv_review_prompt.md`
- `adv_review_results.md`

Review gate:

- Verify schema conformance, source quotes, page references, numeric/table QA
  flags, no unsupported claims, batch completeness, and duplicate handling.

### Normalize

Purpose:

- Normalize reviewed Claims JSON into stable machine-readable JSON without
  changing evidence meaning.

Expected output:

- Raw input reference.
- Normalized JSON.
- Validation schema.
- Normalization log.
- Validation report.
- Review files.

Review gate:

- Verify IDs, source references, flags, counts, and preservation of evidence
  meaning.

### Export

Purpose:

- Export reviewed normalized JSON to downstream tables or databases only after
  extraction and normalization have passed review.

Expected output:

- Export manifest.
- Table schema.
- Export files.
- Load logs if applicable.
- Validation report.
- Review files.

Review gate:

- Verify row counts, keys, source links, retained flags, and no unapproved
  numeric claims.

## 4. Standard Files

Every major task folder should contain:

- `README.md`
- `how_to_reproduce.md`
- `adv_review_prompt.md`
- `adv_review_results.md`
- One clear primary output artifact or folder.

Run folders should also include:

- Input manifest with exact source files.
- Script/version info if automated.
- Deterministic rerun instructions.
- Machine-readable logs/results.
- Human-readable QA report.

## 5. Non-Actions

Do not:

- Modify, move, rename, or delete raw PDFs.
- Treat Markdown tables/charts/numbers as source truth.
- Start full Claims JSON extraction before section review and pilot review pass.
- Create production normalized JSON before reviewed Claims JSON exists.
- Export to database/table before normalization review passes.
- Treat pilot, schema-discovery, or schema-hardening outputs as final research
  data.
