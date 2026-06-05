# 6-PDF Cross-Year Conversion Quality Report

## Scope

This report reviews only:

- `agentic/02_pdf_to_md/runs/2026-06-05_6pdf_cross_year_pilot/`

It evaluates whether `pymupdf4llm` Markdown is usable for commentary-focused LLM work. It does not validate tables, chart values, or numeric series for database use.

## Selected PDFs

| Sector | Year | Source PDF | Output Markdown |
|---|---|---|---|
| Education | 2017-18 | `datalab_master/Master Data/pakistan_economic_survey/2017-18/Education.pdf` | `converted_md/2017-18/education.md` |
| Education | 2019-20 | `datalab_master/Master Data/pakistan_economic_survey/2019-20/Education.pdf` | `converted_md/2019-20/education.md` |
| Education | 2023-24 | `datalab_master/Master Data/pakistan_economic_survey/2023-24/Education.pdf` | `converted_md/2023-24/education.md` |
| Transport | 2015-16 | `datalab_master/Master Data/pakistan_economic_survey/2015-16/Transport.pdf` | `converted_md/2015-16/transport.md` |
| Transport | 2016-17 | `datalab_master/Master Data/pakistan_economic_survey/2016-17/Transport_And_Communications.pdf` | `converted_md/2016-17/transport.md` |
| Transport | 2024-25 | `datalab_master/Master Data/pakistan_economic_survey/2024-25/Transport_And_Communication.pdf` | `converted_md/2024-25/transport.md` |

## Output Statistics

| Output | Bytes | Lines | Page markers | Source pages | Markdown table lines | Encoding/artifact hits |
|---|---:|---:|---:|---:|---:|---:|
| `converted_md/2015-16/transport.md` | 106,897 | 1,455 | 32 | 32 | 391 | 43 |
| `converted_md/2016-17/transport.md` | 90,878 | 1,365 | 26 | 26 | 298 | 57 |
| `converted_md/2017-18/education.md` | 42,370 | 431 | 11 | 11 | 113 | 17 |
| `converted_md/2019-20/education.md` | 62,041 | 691 | 17 | 17 | 187 | 4 |
| `converted_md/2023-24/education.md` | 85,458 | 917 | 21 | 21 | 258 | 51 |
| `converted_md/2024-25/transport.md` | 66,035 | 770 | 26 | 26 | 0 | 42 |

Page markers are present as:

- `<!-- source_pdf_page: N -->`
- `## PDF page N`

For all six outputs, the number of inserted page markers matches the source PDF page count recorded in `selected_pdf_map.json`.

## Prose and Headings Readability

Overall narrative prose is readable enough for later extraction of policy commentary, sector narratives, constraints, risks, stated causes/effects, and outlooks.

Positive signs:

- Major chapter headings and section headings usually survive.
- Paragraph order is generally coherent on narrative pages.
- Page boundaries are explicit and stable.
- Bullets and many subheadings are preserved well enough for navigation.

Observed weaknesses:

- Heading hierarchy is not always semantically clean.
- Some tables are promoted into large noisy Markdown blocks.
- Some text appears out of ideal order around boxes, infographics, and dense tables.
- Some punctuation has mojibake, especially `â€™`.
- Some image content is omitted with placeholders.
- The 2024-25 Transport output has readable prose but no Markdown table lines, suggesting tables or infographic-like elements were not represented as Markdown tables.

## Tables and Charts

Tables and charts are not trusted from this conversion.

Usable for commentary:

- Table titles and nearby narrative often provide useful context.
- Some tables can help identify topics that need manual source checking.

Not safe for extraction:

- Numeric cells may be misaligned.
- Multi-row headers are noisy.
- Layout boxes can duplicate surrounding prose into table cells.
- Infographic/chart content may be omitted or flattened.
- Some output has no Markdown table representation despite containing transport-sector quantitative material.

Any table or chart value used later must be verified against the original PDF or a separate table extraction workflow.

## Obvious Issues by File

| Output | Main issues |
|---|---|
| `2017-18/education.md` | First page SDG box creates a noisy Markdown table with duplicated surrounding prose; prose after the box is readable. |
| `2019-20/education.md` | Similar to the prior two-PDF pilot; prose is readable, page markers complete, table quality mixed. |
| `2023-24/education.md` | Good narrative readability, but visible punctuation mojibake and occasional odd heading conversion. |
| `2015-16/transport.md` | Dense table sections create many table lines; prose appears usable but table content needs distrust. |
| `2016-17/transport.md` | Similar dense table/layout noise; narrative sections remain usable. |
| `2024-25/transport.md` | Strong prose readability after the infographic opening, but picture placeholders and no Markdown table lines indicate weak table/chart capture. |

## Verdict

**CONDITIONAL PASS**

`pymupdf4llm` is consistent enough across this six-PDF cross-year pilot for commentary-focused Markdown, provided the next extraction step is constrained to narrative claims and keeps page markers attached.

Do not use this Markdown as source truth for numeric claims, table extraction, chart extraction, or publication-grade evidence. The original PDFs remain the authoritative sources.
