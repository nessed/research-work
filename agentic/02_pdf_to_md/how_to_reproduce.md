# 02_pdf_to_md Reproduction Notes

## Purpose

Run a reproducible 6-PDF cross-year pilot to test whether `pymupdf4llm` produces Markdown suitable for later commentary-focused extraction from Pakistan Economic Survey Education and Transport chapters.

This run does not perform commentary extraction, table/numeric extraction, database import, or any modification of raw source PDFs.

## Source Inputs

Project root:

- `C:\Users\Ali\Desktop\datalab_ali`

Raw PDF source root:

- `datalab_master/Master Data/pakistan_economic_survey/`

Folder map used for selection:

- `agentic/01_pes_folder_map/pes_folder_tree.json`

Selection was made from the JSON map first, then every chosen source PDF was verified to exist under the raw source root.

## Run Folder

Run folder:

- `agentic/02_pdf_to_md/runs/2026-06-05_6pdf_cross_year_pilot/`

Batch manifest:

- `agentic/02_pdf_to_md/runs/2026-06-05_6pdf_cross_year_pilot/selected_pdf_map.json`

Batch outputs:

- `agentic/02_pdf_to_md/runs/2026-06-05_6pdf_cross_year_pilot/converted_md/<year>/<sector>.md`

If the base run folder already exists, `convert_pdfs.py` creates the next available suffix such as `_v2` instead of overwriting it.

## Random Seed

Seed:

- `20260605`

Selection rule implemented:

- choose 3 Education PDFs from 3 random years;
- choose 3 Transport PDFs from 3 random years;
- enforce distinct years across all 6 selected PDFs;
- use candidates discovered in `pes_folder_tree.json`;
- verify selected source PDFs exist under the raw PES source root.

## Selected PDFs and Outputs

| Sector | Year | Source PDF | Output Markdown |
|---|---|---|---|
| Education | 2017-18 | `datalab_master/Master Data/pakistan_economic_survey/2017-18/Education.pdf` | `agentic/02_pdf_to_md/runs/2026-06-05_6pdf_cross_year_pilot/converted_md/2017-18/education.md` |
| Education | 2019-20 | `datalab_master/Master Data/pakistan_economic_survey/2019-20/Education.pdf` | `agentic/02_pdf_to_md/runs/2026-06-05_6pdf_cross_year_pilot/converted_md/2019-20/education.md` |
| Education | 2023-24 | `datalab_master/Master Data/pakistan_economic_survey/2023-24/Education.pdf` | `agentic/02_pdf_to_md/runs/2026-06-05_6pdf_cross_year_pilot/converted_md/2023-24/education.md` |
| Transport | 2015-16 | `datalab_master/Master Data/pakistan_economic_survey/2015-16/Transport.pdf` | `agentic/02_pdf_to_md/runs/2026-06-05_6pdf_cross_year_pilot/converted_md/2015-16/transport.md` |
| Transport | 2016-17 | `datalab_master/Master Data/pakistan_economic_survey/2016-17/Transport_And_Communications.pdf` | `agentic/02_pdf_to_md/runs/2026-06-05_6pdf_cross_year_pilot/converted_md/2016-17/transport.md` |
| Transport | 2024-25 | `datalab_master/Master Data/pakistan_economic_survey/2024-25/Transport_And_Communication.pdf` | `agentic/02_pdf_to_md/runs/2026-06-05_6pdf_cross_year_pilot/converted_md/2024-25/transport.md` |

## Environment

Python executable used:

- `C:\Users\Ali\AppData\Local\Python\bin\python.exe`

Python version:

- `3.14.5`

Package versions:

- `pymupdf==1.27.2.3`
- `pymupdf4llm==1.27.2.3`

Version check command:

```powershell
& 'C:\Users\Ali\AppData\Local\Python\bin\python.exe' -c "import importlib.metadata as m; import fitz; import pymupdf4llm; print(m.version('pymupdf')); print(m.version('pymupdf4llm'))"
```

## Conversion Command

Run from project root:

```powershell
& 'C:\Users\Ali\AppData\Local\Python\bin\python.exe' 'agentic\02_pdf_to_md\convert_pdfs.py'
```

The script writes:

- `selected_pdf_map.json`
- six Markdown files under `converted_md/<year>/<sector>.md`

## Conversion Method

The conversion uses:

- `pymupdf4llm.to_markdown(str(input_pdf), page_chunks=True)`

For each returned page chunk, the wrapper writes:

- `<!-- source_pdf_page: N -->`
- `## PDF page N`
- the Markdown text returned by `pymupdf4llm`

This preserves PDF page boundaries for later source-grounded commentary extraction.

## Limitations

- PDF page markers are PDF page indices from the conversion chunks, not necessarily printed Economic Survey page numbers.
- Tables and charts are not trusted for numeric extraction from Markdown.
- Some layout-derived tables are noisy or missing as Markdown tables.
- Some image-only or infographic content appears as omitted-picture placeholders.
- Some punctuation has encoding artifacts such as `â€™`.
- No OCR fallback was attempted.
- No visual page-by-page reconciliation against the original PDFs was performed.
- The original PDFs remain source truth.
