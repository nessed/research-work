# Adversarial Review Prompt — 2016-17 Claims Smoke Test

You are a fresh-context reviewer. You have not seen the extraction run or the
conversation that produced it. Your task: decide PASS or FAIL on this smoke test
output before it is used downstream.

## What to review

- `../claims.jsonl` - final root output containing 73 claim records across 3 source files:
  Agriculture.md (32), Health.md (20), Trade.md (21).
- `extraction_manifest.json` — run metadata and SHA-256 hash.
- `extraction_report.md` — per-document counts, notes, QA summary.
- Input sections: `agentic/03_section_splitting/runs/2016-17_section_split_pymupdf4llm_hardened/sections.jsonl`
- Schema: `agentic/archive/04_commentary_schema_discovery/schema/commentary_schema_v0.1.json`

## Checks

### 1. Manifest reconciliation
- Does root `claims.jsonl` line count = 73 (as stated in manifest)?
- Does SHA-256 match? Expected: dd65e72b7f6dd39bc8b1e267c5b921e12324c111fef6ad9d6a4236fbce2f358e
- Does the schema version match commentary_schema_v0.1?

### 2. Required fields (sample 20+ records spread across all 3 files)
- All required fields present and non-empty where required.
- needs_human_review is true on every record without exception.
- numeric_or_table_sensitive and requires_pdf_numeric_qa are booleans.
- topic_tags, actors, policy_or_programmes, data_status_flags are arrays.
- comparison is a dict with a direction field.

### 3. Controlled vocabulary (same sample)
- claim_type in {sector_performance, cause_effect, policy_action, commitment_or_plan,
  constraint, risk_or_shock, outlook, reform, investment_priority, programme_or_project,
  regional_comparison, data_caveat, need_for_improvement, security_cost, publication_note, other}
- evidence_type in {prose, table_note, table_or_indicator, figure_text,
  preface_or_publication_note, table_of_contents, mixed}
- sentiment_signal in {positive, negative, mixed, neutral, unclear, ""}
- time_orientation in {past, current, past_or_current, future, ongoing, multi_period, general, unclear, ""}
- confidence in {high, medium, low}
- comparison.direction in {increase, decrease, improvement, deterioration, higher_than,
  lower_than, shift, no_change, unclear, ""}

### 4. Source grounding (10 records minimum, across all 3 files)
- For each sampled record: locate source_file in sections.jsonl, find sections covering
  source_page, confirm source_quote appears in the section text (verbatim after
  whitespace normalization).
- Note: sections.jsonl uses U+FFFD for apostrophes (PDF artifact). Normalize before comparing.
- Note: some sections have broken-word bold artifacts (e.g., "p **r** ogram"). Strip ** before matching.
- Flag any record where the quote cannot be traced.

### 5. Numeric flagging
- Every claim mentioning a number, percentage, target, or table reference must have
  numeric_or_table_sensitive=true AND requires_pdf_numeric_qa=true.
- Flag any record that presents a numeric value without these flags.

### 6. No fabrication
- source_quote must be a literal excerpt, not paraphrased or summarized.
- No field should contain an actor, cause, or effect that is not grounded in the
  source passage.

### 7. Schema compliance
- No extra fields beyond schema v0.1.
- No field redefined or repurposed.

### 8. Coverage plausibility
- 32 claims from 66 Agriculture sections: plausible (~0.48/section average)?
- 20 claims from 41 Health sections: plausible?
- 21 claims from 46 Trade sections: plausible?
- Any source file with zero records that should have produced claims?

## Output

Write findings in `adv_review_results.md` in this run folder. Use the structure:
1. Overall verdict: PASS or FAIL
2. Evidence checked: what you read, sample sizes, how you traced quotes
3. Findings: any issues, keyed to record or file
4. Residual risks: known limitations that do not block use
5. Conclusion: one-paragraph summary with recommendation
