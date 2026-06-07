# How To Reproduce

This is the run-level reproducibility file for the `2020-21`
PDF-to-Markdown conversion. The canonical Step 02 guide is
`agentic/02_pdf_to_md/README.md`; this file only records this run's exact
scope, commands, environment, QA, results, and caveats.

## Scope

- Input folder:
  `datalab_master/Master Data/pakistan_economic_survey/2020-21`
- Output folder:
  `agentic/02_pdf_to_md/runs/2020-21_pymupdf4llm_hardened/converted_md`
- PDFs selected:
  all `*.pdf` files directly inside the input folder, sorted
  case-insensitively by filename
- Scope caveat:
  the direct input folder contains cross-year supplement PDFs
  (`Supplement_2017_18.pdf`, `Supplement_2018_19.pdf`,
  `Supplement_2019_20.pdf`, and `Supplement_2021_22.pdf`). They were converted
  because this Step 02 run used direct-folder PDF scope. Downstream source-year
  processing must exclude or separately label them if using strict `2020-21`
  commentary scope.
- Non-PDF files:
  `manifest.csv` is used for provenance but is outside conversion scope
- Original PDFs:
  not modified, renamed, moved, normalized, deduplicated, or deleted

## Selected PDFs

```text
Agriculture.pdf
Annex_I_Contingent_Liabilities.pdf
Annex_Ii_Tax_Expenditure.pdf
Annex_Iii_Sezones.pdf
Annex_Iv_Covid.pdf
Capital_Markets.pdf
Climate_Change.pdf
Economic_Indicators.pdf
Education.pdf
Energy.pdf
Fiscal.pdf
Growth.pdf
Health.pdf
Inflation.pdf
Manufacturing.pdf
Money_And_Credit.pdf
Overview.pdf
Pes_2020_21.pdf
Population.pdf
Public_Debt.pdf
Social_Protection.pdf
Statistical_Supplement.pdf
Supplement_2017_18.pdf
Supplement_2018_19.pdf
Supplement_2019_20.pdf
Supplement_2020_21.pdf
Supplement_2021_22.pdf
Trade_And_Payments.pdf
Transport.pdf
```

## Environment Observed

- Python executable:
  `C:\Users\Ali\AppData\Local\Python\pythoncore-3.14-64\python.exe`
- Python version:
  `3.14.5`
- Platform:
  `Windows-11-10.0.26200-SP0`
- PyMuPDF:
  `1.27.2.3`
- PyMuPDF4LLM:
  `1.27.2.3`
- Git branch:
  `main`
- Git commit:
  `a96988c564c524a117febbd8057dab6128c7d094`

The full observed environment is recorded in `repro_manifest.json`.

## Conversion Command

Run from repository root:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" "agentic\02_pdf_to_md\runs\2020-21_pymupdf4llm_hardened\convert_2020_21_pymupdf4llm.py"
```

The retained script writes:

- `converted_md/*.md`
- `repro_manifest.json`
- `conversion_log.json`

Each Markdown page is preceded by an explicit page marker:

```markdown
<!-- page 1 -->
```

## Conversion Caveat

This run folder keeps the requested `pymupdf4llm_hardened` name, but the final
retained conversion path uses PyMuPDF plain text extraction for all selected
PDFs. PyMuPDF4LLM did not complete reliably within bounded runtime for the
large combined PDF and table-heavy annex/supplement files before final
manifest/log creation.

The fallback is deterministic and recorded per file in `repro_manifest.json`
and `conversion_log.json`.

## QA Command

Run from repository root:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" "agentic\02_pdf_to_md\runs\2020-21_pymupdf4llm_hardened\qa_2020_21_pymupdf4llm.py"
```

The QA script writes:

- `qa_results.json`
- `qa_report.md`

It checks selected PDF count versus conversion log count, failed conversions,
Markdown output existence, page marker presence, page marker count versus PDF
page count, output hashes, sampled PDF-to-MD prose fidelity, and the
numeric/table/chart limitation policy.

## Run Result

- PDFs found: `29`
- PDFs converted/logged: `29`
- Failed conversions: `0`
- Structural QA: `PASS`
- Deterministic prose fidelity QA: `PASS`
- Page-marker mismatches: `0`
- Hash mismatches: `0`
- Table/chart/numeric fidelity: `NOT_CERTIFIED`

## Research Use Policy

Follow `agentic/02_pdf_to_md/README.md`. Markdown is working text only; original
PDFs remain source truth. Tables, chart text, numeric values, rankings, totals,
and footnotes remain `NOT_CERTIFIED` unless separately QA'd against the source
PDFs.

This run stops after Step 02. It does not section split, extract claims,
normalize JSON, export, or read any source folder other than the `2020-21`
source folder.
