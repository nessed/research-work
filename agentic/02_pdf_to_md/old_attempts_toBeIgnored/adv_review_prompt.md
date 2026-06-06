# Adversarial Review Prompt

You are a fresh-context adversarial reviewer. Review the Step 2 PDF-to-Markdown pilot in this workspace.

## Scope

Project root:

- `C:\Users\Ali\Desktop\datalab_ali`

Review only:

- `PROJECT_CONTEXT.md`
- `agentic/01_pes_folder_map/pes_folder_tree.json`
- `agentic/02_pdf_to_md/convert_pdfs.py`
- `agentic/02_pdf_to_md/how_to_reproduce.md`
- `agentic/02_pdf_to_md/conversion_quality.md`
- `agentic/02_pdf_to_md/runs/2026-06-05_6pdf_cross_year_pilot/selected_pdf_map.json`
- `agentic/02_pdf_to_md/runs/2026-06-05_6pdf_cross_year_pilot/converted_md/`

Do not modify raw `datalab_master/Master Data`.
Do not process additional PDFs.
Do not create `03_*`.
Do not start commentary extraction, table extraction, or database import.

## Checks

Verify:

1. The run stayed inside `agentic/02_pdf_to_md/`.
2. No `agentic/03_*` folder was created.
3. The selected six PDFs came from `agentic/01_pes_folder_map/pes_folder_tree.json`, not manual guesses.
4. The selected source PDFs exist under `datalab_master/Master Data/pakistan_economic_survey/`.
5. The selection uses a reproducible random seed.
6. There are exactly 3 Education PDFs from 3 different years.
7. There are exactly 3 Transport PDFs from 3 different years.
8. No more than 6 PDFs were converted in the current run.
9. The run output structure is:
   - `selected_pdf_map.json`
   - `converted_md/<year>/<sector>.md`
10. Root-level Step 2 files are limited to method/control/review files plus the `runs/` container.
11. Each converted Markdown file has page markers.
12. Page marker counts match the manifest/source page counts.
13. `how_to_reproduce.md` is sufficient to reproduce the run.
14. `conversion_quality.md` is honest about prose readability, headings, page markers, and weaknesses.
15. The quality verdict is defensible for commentary-focused extraction.
16. The report does not overtrust tables, charts, or numeric values.

## Output

Write a concise adversarial review with:

- verdict: PASS, CONDITIONAL PASS, or FAIL;
- blocking issues, if any;
- non-blocking issues or cautions;
- evidence checked;
- final recommendation.

The parent process will save your final answer to:

- `agentic/02_pdf_to_md/adv_review_results.md`
