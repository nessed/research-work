# How To Reproduce

This is the run-level reproducibility file for the `2015-16` PyMuPDF4LLM
PDF-to-Markdown conversion. The canonical stage rules live in
`agentic/02_pdf_to_md/README.md`; this file only records this run's scope,
commands, environment, QA, and result.

## Scope

- Input folder:
  `datalab_master/Master Data/pakistan_economic_survey/2015-16`
- Output folder:
  `agentic/02_pdf_to_md/runs/2015-16_pymupdf4llm_hardened/converted_md`
- PDFs selected:
  all `*.pdf` files directly inside the input folder, sorted by filename
- Non-PDF files:
  `manifest.csv` is used for provenance; `Statistical_Supplement.zip` is not
  converted
- Original PDFs:
  not modified, renamed, moved, or deleted

## Environment Observed

- Python: recorded in `repro_manifest.json`
- PyMuPDF: recorded in `repro_manifest.json`
- PyMuPDF4LLM: recorded in `repro_manifest.json`
- Git branch/commit, when available: recorded in `repro_manifest.json`

## Conversion Method

The retained conversion script is:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" "agentic\02_pdf_to_md\runs\2015-16_pymupdf4llm_hardened\convert_2015_16_pymupdf4llm.py"
```

It calls:

```python
pymupdf4llm.to_markdown(str(pdf_path), page_chunks=True)
```

Each Markdown page chunk is written with explicit source PDF page markers:

```markdown
<!-- page 1 -->
```

For bounded audit runs where Markdown already exists, regenerate hashes,
manifest, and logs without reconverting:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" "agentic\02_pdf_to_md\runs\2015-16_pymupdf4llm_hardened\convert_2015_16_pymupdf4llm.py" --reuse-existing
```

## Headless QA

Run:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" "agentic\02_pdf_to_md\runs\2015-16_pymupdf4llm_hardened\qa_2015_16_pymupdf4llm.py"
```

The QA script writes:

- `qa_results.json`
- `qa_report.md`

The script exits nonzero if structural checks fail or deterministic prose
fidelity sampling fails.

## Run Result

- PDFs found: `29`
- PDFs converted/logged: `29`
- Failed conversions: `0`
- Structural QA: `PASS`
- Deterministic prose fidelity QA: `PASS`
- Table/chart/numeric fidelity: `NOT_CERTIFIED`

## Research Use Policy

Follow `agentic/02_pdf_to_md/README.md`. Markdown is working text only; original
PDFs remain source truth, and table/chart/numeric claims require separate PDF
QA.
