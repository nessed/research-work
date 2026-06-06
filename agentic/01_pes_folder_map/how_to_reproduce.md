# Task Name

01_pes_folder_map

## Purpose

Create a reproducible filesystem inventory of the Pakistan Economic Survey (PES) corpus before any PDF inspection, extraction, family mapping, or content analysis.

Use the inventory to check:

- year coverage
- file counts
- PDF counts
- duplicate-looking files
- unusual filenames
- source folder layout
- missing-looking or inconsistent chapter naming

## Inputs

Source root:

`datalab_master/Master Data/pakistan_economic_survey`

Input files:

- all files directly inside each year folder under the source root
- `manifest.csv` files when present, recorded only as filesystem entries
- PDF files recorded by filename and filesystem metadata only

## Output

Generated files:

- `agentic/01_pes_folder_map/pes_folder_tree.json`
- `agentic/01_pes_folder_map/how_to_reproduce.md`
- `agentic/01_pes_folder_map/adv_review_prompt.md`
- `agentic/01_pes_folder_map/adv_review_results.md`

Primary reproducible output:

`agentic/01_pes_folder_map/pes_folder_tree.json`

## Reproduction Procedure

1. Locate source root: `datalab_master/Master Data/pakistan_economic_survey`.
2. Enumerate immediate subfolders of the source root.
3. Treat each immediate subfolder as a PES year folder.
4. Do not recurse below the file level unless a year folder contains subfolders.
5. For each year folder, list all contained filesystem entries.
6. For each file, record filename exactly as stored.
7. For each file, record extension exactly as stored or derived from the filename.
8. For each file, record file size in bytes.
9. For each file, record path relative to the repository root.
10. Classify files with `.pdf` or `.PDF` extension as PDFs.
11. Classify all other files separately as non-PDF files.
12. Count PDFs per year folder.
13. Count non-PDF files per year folder.
14. Compute total year folder count.
15. Compute total PDF count across all year folders.
16. Compute total non-PDF file count across all year folders.
17. Export the inventory as JSON to `agentic/01_pes_folder_map/pes_folder_tree.json`.
18. Preserve source filenames, relative paths, and counts exactly.

## Validation Procedure

1. Confirm source root exists.
2. Confirm every listed year folder exists under the source root.
3. Confirm the inventory year count equals the number of immediate year folders.
4. For each year, independently count PDF files in the source folder.
5. Compare each independent per-year PDF count to the JSON.
6. Sum independent per-year PDF counts.
7. Compare the independent total PDF count to the JSON.
8. Confirm every listed relative path exists on disk.
9. Confirm every listed file size matches the filesystem size.
10. Confirm non-PDF files are not counted as PDFs.
11. Flag duplicate-looking filenames within and across year folders.
12. Flag weird filenames, spacing differences, casing differences, and typos.
13. Flag missing-looking chapter sequences or inconsistent chapter naming.
14. Record findings in `agentic/01_pes_folder_map/adv_review_results.md`.

## Constraints

- Do not modify raw files in `datalab_master/Master Data`.
- Do not rename, move, delete, or normalize source files.
- Do not inspect PDF contents.
- Do not open PDFs for text, tables, pages, metadata, OCR, or embedded files.
- Use filesystem metadata only.
- Preserve exact source filenames.
- Preserve exact relative paths.
- Keep generated files under `agentic/01_pes_folder_map/`.
- Do not start extraction.
- Do not start family mapping.
- Do not infer data values from filenames.

## Known Limitations

- Does not verify PDF readability.
- Does not verify PDF page counts.
- Does not verify PDF text quality.
- Does not verify tables or indicators.
- Does not verify whether files are official or complete.
- Does not validate `manifest.csv` contents.
- Does not verify source URLs.
- Does not decide whether duplicate-looking files are true duplicates.
- Does not determine whether missing-looking chapters are actually missing.

## Out of Scope

- PDF content inspection
- OCR
- table extraction
- indicator extraction
- metadata extraction from inside PDFs
- chapter-family mapping
- vintage classification
- source URL validation
- raw file cleanup
- filename normalization
- deduplication
- changes to `Master Data`
