# Agentic Reproducibility Log

This is the top-level reproducibility index for the `agentic/` workflow. Keep
this file current when major steps are added, moved, repeated, or archived.

## Ground Rules

- Raw source files live under `datalab_master/Master Data/`.
- Do not modify, rename, move, delete, normalize, or deduplicate raw source
  files.
- Original PDFs remain source truth.
- Converted Markdown is a working text layer only.
- Do not treat table, chart, or numeric values from Markdown as final data.
- Any numeric/table/chart claim needs separate PDF QA before research use.
- Generated research work should live under `agentic/`.
- Archive or label old attempts instead of mixing them with active outputs.

## Current Folder Map

- `agentic/WORKSPACE_STRUCTURE.md`
  - Canonical folder structure and active/archive rules.
- `agentic/01_pes_folder_map/`
  - Reproducible filesystem inventory of the PES corpus.
- `agentic/02_pdf_to_md/`
  - Hardened PDF-to-Markdown run and archived conversion attempts.
- `agentic/03_commentary_schema_discovery/`
  - Pattern scan, working schema, stress tests, and extraction pilots.
- `agentic/reviews/`
  - Cross-cutting adversarial reviews.
- `agentic/sitreps/`
  - Situation reports.

## Step 01: PES Folder Map

Detailed reproduction doc:

- `agentic/01_pes_folder_map/how_to_reproduce.md`

Input:

- `datalab_master/Master Data/pakistan_economic_survey`

Primary output:

- `agentic/01_pes_folder_map/pes_folder_tree.json`

Review evidence:

- `agentic/01_pes_folder_map/adv_review_prompt.md`
- `agentic/01_pes_folder_map/adv_review_results.md`

Result:

- PASS / high confidence filesystem inventory.
- 10 year folders and 287 PDFs were recorded in the completed baseline.

## Step 02: PDF To Markdown Conversion

Active hardened run:

- `agentic/02_pdf_to_md/runs/2015-16_pymupdf4llm_hardened`

Detailed reproduction doc:

- `agentic/02_pdf_to_md/runs/2015-16_pymupdf4llm_hardened/how_to_reproduce.md`

Input:

- `datalab_master/Master Data/pakistan_economic_survey/2015-16`

Active converted Markdown:

- `agentic/02_pdf_to_md/runs/2015-16_pymupdf4llm_hardened/converted_md`

Retained scripts:

- `convert_2015_16_pymupdf4llm.py`
- `qa_2015_16_pymupdf4llm.py`

Machine-readable evidence:

- `repro_manifest.json`
- `conversion_log.json`
- `qa_results.json`
- `qa_report.md`

Run result:

- PDFs found: `29`
- Logged conversions: `29`
- Failed conversions: `0`
- Structural QA: `PASS`
- Deterministic prose fidelity QA: `PASS`
- Table/chart/numeric fidelity: `NOT_CERTIFIED`

Archived conversion material:

- `agentic/02_pdf_to_md/archive/legacy_6pdf_pilots/`
- `agentic/02_pdf_to_md/archive/superseded_single_file_attempts/`
- `agentic/02_pdf_to_md/archive/empty_or_path_confused_outputs/`

Important path note:

- `processed_pdfs/` is not an active destination.
- Active derived PDF-to-Markdown outputs live under `agentic/02_pdf_to_md/runs/`.

## Step 03: Commentary Schema Discovery

Folder:

- `agentic/03_commentary_schema_discovery`

Local docs:

- `agentic/03_commentary_schema_discovery/README.md`
- `agentic/03_commentary_schema_discovery/how_to_reproduce.md`

Active outputs:

- `pattern_scan/commentary_pattern_scan.md`
- `schema/commentary_schema_draft.json`
- `schema/commentary_schema_v0.1.json`
- `stress_tests/schema_stress_test_claims.json`
- `stress_tests/schema_stress_test_review.md`
- `stress_tests/hard_case_claims.json`
- `stress_tests/hard_case_schema_validation.md`
- `extraction_pilots/extraction_pilot_claims.json`
- `extraction_pilots/extraction_pilot_review.md`

Result:

- Working schema v0.1 held through random stress tests, hard-case tests, and a
  five-file extraction pilot.
- This is still pilot work, not full extraction.

## Validation Commands

Validate schema-discovery JSON:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" -c "import json, pathlib; [json.load(open(p, encoding='utf-8')) for p in pathlib.Path(r'agentic\03_commentary_schema_discovery').rglob('*.json')]; print('json_ok')"
```

Regenerate hardened conversion manifest/log from existing Markdown:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" "agentic\02_pdf_to_md\runs\2015-16_pymupdf4llm_hardened\convert_2015_16_pymupdf4llm.py" --reuse-existing
```

Run hardened conversion QA:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" "agentic\02_pdf_to_md\runs\2015-16_pymupdf4llm_hardened\qa_2015_16_pymupdf4llm.py"
```

## Update Protocol

When adding a workflow step:

1. Put active outputs under a clearly named `agentic/` task folder.
2. Add or update `how_to_reproduce.md`.
3. Add or update `adv_review_prompt.md`.
4. Save fresh-context review results when available.
5. Record inputs, outputs, method, constraints, random seed if used, and
   validation result.
6. Keep original PDFs as source truth.
7. Keep numeric/table/chart claims marked for PDF QA.

When moving files:

1. Update this file.
2. Update `agentic/WORKSPACE_STRUCTURE.md` if structure changes.
3. Preserve old location notes in archive READMEs.
4. Do not silently delete old context unless Ali explicitly asks.

## Next Planned Step

Complete the workspace-cleanup adversarial review, then continue with controlled
commentary extraction pilots only after Ali asks.
