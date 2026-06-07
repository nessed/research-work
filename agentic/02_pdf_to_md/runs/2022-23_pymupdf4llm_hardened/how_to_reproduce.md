# How To Reproduce

This is the run-level reproducibility file for the `2022-23` PyMuPDF4LLM
PDF-to-Markdown conversion. The canonical stage rules live in
`agentic/02_pdf_to_md/README.md`; this file records only this run's scope,
commands, environment, QA, and result.

## Scope

- Input folder:
  `datalab_master/Master Data/pakistan_economic_survey/2022-23`
- Output folder:
  `agentic/02_pdf_to_md/runs/2022-23_pymupdf4llm_hardened/converted_md`
- PDFs selected:
  all `*.pdf` files directly inside the input folder, sorted by filename
- Source PDFs:
  read only; not modified, renamed, moved, deleted, normalized, or deduplicated

## Selected PDFs

See `repro_manifest.json` field `selected_pdfs`. The final run selected 29
direct PDFs from the 2022-23 source folder.

## Environment Observed

- Python executable and version: recorded in `repro_manifest.json`
- PyMuPDF version: recorded in `repro_manifest.json`
- PyMuPDF4LLM version: recorded in `repro_manifest.json`
- Git branch, commit, and dirty state: recorded in `repro_manifest.json`

## Conversion Command

The retained conversion script is:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" "agentic\02_pdf_to_md\runs\2022-23_pymupdf4llm_hardened\convert_2022_23_pymupdf4llm.py"
```

The conversion was completed through resumed passes because several large PDFs
exceeded interactive command timeouts. To reproduce the final manifest/log from
existing outputs and convert any missing outputs, run:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" "agentic\02_pdf_to_md\runs\2022-23_pymupdf4llm_hardened\convert_2022_23_pymupdf4llm.py" --reuse-existing
```

For targeted retries, the retained script also supports:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" "agentic\02_pdf_to_md\runs\2022-23_pymupdf4llm_hardened\convert_2022_23_pymupdf4llm.py" --only Supplement_2018_19.pdf
```

## Headless QA

Run:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" "agentic\02_pdf_to_md\runs\2022-23_pymupdf4llm_hardened\qa_2022_23_pymupdf4llm.py"
```

The QA script writes:

- `qa_results.json`
- `qa_report.md`

The script exits nonzero if structural checks fail, deterministic prose
fidelity sampling fails, or required limitation statements are missing.

## Run Result

- PDFs found: `29`
- PDFs converted/logged: `29`
- Failed conversions: `0`
- Structural QA: recorded in `qa_results.json`
- Deterministic prose fidelity QA: recorded in `qa_results.json`
- Table/chart/numeric fidelity: `NOT_CERTIFIED`

## Research Use Policy

Markdown is working text only. Original PDFs remain source truth. Tables, chart
values, image content, exact numbers, rankings, totals, row/column structure,
and footnotes remain `NOT_CERTIFIED` unless separately checked against the
source PDFs.
