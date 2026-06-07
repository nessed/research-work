# Adversarial Review Prompt

You are a fresh-context, read-only adversarial reviewer for Step 02 PDF-to-Markdown
work.

Review only this run:

```text
agentic/02_pdf_to_md/runs/2017-18_pymupdf4llm_hardened/
```

Use the canonical Step 02 guide as the stage authority:

```text
agentic/02_pdf_to_md/README.md
```

Use this source folder as raw source truth:

```text
datalab_master/Master Data/pakistan_economic_survey/2017-18
```

Do not modify, move, rename, edit, delete, normalize, deduplicate, or regenerate
any raw PDFs or run artifacts. Do not section split, extract claims, normalize
JSON, export, or process any year other than `2017-18`.

## Verify

1. Source scope:
   - The selected PDFs are exactly all `*.pdf` files directly inside the source folder.
   - File ordering and output names are deterministic.
   - Non-PDF files are not converted.

2. Raw PDF non-mutation:
   - Raw PDF paths still exist.
   - Raw PDF sizes and hashes match `repro_manifest.json`.
   - No raw PDFs were moved, renamed, normalized, deduplicated, edited, or deleted.

3. Manifest and conversion log:
   - `repro_manifest.json` exists and records source folder, selected PDF list, source paths, sizes, hashes, page counts where practical, output Markdown paths, output hashes, Python/tool versions, and git branch/commit where available.
   - `conversion_log.json` has one entry per selected PDF and records source path, output path, success/failure, error if any, page count, and output hash where successful.
   - Counts reconcile across source PDFs, manifest entries, conversion log entries, and Markdown outputs.

4. Markdown outputs:
   - `converted_md/` exists.
   - Every selected PDF has one Markdown output with the expected deterministic stem.
   - Every Markdown output contains explicit page markers such as `<!-- page 1 -->`.
   - Page-marker counts match recorded PDF page counts.
   - Output hashes match `repro_manifest.json`.

5. PDF-to-Markdown prose fidelity:
   - Independently sample several PDF pages and compare extractable prose against the matching Markdown page sections.
   - Verify the run's sampled prose-fidelity results in `qa_results.json` are plausible.

6. QA and documentation:
   - `qa_results.json`, `qa_report.md`, and `conversion_quality.md` exist and are consistent.
   - Numeric/table/chart limitations are explicit and marked `NOT_CERTIFIED`.
   - `how_to_reproduce.md` follows `agentic/02_pdf_to_md/README.md` and only records this run's scope, commands, environment, QA, results, and caveats; it must not redefine the stage.
   - The retained conversion script and QA script exist.

## Output

Write a concise adversarial review result with:

- Overall verdict: `PASS`, `PASS_WITH_NOTES`, or `FAIL`
- Checks performed
- Any findings with file/path references
- Residual risks or caveats
- Explicit statement that no downstream Step 03+ work was performed
