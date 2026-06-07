# How to Reproduce — Claims JSON Extraction (Stage Level)

Pipeline position: Sections JSONL → Claims JSONL

This file describes the stage-level procedure. Run-specific paths, commands,
model versions, and results belong in each run folder's own `how_to_reproduce.md`.

## Prerequisites

- A reviewed, PASS-rated `sections.jsonl` from a completed step-03 run under
  `agentic/03_section_splitting/runs/<year>_<label>/`.
- Do not extract from unreviewed or in-progress section runs.
- The frozen schema at
  `agentic/archive/04_commentary_schema_discovery/schema/commentary_schema_v0.1.json`.
- This stage's `extraction_prompt.md` (the single source of extraction rules).
- `validate_claims.py` (this stage folder) for post-extraction QA.

## Step 1 — Create the run folder

```
agentic/04_claims_json/runs/<year>_claims_<label>/
```

Use the same year and label as the source section run where possible.

## Step 2 — Identify the source files in the sections JSONL

Extract the distinct `source_md_path` values from `sections.jsonl`:

```python
import json
from collections import Counter
paths = Counter()
with open("sections.jsonl", encoding="utf-8") as f:
    for line in f:
        r = json.loads(line)
        paths[r["source_md_path"]] += 1
for p, n in sorted(paths.items()):
    print(n, p)
```

This gives you the list of documents to process and their section counts.
Record this list in the run's `extraction_manifest.json`.

## Step 3 — Extract claims per document

For each `source_md_path`:

1. Filter `sections.jsonl` to only that document's lines.
2. Feed those section records to the LLM using `extraction_prompt.md` as the
   system/task prompt. Model: `claude-sonnet-4-6`.
3. Receive a JSON array of claim records.
4. Append each claim record as one line to `claims.jsonl` (newline-delimited JSON).

Process documents one at a time. Do not batch multiple documents in one LLM call.

## Step 4 — QA

Run `validate_claims.py` against the completed `claims.jsonl` and the source
`sections.jsonl`:

```
python agentic/04_claims_json/validate_claims.py \
    --claims  agentic/04_claims_json/runs/<run>/claims.jsonl \
    --sections agentic/03_section_splitting/runs/<run>/sections.jsonl
```

Fix any validation errors and re-run until the script exits clean.

## Step 5 — Write run evidence files

Every run folder must contain:

- `claims.jsonl` — one JSON object per claim record, newline-delimited.
- `extraction_manifest.json` — input section run path, schema version used,
  model name and version, per-document record counts, total record count,
  SHA-256 hash of `claims.jsonl`, and run environment (OS, Python version, date).
- `extraction_report.md` — per-document claim counts, skipped sections and
  reasons, schema-fit notes (flagged future schema needs, not new fields),
  QA summary, and overall pass/fail judgement.
- `how_to_reproduce.md` — year, source section run path, schema version, exact
  prompt file used, model, QA command and result, run date, caveats.
- `adv_review_prompt.md` — run-specific fresh-context reviewer instructions.
- `adv_review_results.md` — reviewer findings and PASS/FAIL verdict.

## Step 6 — Adversarial review

A fresh-context reviewer (new Claude session, no memory of the extraction run)
must verify the run using `adv_review_prompt.md` before the output is used
downstream. The reviewer checks source grounding, controlled vocab, numeric
flagging, no fabricated quotes, and manifest/count reconciliation.

## Review gate

Do not pass `claims.jsonl` to step 05 (normalize) until `adv_review_results.md`
carries a PASS verdict.

## Source truth

Original PDFs remain source truth throughout. Markdown is a working text layer.
Table, chart, and numeric values from Markdown are not certified until separately
QA'd against the source PDFs.
