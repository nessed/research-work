# Section Split Report

## Summary

- Generated UTC: `2026-06-07T00:44:14+00:00`
- Overall status: `PASS`
- Source year: `2018-19`
- Source PDF-to-MD run: `agentic/02_pdf_to_md/runs/2018-19_pymupdf4llm_hardened`
- Source Markdown files: `22`
- Markdown files with sections: `22`
- Excluded Markdown files: `5`
- Sections written: `2736`
- Numeric/table-sensitive sections: `2682`
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

- Section type counts: `{'heading_section': 1402, 'paragraph_block': 546, 'table_or_figure_adjacent': 788}`
- Markdown quality flag counts: `{'broken_words': 133, 'figure_text': 14, 'none': 271, 'numeric_dense_text': 1846, 'omitted_picture_placeholder': 1259, 'table_layout_noise': 786}`

## Excluded Inputs

- `agentic/02_pdf_to_md/runs/2018-19_pymupdf4llm_hardened/converted_md/Statistical_Supplement.md`: duplicate alias of Supplement_2018_19.pdf by source and output hash; excluded from sections to avoid duplicate 2018-19 supplement sections
- `agentic/02_pdf_to_md/runs/2018-19_pymupdf4llm_hardened/converted_md/Supplement_2017_18.md`: prior-year supplement file in 2018-19 folder; excluded to keep section layer source_year homogeneous
- `agentic/02_pdf_to_md/runs/2018-19_pymupdf4llm_hardened/converted_md/Supplement_2019_20.md`: later-year supplement file in 2018-19 folder; excluded to keep section layer source_year homogeneous
- `agentic/02_pdf_to_md/runs/2018-19_pymupdf4llm_hardened/converted_md/Supplement_2020_21.md`: later-year supplement file in 2018-19 folder; excluded to keep section layer source_year homogeneous
- `agentic/02_pdf_to_md/runs/2018-19_pymupdf4llm_hardened/converted_md/Supplement_2021_22.md`: later-year supplement file in 2018-19 folder; excluded to keep section layer source_year homogeneous

## Issues

- None.

## Research Use Limits

Sections are source-tagged Markdown text units only. They are not claims,
summaries, interpretations, conclusions, or database-ready facts. Any
table, chart, numeric, ranking, total, or footnote content remains
uncertified until separately checked against the source PDF.
