# How to Reproduce

## Inputs

- `agentic/02_pdf_to_md/runs/2021-22_pymupdf4llm_hardened/converted_md/`
- Exclusions applied for homogeneous year scope:
  - `Highlights.pdf` (empty output)
  - `Supplement_2017_18.pdf`
  - `Supplement_2018_19.pdf`
  - `Supplement_2019_20.pdf`
  - `Supplement_2020_21.pdf`

## Command

Run from the `2021-22_section_split_pymupdf4llm_hardened` directory:

```bash
python split_2021_22_sections.py
```

## Expected Outputs

- `sections.jsonl`: 1061 records
- `section_manifest.json`
- `section_split_report.md`
