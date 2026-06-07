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
  - Canonical PDF-to-Markdown stage instructions, run folders, and archived
    conversion attempts.
- `agentic/03_section_splitting/`
  - Reviewed Markdown-to-sections runs with included/excluded input evidence.
- `agentic/archive/04_commentary_schema_discovery/`
  - Completed schema discovery/hardening and pilot evidence retained as
    provenance for Claims JSON extraction.
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

Canonical stage instructions:

- `agentic/02_pdf_to_md/README.md`

Run-level reproduction docs:

- `agentic/02_pdf_to_md/runs/2015-16_pymupdf4llm_hardened/how_to_reproduce.md`
- `agentic/02_pdf_to_md/runs/2016-17_pymupdf4llm_hardened/how_to_reproduce.md`

Rule:

- The base `README.md` is the instruction source for Step 02. Run-level
  `how_to_reproduce.md` files record only run-specific paths, commands,
  observed environment, QA, results, and caveats.

Archived conversion material:

- `agentic/02_pdf_to_md/archive/legacy_6pdf_pilots/`
- `agentic/02_pdf_to_md/archive/superseded_single_file_attempts/`
- `agentic/02_pdf_to_md/archive/empty_or_path_confused_outputs/`

Important path note:

- `processed_pdfs/` is not an active destination.
- Active derived PDF-to-Markdown outputs live under `agentic/02_pdf_to_md/runs/`.

## Step 03: Sections

Detailed reproduction docs:

- `agentic/03_section_splitting/runs/*/how_to_reproduce.md`

Primary outputs:

- `sections.jsonl`
- `section_manifest.json`
- `section_split_report.md`

Required source-scope evidence:

- Included input Markdown files.
- Excluded input Markdown files.
- Reason for each exclusion.
- Source year decision used by the run.

Important invariant:

- Folder year is not automatically source year. Section runs must decide which
  Markdown files are valid inputs for the intended `source_year`.

Completed runs:

- `agentic/03_section_splitting/runs/2016-17_section_split_pymupdf4llm_hardened/`
  Result: PASS — 2,121 sections, adversarial review passed. Use as template.

In-progress runs:

- `agentic/03_section_splitting/runs/2018-19_section_split_pymupdf4llm_hardened/`
  Status: script committed; `sections.jsonl` not yet produced.

## Archived Design Evidence: Commentary Schema

Folder:

- `agentic/archive/04_commentary_schema_discovery`

Local docs:

- `agentic/archive/04_commentary_schema_discovery/README.md`
- `agentic/archive/04_commentary_schema_discovery/how_to_reproduce.md`

Retained provenance:

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
- 2016-17 schema hardening did not require a major redesign.
- This is completed design evidence for Claims JSON extraction, not a recurring
  active pipeline stage and not full extraction.

## Future Active Stages

The remaining active workflow is:

```text
Claims JSON -> Normalize -> Export
```

Claims JSON should begin with a small reviewed pilot inside that stage, then
scale only after pilot QA/review passes.

## Validation Commands

Validate retained schema/provenance JSON:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" -c "import json, pathlib; [json.load(open(p, encoding='utf-8')) for p in pathlib.Path(r'agentic\archive\04_commentary_schema_discovery').rglob('*.json')]; print('json_ok')"
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

## Pipeline Shape

The active pipeline outline is:

```text
PDF -> MD -> Sections -> Claims JSON -> Normalize -> Export
```

