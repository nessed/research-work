# Conversion Quality

## Run Reviewed

- Input folder:
  `C:\Users\Ali\Desktop\datalab_ali\datalab_master\Master Data\pakistan_economic_survey\2015-16`
- Output folder:
  `C:\Users\Ali\Desktop\datalab_ali\processed_pdfs\2015-16_pymupdf4llm`
- Conversion method:
  direct `pymupdf4llm.to_markdown(str(pdf_path), page_chunks=True)`
- Review date:
  2026-06-06

## Structural Checks

PASS.

- PDFs listed in `conversion_log.json`: `29`
- Markdown outputs present: `29`
- Failed log entries: `0`
- Missing Markdown outputs: `0`
- Zero-length Markdown outputs: `0`
- Page-marker mismatches against logged PDF page counts: `0`

Every output Markdown file contains explicit page markers in this form:

```markdown
<!-- page 1 -->
```

The page marker count matched the logged PDF page count for all 29 files.

## PDF-To-Markdown Spot Checks

Selected source PDFs were compared against the generated Markdown using direct
PyMuPDF first-page text extraction and normalized word overlap.

| PDF | Pages | First-page PDF words | First-page MD words | First-page overlap |
| --- | ---: | ---: | ---: | ---: |
| Agriculture.pdf | 41 | 564 | 572 | 100.0% |
| Growth_And_Investment.pdf | 34 | 549 | 556 | 82.2% |
| Economic_Indicators.pdf | 6 | 605 | 901 | 76.0% |
| Research_Team.pdf | 1 | 95 | 133 | 100.0% |
| Supplement_2021_22.pdf | 216 | 29 | 43 | 100.0% |

Interpretation:

- Prose-heavy chapter files look usable for commentary extraction.
- The Markdown retains page-level traceability.
- Some files include image placeholders such as `Picture ... intentionally omitted`.
- Table-heavy files can reorder or reshape text, especially indicator and supplement material.
- Numeric/table values should not be treated as verified source truth from Markdown alone.

## Fit For Current Purpose

PASS for prose/commentary extraction with source-grounded page references.

LIMITED for:

- tables
- numeric values
- chart-derived values
- row/column structure
- exact formatting

For commentary extraction, the generated Markdown can be used as a working text
layer if claims remain grounded to page markers and checked against the original
PDF where needed.

For numeric ingestion or publishable factual claims, use the source PDFs and
separate table QA.

## Artifacts Reviewed

- `conversion_log.json`
- all 29 generated `.md` files
- selected original PDFs for direct first-page text comparison

