# sample/ — tiny smoke test

`sample_sections.jsonl` holds **5 real** Step 03 section records (2018-19
Agriculture). It exists so you can prove the plumbing end-to-end on a tiny input
before committing a full year.

## A) Offline scaffolding check (no LLM, no Claude needed)

From the package root (`portable_step04/`):

```powershell
# 1. build jobs from the sample
python engine/build_jobs.py `
  --sections sample/sample_sections.jsonl `
  --run-dir runs/_smoke `
  --year 2018-19 `
  --sections-per-job 3 `
  --prompt-file config/extraction_prompt.md `
  --schema-file config/claim_array_output_schema.json
```

This writes `runs/_smoke/_supporting/jobs.jsonl` + `source_scope.json`. No model
is called. Delete `runs/_smoke` afterwards — it is throwaway.

## B) Tiny live smoke (uses 1-2 Claude calls — run on the professor's PC)

After the auth check in `../REPRODUCE.md` passes:

```powershell
python engine/run_step04.py --engine claude `
  --run-dir runs/_smoke `
  --schema-file config/claim_array_output_schema.json `
  --prompt-file config/extraction_prompt.md `
  --chunk 3 --concurrency 1

python engine/finalize_claims.py --run-dir runs/_smoke
python engine/validate_claims.py --claims runs/_smoke/claims.jsonl --sections sample/sample_sections.jsonl
```

Expect `FINALIZE OK` then `RESULT: PASS`. If you see that, the package works on
this machine and you can proceed to a real year. Then delete `runs/_smoke`.
