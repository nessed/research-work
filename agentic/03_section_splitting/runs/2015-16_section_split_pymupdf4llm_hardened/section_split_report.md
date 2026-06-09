# Section Split Report

## Summary

- Generated UTC: `2026-06-08T18:00:05+00:00`
- Overall status: `PASS`
- Source year: `2015-16`
- Source PDF-to-MD run: `agentic/02_pdf_to_md/runs/2015-16_pymupdf4llm_hardened`
- Source Markdown files: `24`
- Markdown files with sections: `24`
- Excluded Markdown files: `5`
- Sections written: `1157`
- Numeric/table-sensitive sections: `1134`
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

- Section type counts: `{'heading_section': 566, 'paragraph_block': 128, 'table_or_figure_adjacent': 463}`
- Markdown quality flag counts: `{'broken_words': 34, 'encoding_artifact': 16, 'figure_text': 12, 'none': 177, 'numeric_dense_text': 864, 'omitted_picture_placeholder': 136, 'table_layout_noise': 459}`

## Excluded Inputs

- `agentic/02_pdf_to_md/runs/2015-16_pymupdf4llm_hardened/converted_md/Supplement_2017_18.md`: later-year supplement file in 2015-16 folder; excluded to keep section layer source_year homogeneous
- `agentic/02_pdf_to_md/runs/2015-16_pymupdf4llm_hardened/converted_md/Supplement_2018_19.md`: later-year supplement file in 2015-16 folder; excluded to keep section layer source_year homogeneous
- `agentic/02_pdf_to_md/runs/2015-16_pymupdf4llm_hardened/converted_md/Supplement_2019_20.md`: later-year supplement file in 2015-16 folder; excluded to keep section layer source_year homogeneous
- `agentic/02_pdf_to_md/runs/2015-16_pymupdf4llm_hardened/converted_md/Supplement_2020_21.md`: later-year supplement file in 2015-16 folder; excluded to keep section layer source_year homogeneous
- `agentic/02_pdf_to_md/runs/2015-16_pymupdf4llm_hardened/converted_md/Supplement_2021_22.md`: later-year supplement file in 2015-16 folder; excluded to keep section layer source_year homogeneous

## Issues

- None.

## Research Use Limits

Sections are source-tagged Markdown text units only. They are not claims,
summaries, interpretations, conclusions, or database-ready facts. Any
table, chart, numeric, ranking, total, or footnote content remains
uncertified until separately checked against the source PDF.
