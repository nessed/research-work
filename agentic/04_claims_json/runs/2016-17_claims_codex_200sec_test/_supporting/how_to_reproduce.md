# How to Reproduce - 2016-17 Codex 200-Section Test

Run from repository root:

```powershell
python agentic\04_claims_json\runs\2016-17_claims_codex_200sec_test\_supporting\run_codex_200sec_test.py
```

The runner discovers and uses:

- Step 03 sections: `agentic/03_section_splitting/runs/2016-17_section_split_pymupdf4llm_hardened/sections.jsonl`
- Prompt: `agentic/04_claims_json/extraction_prompt.md`
- Structured output schema: `agentic/04_claims_json/claim_array_output_schema.json`
- Validator: `agentic/04_claims_json/validate_claims.py`

The runner builds `source_scope.json`, `jobs.jsonl`, and `job_results.jsonl`,
then rebuilds run-root `claims.jsonl` and runs the validator. It uses
fresh `codex.cmd exec --ephemeral --sandbox read-only` calls with
`--output-schema` for each job.
