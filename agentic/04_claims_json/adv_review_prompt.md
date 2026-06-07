# Adversarial Review Prompt — Claims JSON (Stage Base)

You are a fresh-context reviewer. You have not seen the extraction run or the
conversation that produced it. Your job is to verify that the `claims.jsonl`
output is trustworthy as a source-grounded commentary layer before it is used
downstream.

## What you are reviewing

- `claims.jsonl` — one JSON record per extracted commentary claim.
- `extraction_manifest.json` — run metadata, counts, hashes.
- `extraction_report.md` — run notes and QA summary.
- `how_to_reproduce.md` — run-specific reproduction instructions.
- Source: the `sections.jsonl` used as input (referenced in manifest).
- Schema: `agentic/archive/04_commentary_schema_discovery/schema/commentary_schema_v0.1.json`.

## What to check

### 1. Manifest and count reconciliation
- Does the `claims.jsonl` line count match the total in `extraction_manifest.json`?
- Does the SHA-256 hash in the manifest match the actual file?
- Does the input section run path in the manifest point to a real PASS-reviewed
  section run folder?
- Is the schema version recorded and does it match `commentary_schema_v0.1.json`?

### 2. Required fields
For a random sample of at least 20 records (spread across multiple source files),
verify:
- All required fields are present and non-empty where schema requires it:
  `source_year`, `source_file`, `source_page`, `evidence_type`, `source_quote`,
  `claim_type`, `claim`, `confidence`, `needs_human_review`.
- `needs_human_review` is `true` on every record without exception.
- `numeric_or_table_sensitive` and `requires_pdf_numeric_qa` are booleans.
- `topic_tags`, `actors`, `policy_or_programmes`, `data_status_flags` are arrays.

### 3. Controlled vocabulary
For the same sample, verify:
- `claim_type` is one of the allowed values in schema v0.1.
- `evidence_type` is one of the allowed values.
- `sentiment_signal` is one of the allowed values or empty.
- `time_orientation` is one of the allowed values or empty.
- `confidence` is one of `"high"`, `"medium"`, `"low"`.
- `comparison.direction` is one of the allowed values or empty.

### 4. Source grounding
For at least 10 records from different source files:
- Locate the cited `source_file` and `source_page` in the source `sections.jsonl`.
- Confirm the `source_quote` appears (verbatim after whitespace trim) in the
  section text at or near the cited page.
- Flag any record where the quote cannot be traced back to the source section.

### 5. Numeric and table flagging
- For any claim that mentions a number, percentage, ranking, target, or table
  reference: confirm `numeric_or_table_sensitive` is `true` and
  `requires_pdf_numeric_qa` is `true`.
- Flag any record that presents a numeric value as a final fact without these flags.

### 6. No fabrication
- Confirm no `source_quote` is paraphrased, summarized, or invented. It must be a
  literal excerpt from the section text.
- Confirm no field contains a value that cannot be grounded in the source passage
  (e.g. an actor name not present in the text, a cause or effect that is inferred).

### 7. Schema compliance
- Confirm no extra fields exist beyond the schema template.
- Confirm no schema field has been redefined or repurposed.
- If `extraction_report.md` flags any schema-fit gaps, note whether they were
  handled correctly (documented in the report, not invented as new fields).

### 8. Coverage plausibility
- Is the record count plausible relative to the section count and document scope?
  A very low count (e.g. <5 claims from a 100-section prose chapter) or very high
  count (e.g. >10 claims per section on average) should be noted.
- Are there any source files with zero records that should have produced claims?

## Output format

Write your findings in `adv_review_results.md` in the run folder. Structure:

1. **Overall verdict**: PASS or FAIL (a FAIL means downstream use is blocked).
2. **Evidence checked**: what you read, sample sizes, how you traced quotes.
3. **Findings**: any issues found, keyed to record or source file.
4. **Residual risks**: known limitations that do not block use but should be noted
   (e.g. sector field is filename-derived and not a normalized taxonomy).
5. **Conclusion**: one paragraph summary with recommendation.

A PASS means: source grounding is confirmed, controlled vocab is respected, numeric
flags are present where required, no fabricated quotes, counts reconcile. Residual
risks are noted but do not block downstream use.

A FAIL means: blocking issues found. Re-extraction or prompt correction is required
before downstream use.
