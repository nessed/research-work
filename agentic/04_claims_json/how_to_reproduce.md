# How to Reproduce - Claims JSON Extraction

Pipeline position:

```text
Step 03 sections.jsonl -> Step 04 claims.jsonl
```

This is the stage-level runbook for agents. Run-specific paths, counts, hashes,
engine versions, and results belong in each run folder's
`_supporting/how_to_reproduce.md`.

## Minimal Agent Instruction

An agent should be able to run Step 04 from this instruction:

```text
<YEAR> Step 3 is done. Run Step 4.
```

The agent must discover the Step 03 run, create a Step 04 run folder, create
jobs, extract claims by job, validate, write governance files, and stop before
Step 05.

## Prerequisites

- A PASS-reviewed Step 03 run under `agentic/03_section_splitting/runs/`.
- The Step 03 run contains `sections.jsonl` and `adv_review_results.md`.
- The Step 04 schema exists at
  `agentic/archive/04_commentary_schema_discovery/schema/commentary_schema_v0.1.json`.
- The Step 04 extraction prompt exists at
  `agentic/04_claims_json/extraction_prompt.md`.
- The Step 04 structured-output schema exists at
  `agentic/04_claims_json/claim_array_output_schema.json`.
- The Step 04 validator exists at
  `agentic/04_claims_json/validate_claims.py`.
- Claude Code headless is available as `claude.cmd --print`.

Use `claude.cmd`, not `claude`, on Windows because PowerShell may block the
`.ps1` launcher.

## Step 1 - Discover the Step 03 input

Given a year such as `2016-17`, find the matching PASS-reviewed Step 03 run:

```text
agentic/03_section_splitting/runs/<year>_section_split_*/
```

Preflight checks:

- `sections.jsonl` exists.
- `adv_review_results.md` exists and says PASS.
- All section records parse as JSON.
- Section records include `section_id`, `source_year`, `source_md_path`,
  `source_pdf_path`, `sector`, `heading_text`, `start_page`, `end_page`,
  `section_type`, `numeric_or_table_sensitive`, `markdown_quality_flags`, and
  `text`.

If multiple Step 03 runs match the same year, use the newest PASS-reviewed
`*_hardened` run unless the user named a different run.

## Step 2 - Create the Step 04 run folder

Create:

```text
agentic/04_claims_json/runs/<year>_claims_<label>/
```

The run root is final-output-only:

```text
claims.jsonl
```

Create `_supporting/` for all other files.

## Step 3 - Build source_scope.json

Read the full Step 03 `sections.jsonl` and count sections by `source_md_path`.

Write:

```text
_supporting/source_scope.json
```

The source scope must explicitly record included and excluded source files. Do
not silently skip any source file.

For years where Step 03 includes both chapter-level files and a duplicate
full-survey file, exclude the duplicate only if this is recorded, for example:

```json
{
  "source_md_path": "agentic/02_pdf_to_md/runs/2016-17_pymupdf4llm_hardened/converted_md/Pakistan_Es_2016_17_Pdf.md",
  "reason": "Duplicate full-survey Markdown; chapter-level files are the extraction source for this Step 04 run."
}
```

## Step 4 - Create jobs.jsonl

Group included sections by `source_md_path`. Within each source file, keep the
original section order and split into jobs:

- default: 20 sections per job;
- if a 20-section job is too large for a model call, split it smaller;
- never split one section record across jobs;
- if one section is huge, process that section alone.

Write one line per job to:

```text
_supporting/jobs.jsonl
```

Each job must contain stable metadata: `job_id`, source file/path, ordered
section ids, section records, input hash, prompt hash, schema hash, runner label,
and engine contract.

Example with 20-section jobs:

```text
Agriculture.md, 66 sections -> 4 jobs
Health.md, 41 sections -> 3 jobs
Trade.md, 46 sections -> 3 jobs
```

## Step 5 - Run extraction jobs

For each incomplete job:

1. Create a fresh prompt from:
   - `extraction_prompt.md`;
   - schema v0.1;
   - only the section records inside the current job.
2. Run Claude headlessly. The `--json-schema` argument must receive the JSON
   schema content, so the runner should read
   `agentic/04_claims_json/claim_array_output_schema.json` and pass that string:

```powershell
$schema = Get-Content -Raw agentic/04_claims_json/claim_array_output_schema.json
claude.cmd --print --output-format json --json-schema $schema "<job prompt>"
```

3. Parse the model output as JSON.
4. Validate the job output before accepting it.
5. Append accepted job output to:

```text
_supporting/job_results.jsonl
```

6. Update:

```text
_supporting/run_state.json
```

If a job fails parsing, schema validation, quote grounding, or numeric-flag
checks, save the failure under `_supporting/failed_jobs/` and stop or retry that
job. Do not continue as if the run passed.

## Step 6 - Finalize claims.jsonl

When all included jobs are complete, rebuild final output from
`_supporting/job_results.jsonl` in stable job order:

```text
agentic/04_claims_json/runs/<run>/claims.jsonl
```

Do not manually append model output directly into final `claims.jsonl`.

## Step 7 - Run final validator

Run the Step 04 validator against final claims and the original Step 03 sections:

```powershell
python agentic/04_claims_json/validate_claims.py `
  --claims agentic/04_claims_json/runs/<run>/claims.jsonl `
  --sections agentic/03_section_splitting/runs/<step03_run>/sections.jsonl
```

If this Python launcher is unavailable on Windows, use the real Python path
recorded by the Step 03 manifest or environment. The validator must exit clean
before Step 04 can pass.

## Step 8 - Write run evidence

Write these files under `_supporting/`:

- `extraction_manifest.json`: input path, source scope, schema/prompt hashes,
  job counts, claim counts, output SHA-256, engine/version, date, environment.
- `extraction_report.md`: source scope summary, per-source claim counts, failed
  or skipped jobs, validator result, caveats, PASS/FAIL.
- `how_to_reproduce.md`: exact paths and commands used for this run.
- `adv_review_prompt.md`: run-specific reviewer instructions.
- `adv_review_results.md`: reviewer findings.

## Step 9 - Adversarial review

Only after final validator PASS, run or request a fresh-context adversarial
review. The reviewer checks final `claims.jsonl`, original `sections.jsonl`,
source scope, manifest, report, schema, and validator result.

Step 04 is PASS only if:

- every included job completed;
- final validator passed;
- manifest count/hash reconcile;
- adversarial review passed.

## Smoke Tests

Smoke tests may use a small source scope such as Agriculture, Health, and Trade.
They must still follow the same job/result/finalize/validate gates.

Do not use the old `smoke_*_sections.jsonl` and `smoke_*_claims.jsonl` pattern
for production runs. Those files are historical evidence from the first smoke
test, not the scalable Step 04 method.
