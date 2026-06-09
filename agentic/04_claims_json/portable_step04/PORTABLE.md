# PORTABLE.md — what this package is, why, and how to rebuild it

Context/memory note for the maintainer (Ali). This is the self-contained Step 04
package meant to run on another PC — specifically a professor's **Claude Max** PC —
to extract Claims JSON from an already-finished Step 03 `sections.jsonl`.

## Why this exists

Step 04 is the only token-heavy stage and the one that kept failing. The documented
struggle (`git b94aa5b` "before claude overhaul oim still struggling w last stage")
was **Claude parallel execution on Windows**, made worse by the old 2018-19 runbook's
`--chunk 20 --concurrency 3` (one oversized call per job × 3 in parallel). Two pieces
were also missing from the shared path: a **finalizer** (nothing built `claims.jsonl`
from job results) and a **generic job builder** (only per-year hardcoded `gen_jobs.py`
existed). This package fixes both and ships an aligned, low-risk run recipe.

## What the zip contains

```
PROMPT.md        Operator prompt to paste into Claude on the target PC.
REPRODUCE.md     Exact command-by-command run guide.
PORTABLE.md      This file.
requirements.txt Optional jsonschema; everything works without it.
engine/
  run_step04.py      Multi-engine runner. COPIED from the repo, with ONE edit:
                     record_failure() now writes content context (source file,
                     section ids, page range, headings, numeric flag, text
                     preview) into _supporting/failed_jobs/<job_id>.txt.
  validate_claims.py COPIED verbatim. The Step 04 gate. Pure stdlib.
  build_jobs.py      NEW. Year-agnostic: sections.jsonl -> jobs.jsonl. Excludes
                     are explicit and reason-bearing (--exclude FILENAME=REASON).
  finalize_claims.py NEW. job_results.jsonl -> claims.jsonl with a hard
                     reconciliation gate (no partial output).
config/
  extraction_prompt.md            COPIED verbatim. The --prompt-file.
  claim_array_output_schema.json  COPIED verbatim. The --json-schema (array of
                                  29-key claim objects, additionalProperties:false).
input/           Drop your Step 03 sections.jsonl here as input/<year>/sections.jsonl.
runs/            Step 04 outputs land here (one folder per run).
sample/          5 real 2018-19 Agriculture sections + a tiny smoke-test guide.
```

## Source repo files copied from

| Package path | Copied from |
|---|---|
| `engine/run_step04.py` | `agentic/04_claims_json/run_step04.py` (+ failure-context edit) |
| `engine/validate_claims.py` | `agentic/04_claims_json/validate_claims.py` |
| `config/extraction_prompt.md` | `agentic/04_claims_json/extraction_prompt.md` |
| `config/claim_array_output_schema.json` | `agentic/04_claims_json/claim_array_output_schema.json` |
| `sample/sample_sections.jsonl` | first 5 substantive Agriculture records of `agentic/03_section_splitting/runs/2018-19_section_split_pymupdf4llm_hardened/sections.jsonl` |

`build_jobs.py` reimplements the logic of
`agentic/04_claims_json/runs/2018-19_claims_claude_full/_supporting/gen_jobs.py`
in a generic, parameterized form.

## What it intentionally does NOT include

- No raw PDFs, no `Master Data/`, no other pipeline stages.
- No per-year run folders or sitreps.
- No Gemini/Codex setup. `run_step04.py` still contains those lanes internally, but
  the docs/sample are Claude-only; Gemini needs `google-genai` + an API key (which
  this package deliberately avoids), and Codex needs its own CLI.
- No normalization (Step 05) or export (Step 06) anything.

## Assumptions

- The target machine has Python 3.10+ and the Claude Code CLI logged into the Max
  account; auth is machine-level.
- The input `sections.jsonl` is a **PASS-reviewed** Step 03 output with the standard
  fields (`section_id`, `source_md_path`, `start_page`, `end_page`, `heading_text`,
  `numeric_or_table_sensitive`, `text`, ...).
- Windows PowerShell is the documented shell; commands map directly to bash.

## Run recipe (aligned, not the old failing one)

`--engine claude --chunk 3 --concurrency 1 [--rpm 20]`. Small chunk keeps each
model response short and well-formed; concurrency 1 sidesteps the Windows
parallel-Claude failure. Scale concurrency cautiously (2) only after a clean run.

## How to rebuild the zip if the main repo changes

From repo root:
1. Re-copy the four source files into `engine/` and `config/` (re-apply the
   `record_failure()` edit to `run_step04.py` — see `engine/run_step04.py` for the
   `summarize_job_context` helper and its call site).
2. Re-check syntax: `python -m py_compile engine/*.py`.
3. Re-zip:
   ```powershell
   Compress-Archive -Path agentic/04_claims_json/portable_step04/* `
     -DestinationPath agentic/04_claims_json/portable_step04.zip -Force
   ```
`build_jobs.py` and `finalize_claims.py` are original to this package — they have no
upstream to track, but keep them in sync if the job/result/run_state formats in
`run_step04.py` ever change.
