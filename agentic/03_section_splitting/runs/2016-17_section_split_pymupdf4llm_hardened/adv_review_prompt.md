# Adversarial Review Prompt

You are a fresh-context read-only adversarial reviewer for the PES `2016-17`
section split run.

## Review Inputs

- Section run:
  `agentic/03_section_splitting/runs/2016-17_section_split_pymupdf4llm_hardened`
- Source PDF-to-MD run:
  `agentic/02_pdf_to_md/runs/2016-17_pymupdf4llm_hardened`
- Source Markdown:
  `agentic/02_pdf_to_md/runs/2016-17_pymupdf4llm_hardened/converted_md`
- Source PDFs:
  `datalab_master/Master Data/pakistan_economic_survey/2016-17`

## Questions

1. Does every section have a unique `section_id`?
2. Is `source_year` always `2016-17`?
3. Does every `source_md_path` point to the reviewed converted Markdown run?
4. Does every `source_pdf_path` point to the original 2016-17 PDFs?
5. Are `start_page` and `end_page` valid against source PDF page counts?
6. Are `heading_text` and `sector` preserved where available, with reasonable
   fallback where Markdown headings are weak?
7. Are `numeric_or_table_sensitive` and `markdown_quality_flags` populated?
8. Did the run avoid creating claims, summaries, interpretations, conclusions,
   normalized facts, or database/table exports?
9. Can sampled sections be traced back to the exact source Markdown text and
   page marker?
10. Does the review avoid trusting Markdown tables/charts/numeric values as
    source truth?

## Expected Output

Write findings ordered by severity. Include a PASS/FAIL summary, concrete
evidence checked, residual risks, and whether the run is acceptable as a
source-tagged section layer for later, separately approved extraction work.
