# Conversion Quality

## Summary

- Run: `2020-21_pymupdf4llm_hardened`
- Overall status: `PASS`
- Source folder: `datalab_master/Master Data/pakistan_economic_survey/2020-21`
- Selected PDFs: `29` direct `*.pdf` files, sorted case-insensitively by filename
- Converted Markdown files: `29`
- Failed conversions: `0`
- Structural QA: `PASS`
- Prose fidelity QA: `PASS`
- Table/chart/numeric certification: `NOT_CERTIFIED`

## Conversion Method

The retained converter writes one Markdown file per selected source PDF under
`converted_md/`, with explicit page markers such as:

```markdown
<!-- page 1 -->
```

For this run, all selected PDFs were converted with PyMuPDF plain text
extraction as a hardened fallback. PyMuPDF4LLM did not complete reliably within
bounded runtime for the large combined PDF and table-heavy annex/supplement
files before final manifest/log creation.

## Page Marker Result

QA found:

- Page-marker mismatches: `0`
- Missing outputs: `0`
- Zero-byte outputs: `0`
- Output hash mismatches: `0`

Every converted Markdown file has page markers matching the source PDF page
count recorded in `repro_manifest.json`.

## Prose Fidelity Sampling

The QA script sampled one extractable prose page per selected PDF using seed
`20260607` and compared PDF text tokens to the corresponding Markdown page.

- Sample count: `29`
- PASS samples: `29`
- FAIL samples: `0`

This supports use of the Markdown as working prose text for later commentary
work, subject to the limitations below.

## NOT_CERTIFIED Content

Markdown tables, chart text, numeric values, row/column structure, rankings,
totals, and footnotes are `NOT_CERTIFIED`.

Any numeric, table-derived, chart-derived, ranking, total, or footnote claim
must be separately QA'd against the original source PDF before research use.

## Known Limitations

- Original PDFs remain the source truth.
- Markdown is working text only.
- PyMuPDF text extraction does not certify table layout or chart/image content.
- Prose token overlap is a sampled QA check, not a full manual page-by-page
  proofread.
- The selected direct-folder PDFs include cross-year supplement files
  (`Supplement_2017_18.pdf`, `Supplement_2018_19.pdf`,
  `Supplement_2019_20.pdf`, and `Supplement_2021_22.pdf`) because they are
  direct PDFs in the `2020-21` source folder. Downstream stages must exclude
  or separately label them if the intended source-year scope is strict
  `2020-21` commentary only.
- The run intentionally stops after Step 02; no section splitting, claim
  extraction, JSON normalization, export, or downstream processing was done.
