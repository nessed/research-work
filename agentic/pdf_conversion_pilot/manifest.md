# Task Name

pdf_conversion_pilot

## Purpose

Test whether `pymupdf4llm` can convert selected Pakistan Economic Survey PDFs into Markdown that is good enough for later LLM-based commentary extraction.

This is a scoped pilot only. It does not perform commentary extraction, family mapping, database import, or quantitative data extraction.

## Exact Input PDFs

- `C:\Users\Ali\Desktop\datalab_ali\datalab_master\Master Data\pakistan_economic_survey\2019-20\Education.pdf`
- `C:\Users\Ali\Desktop\datalab_ali\datalab_master\Master Data\pakistan_economic_survey\2021-22\Pes13_Transport.pdf`

## Exact Output Files

- `agentic/pdf_conversion_pilot/education_2019_20.md`
- `agentic/pdf_conversion_pilot/transport_2021_22.md`
- `agentic/pdf_conversion_pilot/quality_report.md`
- `agentic/pdf_conversion_pilot/manifest.md`
- `agentic/pdf_conversion_pilot/convert_pdfs.py`

## Environment

Python executable used:

- `C:\Users\Ali\AppData\Local\Python\bin\python.exe`

Python version:

- `3.14.5`

Package versions:

- `pymupdf==1.27.2.3`
- `pymupdf4llm==1.27.2.3`

Installation command used because the packages were initially missing:

```powershell
& 'C:\Users\Ali\AppData\Local\Python\bin\pip.exe' install pymupdf pymupdf4llm
```

## Conversion Method

The conversion was performed with `pymupdf4llm.to_markdown(..., page_chunks=True)` in:

- `agentic/pdf_conversion_pilot/convert_pdfs.py`

The script processes only the two input PDFs listed above. For each page chunk, it writes:

- an HTML comment marker: `<!-- source_pdf_page: N -->`
- a Markdown page heading: `## PDF page N`
- the Markdown text returned by `pymupdf4llm`

Output files are written as UTF-8 Markdown.

## Reproduction Steps

1. Use repository root: `C:\Users\Ali\Desktop\datalab_ali`.
2. Confirm the two input PDFs exist at the exact paths listed above.
3. Confirm Python:

```powershell
& 'C:\Users\Ali\AppData\Local\Python\bin\python.exe' --version
```

4. Confirm packages:

```powershell
& 'C:\Users\Ali\AppData\Local\Python\bin\python.exe' -c "import importlib.metadata as m; import fitz; import pymupdf4llm; print(m.version('pymupdf')); print(m.version('pymupdf4llm'))"
```

5. If missing, install only the required packages:

```powershell
& 'C:\Users\Ali\AppData\Local\Python\bin\pip.exe' install pymupdf pymupdf4llm
```

6. Run the conversion script:

```powershell
& 'C:\Users\Ali\AppData\Local\Python\bin\python.exe' 'agentic\pdf_conversion_pilot\convert_pdfs.py'
```

7. Review:

- `agentic/pdf_conversion_pilot/education_2019_20.md`
- `agentic/pdf_conversion_pilot/transport_2021_22.md`
- `agentic/pdf_conversion_pilot/quality_report.md`

## Validation Performed

- Confirmed both requested source PDFs exist.
- Confirmed both Markdown outputs were generated.
- Confirmed each Markdown output has 17 inserted PDF page markers.
- Spot-checked the beginning and middle of each Markdown output for headings, paragraphs, tables, page markers, and obvious extraction artifacts.
- Confirmed no other PDFs were intentionally processed.

## Limitations

- Quality review is based on the generated Markdown, not a full visual reconciliation against the source PDFs.
- Inserted page markers are PDF page indices from `pymupdf4llm` page chunks; they may differ from printed Economic Survey page numbers.
- Tables are not reliable enough for direct publication-grade numeric extraction.
- Some punctuation appears as mojibake, for example `â€™`.
- Some image text is omitted or represented as placeholders.
- No OCR fallback was attempted.
- No commentary extraction was performed.
- No family mapping was performed.
- No raw PDF was modified.
