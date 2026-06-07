# How To Reproduce

This is the run-level reproducibility file for the `2019-20` PDF-to-Markdown
conversion. The canonical stage rules live in
`agentic/02_pdf_to_md/README.md`; this file only records this run's scope,
commands, environment, QA, results, and caveats.

## Scope

- Input folder:
  `datalab_master/Master Data/pakistan_economic_survey/2019-20`
- Output folder:
  `agentic/02_pdf_to_md/runs/2019-20_pymupdf4llm_hardened/converted_md`
- PDFs selected:
  all `*.pdf` files directly inside the input folder, sorted
  case-insensitively by filename
- Non-PDF files:
  `manifest.csv` is used for provenance but is not converted
- Original PDFs:
  not modified, renamed, moved, normalized, deduplicated, or deleted

## Environment Observed

- Python executable:
  `C:\Users\Ali\AppData\Local\Python\pythoncore-3.14-64\python.exe`
- Python: `3.14.5`
- Platform: `Windows-11-10.0.26200-SP0`
- PyMuPDF: `1.27.2.3`
- PyMuPDF4LLM: `1.27.2.3`
- Git branch: `main`
- Git commit: `2927124a0730ef205b7211c7300efae3fedbf2dc`

The complete environment record is in `repro_manifest.json`.

## Conversion Command

Run from repository root:

```powershell
& "C:\Users\Ali\AppData\Local\Python\pythoncore-3.14-64\python.exe" "agentic\02_pdf_to_md\runs\2019-20_pymupdf4llm_hardened\convert_2019_20_pymupdf4llm.py"
```

For bounded audit reruns where Markdown already exists, regenerate hashes,
manifest, and logs while reusing small-PDF outputs:

```powershell
& "C:\Users\Ali\AppData\Local\Python\pythoncore-3.14-64\python.exe" "agentic\02_pdf_to_md\runs\2019-20_pymupdf4llm_hardened\convert_2019_20_pymupdf4llm.py" --reuse-existing
```

The conversion script writes:

- `converted_md/`
- `repro_manifest.json`
- `conversion_log.json`

## Conversion Method

- PDFs with 100 pages or fewer use:

```python
pymupdf4llm.to_markdown(str(pdf_path), page_chunks=True)
```

- PDFs over 100 pages use PyMuPDF page text extraction as a long-PDF fallback
  because PyMuPDF4LLM layout conversion exceeded practical runtime for the
  516-page full survey PDF.
- Every Markdown page begins with an explicit marker:

```markdown
<!-- page 1 -->
```

## QA Command

Run from repository root:

```powershell
& "C:\Users\Ali\AppData\Local\Python\pythoncore-3.14-64\python.exe" "agentic\02_pdf_to_md\runs\2019-20_pymupdf4llm_hardened\qa_2019_20_pymupdf4llm.py"
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
- Prose fidelity samples: `27 PASS`, `2 SKIP`
- Conversion log output hash checks: `PASS`
- Table/chart/numeric fidelity: `NOT_CERTIFIED`

## Caveats

- `Inflation.pdf` and `Inflation(1).pdf` were both selected because both are
  direct PDFs in the source folder.
- Supplements for other years inside this source folder were converted as
  direct source-folder PDFs. Later section splitting must decide source-year
  inclusion/exclusion.
- Markdown is working text only. Original PDFs remain source truth.
- Tables, chart text, numeric values, rankings, totals, and footnotes remain
  NOT_CERTIFIED unless separately QA'd against PDFs.
