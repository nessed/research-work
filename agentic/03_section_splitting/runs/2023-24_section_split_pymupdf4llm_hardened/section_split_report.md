# Section Split Report

## Summary

- Generated UTC: `2026-06-08T18:32:19+00:00`
- Overall status: `PASS`
- Source year: `2023-24`
- Source PDF-to-MD run: `agentic/02_pdf_to_md/runs/2023-24_pymupdf4llm_hardened`
- Source Markdown files: `24`
- Markdown files with sections: `24`
- Excluded Markdown files: `5`
- Sections written: `2267`
- Numeric/table-sensitive sections: `2235`
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

- Section type counts: `{'heading_section': 815, 'paragraph_block': 515, 'table_or_figure_adjacent': 937}`
- Markdown quality flag counts: `{'broken_words': 53, 'encoding_artifact': 4, 'figure_text': 34, 'none': 383, 'numeric_dense_text': 1617, 'omitted_picture_placeholder': 257, 'table_layout_noise': 919}`

## Excluded Inputs

- `agentic/02_pdf_to_md/runs/2023-24_pymupdf4llm_hardened/converted_md/Supplement_2017_18.md`: prior-year supplement file in 2023-24 folder
- `agentic/02_pdf_to_md/runs/2023-24_pymupdf4llm_hardened/converted_md/Supplement_2018_19.md`: prior-year supplement file in 2023-24 folder
- `agentic/02_pdf_to_md/runs/2023-24_pymupdf4llm_hardened/converted_md/Supplement_2019_20.md`: prior-year supplement file in 2023-24 folder
- `agentic/02_pdf_to_md/runs/2023-24_pymupdf4llm_hardened/converted_md/Supplement_2020_21.md`: prior-year supplement file in 2023-24 folder
- `agentic/02_pdf_to_md/runs/2023-24_pymupdf4llm_hardened/converted_md/Supplement_2021_22.md`: prior-year supplement file in 2023-24 folder

## Issues

- None.

## Research Use Limits

Sections are source-tagged Markdown text units only. They are not claims,
summaries, interpretations, conclusions, or database-ready facts. Any
table, chart, numeric, ranking, total, or footnote content remains
uncertified until separately checked against the source PDF.
