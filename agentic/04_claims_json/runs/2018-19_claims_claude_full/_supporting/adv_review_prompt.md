# Adversarial Review Prompt — 2018-19 Claims Extraction (claude, full year)

You are a fresh-context reviewer. You have not seen the extraction run or the
conversation that produced it. Your job is to decide whether this Step 04 run
can feed Step 05.

## Run Context

| Field | Value |
|---|---|
| Run label | `2018-19_claims_claude_full` |
| Source year | 2018-19 |
| Engine | claude (headless, non-bare OAuth) |
| Runner | `agentic/04_claims_json/run_step04.py` |
| Jobs total | 56 |
| Included sections | 970 across 17 chapter files |
| Excluded sections | 1766 (full-survey duplicate + supplement + 3 annex files) |

## Files to Review

- `claims.jsonl` (run root — final output)
- `_supporting/source_scope.json`
- `_supporting/jobs.jsonl`
- `_supporting/job_results.jsonl`
- `_supporting/run_state.json`
- `_supporting/extraction_manifest.json`
- `_supporting/extraction_report.md`
- `_supporting/how_to_reproduce.md`
- Step 03 input:
  `agentic/03_section_splitting/runs/2018-19_section_split_pymupdf4llm_hardened/sections.jsonl`
- Schema:
  `agentic/archive/04_commentary_schema_discovery/schema/commentary_schema_v0.1.json`
- Output schema:
  `agentic/04_claims_json/claim_array_output_schema.json`
- Validator:
  `agentic/04_claims_json/validate_claims.py`

## Blocking Checks

### 1. Source Scope

- Step 03 run path exists and has a PASS adversarial review.
- `source_scope.json` explicitly lists all 22 source files from Step 03.
- All 17 included files and all 5 excluded files are named with counts and reasons.
- `Economic_Survey_2018_19.md` is excluded as the full-survey duplicate —
  confirm the reason is recorded and the 1355-section count matches.
- `Supplement_2018_19.md`, `Annex_I.md`, `Annex_Ii.md`, `Economic_Indicators_1819.md`
  are excluded as statistical/tabular files — confirm reasons are plausible.
- No chapter-level source file was silently skipped.

### 2. Job Coverage and Resume State

- 970 included sections appear across exactly 56 jobs (no section in two jobs,
  no section missing).
- `run_state.json` shows all 56 jobs in `completed[]` and 0 in `failed[]`.
- No `_supporting/failed_jobs/` entries remain unresolved.
- Each job record in `jobs.jsonl` carries `input_hash`, `prompt_hash`,
  `schema_hash`, `runner_label`, and `engine_contract`.
- `claims.jsonl` was rebuilt from `job_results.jsonl` in stable job order, not
  manually assembled.

### 3. Manifest and Count Reconciliation

- `claims.jsonl` line count matches manifest total.
- Manifest SHA-256 matches actual `claims.jsonl`.
- Per-source claim counts reconcile between manifest, extraction report, and
  `job_results.jsonl`.
- Schema version and prompt path are recorded in the manifest.

### 4. Schema Compliance

Sample at minimum 50 records spanning at least 5 different source files:

- No missing or extra fields relative to `claim_array_output_schema.json`.
- `comparison` object has exactly `dimension`, `baseline`, `comparator`,
  `direction`.
- Controlled vocab values are valid (see schema enum lists).
- Boolean fields are booleans, not strings.
- Array fields (`topic_tags`, `actors`, `policy_or_programmes`,
  `data_status_flags`, `markdown_quality_flags`) are arrays.
- `needs_human_review` is `true` on every record.

### 5. Source Grounding

For at least 30 records spanning multiple source files:

- Locate the cited `source_file` and `source_page` in Step 03 `sections.jsonl`.
- Confirm `source_quote` is a literal excerpt from the `text` field of that
  section (approved normalisation: collapse whitespace and strip Markdown
  formatting artifacts only).
- Confirm the `claim` paraphrase is supported by the quoted text and its
  immediate local context.
- Flag any record where `actor`, `cause`, `effect`, `policy_or_programme`, or
  `geography` is inferred rather than grounded.

### 6. Numeric and Table Flagging

- Any claim that cites a number, percentage, target, ranking, table, chart, or
  directional movement must have `numeric_or_table_sensitive=true` and
  `requires_pdf_numeric_qa=true`.
- No table value may appear as a certified final fact in `claim` text.
- Pay particular attention to Transport (156 sections), Health_And_Nutrition
  (80 sections), Agriculture (71 sections), and Captial_Markets (71 sections)
  as the largest chapters.

### 7. Coverage Plausibility

- Total claim count is plausible relative to 970 included sections.
- Per-chapter claim density (claims per section) is consistent across chapters
  of similar type.
- Any chapter returning zero claims must be documented with a reason.
- Chapters with anomalously high or low claim counts must be investigated.

### 8. Folder Cleanliness

- Run root contains only `claims.jsonl`.
- `_supporting/` contains only the documented audit/state files plus
  `gen_jobs.py`.
- No `smoke_*`, per-chapter output files, or temporary debug files are present
  in the run root or `_supporting/`.

## Output Format

Write findings to `_supporting/adv_review_results.md`:

1. **Overall verdict**: PASS or FAIL.
2. **Evidence checked**: files read, record sample sizes, any scripts or
   commands run.
3. **Findings**: blocking issues first, keyed to file / record / job where
   possible.
4. **Residual risks**: non-blocking limitations or caveats.
5. **Conclusion**: whether this Step 04 run may feed Step 05.

Use FAIL if any blocking check fails. Do not give PASS merely because the
automated validator passed.
