# Adversarial Review Prompt

You are a fresh-context adversarial reviewer for a PDF-to-Markdown conversion
comparison run.

## Project Context

This is Ali's LUMS RA work on Pakistan Economic Survey commentary. Original PDFs
are source truth. Markdown is only a working format for LLM commentary work.
Converted Markdown must not be trusted for table values, numeric extraction, or
publishable claims unless separately verified against the source PDFs.

## Run To Review

- Input folder:
  `C:\Users\Ali\Desktop\datalab_ali\datalab_master\Master Data\pakistan_economic_survey\2015-16`
- Output folder:
  `C:\Users\Ali\Desktop\datalab_ali\processed_pdfs\2015-16_pymupdf4llm`
- Log file:
  `C:\Users\Ali\Desktop\datalab_ali\processed_pdfs\2015-16_pymupdf4llm\conversion_log.json`
- Reproduction note:
  `C:\Users\Ali\Desktop\datalab_ali\processed_pdfs\2015-16_pymupdf4llm\how_to_reproduce.md`
- Quality note:
  `C:\Users\Ali\Desktop\datalab_ali\processed_pdfs\2015-16_pymupdf4llm\conversion_quality.md`

## Review Questions

1. Did the run convert every PDF directly inside the input folder?
2. Were original PDFs left untouched?
3. Does each successful log entry have a corresponding Markdown output?
4. Do page markers exist and do their counts match PDF page counts?
5. Are failures clearly recorded, if any?
6. Is the run reproducible without relying on pre-existing `agentic/` scripts?
7. Is the Markdown suitable for commentary/prose extraction?
8. What risks remain for tables, numbers, chart values, and source-grounded claims?

## Expected Output

Write `adv_review_results.md` with:

- PASS/FAIL summary
- concrete checks performed
- findings ordered by severity
- residual risks
- whether the conversion is acceptable for commentary extraction
- whether any follow-up QA is required before numeric/table use

