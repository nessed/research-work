# Current Progress

Last updated: 2026-06-11

## Pipeline Status — All Years

| Year | 02 PDF→MD | 03 Sections | 04 Claims |
|---|---|---|---|
| 2015-16 | ✅ PASS audited | ✅ PASS (1,157 sections) | ❌ |
| 2016-17 | ✅ PASS audited | ✅ PASS (2,121 sections) | ⬜ empty stub |
| 2017-18 | ✅ PASS audited | ✅ PASS (2,234 sections) | ❌ |
| 2018-19 | ✅ PASS audited | ✅ PASS (2,736 sections) | ❌ |
| 2019-20 | ✅ PASS audited | ✅ PASS (1,664 sections) | ❌ |
| 2020-21 | ✅ PASS audited | ✅ PASS (1,136 sections) | ❌ |
| 2021-22 | ✅ PASS audited | ✅ PASS (1,061 sections) | ❌ |
| 2022-23 | ✅ PASS audited | ✅ PASS (2,239 sections) | ❌ |
| 2023-24 | ✅ PASS audited | ✅ PASS (2,267 sections) | ❌ |
| 2024-25 | ✅ PASS audited | ✅ PASS (1,227 sections) | ❌ |
| **Totals** | **10/10 PASS audited** | **10/10 PASS** | **0/10 production-ready** |

## Active Area

Step 04 (claims extraction) — first real per-year run. Extraction is now executed
by an **independent, tried-and-tested portable runner** hosted at
https://github.com/nessed/portable-claims-extractor. This repo only points jobs at
that runner; the runner owns the engine/parallelism mechanics. It has **passed a
live Claude smoke run** (`runs/_smoke_run_step04/`: 1 job completed, 0 failed,
engine=claude, 2026-06-07), so Step 04 **runs** reliably. The full 2018-19 job set
is **built** (`runs/2018-19_claims_claude_full/_supporting/jobs.jsonl`, ~1.6 MB)
but **not yet executed/finalized** — no `claims.jsonl` exists for any year yet, so
Step 04 is 0/10 production-ready (machinery proven, production data pending). Next
concrete step is to execute that 2018-19 job set through the runner, finalize,
validate, then adversarially review it.

## Portable Step 04 Package

- **Independent runner repo (canonical):** https://github.com/nessed/portable-claims-extractor
  — tried and tested; this is what actually executes Step 04 extraction. The local
  `agentic/04_claims_json/` only builds jobs and points them at this runner.
- Local mirror: `agentic/04_claims_json/portable_step04/` + zip `portable_step04.zip`.
- Purpose: run Step 04 on another PC (professor's Claude Max) with only Python +
  Claude Code CLI. No API key; non-bare `claude -p`; MCP config `{"mcpServers":{}}`.
- Contents: `PROMPT.md`, `REPRODUCE.md`, `PORTABLE.md`, `requirements.txt` (jsonschema
  optional), `engine/` (run_step04.py [+rich failure-context edit], validate_claims.py,
  build_jobs.py [NEW, generic], finalize_claims.py [NEW]), `config/` (prompt + schema),
  `input/`, `runs/`, `sample/` (5 real 2018-19 Agriculture sections).
- Closed two pipeline gaps: a **generic job builder** (year-agnostic, reason-bearing
  `--exclude FILENAME=REASON`) and the missing **finalizer** (`job_results.jsonl` →
  `claims.jsonl` with a hard reconciliation gate — no partial output).
- Verified offline (no LLM): build_jobs → finalize fail-path blocks → reconciled path
  writes → validate RESULT: PASS.
- Live Claude smoke now PASSED: `runs/_smoke_run_step04/` (1 job completed, 0 failed,
  `last_engine: claude`, 2026-06-07) — parallel-Claude path works end-to-end on one job.
- Aligned run recipe (replaces the old failing `--chunk 20 --concurrency 3`):
  `--engine claude --chunk 3 --concurrency 1`.

## Step 04 failure context (resolved)

The earlier Step 04 struggle was **not token limits**. Evidence (`git b94aa5b` + two
`diagnose_claude_parallel*.py` probes that saved no output) pointed to **Claude
parallel execution on Windows**, worsened by oversized single-call chunks. This is
now **resolved**: extraction was moved to the independent portable runner
(https://github.com/nessed/portable-claims-extractor) with the `--chunk 3
--concurrency 1` recipe, which is tried and tested and passed the live smoke run.

## Critical Path

```
[done] portable_step04 engine built + live Claude smoke PASS (1 job)
[done] 2018-19 full job set built (jobs.jsonl ~1.6 MB)
[now]  → execute 2018-19 full run → finalize (job_results → claims.jsonl)
       → validate_claims PASS gate → adversarial review of 2018-19 claims
       → roll out remaining 9 years' Step 04 runs (Step 03 already 10/10)
```

## Notes

- Step 02 uses no LLM tokens (local pymupdf4llm library). All 10 years PASS audited.
- Step 03 uses no LLM tokens (deterministic regex script). Use `split_2016_17_sections.py` as template.
- Step 04 is the only token-heavy step. Engine reliability is resolved: extraction
  runs on the independent portable runner (https://github.com/nessed/portable-claims-extractor),
  tried and tested. Remaining work is executing/finalizing per-year production runs, not the engine.
- Step 04 stage files already exist (`extraction_prompt.md`, `claim_array_output_schema.json`,
  `validate_claims.py`, `run_step04.py`, per-year `gen_jobs.py`); the portable package
  bundles the needed subset plus the new generic builder + finalizer.
- Per-MD chunking strategy: slice `sections.jsonl` by `source_md_path` at runtime; feed one doc at a time to LLM; cat outputs into one `claims.jsonl` per year.
- Normalization (step 05) is global across all years — do not normalize per-year or per-shard.

## Next Immediate Actions

1. Execute the built 2018-19 full job set (`runs/2018-19_claims_claude_full/_supporting/jobs.jsonl`)
   with `--engine claude --chunk 3 --concurrency 1`.
2. Finalize (`job_results.jsonl` → `claims.jsonl`, hard reconciliation gate) and run
   `validate_claims.py` — must PASS before the output counts.
3. Run a fresh-context adversarial review of the 2018-19 claims, then roll out the
   remaining 9 years.
