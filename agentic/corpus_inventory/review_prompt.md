# Review Prompt: PES Corpus Inventory

You are reviewing the reproducibility of the PES corpus inventory task.

Read `agentic/corpus_inventory/manifest.md` first.

Your job is to independently verify `agentic/corpus_inventory/pes_inventory.json` against the source folders under:

`datalab_master/Master Data/pakistan_economic_survey`

Do not inspect PDF contents. Do not parse PDFs. Do not OCR. Do not modify any files under `Master Data/`.

Check the following:

- the PES source root exists
- the year count is correct
- each listed year folder exists
- PDF counts per year match the source folders
- total PDF count matches the source folders
- listed relative paths exist
- non-PDF files are separated from PDF files
- duplicate PDF filenames across years are visible
- odd or inconsistent filenames are flagged
- missing-looking chapters or inconsistent chapter naming are flagged
- any source layout inconsistencies are flagged

Write findings to:

`agentic/corpus_inventory/review_report.md`

The report should be concise and evidence-based. If the inventory passes a check, say so briefly. If a check fails, include the exact year, filename, path, or count involved.

Stay within the scope of this task: inventory review only.
