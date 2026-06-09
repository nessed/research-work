# Adversarial Review Prompt

You are a fresh-context read-only reviewer. Review a future section-splitting
run for reproducibility and source grounding.

Do not edit, move, rename, delete, or create files.
Do not modify raw PDFs.
Do not modify converted Markdown.
Do not extract claims.
Do not create summaries or interpretations.

## Review Inputs

Read:

- `agentic/03_section_splitting/README.md`
- `agentic/03_section_splitting/section_schema.json`
- `agentic/03_section_splitting/split_rules.md`
- `agentic/03_section_splitting/how_to_reproduce.md`
- the run folder being reviewed
- the run's `section_manifest.json`
- the run's `sections.jsonl`
- the run's `section_split_report.md`
- small samples from the source converted Markdown files as needed

## Checks

Verify:

1. Every `section_id` is unique within the run.
2. Every `source_md_path` exists.
3. Every `source_pdf_path` points to an original raw PDF and was not modified.
4. Every `start_page` and `end_page` is valid for the source Markdown page
   markers.
5. Every section text comes from the converted Markdown.
6. No claims, summaries, interpretations, conclusions, or database-ready facts
   were created.
7. Table-heavy, figure-heavy, numeric-heavy, chart-adjacent, or exact-value
   sections are flagged with `numeric_or_table_sensitive: true`.
8. Markdown quality issues are captured in `markdown_quality_flags`.
9. The output is reproducible from the documented input folder and rules.
10. Counts in `section_manifest.json`, `sections.jsonl`, and
    `section_split_report.md` reconcile.

## Output

Write findings to the run's:

```text
adv_review_results.md
```

## PASS / FAIL Standard

PASS only if:

- section IDs are unique
- pages are valid
- sections are source-grounded in Markdown
- source PDF paths are preserved
- no claims or summaries are created
- numeric/table/figure-sensitive sections are flagged
- outputs are reproducible

FAIL if:

- page provenance is missing or invalid
- section text is invented or summarized
- claims are extracted
- raw PDFs or converted Markdown were modified
- numeric/table-heavy sections are not flagged
- output counts do not reconcile
- the run cannot be reproduced from the documented inputs

