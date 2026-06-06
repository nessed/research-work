# Split Rules

These rules define the future Markdown section-splitting engine. They are
simple by design.

## Core Rule

The splitter creates source-tagged sections from converted Markdown. It does not
create claims, summaries, interpretations, conclusions, or database-ready facts.

## Page Tracking

- Use existing Markdown page markers for page tracking.
- Expected marker format:

```markdown
<!-- page N -->
```

- Each section must record `start_page` and `end_page`.
- If a section crosses page markers, preserve the full page span.
- If page markers are missing or malformed, flag the issue in the split report.

## Heading Boundaries

- Use Markdown headings as primary section boundaries.
- Preserve the nearest heading text in `heading_text`.
- If a file has weak or inconsistent headings, use the best local heading and
  flag the case in `markdown_quality_flags`.

## Long Sections

- Split very long sections into paragraph blocks.
- Paragraph-block splitting should preserve paragraph order.
- A paragraph block must not combine unrelated headings.
- A paragraph block must keep the same source page tracking rules.

## Tables, Figures, And Numeric Text

- Keep table, figure, chart-adjacent, and numeric-heavy text when it appears in
  Markdown.
- Do not certify table, chart, figure, or numeric accuracy from Markdown.
- Set `numeric_or_table_sensitive: true` for sections containing exact numbers,
  tables, chart text, rankings, totals, percentages, or figure/table captions.
- Add relevant `markdown_quality_flags`, such as `table_layout_noise`,
  `figure_text`, `broken_words`, `page_order_noise`, or
  `omitted_picture_placeholder`.

## No Interpretation

- Do not summarize.
- Do not paraphrase.
- Do not infer missing headings.
- Do not classify claims.
- Do not extract cause-effect, policy, risk, outlook, or sentiment claims.
- Do not normalize entities.
- Do not create database/table exports.

## Determinism

- The same input folder and same rules should produce the same section IDs,
  section order, page spans, and counts.
- Section IDs must be stable within a run and unique across that run.
