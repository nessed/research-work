# How to Reproduce — 2018-19 Claims Extraction (claude, full year)

## Run Identity

| Field | Value |
|---|---|
| Run label | `2018-19_claims_claude_full` |
| Source year | 2018-19 |
| Engine | claude (headless, non-bare OAuth) |
| Runner | `agentic/04_claims_json/run_step04.py` |
| Step 03 input | `agentic/03_section_splitting/runs/2018-19_section_split_pymupdf4llm_hardened/` |
| Schema | `agentic/04_claims_json/claim_array_output_schema.json` |
| Extraction prompt | `agentic/04_claims_json/extraction_prompt.md` |

## Source Scope Summary

970 sections included from 17 chapter-level source files. 1766 sections excluded
from 5 files (full-survey duplicate, statistical supplement, and 3 annex/indicator
files). See `source_scope.json` for per-file counts and exclusion reasons.

**Included (17 files, 970 sections, 56 jobs):**

| Source file | Sections | Jobs |
|---|---|---|
| Agriculture.md | 71 | 4 |
| Captial_Markets.md | 71 | 4 |
| Climate_Change.md | 58 | 3 |
| Education.md | 67 | 4 |
| Energy.md | 24 | 2 |
| Fiscal_Development.md | 49 | 3 |
| Growth.md | 22 | 2 |
| Health_And_Nutrition.md | 80 | 4 |
| Inflaton.md | 19 | 1 |
| Manufacturing.md | 50 | 3 |
| Money_And_Credit.md | 50 | 3 |
| Overview_Of_The_Economy.md | 38 | 2 |
| Population.md | 42 | 3 |
| Public_Debt.md | 65 | 4 |
| Social_Protection.md | 33 | 2 |
| Trade_And_Payments.md | 75 | 4 |
| Transport.md | 156 | 8 |

**Excluded (5 files, 1766 sections):**

| Source file | Sections | Reason |
|---|---|---|
| Economic_Survey_2018_19.md | 1355 | Duplicate full-survey Markdown; chapter files are canonical |
| Supplement_2018_19.md | 392 | Statistical tables supplement; no narrative claims |
| Annex_I.md | 5 | Statistical annex tables; no narrative claims |
| Annex_Ii.md | 8 | Statistical annex tables; no narrative claims |
| Economic_Indicators_1819.md | 6 | Indicator tables; no narrative claims |

## Step 1 — Build jobs

Run once from the repo root to regenerate `source_scope.json` and `jobs.jsonl`:

```powershell
python agentic/04_claims_json/runs/2018-19_claims_claude_full/_supporting/gen_jobs.py
```

Expected output: 56 jobs, 970 included sections.

## Step 2 — Run extraction

Run from the repo root. The command is idempotent — re-running resumes from where
it left off:

```powershell
python agentic/04_claims_json/run_step04.py `
  --engine claude `
  --run-dir agentic/04_claims_json/runs/2018-19_claims_claude_full `
  --schema-file agentic/04_claims_json/claim_array_output_schema.json `
  --prompt-file agentic/04_claims_json/extraction_prompt.md `
  --chunk 20 `
  --concurrency 3
```

To retry failed jobs only:

```powershell
python agentic/04_claims_json/run_step04.py `
  --engine claude `
  --run-dir agentic/04_claims_json/runs/2018-19_claims_claude_full `
  --schema-file agentic/04_claims_json/claim_array_output_schema.json `
  --prompt-file agentic/04_claims_json/extraction_prompt.md `
  --chunk 20 `
  --concurrency 1 `
  --only-failed
```

Progress is visible in the terminal (`ok job_XXXX: N claims via claude`).
Results accumulate in `_supporting/job_results.jsonl` after each job.
Failures are written to `_supporting/failed_jobs/<job_id>.txt`.

## Step 3 — Finalize claims.jsonl (Step 06)

After all 56 jobs complete with no failures, run Step 06 to rebuild the final
output from `job_results.jsonl` in stable job order:

```text
agentic/04_claims_json/runs/2018-19_claims_claude_full/claims.jsonl
```

This is Step 06 — do not write `claims.jsonl` manually or during extraction.

## Step 4 — Validate

```powershell
python agentic/04_claims_json/validate_claims.py `
  --claims agentic/04_claims_json/runs/2018-19_claims_claude_full/claims.jsonl `
  --sections agentic/03_section_splitting/runs/2018-19_section_split_pymupdf4llm_hardened/sections.jsonl
```

Validator must exit clean before the run can be marked PASS.

## Step 5 — Adversarial review

See `adv_review_prompt.md` in this folder for reviewer instructions.
Run or request the review only after the final validator passes.
Write findings to `adv_review_results.md` in this folder.
