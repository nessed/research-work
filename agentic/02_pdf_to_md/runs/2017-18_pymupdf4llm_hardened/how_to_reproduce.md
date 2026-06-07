# How To Reproduce

This is the run-level reproducibility file for the `2017-18` PyMuPDF4LLM
PDF-to-Markdown conversion. The canonical stage rules live in
`agentic/02_pdf_to_md/README.md`; this file only records this run's exact scope,
commands, environment, QA, results, and caveats.

## Scope

- Input folder:
  `datalab_master/Master Data/pakistan_economic_survey/2017-18`
- Output folder:
  `agentic/02_pdf_to_md/runs/2017-18_pymupdf4llm_hardened/converted_md`
- PDFs selected:
  all `*.pdf` files directly inside the input folder, sorted by filename
- Non-PDF files:
  `manifest.csv` is used for provenance only and is not converted
- Original PDFs:
  not modified, renamed, moved, deduplicated, normalized, or deleted

## Environment Observed

- Python: recorded in `repro_manifest.json`
- PyMuPDF: recorded in `repro_manifest.json`
- PyMuPDF4LLM: recorded in `repro_manifest.json`
- Git branch/commit, when available: recorded in `repro_manifest.json`

Observed values for this run:

- Python executable: `C:\Users\Ali\AppData\Local\Python\pythoncore-3.14-64\python.exe`
- Python version: `3.14.5`
- PyMuPDF: `1.27.2.3`
- PyMuPDF4LLM: `1.27.2.3`
- Git branch: `main`
- Git commit: `2927124a0730ef205b7211c7300efae3fedbf2dc`

## Conversion Method

The retained conversion script is:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" "agentic\02_pdf_to_md\runs\2017-18_pymupdf4llm_hardened\convert_2017_18_pymupdf4llm.py"
```

It calls:

```python
pymupdf4llm.to_markdown(str(pdf_path), page_chunks=True)
```

Each Markdown page chunk is written with explicit source PDF page markers:

```markdown
<!-- page 1 -->
```

For resumed runs where Markdown already exists, regenerate hashes, manifest,
and logs while reusing completed outputs:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" "agentic\02_pdf_to_md\runs\2017-18_pymupdf4llm_hardened\convert_2017_18_pymupdf4llm.py" --reuse-existing
```

## Headless QA

Run:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" "agentic\02_pdf_to_md\runs\2017-18_pymupdf4llm_hardened\qa_2017_18_pymupdf4llm.py"
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
- Page-marker mismatches: `0`
- Missing outputs: `0`
- Zero-byte outputs: `0`
- Output hash mismatches: `0`
- Conversion log output hash mismatches: `0`
- Table/chart/numeric fidelity: `NOT_CERTIFIED`

## Run Caveats

- Conversion took multiple resumed passes because large PDFs exceeded shorter command timeouts.
- Final conversion was completed with `--reuse-existing`, so the final manifest records `generation_mode` as `reuse_existing_outputs`.
- `Statistical_Supplement.pdf` and `Supplement_2017_18.pdf` have identical source hashes and identical output hashes; both raw files were preserved and converted as separate selected PDFs.

## Research Use Policy

Follow `agentic/02_pdf_to_md/README.md`. Markdown is working text only; original
PDFs remain source truth, and table/chart/numeric claims require separate PDF
QA.
