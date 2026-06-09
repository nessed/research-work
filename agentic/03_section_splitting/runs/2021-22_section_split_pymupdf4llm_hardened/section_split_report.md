# Section Split Report

## Summary

- Generated UTC: `2026-06-08T18:19:02+00:00`
- Overall status: `PASS`
- Source year: `2021-22`
- Source PDF-to-MD run: `agentic/02_pdf_to_md/runs/2021-22_pymupdf4llm_hardened`
- Source Markdown files: `23`
- Markdown files with sections: `23`
- Excluded Markdown files: `5`
- Sections written: `1061`
- Numeric/table-sensitive sections: `1061`
- Forbidden claim/summary fields present: `False`

## QA Checks

- Unique `section_id`: `PASS`
- Valid `source_year`: checked for every section.
- Valid `source_md_path`: checked against the PDF-to-MD manifest.
- Valid `source_pdf_path`: checked against the PDF-to-MD manifest.
- Valid `start_page`/`end_page`: checked against source PDF page counts.
- `heading_text` and `sector`: required and preserved where available.
- `numeric_or_table_sensitive`: boolean required for every section.
- `markdown_quality_flags`: non-empty list required for every section.
- No claim, summary, interpretation, outlook, risk, sentiment, or policy-action fields are allowed.

## Counts

- Section type counts: `{'heading_section': 1, 'paragraph_block': 514, 'table_or_figure_adjacent': 546}`
- Markdown quality flag counts: `{'broken_words': 261, 'figure_text': 28, 'none': 21, 'numeric_dense_text': 1040, 'table_layout_noise': 538}`

## Excluded Inputs

- `agentic/02_pdf_to_md/runs/2021-22_pymupdf4llm_hardened/converted_md/Highlights.md`: empty Markdown output due to image-only PDF; excluded to pass QA checks
- `agentic/02_pdf_to_md/runs/2021-22_pymupdf4llm_hardened/converted_md/Supplement_2017_18.md`: prior-year supplement file in 2021-22 folder
- `agentic/02_pdf_to_md/runs/2021-22_pymupdf4llm_hardened/converted_md/Supplement_2018_19.md`: prior-year supplement file in 2021-22 folder
- `agentic/02_pdf_to_md/runs/2021-22_pymupdf4llm_hardened/converted_md/Supplement_2019_20.md`: prior-year supplement file in 2021-22 folder
- `agentic/02_pdf_to_md/runs/2021-22_pymupdf4llm_hardened/converted_md/Supplement_2020_21.md`: prior-year supplement file in 2021-22 folder

## Issues

- None.

## Research Use Limits

Sections are source-tagged Markdown text units only. They are not claims,
summaries, interpretations, conclusions, or database-ready facts. Any
table, chart, numeric, ranking, total, or footnote content remains
uncertified until separately checked against the source PDF.
