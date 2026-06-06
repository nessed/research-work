# Five-File Random Extraction Pilot

## Run Setup

- Source year: 2015-16
- Run date: 2026-06-06
- Random seed: `20260607`
- Corpus: 29 converted PES Markdown files in `agentic/02_pdf_to_md/2015-16_pymupdf4llm`
- Schema used: `schema/commentary_schema_v0.1.json`
- Sample size: 5 Markdown files, 5 records per file, 25 records total

Sampled files:

- `Health.md`
- `Trade.md`
- `Annexure_Iv_War_On_Terror.md`
- `Capital_Markets.md`
- `Education.md`

## Result

Schema v0.1 held for this random pilot. No schema revision is required from this pass.

The sample was useful because it covered several different commentary styles:

- Social-sector commitment and programme language in `Health.md` and `Education.md`
- External shock, competitiveness, and export-policy language in `Trade.md`
- Focused security-cost framing in `Annexure_Iv_War_On_Terror.md`
- Reform, market performance, and future-roadmap language in `Capital_Markets.md`

The schema handled these using the existing `claim_type`, `topic_tags`, `cause`, `effect`, `constraint_or_risk`, `policy_or_programme`, `comparison`, `numeric_or_table_sensitive`, and `requires_pdf_numeric_qa` fields.

## Where The Schema Held

`claim_type` worked as the main pattern classifier. The pilot reused existing types including `cause_effect`, `policy_action`, `commitment_or_plan`, `constraint`, `risk_or_shock`, `outlook`, `reform`, `programme_or_project`, `sector_performance`, and `security_cost`.

`topic_tags` worked better than adding many new sector-specific fields. The same record can be tagged as `health`, `programme`, and `disease_control`, or as `trade`, `exports`, and `constraint`.

`policy_or_programmes` was necessary. PES prose often names multiple linked policies in one paragraph, especially in Health, Education, Capital Markets, and Trade.

`comparison` was useful for time comparisons, reform before/after framing, and market classification shifts. It should stay optional because many prose claims are not clean comparisons.

`numeric_or_table_sensitive` and `requires_pdf_numeric_qa` are essential. Even when extracting commentary, many claims are anchored to tables, percentages, targets, or before/after values that should not be trusted from Markdown alone.

## Stress Points

The annexure showed that some files are not sector narratives but cost-accounting narratives. The existing `security_cost` type handled this well enough, but future extraction rules should say that annexes/supplements may produce fewer prose claims and more metadata or table-sensitive claims.

Some claims combine action, outlook, and expected effect in one sentence. Example: STPF is both a policy action and an expected export-diversification mechanism. For consistency, extraction should pick one primary `claim_type` and use tags plus cause/effect fields for the secondary meaning.

Table-adjacent prose can be tempting to over-extract. In this pilot, exact values were not treated as final data. Any record using table labels, targets, percentages, or cumulative cost values was flagged for PDF numeric QA.

Markdown quality issues remain visible. `Education.md` includes broken words in the Overall Assessment section, and table-heavy areas in Trade, Health, Education, Capital Markets, and the War on Terror annex have layout noise.

## Practical Extraction Rules To Add Next

- Extract one record per distinct commentary claim, not one record per sentence.
- Use `claim_type` for the primary pattern only.
- Use `topic_tags` for cross-cutting themes instead of creating new fields.
- Keep `source_quote` short and quote-grounded.
- Do not extract table values as final facts from Markdown.
- Set `numeric_or_table_sensitive: true` whenever a claim depends on a number, table, chart, target, percentage, ranking, or exact before/after movement.
- Set `requires_pdf_numeric_qa: true` for all numeric/table-sensitive claims.
- Use `confidence` for extraction/classification confidence, not truth confidence.
- Keep `needs_human_review: true` for this RA workflow.

## Next Step

Freeze schema v0.1 for prompt-writing and create extraction instructions for a controlled 5-6 chapter pilot. The next pilot should test consistency between extractors or runs, not revise the schema unless a genuinely new repeatable pattern appears.

Original PDFs remain source truth. Tables, charts, and numeric values need separate QA before becoming database-ready data.
