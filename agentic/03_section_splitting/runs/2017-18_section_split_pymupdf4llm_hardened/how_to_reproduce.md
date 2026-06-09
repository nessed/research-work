# How to Reproduce

## Inputs

- `agentic/02_pdf_to_md/runs/2017-18_pymupdf4llm_hardened/converted_md/`
- Exclusions applied for homogeneous year scope:
  - `Supplement_2018_19.pdf`
  - `Supplement_2019_20.pdf`
  - `Supplement_2020_21.pdf`
  - `Supplement_2021_22.pdf`
  - `Statistical_Supplement.pdf` (duplicate alias of 2017-18 supplement)

## Command

Run from the `2017-18_section_split_pymupdf4llm_hardened` directory:

```bash
python split_2017_18_sections.py
```

## Expected Outputs

- `sections.jsonl`: 2234 records
- `section_manifest.json`
- `section_split_report.md`
