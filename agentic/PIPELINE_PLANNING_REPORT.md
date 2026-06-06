# Pipeline Planning Report

## 1. Current Repo State

Active source truth remains `datalab_master/Master Data/`. Raw PDFs must stay
untouched.

Active derived work is under `agentic/`:

- `01_pes_folder_map/`: completed PES filesystem inventory.
  `adv_review_results.md` reports PASS/high confidence: 10 year folders, 287
  PDFs, no count/path/size mismatches.
- `02_pdf_to_md/runs/2015-16_pymupdf4llm_hardened/`: active 2015-16 Markdown
  conversion run. It has 29 Markdown outputs, page markers, conversion script,
  QA script, manifest, logs, and QA reports. Headless QA passed for structure
  and prose fidelity only. Tables, charts, images, and numeric claims are not
  certified. Fresh-context adversarial review is still pending.
- `03_commentary_schema_discovery/`: active schema and pattern discovery area.
  It has pattern scan, schema v0.1, stress tests, hard-case tests, and a
  five-file extraction pilot. This is pilot evidence, not full extraction.
  Fresh-context adversarial review is still pending.
- `reviews/`: available for cross-cutting reviews, currently empty except
  `.gitkeep`.
- `sitreps/`: situation reports.

`TASK_FOLDER_STANDARD.md` is not present; task-folder standards currently live
in `PROJECT_CONTEXT.md`.

The working tree currently shows a large uncommitted cleanup/reorganization.
Active vs archived paths are documented, but this state is not yet git-stable.

## 2. Original Roadmap Vs Current Reality

- Raw Economic Survey PDF: done and reviewed as inventory. Raw PDFs are
  protected; folder map passed review.
- Convert to Markdown with page markers: done only for the active 2015-16 run;
  needs fresh-context adversarial review before being treated as hardened
  research evidence.
- Split by chapter / sector / subsection: partially done or skipped.
  Chapter/sector is implicit from PDF/Markdown filenames, but there is no
  reproducible split-unit manifest for subsection-level units.
- Identify repeatable commentary patterns: partially done. Pattern scan and
  schema pilots exist for 2015-16, but top-level adversarial review is pending.
- Extract structured claims: partially done as pilots only. Stress tests and
  five-file pilot claims exist; no full extraction has started.
- Normalize into JSON: not started as production normalization. Schema and
  pilot JSON exist, but no normalized research dataset exists.
- Export to database/table: not started and should remain out of scope.

## 3. Recommended Pipeline From Here

1. Freeze the current cleanup target for review: document expected active
   folders, archive folders, pending reviews, and known uncommitted path
   changes.
2. Run fresh-context adversarial review of current workspace organization, the
   2015-16 hardened PDF-to-MD run, and schema-discovery outputs.
3. If review passes or issues are corrected, make the active/archive layout
   git-stable.
4. Create the next active step as `04_md_split_units`, focused only on
   reproducible Markdown split units.
5. Define split-unit acceptance criteria before any pilot: stable `unit_id`,
   source Markdown path, original PDF path, source year/file, page span, unit
   type, heading/subsection labels, unit text, markdown quality flags, and
   numeric/table/figure sensitivity flags.
6. Run a small 2015-16 split-unit pilot only after approval. The split layer
   must produce units only: no claims, summaries, interpretations, or
   database-ready facts.
7. Adversarially review the split spec and pilot before any extraction consumes
   it.
8. Later, with separate approval, run extraction pilots, full extraction, JSON
   normalization, and database export design.

## 4. Folder Plan

Keep current active folders:

- `agentic/01_pes_folder_map/`
- `agentic/02_pdf_to_md/runs/2015-16_pymupdf4llm_hardened/`
- `agentic/03_commentary_schema_discovery/`

Use archive folders only for superseded evidence, each with a README explaining
original path, new path, reason, date, and status.

Add next only when approved:

- `agentic/04_md_split_units/`
  - `runs/2015-16_split_units_pilot/`
  - `archive/`

Future roadmap folders should remain planned, not created yet:

- `agentic/05_extraction_pilots/`
- `agentic/06_structured_claim_extraction/`
- `agentic/07_json_normalization/`
- `agentic/08_database_export/`

Use `agentic/reviews/` for cross-cutting reviews such as workspace cleanup
review. Keep task-local reviews inside each task folder.

## 5. Standard Files Per Step

Every major task folder should contain:

