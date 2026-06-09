# Section Split Report

## Summary

- Generated UTC: `2026-06-08T18:22:58+00:00`
- Overall status: `PASS`
- Source year: `2022-23`
- Source PDF-to-MD run: `agentic/02_pdf_to_md/runs/2022-23_pymupdf4llm_hardened`
- Source Markdown files: `24`
- Markdown files with sections: `24`
- Excluded Markdown files: `5`
- Sections written: `2239`
- Numeric/table-sensitive sections: `2137`
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

- Section type counts: `{'heading_section': 916, 'paragraph_block': 420, 'table_or_figure_adjacent': 903}`
- Markdown quality flag counts: `{'broken_words': 87, 'encoding_artifact': 6, 'figure_text': 34, 'none': 442, 'numeric_dense_text': 1487, 'omitted_picture_placeholder': 311, 'table_layout_noise': 881}`

## Excluded Inputs

- `agentic/02_pdf_to_md/runs/2022-23_pymupdf4llm_hardened/converted_md/Supplement_2017_18.md`: prior-year supplement file in 2022-23 folder
- `agentic/02_pdf_to_md/runs/2022-23_pymupdf4llm_hardened/converted_md/Supplement_2018_19.md`: prior-year supplement file in 2022-23 folder
- `agentic/02_pdf_to_md/runs/2022-23_pymupdf4llm_hardened/converted_md/Supplement_2019_20.md`: prior-year supplement file in 2022-23 folder
- `agentic/02_pdf_to_md/runs/2022-23_pymupdf4llm_hardened/converted_md/Supplement_2020_21.md`: prior-year supplement file in 2022-23 folder
- `agentic/02_pdf_to_md/runs/2022-23_pymupdf4llm_hardened/converted_md/Supplement_2021_22.md`: prior-year supplement file in 2022-23 folder

## Issues

- None.

## Research Use Limits

Sections are source-tagged Markdown text units only. They are not claims,
summaries, interpretations, conclusions, or database-ready facts. Any
table, chart, numeric, ranking, total, or footnote content remains
uncertified until separately checked against the source PDF.
