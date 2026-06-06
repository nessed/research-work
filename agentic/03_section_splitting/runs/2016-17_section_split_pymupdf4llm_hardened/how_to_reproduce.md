# How To Reproduce

This folder contains the `2016-17` section split run created from the reviewed
PDF-to-Markdown run:

```text
agentic/02_pdf_to_md/runs/2016-17_pymupdf4llm_hardened/
```

## Scope

- Input Markdown:
  `agentic/02_pdf_to_md/runs/2016-17_pymupdf4llm_hardened/converted_md`
- Input provenance:
  `agentic/02_pdf_to_md/runs/2016-17_pymupdf4llm_hardened/repro_manifest.json`
- Output:
  `agentic/03_section_splitting/runs/2016-17_section_split_pymupdf4llm_hardened/sections.jsonl`
- Original PDFs:
  not modified, renamed, moved, or deleted
- Converted Markdown:
  read as input only; not modified
- Scope exclusion:
  later-year supplement files named `Supplement_20*_*.md` are excluded from
  `sections.jsonl` even though they exist in the reviewed PDF-to-MD folder,
  because their source documents are later survey years and must not be tagged
  as `2016-17` sections.

## Run Command

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" "agentic\03_section_splitting\runs\2016-17_section_split_pymupdf4llm_hardened\split_2016_17_sections.py"
```

The script writes:

- `sections.jsonl`
- `section_manifest.json`
- `section_split_report.md`

## Split Method

- Uses existing `<!-- page N -->` markers for page tracking.
- Excludes later-year supplement Markdown files to keep the section layer
  homogeneous for source year `2016-17`.
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

## Research Use Policy

Sections are source-tagged Markdown text units only. They are not claims,
summaries, interpretations, conclusions, or database-ready facts. Tables,
charts, numbers, rankings, totals, and footnotes remain uncertified until
separately checked against the original source PDFs.
