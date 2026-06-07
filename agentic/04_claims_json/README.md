# Step 04: Claims JSON

This is the canonical instruction document for the Claims JSON extraction stage.
Follow this file first for every run. Use each run folder's `how_to_reproduce.md`
only for that run's exact input paths, script or prompt, commands, and results.

## Purpose

Extract source-grounded commentary claims from reviewed section text and write
them as structured JSON records following the frozen schema v0.1.

Claims JSON is a working extraction layer. It records what the PES commentary
says, not verified facts. Every claim must be traceable to a source section, a
source page marker, and a short source quote from the Markdown.

## Source Input

- Input must be a `sections.jsonl` from a reviewed and PASS-rated section split
  run under `agentic/03_section_splitting/runs/`.
- Do not extract from unreviewed or in-progress section runs.
- Original PDFs remain source truth. Markdown is a working text layer.
- Do not touch, rewrite, move, or annotate raw PDFs during Step 04.
- Table, chart, and numeric values from Markdown are not source truth unless
  separately QA'd against the PDFs.

## Schema

Use the frozen schema:

```text
agentic/archive/04_commentary_schema_discovery/schema/commentary_schema_v0.1.json
```

Do not modify the schema during extraction. If a genuinely new repeatable
pattern appears that the schema cannot handle, document it in the run's
`extraction_report.md` and flag it for schema review — do not invent new fields
mid-run.

Required fields per record: `source_year`, `source_file`, `sector`,
`source_page`, `evidence_type`, `source_quote`, `claim_type`, `claim`,
`numeric_or_table_sensitive`, `requires_pdf_numeric_qa`, `markdown_quality_flags`,
`confidence`, `needs_human_review`.

## Extraction Rules

Derived from the five-file random extraction pilot and stress tests in
`agentic/archive/04_commentary_schema_discovery/`.

Step 04 is a CLI-agent execution stage. It does not require an API client or
API key. Process source documents internally one at a time, using each
document's section records from the year-level `sections.jsonl`. Govern the run
at the year level: one reviewed source-year input, one Step 04 run folder, one
final root `claims.jsonl`.

**Granularity**
- Extract one record per distinct commentary claim, not one record per sentence.
- Do not merge unrelated claims into one record.

**Claim type**
- Use `claim_type` for the primary commentary pattern only.
- When a claim combines action, outlook, and expected effect in one sentence,
  pick one primary type; use `cause`, `effect`, and `topic_tags` for the rest.

**Topic tags**
- Use `topic_tags` for cross-cutting themes instead of creating new fields.

**Source quote**
- Keep `source_quote` short and directly traceable to the source section text.
- Do not paraphrase in `source_quote`.

**Numeric and table sensitivity**
- Set `numeric_or_table_sensitive: true` whenever a claim depends on a number,
  table, chart, target, percentage, ranking, or exact before/after movement.
- Set `requires_pdf_numeric_qa: true` for all numeric/table-sensitive claims.
- Do not extract table values as final facts from Markdown.

**Annexes and supplements**
- Annexe and supplement sections typically produce fewer prose claims and more
  metadata or table-sensitive claims. This is expected, not a gap.

**Confidence and review flags**
- Use `confidence` for extraction and classification confidence, not for truth
  confidence in the underlying government claim.
- Keep `needs_human_review: true` on every record in this RA workflow.

## Required Run Layout

Create one run folder under:

```text
agentic/04_claims_json/runs/<year>_<tool>_<label>/
```

Each run folder must contain:

- `claims.jsonl` - the only final output at the run root; one JSON object per
  extracted claim record.
- `_supporting/` - all non-final run evidence, including the manifest, report,
  how-to, review prompt/results, logs, helper scripts, notes, and intermediate
  files.

The run root must not contain intermediate claim files, logs, scripts, review
paperwork, or prompt copies outside `_supporting/`.

## Required QA

The validator is the objective gate for Step 04. Every run must verify:

- All required fields are present on every record.
- `claim_type` values are from the controlled vocabulary in schema v0.1.
- `evidence_type` values are from the controlled vocabulary.
- `source_page` is present and matches a page marker in the source section.
- `source_quote` is non-empty and traceable to the source section text.
- `numeric_or_table_sensitive` is a boolean on every record.
- `needs_human_review` is `true` on every record.
- Record count is plausible relative to section count and source year scope.
- No fabricated values, no inferred numeric claims presented as source text, no
  database-ready normalized facts.

Do not normalize, export, deduplicate into final fact tables, or start Step 05/06
work in Step 04.

## Review Gate

Before downstream use, a fresh-context read-only reviewer must verify:

- Source grounding: `source_quote` traces back to the cited section and page.
- Controlled vocab adherence: `claim_type` and `evidence_type` are valid values.
- Numeric flagging: numeric/table-sensitive claims are flagged, not extracted as
  final data.
- No fabricated or inferred claims presented as source quotes.
- Extraction manifest, input path, schema version, and record counts reconcile.
- `needs_human_review` is `true` on every record.

Do not proceed downstream if the validator fails or the fresh-context review
fails. Fix the Step 04 output first, then rerun validation and review.

## Run-Level Reproducibility

Run-level `how_to_reproduce.md` files should not redefine this stage. They
should only state:

- Year, input section run path, and schema version used.
- Output folder.
- Exact script or prompt used for extraction.
- Observed model or tool version and environment.
- QA command or procedure.
- Run result and any run-specific caveats.
