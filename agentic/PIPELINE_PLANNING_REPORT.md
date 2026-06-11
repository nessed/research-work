# Pipeline Planning Report

This document defines the timeless workflow for Pakistan Economic Survey.
commentary work. Live status, blockers, review queues, git state, and
next actions belong in `CURRENT_PROGRESS.md`, not here.

## 1. Pipeline Order

The workflow order is:

1. `01_pes_folder_map`
2. `02_pdf_to_md`
3. `03_section_splitting`
4. `04_commentary_schema_discovery` / Schema Discovery & Hardening
5. `05_extraction_pilots`
6. `06_structured_claim_extraction`
7. `07_json_normalization`
8. `08_database_export`

Do not change this order without an explicit design decision.

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

### 01 PES Folder Map

Purpose:

- Inventory the PES source folders and files without modifying raw data.
- Record paths, counts, file sizes, and source-folder structure.

Expected output:

- `pes_folder_tree.json`
- `how_to_reproduce.md`
- `adv_review_prompt.md`
- `adv_review_results.md`

Review gate:

- Recount folders/files and verify paths, counts, sizes, and classifications
  against the filesystem.

### 02 PDF To Markdown

Purpose:

- Convert selected source PDFs into Markdown with explicit page markers.
- Preserve enough provenance to reproduce the conversion and QA it against PDFs.

Expected run output:

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

### 03 Section Splitting

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

Expected run output:

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

### 04 Commentary Schema Hardening

Purpose:

- Maintain and stress-test the qualitative commentary schema.
- Future years should mostly harden the existing schema with justified edge
  cases, not rediscover the schema from scratch.

Expected output:

- Sample selection manifest.
- Schema stress-test notes.
- Proposed schema changes or a clear "no change needed" decision.
- Updated schema draft only when justified.
- QA/review notes.

Sample requirements:

- Use small, diverse samples from reviewed section outputs.
- Cover prose-heavy narrative, table/numeric-sensitive material,
  policy/programme material, and weak Markdown where available.
- Do not create a full research dataset.
- Do not treat pilot/schema-hardening records as final data.

Review gate:

- Verify that schema changes are justified by samples and that the work did not
  become full extraction.

### 05 Extraction Pilots

Purpose:

- Run controlled pilot extraction using reviewed sections and the hardened
  commentary schema.
- Test whether prompts/rules produce source-grounded commentary summaries,
  narrative tracking records, and cause-effect claims without over-inference.

Expected output:

- Pilot input manifest.
- Extraction prompt/rules.
- Pilot output JSON/JSONL.
- Pilot QA report.
- `how_to_reproduce.md`
- `adv_review_prompt.md`
- `adv_review_results.md`

Review gate:

- Verify schema conformance, source quotes, page references, numeric/table QA
  flags, and no unsupported claims.

### 06 Structured Claim Extraction

Purpose:

- Run approved extraction over a defined batch after pilot review passes.
- Preserve source grounding and human-review flags.

Expected output:

- Extraction manifest.
- Raw extraction JSON/JSONL.
- Extraction logs.
- QA report.
- Review files.

Review gate:

- Verify batch completeness, source grounding, duplicate handling, schema
  validity, and numeric/table flags.

### 07 JSON Normalization

Purpose:

- Normalize reviewed extraction output into stable machine-readable JSON without
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

### 08 Database Export

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
- Start full extraction before section and schema gates pass.
- Create production normalized JSON before reviewed extraction exists.
- Export to database/table before normalization review passes.
- Treat pilot/schema-hardening outputs as final research data.
