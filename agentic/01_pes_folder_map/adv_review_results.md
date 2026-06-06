All checks complete. Every filesystem reading matches the JSON. Here is the review report.

---

# PES Corpus Inventory — Independent Review Report

## 1. Verdict

**PASS**

## 2. Confidence

**High**

Confidence is high because the review independently re-derived every count, path, and size from filesystem metadata and reconciled all of them against `pes_folder_tree.json` with zero unexplained discrepancies. The corpus is small (10 folders, 297 files total) and was fully enumerated, not sampled.

## 3. Summary

The inventory in `agentic/01_pes_folder_map/pes_folder_tree.json` is an accurate, faithful representation of the source filesystem at `datalab_master/Master Data/pakistan_economic_survey`.

- Source root exists; contains exactly **10 immediate year folders** and no loose files.
- `year_count` (10) is correct.
- Per-year PDF counts all match.
- `total_pdf_count` (287) matches the independent recursive count (287).
- Every listed relative path exists on disk.
- Every listed `size_bytes` matches the filesystem `Length`.
- Non-PDF files (`manifest.csv`, `Statistical_Supplement.zip`) are correctly classified as `other_files` and excluded from PDF counts.
- No nested subdirectories exist below the year level, so no files were missed.

All discrepancies of note are **source-data naming quirks** (typos, duplicates, inconsistent chapter naming) that the inventory recorded *exactly as stored* — which is the manifest's stated requirement. They do not constitute inventory errors.

## 4. Filesystem Validation Checks

| # | Check | Result |
|---|-------|--------|
| 1 | Source root exists | ✅ PASS (`Test-Path` = True) |
| 2 | Every listed year folder exists | ✅ PASS (all 10 present) |
| 3 | Inventory year count = number of immediate year folders | ✅ PASS (10 = 10) |
| 4 | Independent per-year PDF count | ✅ Done (see table below) |
| 5 | Per-year PDF count vs JSON | ✅ PASS (all match) |
| 6 | Sum of independent per-year PDF counts | ✅ 287 |
| 7 | Independent total PDF count vs JSON | ✅ PASS (287 = 287; cross-checked by recursive `Measure-Object` = 287) |
| 8 | Every listed relative path exists | ✅ PASS |
| 9 | Every listed file size matches filesystem | ✅ PASS (all 297 entries) |
| 10 | Non-PDF files not counted as PDFs | ✅ PASS (`.csv`, `.zip` in `other_files` only) |
| 11 | Duplicate-looking filenames | ⚠️ Flagged (see §7 — not errors) |
| 12 | Weird names / spacing / casing / typos | ⚠️ Flagged (see §7 — not errors) |
| 13 | Missing/inconsistent chapter sequences | ⚠️ Flagged (see §7 — not errors) |

No subdirectories exist below year level (recursive directory listing returned only the 10 year folders), confirming the per-folder file enumeration is complete.

## 5. Comparison Against pes_folder_tree.json

Per-year reconciliation (JSON value = filesystem value in all rows):

| Year | JSON pdf_count | FS pdf_count | JSON file_count | FS file_count | other_files | Match |
|------|---------------|--------------|-----------------|---------------|-------------|-------|
| 2015-16 | 29 | 29 | 31 | 31 | manifest.csv, .zip | ✅ |
| 2016-17 | 30 | 30 | 32 | 32 | manifest.csv, .zip | ✅ |
| 2017-18 | 29 | 29 | 30 | 30 | manifest.csv | ✅ |
| 2018-19 | 27 | 27 | 28 | 28 | manifest.csv | ✅ |
| 2019-20 | 29 | 29 | 30 | 30 | manifest.csv | ✅ |
| 2020-21 | 29 | 29 | 30 | 30 | manifest.csv | ✅ |
| 2021-22 | 28 | 28 | 29 | 29 | manifest.csv | ✅ |
| 2022-23 | 29 | 29 | 31 | 31 | manifest.csv, .zip | ✅ |
| 2023-24 | 29 | 29 | 31 | 31 | manifest.csv, .zip | ✅ |
| 2024-25 | 28 | 28 | 30 | 30 | manifest.csv, .zip | ✅ |
| **Total** | **287** | **287** | **302** | **302** | — | ✅ |

All ~287 PDF `size_bytes` values and all 15 `other_files` sizes were compared line-by-line against the filesystem `Length`; every value matched. No path in the JSON was found missing on disk, and no file on disk was found absent from the JSON.

## 6. Mismatches Found

**None.** No count mismatch, no path mismatch, no size mismatch, and no misclassification of non-PDF files.

## 7. Duplicate / Weird Filename Findings

These are properties of the **raw source corpus** and were recorded correctly by the inventory. They are surfaced here per the manifest, with no normalization applied or recommended within this review.

**Cross-year duplicate filenames (identical name + identical size — same files copied into multiple year folders):**
- `Supplement_2017_18.pdf` (6,136,098 B), `Supplement_2018_19.pdf` (5,562,836 B), `Supplement_2019_20.pdf` (1,488,707 B), `Supplement_2020_21.pdf` (1,345,998 B), `Supplement_2021_22.pdf` (2,042,321 B) — this set of five recurs across nearly every year folder with byte-identical sizes. This inflates the corpus-wide PDF total with repeated statistical supplements.