- `README.md`: purpose, active status, inputs, outputs, limits.
- `how_to_reproduce.md`: exact reproduction steps.
- `adv_review_prompt.md`: fresh-context review instructions.
- `adv_review_results.md`: reviewer findings.
- One clear primary output artifact or folder.

Run folders should also include:

- input manifest with exact source files
- script/version info if automated
- deterministic rerun instructions
- machine-readable logs/results
- human-readable QA report
- archive README for superseded runs

Step-specific outputs:

- `01_pes_folder_map`: `pes_folder_tree.json`
- `02_pdf_to_md`: `converted_md/`, `repro_manifest.json`,
  `conversion_log.json`, `qa_results.json`, `qa_report.md`,
  `conversion_quality.md`
- `03_commentary_schema_discovery`: `pattern_scan/`, `schema/`,
  `stress_tests/`, `extraction_pilots/`
- `04_md_split_units`: `split_unit_schema.json` or field guide,
  `split_unit_manifest.json`, `split_qa_results.json`, `split_qa_report.md`

## 6. Review Gates

Fresh-context adversarial/headless review is required after:

- workspace cleanup/folder-state freeze
- any hardened PDF-to-MD run before research use
- schema freeze before extraction
- split-unit spec and pilot before extraction consumes split units
- extraction pilot before full extraction
- any full extraction batch before analysis
- JSON normalization before database export
- database export before downstream use

Pending reviews for `02_pdf_to_md` and `03_commentary_schema_discovery` are
blockers, not bookkeeping.

Reviewers must be read-only and must check reproducibility, active/archive
clarity, source grounding, raw-data protection, Markdown limitations, and
numeric/table/chart risk.

## 7. Adversarial Review / Reproduction Gates

| Step | When Review Is Called | Fresh Reviewer Must Reproduce / Verify | Files To Read | Output File | PASS / FAIL |
| --- | --- | --- | --- | --- | --- |
| Workspace cleanup / active-archive freeze | Before new pipeline work and before committing cleanup | Verify active folders, archived folders, pending reviews, and git status match the documented canonical structure | `PROJECT_CONTEXT.md`, `CURRENT_PROGRESS.md`, `agentic/WORKSPACE_STRUCTURE.md`, `agentic/REPRODUCIBILITY.md`, archive READMEs, `git status --short` | `agentic/reviews/workspace_cleanup_review_YYYYMMDD.md` | PASS if active/archive state is clear, raw data untouched, old paths not treated as active, and pending gates are explicit. FAIL if active outputs are ambiguous or undocumented. |
| `01_pes_folder_map` | Already completed; rerun only if raw PES folder changes | Independently recount year folders, PDFs, non-PDFs, paths, and sizes against `pes_folder_tree.json` | `pes_folder_tree.json`, `how_to_reproduce.md`, raw PES folder metadata only | `agentic/01_pes_folder_map/adv_review_results.md` | PASS if counts, paths, sizes, and classifications match filesystem. FAIL on any unexplained mismatch. |
| `02_pdf_to_md` hardened run | After each conversion run and before Markdown is used for research | Reproduce or verify manifest/log/QA; confirm page markers, file counts, hashes, prose-fidelity QA, and limits on tables/charts/numerics | `how_to_reproduce.md`, conversion script, QA script, `repro_manifest.json`, `conversion_log.json`, `qa_results.json`, `qa_report.md`, small MD/PDF samples | `agentic/02_pdf_to_md/runs/<run_name>/adv_review_results.md` | PASS if selected PDFs, outputs, page markers, logs, hashes, and QA claims match. FAIL if missing outputs, page mismatch, unlogged failures, source mutation, or numeric/table overclaiming. |
| `03_commentary_schema_discovery` | Before schema v0.1 is used for any new extraction pilot | Verify schema was derived from documented pattern scan/stress tests and that pilot records follow schema without becoming final data | `README.md`, `how_to_reproduce.md`, `pattern_scan/`, `schema/commentary_schema_v0.1.json`, `stress_tests/`, `extraction_pilots/` | `agentic/03_commentary_schema_discovery/adv_review_results.md` | PASS if schema fields are justified, pilot/stress records are valid, limits are clear, and no full extraction is implied. FAIL if schema is unsupported, inconsistent, or pilot claims are treated as final. |
| `04_md_split_units` spec | Before running split pilot | Verify split-unit schema/field guide is deterministic and preserves source grounding | `README.md`, `how_to_reproduce.md`, split-unit schema/field guide, planned input manifest | `agentic/04_md_split_units/adv_review_results.md` or run-local review file | PASS if unit IDs, page spans, headings, source paths, PDF links, and quality/numeric flags are fully specified. FAIL if reviewer must guess segmentation rules. |
| `04_md_split_units` pilot | After split pilot and before extraction consumes units | Reproduce/verify split manifest from source Markdown; confirm no claims/summaries were extracted | source Markdown sample, `input_manifest.json`, `split_unit_manifest.json`, `split_qa_results.json`, `split_qa_report.md`, script if used | `agentic/04_md_split_units/runs/<run_name>/adv_review_results.md` | PASS if units are deterministic, source-grounded, page-linked, and claim-free. FAIL if units lose page provenance, merge unrelated sections, invent headings, or extract interpretation. |
| `05_extraction_pilots` | After controlled extraction pilot, before full extraction | Verify pilot inputs, prompts/rules, schema conformance, source quotes, page references, and numeric QA flags | split-unit manifest, schema v0.1, extraction rules/prompt, `pilot_input_manifest.json`, `pilot_claims.json`, pilot QA/review files | `agentic/05_extraction_pilots/runs/<run_name>/adv_review_results.md` | PASS if records are schema-valid, quote-grounded, page-cited, and correctly flagged. FAIL if claims are unsupported, over-inferred, numerics are trusted from Markdown, or prompts are unreproducible. |
| `06_structured_claim_extraction` | After any approved full/batch extraction, before analysis | Verify batch completeness, schema validity, source grounding, duplicate handling, logs, and human-review flags | extraction manifest, raw claims JSON/JSONL, extraction logs, QA report, source split units, schema | `agentic/06_structured_claim_extraction/runs/<run_name>/adv_review_results.md` | PASS if every claim links to a valid source unit/page/quote and batch counts/logs reconcile. FAIL on unsupported claims, missing provenance, silent errors, or unflagged numeric dependence. |
| `07_json_normalization` | After normalization and before export | Reproduce validation; verify normalized records preserve raw claim IDs, source references, flags, and do not alter evidence meaning | raw claims, normalized claims, validation schema, normalization log, validation report | `agentic/07_json_normalization/runs/<run_name>/adv_review_results.md` | PASS if normalized JSON validates and preserves traceability. FAIL if IDs break, evidence changes meaning, records disappear without log, or flags are lost. |
| `08_database_export` | Before database/table output is used downstream | Reproduce export/load validation; verify row counts, schema, keys, source links, and no unapproved numeric claims | normalized JSON, export manifest, table schema, export files, load logs, validation report | `agentic/08_database_export/runs/<run_name>/adv_review_results.md` | PASS if exported tables match normalized inputs and retain provenance. FAIL if counts mismatch, fields are dropped, source links break, or exports imply unverified numeric truth. |

