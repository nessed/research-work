# How To Reproduce

## Run

Step 02 PDF-to-Markdown conversion for Pakistan Economic Survey year 2023-24 only.

Run folder:

`agentic/02_pdf_to_md/runs/2023-24_pymupdf4llm_hardened`

Source folder:

`datalab_master/Master Data/pakistan_economic_survey/2023-24`

Output folder:

`agentic/02_pdf_to_md/runs/2023-24_pymupdf4llm_hardened/converted_md`

## Source Scope

Selection rule: convert all `*.pdf` files directly inside the source folder, sorted case-insensitively by filename.

Selected PDFs:

- `Agriculture.pdf`
- `Annex_1_Contingent.pdf`
- `Annex_2_Tax_Expenditure.pdf`
- `Annex_3_Qna.pdf`
- `Capital_Markets.pdf`
- `Climate_Change.pdf`
- `Economic_Survey_2023_24.pdf`
- `Education.pdf`
- `Energy.pdf`
- `Fiscal_Development.pdf`
- `Growth.pdf`
- `Health.pdf`
- `Highlights.pdf`
- `Inflation.pdf`
- `Information_Technology.pdf`
- `Manufacturing_And_Mining.pdf`
- `Money_And_Credit.pdf`
- `Overview_2023_24.pdf`
- `Population.pdf`
- `Public_Debt.pdf`
- `Social_Indicators.pdf`
- `Social_Protection.pdf`
- `Supplement_2017_18.pdf`
- `Supplement_2018_19.pdf`
- `Supplement_2019_20.pdf`
- `Supplement_2020_21.pdf`
- `Supplement_2021_22.pdf`
- `Trade_And_Payments.pdf`
- `Transport.pdf`

Excluded direct non-PDF files:

- `manifest.csv`
- `Statistical_Supplement.zip`

## Commands

From project root:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" "agentic\02_pdf_to_md\runs\2023-24_pymupdf4llm_hardened\convert_2023_24_pymupdf4llm.py"
```

If the long conversion is interrupted after writing some Markdown outputs, continue and regenerate final manifest/log evidence with:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" "agentic\02_pdf_to_md\runs\2023-24_pymupdf4llm_hardened\convert_2023_24_pymupdf4llm.py" --reuse-existing
```

Run QA:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" "agentic\02_pdf_to_md\runs\2023-24_pymupdf4llm_hardened\qa_2023_24_pymupdf4llm.py"
```

## Observed Environment

Recorded in `repro_manifest.json`:

- Python executable: `C:\Users\Ali\AppData\Local\Python\pythoncore-3.14-64\python.exe`
- Python version: `3.14.5`
- Platform: `Windows-11-10.0.26200-SP0`
- PyMuPDF: `1.27.2.3`
- pymupdf4llm: `1.27.2.3`
- Git branch: `main`
- Git commit: `a96988c564c524a117febbd8057dab6128c7d094`

## Outputs

Required outputs in this run folder:

- `converted_md/`
- `repro_manifest.json`
- `conversion_log.json`
- `qa_results.json`
- `qa_report.md`
- `conversion_quality.md`
- `how_to_reproduce.md`
- `adv_review_prompt.md`
- `adv_review_results.md`
- `convert_2023_24_pymupdf4llm.py`
- `qa_2023_24_pymupdf4llm.py`

## Result

QA status: PASS.

All 29 selected PDFs were converted. Every Markdown output has explicit page markers, and page-marker counts match PDF page counts. Output hashes are recorded in `repro_manifest.json`.

Markdown is working text only. Numeric/table/chart/ranking/footnote content remains NOT_CERTIFIED unless separately QA'd against the source PDFs.

