# PDF Conversion Pilot Quality Report

## Scope

This report assesses only these generated Markdown files:

- `agentic/02_pdf_to_md/education_2019_20.md`
- `agentic/02_pdf_to_md/transport_2021_22.md`

No other PDFs were processed or inspected.

## Status

**PASS for narrative commentary extraction, with limitations.**

`pymupdf4llm` produced readable Markdown for both pilot PDFs. The output is good enough for later LLM-based extraction of themes, claims, policy actions, and narrative commentary, especially because page boundaries were preserved by the conversion wrapper.

It is **not reliable enough for standalone quantitative table extraction** without a separate table review step.

## Output Summary

| Output | Size | Lines | PDF page markers |
|---|---:|---:|---:|
| `education_2019_20.md` | 62,041 bytes | 690 | 17 |
| `transport_2021_22.md` | 51,172 bytes | 710 | 17 |

## Headings and Subheadings

Headings and subheadings are generally readable. Major chapter titles, section titles, table titles, and box headings are preserved with Markdown heading syntax or bold text.

Some headings are over-promoted to the same level, so hierarchy is not always semantically clean. For commentary extraction this is acceptable because the section boundaries are still visible.

## Paragraph Readability

Paragraph text is mostly readable and follows the original narrative order well enough for LLM use.

Visible issues:

- Some encoding artifacts appear, such as `â€™` and related quote/dash artifacts.
- Some words are split or oddly spaced where the PDF layout was awkward.
- A few page headers and footers remain in the text.
- Image placeholders appear, for example `picture ... intentionally omitted`.

These issues are annoying but do not prevent commentary extraction.

## Page Reference Availability

Page references are available as inserted markers:

- `<!-- source_pdf_page: N -->`
- `## PDF page N`

These are PDF page numbers from `pymupdf4llm` page chunks, not necessarily the printed page numbers shown inside the Economic Survey. The printed page numbers also appear in the extracted text in places, but they should not be treated as the primary locator.

## Table Quality

Tables are mixed.

Good:

- Many tables are represented as Markdown tables.
- Rows and visible values are often present.
- Table titles are usually retained.

Weak:

- Complex multi-row headers are often messy.
- Some table captions or surrounding paragraphs are duplicated inside every table column.
- Line breaks inside cells are frequent.
- Table structure is not reliable enough for direct numeric extraction.
- Some table content may need manual review against the source PDF before use.

## Obvious Extraction Issues

- Mojibake/encoding artifacts in punctuation.
- Image text and image placeholders are imperfectly handled.
- Repeated table-heading text appears in some tables, especially in `transport_2021_22.md`.
- Some words are run together or split unexpectedly, especially around table cells and superscripts.
- Markdown heading levels are useful for navigation but not a clean document outline.

## Recommendation

Use `pymupdf4llm` Markdown for the next commentary-extraction pilot.

For that next step, constrain the LLM to:

- extract narrative claims, policy actions, constraints, and stated causes/effects;
- keep every extracted item tied to the inserted PDF page marker;
- avoid treating table values as authoritative unless separately reviewed;
- flag garbled or ambiguous passages instead of repairing them silently.

Do not use these Markdown files as a final source for published numbers.
