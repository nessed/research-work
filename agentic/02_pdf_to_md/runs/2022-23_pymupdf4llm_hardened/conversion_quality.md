# Conversion Quality

## Run Status

- Run: `2022-23_pymupdf4llm_hardened`
- Source folder: `datalab_master/Master Data/pakistan_economic_survey/2022-23`
- Output folder: `agentic/02_pdf_to_md/runs/2022-23_pymupdf4llm_hardened/converted_md`
- Selection rule: all `*.pdf` files directly inside the source folder, sorted case-insensitively by filename
- PDFs selected: `29`
- Markdown outputs: `29`
- Conversion failures: `0`

## Selected PDFs

1. `Agriculture.pdf`
2. `Annex_I_Contingent_Liabilities.pdf`
3. `Annex_Iii_Pakistan_Floods_2022.pdf`
4. `Annexii_Tax_Expenditure_Fy_2023.pdf`
5. `Capital_Markets.pdf`
6. `Climate_Change.pdf`
7. `Economic_Survey_2022_23.pdf`
8. `Education.pdf`
9. `Energy.pdf`
10. `Fiscal_Development.pdf`
11. `Growth_And_Investment.pdf`
12. `Health.pdf`
13. `Highlights.pdf`
14. `Inflation.pdf`
15. `Information_Technology.pdf`
16. `Key_Indicators.pdf`
17. `Manufacturing_And_Mining.pdf`
18. `Money_And_Credit.pdf`
19. `Overview_Of_The_Economy.pdf`
20. `Population.pdf`
21. `Public_Debt.pdf`
22. `Social_Protection.pdf`
23. `Supplement_2017_18.pdf`
24. `Supplement_2018_19.pdf`
25. `Supplement_2019_20.pdf`
26. `Supplement_2020_21.pdf`
27. `Supplement_2021_22.pdf`
28. `Trade_And_Payments.pdf`
29. `Transport.pdf`

## Conversion Method

The retained script `convert_2022_23_pymupdf4llm.py` uses
`pymupdf4llm.to_markdown(str(pdf_path), page_chunks=True)` and writes each page
chunk with an explicit marker:

```markdown
<!-- page 1 -->
```

Long-running conversions were resumed with `--reuse-existing`; completed
Markdown files were not rewritten during resume passes. The final
`repro_manifest.json` and `conversion_log.json` cover all 29 selected direct
PDFs.

## Quality Interpretation

This run is suitable as a working text layer for prose/commentary work after QA
and review. It is not source truth.

Table, chart, numeric, ranking, total, row/column, and footnote content in the
Markdown remains `NOT_CERTIFIED`. Any downstream use of numeric/table/chart
content requires separate QA against the original source PDFs.

## Raw PDF Protection

The raw PDFs were read in place only. They were not moved, renamed, edited,
deleted, normalized, or deduplicated.
