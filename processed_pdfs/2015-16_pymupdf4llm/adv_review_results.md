# Adversarial Review Results

## Summary

PASS for the requested direct PyMuPDF4LLM conversion comparison run.

The run found 29 PDFs directly inside the `2015-16` input folder and produced
29 Markdown files in the requested output folder. The conversion log records
zero failures. Page markers are present and match logged PDF page counts for all
outputs checked.

This review does not certify table or numeric fidelity.

## Checks Performed

- Confirmed `conversion_log.json` contains `29` entries.
- Confirmed all `29` log entries have `"success": true`.
- Confirmed no failed entries are present.
- Confirmed all logged Markdown output paths exist.
- Confirmed no generated Markdown output has zero length.
- Counted `<!-- page ... -->` markers in each Markdown file.
- Compared marker counts against logged PDF page counts.
- Spot-checked selected source PDFs against generated Markdown using direct
  PyMuPDF first-page extraction.

## Findings

### High Severity

None.

### Medium Severity

Table-heavy files remain risky for direct numeric/table use.

Evidence:

- `Economic_Indicators.pdf` first-page normalized overlap was lower than
  prose-heavy chapters, and the Markdown word count was higher than the direct
  first-page PDF extraction.
- Statistical supplement files are large and table-heavy. PyMuPDF4LLM Markdown
  is not enough to guarantee row/column fidelity.

Impact:

- Do not use these Markdown files as trusted numeric source material.
- Any table values, chart values, or exact figures need separate source-PDF QA.

### Low Severity

Some Markdown includes image placeholder text.

Example pattern:

```text
Picture ... intentionally omitted
```

Impact:

- This is acceptable for prose extraction.
- It may add noise to automated extraction and should be filtered or handled in
  later extraction prompts/scripts.

## Structural Result

| Check | Result |
| --- | --- |
| PDFs found | 29 |
| Markdown outputs | 29 |
| Logged failures | 0 |
| Missing outputs | 0 |
| Zero-length outputs | 0 |
| Page-marker mismatches | 0 |

## Spot-Check Result

| PDF | Pages | First-page overlap |
| --- | ---: | ---: |
| Agriculture.pdf | 41 | 100.0% |
| Growth_And_Investment.pdf | 34 | 82.2% |
| Economic_Indicators.pdf | 6 | 76.0% |
| Research_Team.pdf | 1 | 100.0% |
| Supplement_2021_22.pdf | 216 | 100.0% |

The spot checks support the conclusion that prose is generally preserved well
enough for commentary extraction, but table-heavy content still requires
separate validation.

## Reproducibility Review

PASS with one caveat.

The run now includes `how_to_reproduce.md`, which records:

- source and output folders
- branch at run time
- PyMuPDF4LLM and PyMuPDF versions
- the direct API call used
- the page marker format
- equivalent one-off script code
- final run counts

Caveat:

- The actual one-off script used during the run was removed after execution, so
  reproducibility depends on the equivalent script embedded in
  `how_to_reproduce.md` rather than a retained executable script file.

## Original PDF Safety

No evidence suggests that original PDFs were modified. The conversion and review
steps read from:

```text
datalab_master\Master Data\pakistan_economic_survey\2015-16
```

and wrote artifacts only to:

```text
processed_pdfs\2015-16_pymupdf4llm
```

## Final Assessment

Accept this run as a direct PyMuPDF4LLM comparison artifact for
commentary/prose extraction.

Do not use it as a numeric ingestion source or as source truth for tables.

