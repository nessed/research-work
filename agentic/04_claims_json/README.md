# Step 04: Claims JSON

This is the canonical contract for Step 04. It must be strong enough that an
agent can be told only:

```text
<YEAR> Step 3 is done. Run Step 4.
```

and then produce the Step 04 output without manual chapter slicing or
hand-written claim files.

## Purpose

Step 04 converts a reviewed Step 03 `sections.jsonl` into one source-grounded
claims file:

```text
sections.jsonl
-> source_scope.json
-> jobs.jsonl
-> per-job extraction
-> job_results.jsonl
-> claims.jsonl
-> validator
-> adversarial review
```

Claims JSON is a working extraction layer. It records what the PES commentary
says, not verified facts. Every claim must trace to a Step 03 source section,
source page, and short source quote from the Markdown text.

Step 04 stops at `claims.jsonl`. Do not normalize, deduplicate into fact tables,
export to a database, or start Step 05/06 work inside Step 04.

## Autonomous Agent Handoff

Use this prompt for future agents:

```text
You are running Step 04 Claims JSON for <YEAR>. Find the PASS-reviewed Step 03
sections.jsonl for that year under agentic/03_section_splitting/runs/. Follow
agentic/04_claims_json/README.md and how_to_reproduce.md. Produce one final
claims.jsonl, validate it, write run evidence, run or prepare adversarial review,
and stop before Step 05.
```

The agent must discover the correct Step 03 run from the year, verify that it
has a PASS review, create the Step 04 run folder, execute the job-based flow,
and report PASS/FAIL with concrete paths.

## Required Inputs

- A reviewed, PASS-rated Step 03 `sections.jsonl` under
  `agentic/03_section_splitting/runs/`.
- The frozen schema:
  `agentic/archive/04_commentary_schema_discovery/schema/commentary_schema_v0.1.json`.
- The extraction prompt:
  `agentic/04_claims_json/extraction_prompt.md`.
- The structured-output schema for headless jobs:
  `agentic/04_claims_json/claim_array_output_schema.json`.
- The validator:
  `agentic/04_claims_json/validate_claims.py`.

Do not extract from unreviewed or in-progress section runs. Do not touch, move,
rewrite, or annotate raw PDFs during Step 04.

## Production Mechanics

Step 04 uses two scripts under each run's `_supporting/` folder.

### Step 1 — Build jobs (`gen_jobs.py`)

Each run ships a `_supporting/gen_jobs.py` that reads the Step 03 `sections.jsonl`,
applies the source scope (inclusions/exclusions), splits into 20-section jobs, and
writes `source_scope.json` and `jobs.jsonl`. Run it once from the repo root:

```powershell
python agentic/04_claims_json/runs/<run>/_supporting/gen_jobs.py
```

### Step 2 — Extract claims (`run_step04.py`)

The shared multi-engine runner at `agentic/04_claims_json/run_step04.py` powers
extraction. It reads `jobs.jsonl`, calls the chosen engine per job, accumulates
results in `_supporting/job_results.jsonl`, and tracks progress in
`_supporting/run_state.json`. It **never writes `claims.jsonl`** — that is
Step 06 finalize.

```powershell
python agentic/04_claims_json/run_step04.py `
  --engine <gemini|claude|codex> `
  --run-dir agentic/04_claims_json/runs/<run> `
  --schema-file agentic/04_claims_json/claim_array_output_schema.json `
  --prompt-file agentic/04_claims_json/extraction_prompt.md `
  --chunk <N> `
  --concurrency <N>
```

Available engines:

- `claude` — Claude Code subscription, headless non-bare OAuth. Default full-run
  engine. Chunk default: 3 sections/call.
- `gemini` — Google Gemini Flash, free tier via `google-genai` SDK. Bulk lane.
  Requires `GEMINI_API_KEY` env var. Chunk default: 8.
- `codex` — OpenAI Codex CLI. Scalpel/reserve; use via `--only-failed` passes.
  Chunk default: 1.

