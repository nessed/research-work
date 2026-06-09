# Current Progress

Last updated: 2026-06-08

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

Step 04 (claims extraction) — portability + engine reliability. A self-contained
portable Step 04 package was built to run on an external Claude (Max/Pro) machine
from an already-finished Step 03 `sections.jsonl`. Currently being tested on a
fresh download against a Claude Pro plan.

## Portable Step 04 Package (new)

- Location: `agentic/04_claims_json/portable_step04/` + zip `portable_step04.zip`.
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
  writes → validate RESULT: PASS. Live Claude smoke not yet run.
- Aligned run recipe (replaces the old failing `--chunk 20 --concurrency 3`):
  `--engine claude --chunk 3 --concurrency 1`.

## Step 04 failure context (for memory)

The recurring Step 04 struggle is **not documented as token limits** anywhere in the
repo. Evidence (`git b94aa5b` + two `diagnose_claude_parallel*.py` probes that saved
no output) points to **Claude parallel execution on Windows**, worsened by oversized
single-call chunks. Codex 200-sec test was the only engine that passed cleanly.

## Critical Path

```
[now] → test portable_step04 on external Claude plan (Pro now, Max later)
      → tiny live smoke (sample/) must PASS on that machine
      → real per-year Step 04 runs (start 2018-19: jobs already buildable)
      → step 03 100% complete for all 10 years (feed more years into 04)
```

## Notes

- Step 02 uses no LLM tokens (local pymupdf4llm library). All 10 years PASS audited.
- Step 03 uses no LLM tokens (deterministic regex script). Use `split_2016_17_sections.py` as template.
- Step 04 is the only token-heavy step. Engine reliability (not schema) is the open risk.
- Step 04 stage files already exist (`extraction_prompt.md`, `claim_array_output_schema.json`,
  `validate_claims.py`, `run_step04.py`, per-year `gen_jobs.py`); the portable package
  bundles the needed subset plus the new generic builder + finalizer.
- Per-MD chunking strategy: slice `sections.jsonl` by `source_md_path` at runtime; feed one doc at a time to LLM; cat outputs into one `claims.jsonl` per year.
- Normalization (step 05) is global across all years — do not normalize per-year or per-shard.

## Next Immediate Actions

1. Test `portable_step04` on the external Claude plan (fresh download, Claude Pro now).
2. Run the tiny live smoke (`sample/`) on that machine; confirm parallel-Claude works there.
3. On PASS, run a real year (2018-19 jobs already buildable) with `--chunk 3 --concurrency 1`.
