# Adversarial Review Prompt - 2016-17 Codex 200-Section Test

Review this bounded Step 04 test run only. Confirm that it used the canonical
artifact path, selected the first deterministic jobs from Step 03 until the
included section count was closest to 200, did not run full-year extraction,
and stopped before Step 05.

Check:
- `_supporting/source_scope.json`
- `_supporting/jobs.jsonl`
- `_supporting/job_results.jsonl`
- `claims.jsonl`
- `_supporting/extraction_manifest.json`
- `_supporting/extraction_report.md`
- `agentic/04_claims_json/validate_claims.py`