Reviewer rule across all gates: fresh-context, read-only, headless where
possible, no edits, no raw PDF mutation, no new extraction unless the gate
explicitly reviews an approved extraction run.

## 8. What Not To Do Yet

Do not:

- modify, move, rename, or delete raw PDFs
- process new PDFs or years
- start full extraction
- create database/table exports
- treat pilot claims as final data
- treat Markdown tables/charts/numbers as source truth
- rely on archived outputs as active
- create future folders `05` through `08` before their work is approved
- overbuild entity normalization or database schema before split/extraction
  pilots pass review

## 9. Immediate Next 3 Actions

1. Approve a read-only workspace cleanup review target: current active folders,
   archive folders, pending reviews, and uncommitted cleanup state.
2. Run/save fresh-context adversarial reviews for the cleanup state,
   `02_pdf_to_md` hardened run, and `03_commentary_schema_discovery`.
3. After review issues are resolved, approve a small `04_md_split_units`
   spec/pilot plan for 2015-16 Markdown units only.

## 10. Fresh Review Findings

The read-only sub-agent found the plan conditionally sound. Main revisions
incorporated here:

- Do not imply current 2015-16 Markdown is fully hardened until adversarial
  review passes.
- Do not call pilot JSON normalization; production normalization has not
  started.
- Add a freeze/snapshot step before review because git is currently unstable.
- Define split-unit acceptance criteria before running a split pilot.
- Keep future folders as roadmap entries only until explicitly approved.
- Make no-claims-extracted an explicit invariant for the split layer.

## 11. Final Recommendation

Approve only the next gate: a read-only adversarial review of the current
cleanup and active artifacts. After that passes, stabilize the folder layout,
then plan `04_md_split_units` as the next real pipeline stage.
