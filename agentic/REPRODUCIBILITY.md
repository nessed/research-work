# Agentic Reproducibility Log

This is the top-level, living reproducibility record for the `agentic/`
workflow. Keep updating this file as new steps are added, moved, or repeated.

The purpose is to make the whole workflow traceable without digging through
chat history. Subfolders may keep their own detailed reproduction notes; this
file is the index and step-by-step operating record.

## Ground Rules

- Raw PES source files live under `datalab_master/Master Data/`.
- Do not modify, rename, move, delete, normalize, or deduplicate raw source
  files.
- Original PDFs remain source truth.
- Converted Markdown is a working text layer only.
- Do not treat table, chart, or numeric values extracted from Markdown as final
  data.
- Any numeric/table/chart claim needs separate PDF QA before database use.
- Generated work should live under `agentic/`.
- Archive or label old attempts instead of mixing them with active outputs.

## Current Folder Map

- `agentic/01_pes_folder_map/`
  - Filesystem inventory of the PES corpus.
- `agentic/02_pdf_to_md/`
  - PDF-to-Markdown conversion work and active 2015-16 Markdown corpus.
- `agentic/03_commentary_schema_discovery/`
  - Commentary pattern scan, draft schema, stress tests, and extraction pilots.
- `agentic/reviews/`
  - Review material and notes.
- `agentic/sitreps/`
  - Situation reports.

## Step 01: PES Folder Map

Detailed reproduction doc:

- `agentic/01_pes_folder_map/how_to_reproduce.md`

Purpose:

- Create a reproducible filesystem inventory of the Pakistan Economic Survey
  corpus before any PDF inspection, extraction, family mapping, or content
  analysis.

Input:

- `datalab_master/Master Data/pakistan_economic_survey`

Primary output:

- `agentic/01_pes_folder_map/pes_folder_tree.json`

Supporting outputs:

- `agentic/01_pes_folder_map/adv_review_prompt.md`
- `agentic/01_pes_folder_map/adv_review_results.md`

Method summary:

1. Enumerate immediate year folders under the PES source root.
2. Record contained filesystem entries.
3. Preserve exact filenames, extensions, file sizes, and relative paths.
4. Count PDFs and non-PDF files by year.
5. Export the inventory JSON.
6. Review duplicate-looking names, unusual names, and missing-looking chapter
   sequences.

Constraints:

- Filesystem metadata only.
- No PDF content inspection.
- No OCR.
- No extraction.
- No source-file cleanup.

## Step 02: PDF To Markdown Conversion

Detailed reproduction doc:

- `agentic/02_pdf_to_md/2015-16_pymupdf4llm/how_to_reproduce.md`

Important location note:

- The conversion was originally documented as writing to
  `processed_pdfs/2015-16_pymupdf4llm`.
- The active organized copy now lives under
  `agentic/02_pdf_to_md/2015-16_pymupdf4llm`.
- Treat the `agentic/02_pdf_to_md/2015-16_pymupdf4llm` folder as the working
  corpus for downstream schema discovery.

Input:

- `datalab_master/Master Data/pakistan_economic_survey/2015-16`

Active output:

- `agentic/02_pdf_to_md/2015-16_pymupdf4llm`

Conversion method:

```python
pymupdf4llm.to_markdown(str(pdf_path), page_chunks=True)
```

Markdown page markers were inserted as:

```markdown
<!-- page 1 -->
```

Run result:

- PDFs found: `29`
- PDFs converted: `29`
- Failures: `0`

Environment observed in the detailed doc:

- PyMuPDF4LLM: `1.27.2.3`
- PyMuPDF: `1.27.2.3`
- Branch at run time: `new-conversion`

Active corpus note:

- The active folder contains the 29 PES 2015-16 Markdown chapter files plus
  local review/reproduction notes.
- When counting chapter files, exclude local notes such as
  `how_to_reproduce.md`, `conversion_quality.md`, `adv_review_prompt.md`, and
  `adv_review_results.md`.

## Step 03: Commentary Schema Discovery

Folder:

- `agentic/03_commentary_schema_discovery`

Local index:

- `agentic/03_commentary_schema_discovery/README.md`

Purpose:

- Review the converted 2015-16 Markdown files to identify repeatable PES
  commentary patterns that can be standardized into a JSON schema.
- This is schema discovery and pilot extraction, not full extraction.

Core rules:

- Use all 29 Markdown files for high-level pattern discovery.
- Do not extract all claims yet.
- Do not build a database yet.
- Do not process new PDFs.
- Do not trust table/numeric values as final data.
- Original PDFs remain source truth.

### 03A: Pattern Scan

Output:

- `agentic/03_commentary_schema_discovery/pattern_scan/commentary_pattern_scan.md`

Schema draft:

- `agentic/03_commentary_schema_discovery/schema/commentary_schema_draft.json`

Method summary:

1. Review all 29 active 2015-16 Markdown files at a high level.
2. Identify recurring commentary patterns across sectors and chapters.
3. Record pattern names, meanings, example sectors/files, short quotes, schema
   placement recommendation, confidence, and risks.
4. Mark which patterns appear universal versus sector-specific.
5. Keep output practical for repeatable cross-year extraction.

Pattern types reviewed included:

