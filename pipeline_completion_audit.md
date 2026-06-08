# Pipeline Completion Audit

## Step 02: PDF to Markdown
| Year | Run Folder | Raw PDFs | Conv MDs | repro_manifest | conversion_log | qa_results | qa_report | conv script | qa script | adv review | 0-byte MDs | Pg Mismatch | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2015-16 | 2015-16_pymupdf4llm_hardened | 29 | 29 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | 0 | 0 | PASS |
| 2016-17 | 2016-17_pymupdf4llm_hardened | 30 | 30 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | 0 | 0 | PASS |
| 2017-18 | 2017-18_pymupdf4llm_hardened | 29 | 29 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | 0 | 0 | PASS |
| 2018-19 | 2018-19_pymupdf4llm_hardened | 27 | 27 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | 0 | 0 | PASS |
| 2019-20 | 2019-20_pymupdf4llm_hardened | 29 | 29 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | 0 | 0 | PASS |
| 2020-21 | 2020-21_pymupdf4llm_hardened | 29 | 29 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | 0 | 0 | PASS |
| 2021-22 | 2021-22_pymupdf4llm_hardened | 28 | 28 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | 0 | 0 | PASS |
| 2022-23 | 2022-23_pymupdf4llm_hardened | 29 | 29 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | 0 | 0 | PASS |
| 2023-24 | 2023-24_pymupdf4llm_hardened | 29 | 29 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | 0 | 0 | PASS |
| 2024-25 | 2024-25_pymupdf4llm_hardened | 28 | 28 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | 0 | 0 | PASS |

## Step 03: Section Splitting
| Year | Run Folder | sections.jsonl | section_manifest | split_report | adv review | section count | incl/excl recorded | Status |
|---|---|---|---|---|---|---|---|---|
| 2015-16 | 2015-16_section_split_pymupdf4llm_hardened | No | No | No | No | N/A | No | MISSING |
| 2016-17 | 2016-17_section_split_pymupdf4llm_hardened | Yes | Yes | Yes | Yes | 2121 | Yes | PASS |
| 2017-18 | 2017-18_section_split_pymupdf4llm_hardened | No | No | No | No | N/A | No | MISSING |
| 2018-19 | 2018-19_section_split_pymupdf4llm_hardened | Yes | Yes | Yes | Yes | 2736 | Yes | PASS |
| 2019-20 | 2019-20_section_split_pymupdf4llm_hardened | No | No | No | No | N/A | No | MISSING |
| 2020-21 | 2020-21_section_split_pymupdf4llm_hardened | No | No | No | No | N/A | No | MISSING |
| 2021-22 | 2021-22_section_split_pymupdf4llm_hardened | No | No | No | No | N/A | No | MISSING |
| 2022-23 | 2022-23_section_split_pymupdf4llm_hardened | No | No | No | No | N/A | No | MISSING |
| 2023-24 | 2023-24_section_split_pymupdf4llm_hardened | No | No | No | No | N/A | No | MISSING |
| 2024-25 | 2024-25_section_split_pymupdf4llm_hardened | No | No | No | No | N/A | No | MISSING |
