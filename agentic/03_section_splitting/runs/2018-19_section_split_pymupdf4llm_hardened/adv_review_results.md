# Adversarial Review Results

Claude was attempted first for the broader task's fresh-context review path,
but the escalated Claude CLI request was rejected by policy because it would
disclose private workspace/source-derived content to an external Claude service.
This Step 03 review therefore used the Codex fallback reviewer.

## Findings

High: The reviewed run was not homogeneous `2018-19`. It included
`Supplement_2017_18.md` as an input and created sections from it while every
section was labeled `source_year: 2018-19`. The source Markdown itself says
`Pakistan Economic Survey 2017-18` and says the supplement updates the 2017-18
survey.

Medium: The reviewed run double-counted the 2018-19 statistical supplement.
`Statistical_Supplement.md` and `Supplement_2018_19.md` were both included,
had the same source/output hashes, and produced same-order, same-text,
same-page sections.

Low: Sampled section text was traceable to source Markdown only after
whitespace normalization, not as exact byte-for-byte substrings. Example:
source heading whitespace was trimmed in JSONL. This looked like cleanup, not
paraphrase, but it failed a strict exact-text interpretation.

## PASS/FAIL Summary

FAIL for the initially reviewed Step 03 section layer.

Structural checks otherwise passed: `sections.jsonl` had 3,510 records, matching
SHA256 and size, 3,510 unique `section_id`s, all required fields present, and
no extra/generated claim, summary, interpretation, normalized, database, or
export fields.

## Evidence Checked

- Included/excluded scope reconciled mechanically: 24 included + 3 excluded =
  27 converted Markdown files.
- Later-year supplements `2019_20`, `2020_21`, and `2021_22` were excluded and
  did not leak into JSONL.
- Page spans validated against recorded PDF-to-MD manifest page counts: zero
  invalid `start_page`/`end_page` spans.
- Numeric/table limitations were explicit: report recorded 3,454
  numeric/table-sensitive sections and stated tables/charts/numbers remain
  uncertified until PDF QA.

## Required Correction

Rerun or correct the section stage to exclude or relabel `Supplement_2017_18`
and deduplicate or explicitly justify `Statistical_Supplement` vs
`Supplement_2018_19`. Do not proceed from the failed section layer until this
scope issue is fixed and re-reviewed.

## Corrected Rerun Review

After the failed review, the section splitter was corrected and rerun. The
corrected scope:

- includes 22 `2018-19` source-year Markdown files
- excludes `Supplement_2017_18.md` as prior-year
- excludes `Supplement_2019_20.md`, `Supplement_2020_21.md`, and
  `Supplement_2021_22.md` as later-year
- excludes `Statistical_Supplement.md` as a duplicate alias of
  `Supplement_2018_19.md` by source and output hash
- keeps `Supplement_2018_19.md` as the 2018-19 supplement source

### Corrected PASS/FAIL Summary

PASS. The corrected run is acceptable as a source-tagged section layer for
later, separately approved extraction work.

### Corrected Evidence Checked

- `sections.jsonl`: 2,736 records; SHA-256 matches manifest:
  `09e44a0a274b2b74f285499ff4607c996902a49cee1a00ece0686d9f2eab4f7f`.
- Unique `section_id`: 2,736 unique IDs, no duplicates.
- Required fields: all records have required schema fields.
- `source_year`: all records are `2018-19`.
- Scope reconciliation: upstream conversion has 27 Markdown outputs; corrected
  section run has 22 included + 5 excluded = 27.
- Required exclusions present: `Supplement_2017_18`,
  `Supplement_2019_20`, `Supplement_2020_21`, `Supplement_2021_22`, and
  `Statistical_Supplement`.
- Duplicate supplement check: `Statistical_Supplement.pdf` and
  `Supplement_2018_19.pdf` share the same source hash and output Markdown hash
  in the PDF-to-MD manifest; keeping `Supplement_2018_19.md` is justified.
- No excluded `source_md_path` appears in `sections.jsonl`.
- Page spans: all section page ranges valid; direct PyMuPDF check of 22
  included source PDFs found 0 page-count mismatches.
- Traceability: all 2,736 sections' normalized text is contained in the
  declared source Markdown page block.
- No forbidden extraction/export fields found: no claim, summary,
  interpretation, conclusion, outlook, risk, sentiment, normalized, database,
  or export fields.
- Numeric/table limitations are explicit in `section_split_report.md` and
  upstream QA: table/chart/numeric content remains uncertified pending PDF
  verification.

### Corrected Residual Risks

Markdown remains a working layer, not source truth. Tables, chart text, exact
numbers, rankings, totals, and footnotes still require separate PDF-level QA
before claims extraction or research use. The section layer is suitable for
source-tagged text routing, not for factual numeric extraction on its own.
