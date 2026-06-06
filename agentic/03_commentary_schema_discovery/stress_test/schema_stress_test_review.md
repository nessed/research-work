# Schema Stress Test Review

## Summary

This stress test applied the draft commentary schema to 3 deterministic-random
Markdown files from the 29-file PyMuPDF4LLM corpus:

- `Public_Debt.md`
- `Population.md`
- `Supplement_2020_21.md`

The test produced 30 limited records: 10 from each file. This is not a full
claim extraction pass and should not be treated as a database. Original PDFs
remain source truth, and table/chart/numeric values still require separate QA.

## What Worked

- The core source-grounding fields worked: `source_file`, `sector`,
  `subsection`, `source_page`, `source_quote`, and `claim`.
- `claim_type` worked well for prose chapters, especially:
  `cause_effect`, `policy_action`, `commitment_or_plan`, `outlook`, `reform`,
  `constraint`, `regional_comparison`, and `need_for_improvement`.
- `cause` and `effect` were useful for public debt and population narratives.
- `topic_tags` were necessary because many claims are cross-cutting.
- `numeric_or_table_sensitive` was essential and should stay.

## Where The Schema Broke

1. `time_orientation` vocabulary was incomplete.
   - Existing example records already used `past_or_current`, but the controlled
     vocabulary did not include it.
   - Several claims are general/structural truths rather than past/current/future
     claims, so `general` is needed.

2. Supplement records are not normal commentary claims.
   - `Supplement_2020_21.md` is mostly tables, notes, contents, and status
     markers.
   - The schema needs to distinguish prose commentary from table note,
     preface/publication note, table index, and numeric indicator material.

3. Page-level source grounding is too broad for supplements.
   - Dense supplement pages contain many unrelated indicators.
   - The schema needs `source_table_or_figure` and `indicator_or_subject` so a
     record can point below page level.

4. Numeric sensitivity is too coarse as a boolean.
   - A record can be numeric-sensitive because it contains exact values, because
     it depends on a table, because it uses a revised/provisional marker, or
     because a base-year change affects comparability.
   - Add `data_status_flags` and `requires_pdf_numeric_qa`.

5. Actor/programme fields are too flat.
   - Several records contain multiple actors or multiple programmes in one
     sentence.
   - Keep simple string fields for v1, but add optional array fields:
     `actors` and `policy_or_programmes`.

6. Comparison claims need structure.
   - Population claims often compare urban/rural, male/female, age groups, or
     prior/current periods.
   - Public debt claims compare risk indicators across fiscal years.
   - Add a `comparison` object with `dimension`, `baseline`, `comparator`, and
     `direction`.

7. Markdown quality needs a field.
   - `Population.md` has fragmented words in some pages from PDF layout.
   - Add `markdown_quality_flags` so extractors can mark broken words, table
     layout, picture text, or page-order noise.

## Recommended Schema Revisions

- Add `evidence_type` with values such as `prose`, `table_note`,
  `table_or_indicator`, `figure_text`, `preface_or_publication_note`,
  and `table_of_contents`.
- Add `source_table_or_figure`.
- Add `indicator_or_subject`.
- Add `comparison`.
- Add `data_status_flags`.
- Add `requires_pdf_numeric_qa`.
- Expand `time_orientation` to include `past_or_current` and `general`.
- Add optional `actors` and `policy_or_programmes` arrays while keeping the
  existing singular fields for easy use.
- Add `markdown_quality_flags`.

## Revised Extraction Guidance

- For prose chapters, extract one source-grounded commentary claim per record.
- For supplement files, default to extracting only `data_caveat` or
  publication-method records unless a human explicitly asks for numeric/table
  ingestion.
- If a claim depends on an exact value, table, chart, ranking, or base-year
  note, set `numeric_or_table_sensitive = true` and
  `requires_pdf_numeric_qa = true`.
- If the Markdown quote contains fragmented words, keep the quote short and set
  `markdown_quality_flags`.

