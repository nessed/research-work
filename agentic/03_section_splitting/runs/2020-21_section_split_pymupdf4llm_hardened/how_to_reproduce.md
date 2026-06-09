# How to Reproduce

## Inputs

- `agentic/02_pdf_to_md/runs/2020-21_pymupdf4llm_hardened/converted_md/`
- Exclusions applied for homogeneous year scope:
  - `Statistical_Supplement.pdf` (duplicate alias)
  - `Supplement_2017_18.pdf`
  - `Supplement_2018_19.pdf`
  - `Supplement_2019_20.pdf`
  - `Supplement_2021_22.pdf`

## Command

Run from the `2020-21_section_split_pymupdf4llm_hardened` directory:

```bash
python split_2020_21_sections.py
```

## Expected Outputs

- `sections.jsonl`: 1136 records
- `section_manifest.json`
- `section_split_report.md`
