# How To Reproduce

Stage-level guide for section splitting. Run-specific paths, exact commands,
observed environment, and results live in each run folder's own
`how_to_reproduce.md`.

## Input

A run takes one reviewed converted Markdown folder as input, for example:

```text
agentic/02_pdf_to_md/runs/<pdf_to_md_run_name>/converted_md/
```

The converted Markdown must already contain source page markers such as:

```markdown
<!-- page 1 -->
```

## Output

A run writes outputs to a new run folder:

```text
agentic/03_section_splitting/runs/<section_split_run_name>/
```

Expected outputs:

- `sections.jsonl`
  One JSON object per source-tagged section, following `section_schema.json`.
- `section_manifest.json`
  Input files, output files, counts, hashes, environment details, and run
  settings.
- `section_split_report.md`
  Human-readable report with counts, warnings, skipped files, and QA summary.
- `adv_review_prompt.md`
  Run-specific review prompt if it differs from the folder-level prompt.
- `adv_review_results.md`
  Fresh-context read-only review results.

## Run Requirements

The splitter must:

1. Read converted Markdown files from the input `converted_md/` folder.
2. Preserve source page markers for page tracking.
3. Split text using the rules in `split_rules.md`.
4. Create deterministic `section_id` values.
5. Preserve source paths back to both Markdown and PDF.
6. Flag table, figure, numeric, and poor-quality Markdown sections.
7. Write `sections.jsonl`, `section_manifest.json`, and
   `section_split_report.md`.
8. Avoid any claim extraction, summary writing, interpretation, or database
   export.

