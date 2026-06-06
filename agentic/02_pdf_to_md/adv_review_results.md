# Adversarial Review Results — 6-PDF Cross-Year PDF-to-MD Pilot

## Verdict

CONDITIONAL PASS

## What Was Checked

- Read `PROJECT_CONTEXT.md`, `adv_review_prompt.md`, `how_to_reproduce.md`, `conversion_quality.md`, and the run `selected_pdf_map.json`.
- Verified the six selected source PDFs exist under `datalab_master/Master Data/pakistan_economic_survey/`.
- Verified the selected PDFs are present in `agentic/01_pes_folder_map/pes_folder_tree.json`.
- Verified exactly six Markdown files exist under `runs/2026-06-05_6pdf_cross_year_pilot/converted_md/`, and they match the six manifest outputs.
- Checked page markers, heading/prose readability, table/chart handling, placeholders, and obvious conversion artifacts.

## Findings

- Source PDFs exist for all six selected entries.
- Converted Markdown outputs exist for all six selected entries:
  - `2017-18/education.md`
  - `2019-20/education.md`
  - `2023-24/education.md`
  - `2015-16/transport.md`
  - `2016-17/transport.md`
  - `2024-25/transport.md`
- No extra Markdown files were found in the run `converted_md/` folder.
- Page markers are present in every file as both `<!-- source_pdf_page: N -->` and `## PDF page N`.
- Marker counts match manifest/source page counts for all six files: 11, 17, 21, 32, 26, and 26 pages respectively.
- Narrative headings and prose are generally readable enough for later commentary extraction with page references.

## Issues / Risks

- Tables and charts are weak zones. Several files contain noisy Markdown table blocks, while `2024-25/transport.md` has zero Markdown table rows despite containing table/chart-like material flattened into picture text.
- Picture placeholders are common, especially `2024-25/transport.md` with many omitted-picture markers. Some chart/table text is flattened into hard-to-trust text runs.
- Heading hierarchy is not clean. Some repeated running headers and prose fragments are promoted to headings.
- Some layout ordering around boxes, charts, and dense tables is unreliable.
- Converted Markdown should not be treated as source truth for numeric values, tables, charts, or final evidence.

## Reproducibility Check

- `selected_pdf_map.json` records seed `20260605`, source root, JSON map, selected PDFs, source page counts, converted chunks, and output paths.
- `convert_pdfs.py` uses `pes_folder_tree.json`, seeded random selection, distinct selected years, source existence checks, and page-chunk conversion.
- `how_to_reproduce.md` is sufficient to rerun the pilot, assuming the stated Python executable and packages are available.
- The run stayed inside `agentic/02_pdf_to_md/runs/2026-06-05_6pdf_cross_year_pilot/`.
- No `agentic/03_*` folder was found.

## Scaling Judgment

This pilot supports scaling Step 2 beyond six PDFs for commentary-focused Markdown conversion only. It does not support scaling numeric/table extraction from the converted Markdown.

Scaling is defensible if every larger batch keeps automated checks for: selected-source existence, exact output count, no extra converted files, page-marker count matching source page count, and explicit table/chart distrust.

## Required Fixes Before Scaling

- Add or run a post-conversion QA check for every batch that verifies source existence, output existence, exact selected-vs-produced file match, and page-marker counts.
- Keep table/chart/numeric extraction out of Step 2 outputs unless a separate table QA workflow is created.
- Preserve page markers in all future conversion runs.
- Record conversion quality notes per larger batch, especially for image-heavy current-year chapters.

## Final Recommendation

Proceed to a larger Step 2 conversion batch only under the commentary-extraction scope. Use the Markdown for readable narrative, headings, and page-anchored source navigation. Do not use it as final evidence for tables, charts, or numeric claims; those must be checked against the original PDFs or a separate extraction workflow.
