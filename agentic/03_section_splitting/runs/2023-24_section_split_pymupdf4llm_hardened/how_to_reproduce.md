# How to Reproduce

## Inputs

- `agentic/02_pdf_to_md/runs/2023-24_pymupdf4llm_hardened/converted_md/`
- Exclusions applied for homogeneous year scope:
  - `Supplement_2017_18.pdf`
  - `Supplement_2018_19.pdf`
  - `Supplement_2019_20.pdf`
  - `Supplement_2020_21.pdf`
  - `Supplement_2021_22.pdf`

## Command

Run from the `2023-24_section_split_pymupdf4llm_hardened` directory:

```bash
python split_2023_24_sections.py
```

## Expected Outputs

- `sections.jsonl`: 2267 records
- `section_manifest.json`
- `section_split_report.md`
