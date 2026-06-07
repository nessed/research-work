# How to Reproduce - 2016-17 Claims Smoke Test

Run: `2016-17_claims_pymupdf4llm_hardened`  
Date: 2026-06-07  
Status: smoke-test evidence only

## Production Status

This folder records the first Step 04 smoke test. It is not the production
pattern for full-year extraction.

Future Step 04 runs must follow the autonomous job-based contract in
`agentic/04_claims_json/README.md`:

```text
sections.jsonl -> source_scope.json -> jobs.jsonl -> job_results.jsonl -> claims.jsonl
```

Do not reproduce the `smoke_*_sections.jsonl` and `smoke_*_claims.jsonl` pattern
for production runs. Those files were temporary chapter slices for this smoke
test only.

## Source

- Input sections JSONL:
  `agentic/03_section_splitting/runs/2016-17_section_split_pymupdf4llm_hardened/sections.jsonl`
  (PASS-reviewed, 2,121 sections, 25 source files)
- Schema:
  `agentic/archive/04_commentary_schema_discovery/schema/commentary_schema_v0.1.json`
- Extraction prompt:
  `agentic/04_claims_json/extraction_prompt.md`
- Model: `claude-sonnet-4-6`

## Smoke-Test Scope

Three source files were extracted:

- `Agriculture.md`: 66 sections -> 32 claims
- `Health.md`: 41 sections -> 20 claims
- `Trade.md`: 46 sections -> 21 claims

## Historical Steps

1. Filtered the Step 03 `sections.jsonl` by `source_md_path` for each target
   document:
   - `smoke_agriculture_sections.jsonl`
   - `smoke_health_sections.jsonl`
   - `smoke_trade_sections.jsonl`
2. Applied the Step 04 extraction prompt to each document's sections.
3. Wrote per-document smoke claim files:
   - `smoke_agriculture_claims.jsonl`
   - `smoke_health_claims.jsonl`
   - `smoke_trade_claims.jsonl`
4. Combined those records into final run-root `claims.jsonl`.
5. Ran `validate_claims.py` against the final `claims.jsonl` and the original
   Step 03 `sections.jsonl`.

Validation result: PASS, with 0 errors and 0 grounding failures. Coverage
warnings were expected because this was a 3-file smoke scope, not full-year
extraction.

## Caveats

- `gen_agriculture_claims.py` is a stale smoke-test helper and must not be used
  as a production runner.
- Health and Trade were generated directly in-session; there are no production
  `gen_health` or `gen_trade` scripts.
- The current production contract requires deterministic jobs and
  `job_results.jsonl`; this smoke test predates that structure.
- SHA-256 of root `claims.jsonl`:
  `dd65e72b7f6dd39bc8b1e267c5b921e12324c111fef6ad9d6a4236fbce2f358e`.