The runner is safely resumable: re-running the same command skips already-completed
jobs. Use `--only-failed` to reprocess exactly the jobs in `failed[]`. Use
`--shard`/`--num-shards` to split across two terminals with different engines.

Each job is a fresh model context. The model must extract claims only from the
section records inside that job. Final `claims.jsonl` is rebuilt from validated
job results in Step 06. Do not manually append model output directly to final
`claims.jsonl`.

## Source Scope

Before extraction, create `_supporting/source_scope.json`.

The source scope must list:

- input Step 03 run path;
- included `source_md_path` values;
- excluded `source_md_path` values;
- reason for every exclusion;
- source section counts.

Include all reviewed Step 03 source files unless a file is explicitly excluded.
Never silently skip files. If a full-survey Markdown file such as
`Pakistan_Es_2016_17_Pdf.md` duplicates chapter-level files, record the
exclusion and reason in `source_scope.json`.

## Required Run Layout

Create one run folder under:

```text
agentic/04_claims_json/runs/<year>_claims_<label>/
```

The run root must contain only:

```text
claims.jsonl
```

All other run evidence belongs under `_supporting/`:

```text
_supporting/source_scope.json
_supporting/jobs.jsonl
_supporting/job_results.jsonl
_supporting/run_state.json
_supporting/extraction_manifest.json
_supporting/extraction_report.md
_supporting/how_to_reproduce.md
_supporting/adv_review_prompt.md
_supporting/adv_review_results.md
_supporting/failed_jobs/        optional, only for failed/debug cases
```

Production runs must not create per-chapter `smoke_*_sections.jsonl` or
`smoke_*_claims.jsonl` files. Those are historical smoke-test artifacts only.

## Job Contract

Each line in `_supporting/jobs.jsonl` is one extraction job. A job must include:

- stable `job_id`;
- `source_year`;
- `source_file`;
- `source_md_path`;
- ordered `section_ids`;
- the section records for that job;
- job input hash;
- prompt hash;
- schema hash;
- runner/version label;
- engine name/version.

Resume behavior is hash-based. A completed job can be reused only if its input
hash, prompt hash, schema hash, runner/version label, and engine contract still
match. If any hash changes, rerun the job.

## Validation Gates

Step 04 has four gates.

1. Preflight gate, before extraction:
   - Step 03 run exists and has PASS adversarial review.
   - `sections.jsonl`, schema, prompt, and validator exist.
   - Source scope is explicit.
   - Every included section appears in exactly one job.

2. Per-job gate, after each model call:
   - Model output parses as JSON.
   - Output is an array of claim records.
   - Every record matches schema shape and controlled vocab.
   - `needs_human_review` is `true`.
   - Numeric-looking claims are flagged with both numeric QA booleans.
   - Source quotes trace to sections inside the current job.

3. Final validator gate, after merge:
   - Run `validate_claims.py` against final `claims.jsonl` and original
     Step 03 `sections.jsonl`.
   - Manifest count and SHA-256 must match final `claims.jsonl`.
   - No failed or stale jobs may remain.

4. Adversarial review gate:
   - Fresh reviewer verifies final output, source scope, counts, schema,
     grounding, numeric flags, and no fabricated claims.
   - Step 04 is not PASS until this review is PASS.

## Schema Rules

Use the frozen schema v0.1. Do not modify the schema during extraction. If a
genuinely new repeatable pattern appears that the schema cannot handle, document
it in the run report and flag it for future schema review.

Required fields per record include: `source_year`, `source_file`, `sector`,
`source_page`, `evidence_type`, `source_quote`, `claim_type`, `claim`,
`numeric_or_table_sensitive`, `requires_pdf_numeric_qa`,
`markdown_quality_flags`, `confidence`, and `needs_human_review`.

## PASS/FAIL Rule

Step 04 PASS requires all of the following:

- all included jobs completed;
- final `claims.jsonl` exists at the run root;
- final validator exits clean;
- manifest count/hash reconcile;
- `extraction_report.md` records PASS;
- `adv_review_results.md` records PASS.

If any condition fails, Step 04 is FAIL and must not feed Step 05.
