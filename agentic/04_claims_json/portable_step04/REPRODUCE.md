# REPRODUCE — Step 04 Claims JSON (portable run guide)

Command-by-command. Run everything from the package root (`portable_step04/`).
Windows PowerShell syntax (backtick line-continuation). On macOS/Linux, replace
the backticks with `\`.

```
sections.jsonl  ->  build jobs  ->  run extraction (claude)  ->  finalize  ->  validate  ->  stop
```

---

## 0. Prerequisites (one-time, on this machine)

- **Python 3.10+** on PATH.
- **Claude Code CLI** installed and available as `claude` (or `claude.cmd` on Windows).
- That CLI **logged into the professor's Claude Max account** (`claude` interactive
  once, or `claude setup-token`). Auth is machine-level — there is no per-command flag.
- **No Anthropic API key needed.** This uses the subscription via non-bare `claude -p`.

## 1. (Optional) install Python deps

```powershell
pip install -r requirements.txt
```
Optional — it only adds an in-runner schema check. The final validator is pure
stdlib and runs without it. Skip on locked-down machines.

## 2. Check Python works

```powershell
python --version
```
Expect `Python 3.10` or higher.

## 3. Check Claude Code auth (non-bare, subscription)

```powershell
claude -p "reply with the single word ok" --output-format json --max-turns 1
```
Expect JSON containing `"is_error": false` and a result of `ok`. If this errors or
asks you to log in, fix auth before continuing (log in as the Max account). Do
**not** add `--bare`.

## 4. Choose the Step 03 input

Place your reviewed Step 03 file at `input/<year>/sections.jsonl` (see
`input/README.md`). List what's available:

```powershell
Get-ChildItem input -Directory | Select-Object Name
```

Pick the year, e.g. `2018-19`. Target file: `input/2018-19/sections.jsonl`.

## 5. Run the tiny smoke FIRST (do not skip)

Prove the package works on this machine using the bundled 5-section sample —
see `sample/README.md`. Offline scaffolding check, then a 1-job live check, then
delete `runs/_smoke`. Only proceed once you see `FINALIZE OK` and `RESULT: PASS`.

## 6. Build jobs from your chosen year

Set a run folder name, e.g. `runs/2018-19_claims_claude`. Recommended exclusions
for a typical year (adjust filenames to the actual files in your input):

```powershell
python engine/build_jobs.py `
  --sections input/2018-19/sections.jsonl `
  --run-dir runs/2018-19_claims_claude `
  --year 2018-19 `
  --sections-per-job 20 `
  --exclude "Economic_Survey_2018_19.md=Duplicate full-survey Markdown; chapter files are canonical" `
  --exclude "Supplement_2018_19.md=Statistical tables supplement; no narrative claims" `
  --exclude "Annex_I.md=Statistical annex tables; no narrative claims" `
  --exclude "Annex_Ii.md=Statistical annex tables; no narrative claims" `
  --exclude "Economic_Indicators_1819.md=Indicator tables; no narrative claims" `
  --prompt-file config/extraction_prompt.md `
  --schema-file config/claim_array_output_schema.json
```

Notes:
- Every `--exclude` **must** be `FILENAME=REASON`; a bare filename is rejected.
- If a filename you pass isn't in the input, the builder stops and lists the real
  filenames — copy the correct ones from that list.
- Output: `runs/2018-19_claims_claude/_supporting/jobs.jsonl` + `source_scope.json`.

## 7. Run Step 04 extraction (Claude)

First a dry-run to see the exact `claude` argv (uses MCP config `{"mcpServers":{}}`,
`--max-turns 1`, non-bare, `--permission-mode plan` — all baked in):

```powershell
python engine/run_step04.py --engine claude `
  --run-dir runs/2018-19_claims_claude `
  --schema-file config/claim_array_output_schema.json `
  --prompt-file config/extraction_prompt.md `
  --chunk 3 --concurrency 1 --dry-run
```

Then the real run. **Use small chunk + low concurrency** — this avoids the known
Windows parallel-Claude failure and oversized single-call outputs:

```powershell
python engine/run_step04.py --engine claude `
  --run-dir runs/2018-19_claims_claude `
  --schema-file config/claim_array_output_schema.json `
  --prompt-file config/extraction_prompt.md `
  --chunk 3 --concurrency 1 --rpm 20
```

- **Resumable:** re-running the same command skips completed jobs.
- **Retry failures only:** add `--only-failed --concurrency 1`.
- Per-job results accumulate in `_supporting/job_results.jsonl`; progress in
  `_supporting/run_state.json`. The runner never writes `claims.jsonl`.
- Failures land in `_supporting/failed_jobs/<job_id>.txt` — each now includes the
  source file, section IDs, page range, headings, numeric flag, and a text preview
  so you can see exactly what content failed, not just the error.

## 8. Finalize claims.jsonl

```powershell
python engine/finalize_claims.py --run-dir runs/2018-19_claims_claude
```

This **fails hard** unless the run fully reconciles (no failed jobs, every job
completed and present, counts match). Only then does it write
`runs/2018-19_claims_claude/claims.jsonl`. It prints the claim count and a sha256.
If it blocks, read the `[BLOCK]` lines, fix (usually `--only-failed`), and re-run.

## 9. Validate

```powershell
python engine/validate_claims.py `
  --claims runs/2018-19_claims_claude/claims.jsonl `
  --sections input/2018-19/sections.jsonl
```

## 10. Success / failure

- **PASS:** `finalize` printed `FINALIZE OK` **and** the validator printed
  `RESULT: PASS` (0 errors, 0 grounding failures). Warnings about files with no
  claims are expected for excluded/sparse files.
- **FAIL:** validator prints `RESULT: FAIL` with `[ERROR]`/`[GROUND]` lines, or
  finalize blocked. Do not pass FAIL output downstream.

## 11. Copy results back to the main repo

Bring back the whole run folder (final output + all evidence):

```
runs/<year>_claims_claude/claims.jsonl
runs/<year>_claims_claude/_supporting/   (jobs.jsonl, job_results.jsonl, run_state.json,
                                          source_scope.json, failed_jobs/)
```

Place it under `agentic/04_claims_json/runs/<year>_claims_claude/` in the main
repo. **Stop here — do not normalize or export.**
