# Extraction Report - 2016-17 Codex 200-Section Test

Status: PASS

This is a bounded test run only. It uses the documented Step 04 path:

```text
sections.jsonl -> source_scope.json -> jobs.jsonl -> job_results.jsonl -> claims.jsonl -> validator
```

It does not run full-year 2016-17 extraction and does not start Step 05.

## Scope

- Selection rule: Group sections by first-seen source_md_path in sections.jsonl, keep original section order, split into 20-section jobs, then include the first jobs whose cumulative section count is closest to the target.
- Target sections: 200
- Selected jobs: 7
- Included sections: 98
- Included source files: 4
- Excluded/partial source entries recorded: 21

## Extraction

- Engine: codex.cmd exec
- Fresh calls: yes, one `--ephemeral` call per job
- Sandbox: read-only
- Completed jobs: 7
- Failed jobs: 0
- Claim records: 225

## Validation

- Validator return code: 0

```text
Loading claims: C:\Users\Ali\Desktop\datalab_ali\agentic\04_claims_json\runs\2016-17_claims_codex_200sec_test\claims.jsonl
  225 lines loaded
Loading sections: C:\Users\Ali\Desktop\datalab_ali\agentic\03_section_splitting\runs\2016-17_section_split_pymupdf4llm_hardened\sections.jsonl
  2121 sections across 25 files

============================================================
VALIDATION REPORT
============================================================
Total claim records:  225
Parse errors:         0
Errors:               0
Grounding failures:   0
Warnings:             21

Claims per source file:
   139  Agriculture.md
    27  Annex_I_Nfis.md
    25  Annex_Ii_Eco.md
    34  Annex_Iii_Cpec.md

WARNINGS (21):
  [WARN] No claims extracted for source file: Annex_Iv_War.md
  [WARN] No claims extracted for source file: Annex_V_Contingent.md
  [WARN] No claims extracted for source file: Annex_Vi_Tax_Expenditure.md
  [WARN] No claims extracted for source file: Captial_Markets.md
  [WARN] No claims extracted for source file: Climate_Change.md
  [WARN] No claims extracted for source file: Economic_Indicators.md
  [WARN] No claims extracted for source file: Education.md
  [WARN] No claims extracted for source file: Energy.md
  [WARN] No claims extracted for source file: Fiscal.md
  [WARN] No claims extracted for source file: Growth.md
  [WARN] No claims extracted for source file: Health.md
  [WARN] No claims extracted for source file: Inflation.md
  [WARN] No claims extracted for source file: Manufacturing.md
  [WARN] No claims extracted for source file: Money_And_Credit.md
  [WARN] No claims extracted for source file: Overview_2016_17.md
  [WARN] No claims extracted for source file: Pakistan_Es_2016_17_Pdf.md
  [WARN] No claims extracted for source file: Population.md
  [WARN] No claims extracted for source file: Public_Debt.md
  [WARN] No claims extracted for source file: Social_Safety_Nets.md
  [WARN] No claims extracted for source file: Trade.md
  [WARN] No claims extracted for source file: Transport_And_Communications.md

RESULT: PASS

```

## Caveats

- This is not a Step 04 PASS for the full 2016-17 year.
- Coverage warnings are expected because the run intentionally excludes most Step 03 sections.
- Numeric/table-sensitive claims still require PDF numeric QA downstream.
