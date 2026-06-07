# Adversarial Review Prompt - Claims JSON

You are a fresh-context reviewer. You have not seen the extraction run or the
conversation that produced it. Your job is to decide whether Step 04 can feed
Step 05.

Step 04 PASS means one final `claims.jsonl` is source-grounded, schema-compliant,
validated, and supported by reconciled run evidence.

## What You Are Reviewing

- Run root `claims.jsonl`.
- `_supporting/source_scope.json`.
- `_supporting/jobs.jsonl`.
- `_supporting/job_results.jsonl`.
- `_supporting/run_state.json`.
- `_supporting/extraction_manifest.json`.
- `_supporting/extraction_report.md`.
- `_supporting/how_to_reproduce.md`.
- Source Step 03 `sections.jsonl`.
- Schema:
  `agentic/archive/04_commentary_schema_discovery/schema/commentary_schema_v0.1.json`.
- Validator:
  `agentic/04_claims_json/validate_claims.py`.

## Blocking Checks

### 1. Source Scope

- Confirm the Step 03 input path exists and has a PASS adversarial review.
- Confirm included and excluded source files are explicit in `source_scope.json`.
- Confirm no source file was silently skipped.
- If a duplicate full-survey file was excluded, confirm the reason is recorded
  and plausible.

### 2. Job Coverage and Resume State

- Confirm every included Step 03 section appears in exactly one job.
- Confirm all jobs are complete in `run_state.json`.
- Confirm no failed jobs remain unless the report marks the run FAIL.
- Confirm job hashes are present for input, prompt, schema, runner, and engine
  contract.
- Confirm final `claims.jsonl` was rebuilt from completed job results, not
  manually assembled from per-chapter smoke files.

### 3. Manifest and Count Reconciliation

- `claims.jsonl` line count matches manifest total.
- Manifest SHA-256 matches actual `claims.jsonl`.
- Per-source claim counts reconcile between manifest, report, and output.
- Schema version and prompt path are recorded.

### 4. Schema Compliance

For all records if practical, otherwise a broad sample across source files:

- No missing or extra fields.
- `comparison` has exactly `dimension`, `baseline`, `comparator`, `direction`.
- Controlled vocab values are valid.
- Boolean fields are booleans.
- Array fields are arrays.
- `needs_human_review` is true on every record.

### 5. Source Grounding

For at least 20 records across multiple source files:

- Locate the cited `source_file` and `source_page` in Step 03 `sections.jsonl`.
- Confirm `source_quote` is a literal excerpt after approved normalization for
  Markdown artifacts.
- Confirm the claim paraphrase is supported by the quoted/local section text.
- Flag any record where actor, cause, effect, programme, or geography is inferred
  rather than grounded.

### 6. Numeric and Table Flagging

- Any claim depending on numbers, percentages, targets, rankings, tables, charts,
  or exact movements must have `numeric_or_table_sensitive=true` and
  `requires_pdf_numeric_qa=true`.
- No table value may be presented as a certified final fact.

### 7. Coverage Plausibility

- Claim counts should be plausible relative to included source sections.
- Very low counts for prose-heavy chapters or very high counts per section must
  be investigated.
- Zero-claim included source files require a documented reason.

### 8. Folder Cleanliness

- Run root contains only final `claims.jsonl`.
- `_supporting/` contains audit/state files.
- Production runs do not depend on `smoke_*_sections.jsonl`,
  `smoke_*_claims.jsonl`, or stale helper scripts.

## Output Format

Write findings in the run's `_supporting/adv_review_results.md`:

1. Overall verdict: PASS or FAIL.
2. Evidence checked: files read, sample sizes, commands or scripts used.
3. Findings: blocking issues first, keyed to file/record/job where possible.
4. Residual risks: non-blocking limitations.
5. Conclusion: whether Step 04 may feed Step 05.

Use FAIL if any blocking check fails. Do not give PASS merely because the
automated validator passed.