- cause-effect claims
- policy actions
- government commitments
- constraints and bottlenecks
- risks and shocks
- outlook and expectations
- optimism/pessimism signals
- sector performance narratives
- reform narratives
- investment/development priorities
- regional/provincial comparisons
- programme/project mentions
- data-definition caveats
- need-for-improvement statements
- future targets or plans

### 03B: Random 3-File Schema Stress Test

Outputs:

- `agentic/03_commentary_schema_discovery/stress_test/schema_stress_test_claims.json`
- `agentic/03_commentary_schema_discovery/stress_test/schema_stress_test_review.md`

Selection:

- Random seed: `20260606`
- Sampled files:
  - `Public_Debt.md`
  - `Population.md`
  - `Supplement_2020_21.md`

Method summary:

1. Take 2-3 random Markdown files.
2. Extract 10-20 claims each using the draft schema.
3. Identify where the schema breaks.
4. Revise the schema only where the pilot exposes repeatable structure.

Result:

- 32 pilot records.
- Schema was revised after this pass.

### 03C: Hard-Case Schema Stress Test

Outputs:

- `agentic/03_commentary_schema_discovery/stress_test_hard_cases/hard_case_claims.json`
- `agentic/03_commentary_schema_discovery/stress_test_hard_cases/hard_case_schema_review.md`

Selection:

- Dense prose sector: `Agriculture.md`
- Policy-heavy/social sector: `Social_Safety.md`
- Table/indicator-heavy file: `Economic_Indicators.md`

Method summary:

1. Deliberately choose hard cases instead of random files.
2. Extract a small controlled batch of claims.
3. Check whether the revised schema holds.
4. Only revise if something genuinely breaks again.

Result:

- 30 pilot records.
- Schema held.
- Frozen working schema created as:
  `agentic/03_commentary_schema_discovery/schema/commentary_schema_v0.1.json`

### 03D: Five-File Random Extraction Pilot

Outputs:

- `agentic/03_commentary_schema_discovery/extraction_pilot_5_random/extraction_pilot_claims.json`
- `agentic/03_commentary_schema_discovery/extraction_pilot_5_random/extraction_pilot_review.md`

Selection:

- Random seed: `20260607`
- Sampled files:
  - `Health.md`
  - `Trade.md`
  - `Annexure_Iv_War_On_Terror.md`
  - `Capital_Markets.md`
  - `Education.md`

Method summary:

1. Use frozen schema v0.1.
2. Extract 5 claims from each sampled file.
3. Keep claims quote-grounded.
4. Use page markers from Markdown where available.
5. Flag all table/numeric-sensitive records.
6. Review whether schema v0.1 breaks.

Result:

- 25 records total.
- 5 records per sampled file.
- Schema v0.1 held.
- No schema revision required from this pilot.

## Current Working Schema

Current frozen working schema:

- `agentic/03_commentary_schema_discovery/schema/commentary_schema_v0.1.json`

Schema status:

- Draft/frozen for pilot work.
- Not final for full database extraction.
- Safe next use: write extraction rules/prompt instructions and run a controlled
  5-6 chapter extraction pilot.

Important schema behavior:

- `claim_type` should capture the primary pattern.
- `topic_tags` should capture cross-cutting themes.
- `policy_or_programmes` is needed because PES prose often mentions multiple
  policies in one paragraph.
- `comparison` should stay optional.
- `numeric_or_table_sensitive` and `requires_pdf_numeric_qa` are required for
  any claim relying on table values, chart values, targets, rankings,
  percentages, or exact before/after movements.

## Validation Commands

Run from repo root.

Validate all JSON files under schema discovery:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" -c "import json, pathlib; [json.load(open(p, encoding='utf-8')) for p in pathlib.Path(r'agentic\03_commentary_schema_discovery').rglob('*.json')]; print('json_ok')"
```

Count records in the five-file pilot:

```powershell
& "C:\Users\Ali\AppData\Local\Python\bin\python.exe" -c "import json, collections; p=r'agentic\03_commentary_schema_discovery\extraction_pilot_5_random\extraction_pilot_claims.json'; data=json.load(open(p, encoding='utf-8')); print(data['extraction_pilot']['actual_records']); print(dict(collections.Counter(r['source_file'] for r in data['records'])))"
```

Expected five-file pilot count:

```text
25
{'Health.md': 5, 'Trade.md': 5, 'Annexure_Iv_War_On_Terror.md': 5, 'Capital_Markets.md': 5, 'Education.md': 5}
```

## Update Protocol

When adding a new workflow step:

1. Create or update the relevant subfolder reproduction doc.
2. Add the new step to this top-level file.
3. Record inputs, outputs, method, constraints, random seed if used, and
   validation result.
4. Link exact artifact paths.
5. State whether the step changes the schema, freezes the schema, or only tests
   the schema.
6. Keep original PDFs as source truth.
7. Keep numeric/table claims marked for PDF QA.

When moving files:

1. Update this file.
2. Update the subfolder README or `how_to_reproduce.md`.
3. Preserve old location notes if they matter for traceability.
4. Do not silently delete old context unless it is archived elsewhere.

## Next Planned Step

Write extraction rules/prompt instructions using schema v0.1, then run a
controlled 5-6 chapter pilot focused on consistency. Do not start full
extraction until pilot rules and QA checks are stable.