**Within-year duplicates (same size, suggesting same content under two names):**
- 2019-20: `Inflation(1).pdf` and `Inflation.pdf` — both 133,452 B (the `(1)` copy is a clear download duplicate).
- 2017-18: `Statistical_Supplement.pdf` and `Supplement_2017_18.pdf` — both 6,136,098 B.
- 2018-19: `Statistical_Supplement.pdf` and `Supplement_2018_19.pdf` — both 5,562,836 B.
- 2019-20: `Statistical_Supplement.pdf` and `Supplement_2019_20.pdf` — both 1,488,707 B.
- 2020-21: `Statistical_Supplement.pdf` and `Supplement_2020_21.pdf` — both 1,345,998 B.

(Per the manifest, this review does not assert these are true content duplicates — only that names/sizes coincide.)

**Typos in source filenames:**
- `Captial_Markets.pdf` — "Capital" transposed; in 2016-17, 2017-18, 2018-19.
- `Inflaton.pdf` — missing "i"; in 2018-19.
- `Annex_Iii_Covid_19_Advent_And_Impact_Assesment.pdf` — "Assesment"; in 2019-20.
- `Annex_Iii_Sezones.pdf` — "Sezones" (apparently "SEZ Zones"); in 2020-21.

**Weird / encoding-artifact filenames:**
- `Pes05_Money_26Credit.pdf` (2021-22) — the `26` is a leftover URL encoding of `&` (`%26`); intended "Money & Credit".
- `Pakistan_Es_2016_17_Pdf.pdf` (2016-17) — literal "_Pdf" baked into the stem plus the real `.pdf` extension.
- `Inflation(1).pdf` (2019-20) — parenthesized duplicate marker in the name.

**Casing / spacing / singular-plural inconsistencies (same concept, different naming across years):**
- Capital markets: `Capital_Markets` vs `Captial_Markets` (typo) vs `Capital_Market` (singular, 2024-25).
- Transport: `Transport` vs `Transport_And_Communications` vs `Transport_And_Communication` (singular/plural).
- Whole-survey file: `Pakistan_Es_2016_17_Pdf`, `Economic_Survey_2017_18`, `Pes_2019_20`, `Pes_2020_21`, `Economic_Survey_2021_22`, `Economic_Survey_2022_23`, `Economic_Survey_2023_24` — no consistent convention.
- Overview/summary chapter: `Overview_Of_The_Economy`, `Overview_2016_17`, `Overview`, `Executive_Summary`, `Highlights`, `Key_Indicators` — varies by year.

**Chapter-sequence / annex-naming observations:**
- Annex numbering scheme changes year to year: `Annexure_I…Iv` (2015-16), Roman `Annex_I…Vi` (2016-17), Arabic `Annex_1/2/3` (2023-24), and the separator-less `Annexii_Tax_Expenditure_Fy_2023` (2022-23).
- 2022-23 looks like it is "missing" Annex II in the `Annex_I` / `Annex_Iii` pattern, but Annex II is in fact present as `Annexii_Tax_Expenditure_Fy_2023.pdf` — an inconsistent-naming case, **not** a missing file.
- 2021-22 uses an explicit numbered chapter scheme `Pes01_…` through `Pes16_…`; the sequence 01–16 is **complete with no gaps**.

Per the manifest's Known Limitations, this review does not decide whether duplicate-looking files are true duplicates or whether any apparently absent chapter is genuinely missing.

## 8. Reproducibility Issues

- The inventory is reproducible from filesystem metadata alone; re-running enumeration reproduced `year_count`, all per-year counts, the 287 total, and every size.
- Minor environmental note: `root` in the JSON is recorded as a POSIX-style relative path (`./datalab_master/Master Data/pakistan_economic_survey`). It resolves correctly under the repository root on this Windows host; no portability problem was observed, but anyone reproducing on a case-sensitive filesystem should note the corpus relies on case-insensitive matching (e.g., the `Inflation` / `Inflation(1)` pair).
- No `generated_at` drift concern: the JSON timestamp (2026-06-04) predates this review (2026-06-05); the filesystem state is unchanged and still matches.

## 9. Recommended Next Action

**Accept `pes_folder_tree.json` as the validated filesystem inventory and proceed** to the next planned stage (PDF inspection / extraction / family mapping), which is explicitly out of scope here.

Carry the following forward as **inputs to later stages, not inventory fixes** (do not modify raw source files):
1. Treat the recurring `Supplement_*.pdf` set and the `Statistical_Supplement.pdf`/`Supplement_*` same-size pairs as candidate cross-/within-year duplicates during de-duplication, so repeated supplements are not double-processed.
2. Treat `Inflation(1).pdf` (2019-20) as a likely redundant copy of `Inflation.pdf`.
3. Build a filename→canonical-chapter mapping during family mapping to absorb the typos and inconsistent naming (`Captial`, `Inflaton`, `Money_26Credit`, `Annexii…`, singular/plural Transport/Capital, mixed Annex numbering) rather than renaming source files.

No corrective action is required against the inventory itself.

---

Note: no files were created or modified during this review (an attempted scratch CSV export was blocked and never written); the source corpus and `pes_folder_tree.json` are untouched.

