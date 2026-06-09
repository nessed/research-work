#!/usr/bin/env python3
"""finalize_claims.py - deterministic Step 04 finalizer (the missing "sub-step 6").

Pipeline position:
    run_step04.py -> _supporting/job_results.jsonl -> [THIS SCRIPT] -> claims.jsonl

run_step04.py intentionally never writes claims.jsonl. This script rebuilds the
final, year-level claims.jsonl from the accumulated per-job results, in stable
job order, and ONLY when the run fully reconciles.

Fail-hard contract (writes nothing, exits non-zero) if any of:
  - any failed job remains in run_state.json;
  - any job in jobs.jsonl is not in run_state.json completed[] (run incomplete);
  - any completed job has no record in job_results.jsonl (missing result);
  - a job_id appears more than once in job_results.jsonl (duplicate);
  - counts do not reconcile: total jobs == completed == distinct results.

A partial run cannot produce a final claims.jsonl by design. There is no
--allow-partial. Pure standard library.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    records: list[dict] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                sys.exit(f"{path}:{line_no}: invalid JSON: {exc}")
    return records


def die(messages: list[str]) -> "None":
    print("FINALIZE FAILED - run does not reconcile; no claims.jsonl written.\n", file=sys.stderr)
    for m in messages:
        print(f"  [BLOCK] {m}", file=sys.stderr)
    raise SystemExit(1)


def finalize(run_dir: Path) -> int:
    supporting = run_dir / "_supporting"
    jobs_path = supporting / "jobs.jsonl"
    state_path = supporting / "run_state.json"
    results_path = supporting / "job_results.jsonl"

    for label, p in (("jobs.jsonl", jobs_path), ("run_state.json", state_path),
                     ("job_results.jsonl", results_path)):
        if not p.exists():
            sys.exit(f"required input missing: {p}\n(has run_step04.py been run for this run-dir?)")

    expected_ids = [j.get("job_id") for j in read_jsonl(jobs_path)]
    expected_set = set(expected_ids)

    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.exit(f"{state_path}: invalid JSON: {exc}")
    completed = set(state.get("completed", []) or [])
    failed = set(state.get("failed", []) or [])

    results = read_jsonl(results_path)
    result_ids = [r.get("job_id") for r in results]

    problems: list[str] = []

    # 1. No failed jobs may remain.
    if failed:
        problems.append(f"{len(failed)} job(s) still in failed[]: {sorted(failed)}")

    # 2. Every expected job must be completed (run not incomplete).
    not_completed = expected_set - completed
    if not_completed:
        problems.append(f"{len(not_completed)} job(s) never completed: {sorted(not_completed)}")

    # 3. completed[] must not contain unknown jobs.
    unknown_completed = completed - expected_set
    if unknown_completed:
        problems.append(f"{len(unknown_completed)} completed job(s) not in jobs.jsonl: {sorted(unknown_completed)}")

    # 4. Duplicate results.
    seen: set = set()
    dupes: set = set()
    for rid in result_ids:
        if rid in seen:
            dupes.add(rid)
        seen.add(rid)
    if dupes:
        problems.append(f"duplicate job_id(s) in job_results.jsonl: {sorted(dupes)}")

    # 5. Every completed job must have a result.
    missing_results = completed - set(result_ids)
    if missing_results:
        problems.append(f"{len(missing_results)} completed job(s) missing from job_results.jsonl: {sorted(missing_results)}")

    # 6. Results must not contain jobs that aren't completed/expected.
    extra_results = set(result_ids) - completed
    if extra_results:
        problems.append(f"{len(extra_results)} result(s) for non-completed jobs: {sorted(extra_results)}")

    # 7. Hard count reconciliation: total == completed == distinct results.
    if not (len(expected_set) == len(completed) == len(set(result_ids))):
        problems.append(
            "count mismatch: "
            f"total_jobs={len(expected_set)} completed={len(completed)} "
            f"distinct_results={len(set(result_ids))} (all three must be equal)"
        )

    if problems:
        die(problems)

    # Reconciled. Emit claims in stable job order (the order jobs appear in jobs.jsonl).
    results_by_id = {r["job_id"]: r for r in results}
    claims_path = run_dir / "claims.jsonl"
    total_claims = 0
    with claims_path.open("w", encoding="utf-8") as out:
        for job_id in expected_ids:
            claims = results_by_id[job_id].get("claims", []) or []
            for claim in claims:
                out.write(json.dumps(claim, ensure_ascii=False, separators=(",", ":")) + "\n")
                total_claims += 1

    sha = hashlib.sha256(claims_path.read_bytes()).hexdigest()
    print("FINALIZE OK")
    print(f"  jobs reconciled: {len(expected_set)}")
    print(f"  claims written:  {total_claims}")
    print(f"  output:          {claims_path}")
    print(f"  sha256:          {sha}")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Finalize Step 04 claims.jsonl from job_results.jsonl (hard reconciliation gate)."
    )
    parser.add_argument("--run-dir", required=True, help="Step 04 run folder")
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()
    raise SystemExit(finalize(Path(args.run_dir).resolve()))
