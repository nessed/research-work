# Hard-Case Schema Review

## Summary

This hard-case stress test used:

- `Agriculture.md` for dense sector prose, causes, shocks, policies, and
  subsector narratives.
- `Social_Safety.md` for programme-heavy social policy and implementation
  claims.
- `Economic_Indicators.md` for table/indicator-only material and data caveats.

The test produced 34 records. This remains schema validation, not full claim
extraction. Original PDFs remain source truth, and exact table/chart/numeric
values still need separate PDF QA.

## Result

Schema draft v2 held up well enough to freeze as `commentary_schema_v0.1.json`.

No major structural change was required after this hard-case test. The fields
added after the earlier stress test were exactly the fields needed here:

- `evidence_type`
- `source_table_or_figure`
- `indicator_or_subject`
- `comparison`
- `data_status_flags`
- `requires_pdf_numeric_qa`
- `markdown_quality_flags`
- plural `actors` and `policy_or_programmes`

## What The Hard Cases Confirmed

- `Agriculture.md` needs the full cause/effect structure because one sentence
  often contains a shock, a constraint, a performance judgement, and a policy
  implication.
- `Social_Safety.md` needs programme arrays because many passages name BISP
  sub-programmes, donor support, payment mechanisms, and future actions in the
  same local context.
- `Economic_Indicators.md` should not be treated like a prose chapter. Most
  useful records from this file are `data_caveat` records with
  `evidence_type = "table_note"` or `"table_or_indicator"`.
- `numeric_or_table_sensitive` plus `requires_pdf_numeric_qa` is necessary for
  almost every indicator/table-derived record.
- `markdown_quality_flags` is useful for agriculture and social-safety pages
  with broken words, table layout noise, figure text, or picture placeholders.

## Minor Guidance Tweaks

These do not require schema shape changes:

- For hard prose chapters, prefer one primary `claim_type` and use fields/tags
  for secondary dimensions. Example: an agriculture climate passage can be
  `risk_or_shock` while still filling `cause`, `effect`, and `topic_tags`.
- For programme-heavy chapters, use `policy_or_programme` for the main named
  programme and `policy_or_programmes` for all named schemes in the local
  passage.
- For indicator-heavy files, do not infer trend claims from table values during
  commentary extraction. Store table caveats only unless a later numeric QA
  task is explicitly started.
- If a field is not explicit in the quote or local passage, leave it blank
  rather than inferring.

## Freeze Decision

Freeze `schema/commentary_schema_draft.json` as
`schema/commentary_schema_v0.1.json`.

The next task should be writing extraction rules/prompt instructions for a
small multi-chapter pilot using this v0.1 schema.
