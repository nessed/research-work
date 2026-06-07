# How To Reproduce

This folder contains the `2018-19` section split run created from the reviewed
PDF-to-Markdown run:

```text
agentic/02_pdf_to_md/runs/2018-19_pymupdf4llm_hardened/
```

## Scope

- Input Markdown:
  `agentic/02_pdf_to_md/runs/2018-19_pymupdf4llm_hardened/converted_md`
- Input provenance:
  `agentic/02_pdf_to_md/runs/2018-19_pymupdf4llm_hardened/repro_manifest.json`
- Output:
  `agentic/03_section_splitting/runs/2018-19_section_split_pymupdf4llm_hardened/sections.jsonl`
- Original PDFs:
  not modified, renamed, moved, or deleted
- Converted Markdown:
  read as input only; not modified
- Scope exclusion:
  `Supplement_2017_18.md`, `Supplement_2019_20.md`,
  `Supplement_2020_21.md`, and `Supplement_2021_22.md` are excluded from
  `sections.jsonl` even though they exist in the reviewed PDF-to-MD folder,
  because their source documents are not `2018-19` and must not be tagged as
  `2018-19` sections.
- Duplicate supplement exclusion:
  `Statistical_Supplement.md` is excluded because it is a duplicate alias of
  `Supplement_2018_19.md` by source and output hash. Raw PDFs remain untouched;
  this is only a section-layer scope decision to avoid duplicate sections.

## Run Command

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" "agentic\03_section_splitting\runs\2018-19_section_split_pymupdf4llm_hardened\split_2018_19_sections.py"
```

The script writes:

- `sections.jsonl`
- `section_manifest.json`
- `section_split_report.md`

## Split Method

- Uses existing `<!-- page N -->` markers for page tracking.
- Excludes non-2018-19 supplement Markdown files and the duplicate statistical
  supplement alias to keep the section layer homogeneous for source year
  `2018-19`.
- Splits on Markdown headings within each page where available.
- Uses paragraph-block fallback for long or weakly headed text.
- Preserves source Markdown text without summarizing or interpreting it.
- Adds source year, source Markdown path, source PDF path, sector, heading,
  page span, section type, numeric/table sensitivity flag, and Markdown quality
  flags.

## QA

The run script validates:

- unique `section_id`
- valid `source_year`
- valid `source_md_path`
- valid `source_pdf_path`
- valid `start_page` and `end_page`
- present `heading_text` and `sector`
- boolean `numeric_or_table_sensitive`
- present `markdown_quality_flags`
- no claim, summary, interpretation, policy-action, risk, outlook, or
  sentiment fields

## Run Result

- Included source Markdown files: rerun output recorded in `section_manifest.json`
- Excluded Markdown files: rerun output recorded in `section_manifest.json`
- Sections written: rerun output recorded in `section_manifest.json`
- QA status: `PASS`
- Numeric/table-sensitive sections: `3454`

## Research Use Policy

Sections are source-tagged Markdown text units only. They are not claims,
summaries, interpretations, conclusions, or database-ready facts. Tables,
charts, numbers, rankings, totals, and footnotes remain uncertified until
separately checked against the original source PDFs.
