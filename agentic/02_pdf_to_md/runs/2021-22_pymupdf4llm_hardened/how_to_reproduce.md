# How To Reproduce

This is the run-level reproducibility file for the `2021-22` PDF-to-Markdown
conversion. The canonical stage rules live in `agentic/02_pdf_to_md/README.md`;
this file only records this run's scope, commands, environment, QA, and result.

## Scope

- Input folder:
  `datalab_master/Master Data/pakistan_economic_survey/2021-22`
- Output folder:
  `agentic/02_pdf_to_md/runs/2021-22_pymupdf4llm_hardened/converted_md`
- PDFs selected:
  all `*.pdf` files directly inside the input folder, sorted by filename
- Non-PDF files and subfolders:
  `manifest.csv` is used for provenance; only direct PDF files are converted
- Original PDFs:
  not modified, renamed, moved, normalized, deduplicated, or deleted

## Selected PDFs

The selected PDFs are recorded in deterministic order in `repro_manifest.json`
under `selected_pdfs`. This run selected `28` PDFs.

## Environment Observed

- Python: recorded in `repro_manifest.json`
- PyMuPDF: recorded in `repro_manifest.json`
- PyMuPDF4LLM: recorded in `repro_manifest.json`
- Git branch/commit, when available: recorded in `repro_manifest.json`

## Conversion Method

The retained conversion script is:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" "agentic\02_pdf_to_md\runs\2021-22_pymupdf4llm_hardened\convert_2021_22_pymupdf4llm.py"
```

The completed run uses deterministic PyMuPDF page text extraction:

```python
page.get_text("text")
```

Each Markdown page is written with an explicit source PDF page marker:

```markdown
<!-- page 1 -->
```

Run-specific caveat: whole-document and page-wise `pymupdf4llm` attempts timed
out on `Economic_Survey_2021_22.pdf`, the 548-page combined survey PDF, in this
environment. The retained hardened run records this in `repro_manifest.json` and
uses PyMuPDF text extraction to complete the selected source scope.

For bounded audit or resumed runs where Markdown already exists, regenerate
hashes, manifest, and logs while reusing completed outputs:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" "agentic\02_pdf_to_md\runs\2021-22_pymupdf4llm_hardened\convert_2021_22_pymupdf4llm.py" --reuse-existing
```

## Headless QA

Run:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" "agentic\02_pdf_to_md\runs\2021-22_pymupdf4llm_hardened\qa_2021_22_pymupdf4llm.py"
```

The QA script writes:

- `qa_results.json`
- `qa_report.md`

The script exits nonzero if structural checks fail or deterministic prose
fidelity sampling fails.

## Run Result

- PDFs found: `28`
- PDFs converted/logged: `28`
- Failed conversions: `0`
- Structural QA: `PASS`
- Deterministic prose fidelity QA: `PASS`
- Prose sample status counts: `27 PASS`, `1 SKIP`
- Table/chart/numeric fidelity: `NOT_CERTIFIED`

## Research Use Policy

Follow `agentic/02_pdf_to_md/README.md`. Markdown is working text only; original
PDFs remain source truth, and table/chart/numeric/ranking/footnote claims require
separate PDF QA.
