"""
Bounded Step 04 test runner for 2016-17.

This intentionally follows the documented Step 04 artifact path:
sections.jsonl -> source_scope.json -> jobs.jsonl -> job_results.jsonl
-> claims.jsonl -> validate_claims.py

It uses fresh `codex.cmd exec` calls, one per job, and stops at this bounded
test run. It does not run full-year 2016-17 extraction.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import OrderedDict
from pathlib import Path


REQUIRED_KEYS = {
    "source_year",
    "source_file",
    "sector",
    "subsection",
    "source_page",
    "source_table_or_figure",
    "evidence_type",
    "source_quote",
    "claim_type",
    "claim",
    "indicator_or_subject",
    "topic_tags",
    "sentiment_signal",
    "time_orientation",
    "actor",
    "actors",
    "policy_or_programme",
    "policy_or_programmes",
    "constraint_or_risk",
    "cause",
    "effect",
    "comparison",
    "geography",
    "data_status_flags",
    "numeric_or_table_sensitive",
    "requires_pdf_numeric_qa",
    "markdown_quality_flags",
    "confidence",
    "needs_human_review",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


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
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
    return records


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_jsonl(path: Path, payload: object) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n")


def normalize_for_grounding(text: str) -> str:
    text = re.sub(r"\*+", "", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace(chr(0x2018), "'").replace(chr(0x2019), "'")
    text = text.replace(chr(0x201C), '"').replace(chr(0x201D), '"')
    text = text.replace(chr(0x2013), "-").replace(chr(0x2014), "-")
    text = text.replace(chr(0xFFFD), "'")
    text = " ".join(text.split())
    return text.lower()


def quote_is_grounded(source_quote: str, sections: list[dict]) -> bool:
    norm_quote = normalize_for_grounding(source_quote)
    if not norm_quote:
        return False
    for section in sections:
        norm_text = normalize_for_grounding(section["text"])
        if norm_quote in norm_text:
            return True
        sig_words = re.findall(r"\b[a-z]{5,}\b", norm_quote)
        if sig_words:
            hits = sum(1 for word in sig_words if word in norm_text)
            if hits / len(sig_words) >= 0.75:
                return True
    return False


def source_filename(source_md_path: str) -> str:
    return Path(source_md_path.replace("\\", "/")).name


def build_jobs(
    sections: list[dict],
    prompt_hash: str,
    schema_hash: str,
    runner_label: str,
    engine_contract: dict,
    chunk_size: int,
    target_sections: int,
    stop_after_jobs: int | None,
) -> tuple[list[dict], dict]:
    grouped: OrderedDict[str, list[dict]] = OrderedDict()
    for section in sections:
        grouped.setdefault(section["source_md_path"], []).append(section)

    all_jobs: list[dict] = []
    for source_index, (source_path, source_sections) in enumerate(grouped.items(), 1):
        source_file = source_filename(source_path)
        for start in range(0, len(source_sections), chunk_size):
            chunk = source_sections[start : start + chunk_size]
            serializable_input = {
                "source_md_path": source_path,
                "section_ids": [s["section_id"] for s in chunk],
                "sections": chunk,
            }
            input_hash = sha256_text(json.dumps(serializable_input, ensure_ascii=False, sort_keys=True))
            all_jobs.append(
                {
                    "job_id": f"job_{len(all_jobs) + 1:04d}",
                    "source_year": chunk[0]["source_year"],
                    "source_file": source_file,
                    "source_md_path": source_path,
                    "source_index": source_index,
                    "source_job_index": start // chunk_size + 1,
                    "section_ids": [s["section_id"] for s in chunk],
                    "sections": chunk,
                    "section_count": len(chunk),
                    "input_hash": input_hash,
                    "prompt_hash": prompt_hash,
                    "schema_hash": schema_hash,
                    "runner_label": runner_label,
                    "engine_contract": engine_contract,
                }
            )

    best_count = 0
    selected_count = 0
    for index, job in enumerate(all_jobs, 1):
        candidate = selected_count + job["section_count"]
        if abs(candidate - target_sections) <= abs(selected_count - target_sections):
            selected_count = candidate
            best_count = index
        else:
            break

    selected_jobs = all_jobs[:best_count]
    original_closest_job_count = len(selected_jobs)
    original_closest_section_count = sum(job["section_count"] for job in selected_jobs)
    if stop_after_jobs is not None:
        if stop_after_jobs < 1:
            raise ValueError("--stop-after-jobs must be >= 1")
        selected_jobs = selected_jobs[:stop_after_jobs]
    selected_ids = {section_id for job in selected_jobs for section_id in job["section_ids"]}

    included_sources = []
    excluded_sources = []
    for source_path, source_sections in grouped.items():
        included = [s for s in source_sections if s["section_id"] in selected_ids]
        excluded = [s for s in source_sections if s["section_id"] not in selected_ids]
        source_entry = {
            "source_md_path": source_path,
            "source_file": source_filename(source_path),
            "source_section_count": len(source_sections),
            "included_section_count": len(included),
            "excluded_section_count": len(excluded),
        }
        if included:
            included_sources.append(
                {
                    **source_entry,
                    "included_section_ids": [s["section_id"] for s in included],
                    "inclusion_reason": (
                        "Selected by first deterministic Step 04 jobs from Step 03 JSONL "
                        f"until cumulative included sections were closest to {target_sections}."
                    ),
                }
            )
        if excluded:
            reason = (
                "Outside bounded 200-section Codex test scope; not extracted in this run."
            )
            if source_filename(source_path) == "Pakistan_Es_2016_17_Pdf.md":
                reason = (
                    "Duplicate full-survey Markdown and outside bounded 200-section "
                    "Codex test scope; chapter-level files are the extraction source."
                )
            excluded_sources.append(
                {
                    **source_entry,
                    "excluded_section_ids": [s["section_id"] for s in excluded],
                    "reason": reason,
                }
            )

    source_scope = {
        "source_year": "2016-17",
        "scope_type": "bounded_codex_headless_test",
        "target_included_sections": target_sections,
        "stop_after_jobs": stop_after_jobs,
        "closest_to_target_job_count": original_closest_job_count,
        "closest_to_target_section_count": original_closest_section_count,
        "selected_job_count": len(selected_jobs),
        "selected_section_count": sum(job["section_count"] for job in selected_jobs),
        "selection_rule": (
            "Group sections by first-seen source_md_path in sections.jsonl, keep original "
            "section order, split into 20-section jobs, then include the first jobs whose "
            "cumulative section count is closest to the target."
        ),
        "included_sources": included_sources,
        "excluded_sources": excluded_sources,
    }
    return selected_jobs, source_scope


def build_prompt(base_prompt: str, job: dict) -> str:
    job_payload = {
        "job_id": job["job_id"],
        "source_year": job["source_year"],
        "source_file": job["source_file"],
        "source_md_path": job["source_md_path"],
        "section_ids": job["section_ids"],
        "sections": job["sections"],
    }
    return (
        base_prompt
        + "\n\n## Current Extraction Job\n\n"
        + json.dumps(job_payload, ensure_ascii=False, indent=2)
        + "\n\nFor this Codex structured-output call, return a JSON object with exactly "
        + 'one key, "claims", whose value is the claim-record array described above. '
        + "Do not include any other keys."
    )


def parse_codex_output(path: Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        raise ValueError(f"{path}: empty Codex output")
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("[")
        end = raw.rfind("]")
        if start < 0 or end < start:
            raise
        parsed = json.loads(raw[start : end + 1])
    if not isinstance(parsed, list):
        if isinstance(parsed, dict) and isinstance(parsed.get("claims"), list):
            return parsed["claims"]
        raise ValueError(f"{path}: output is not a JSON array or claims object")
    return parsed


def build_codex_wrapper_schema(array_schema_path: Path, wrapper_schema_path: Path) -> None:
    array_schema = json.loads(array_schema_path.read_text(encoding="utf-8"))
    wrapper = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Codex Step 04 wrapped claim extraction job output",
        "type": "object",
        "additionalProperties": False,
        "required": ["claims"],
        "properties": {
            "claims": array_schema,
        },
    }
    write_json(wrapper_schema_path, wrapper)


def validate_job_claims(job: dict, claims: list[dict]) -> list[str]:
    errors: list[str] = []
    section_ids = set(job["section_ids"])
    sections = job["sections"]
    for index, claim in enumerate(claims, 1):
        if not isinstance(claim, dict):
            errors.append(f"{job['job_id']} claim {index}: not an object")
            continue
        keys = set(claim)
        if keys != REQUIRED_KEYS:
            errors.append(
                f"{job['job_id']} claim {index}: key mismatch missing="
                f"{sorted(REQUIRED_KEYS - keys)} extra={sorted(keys - REQUIRED_KEYS)}"
            )
        if claim.get("source_year") != job["source_year"]:
            errors.append(f"{job['job_id']} claim {index}: wrong source_year")
        if claim.get("source_file") != job["source_file"]:
            errors.append(f"{job['job_id']} claim {index}: wrong source_file")
        if claim.get("needs_human_review") is not True:
            errors.append(f"{job['job_id']} claim {index}: needs_human_review not true")
        source_quote = claim.get("source_quote")
        if not isinstance(source_quote, str) or not quote_is_grounded(source_quote, sections):
            errors.append(f"{job['job_id']} claim {index}: source_quote not grounded in job sections")

    # The schema does not include section_id, so quote grounding is the job-local traceability gate.
    if not section_ids:
        errors.append(f"{job['job_id']}: no source section ids")
    return errors


def run_codex_job(
    repo_root: Path,
    schema_path: Path,
    prompt: str,
    output_path: Path,
    timeout_seconds: int,
) -> subprocess.CompletedProcess:
    cmd = [
        "codex.cmd",
        "exec",
        "--ephemeral",
        "--sandbox",
        "read-only",
        "--cd",
        str(repo_root),
        "--output-schema",
        str(schema_path),
        "--output-last-message",
        str(output_path),
        "-",
    ]
    return subprocess.run(
        cmd,
        input=prompt,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout_seconds,
    )


def write_run_docs(
    run_root: Path,
    supporting: Path,
    source_scope: dict,
    manifest: dict,
    validation_stdout: str,
    validation_stderr: str,
    validation_returncode: int,
) -> None:
    status = "PASS" if validation_returncode == 0 and manifest["failed_job_count"] == 0 else "FAIL"
    report = f"""# Extraction Report - 2016-17 Codex 200-Section Test

Status: {status}

This is a bounded test run only. It uses the documented Step 04 path:

```text
sections.jsonl -> source_scope.json -> jobs.jsonl -> job_results.jsonl -> claims.jsonl -> validator
```

It does not run full-year 2016-17 extraction and does not start Step 05.

## Scope

- Selection rule: {source_scope["selection_rule"]}
- Target sections: {source_scope["target_included_sections"]}
- Selected jobs: {source_scope["selected_job_count"]}
- Included sections: {source_scope["selected_section_count"]}
- Included source files: {len(source_scope["included_sources"])}
- Excluded/partial source entries recorded: {len(source_scope["excluded_sources"])}

## Extraction

- Engine: codex.cmd exec
- Fresh calls: yes, one `--ephemeral` call per job
- Sandbox: read-only
- Completed jobs: {manifest["completed_job_count"]}
- Failed jobs: {manifest["failed_job_count"]}
- Claim records: {manifest["claim_count"]}

## Validation

- Validator return code: {validation_returncode}

```text
{validation_stdout.strip()}
{validation_stderr.strip()}
```

## Caveats

- This is not a Step 04 PASS for the full 2016-17 year.
- Coverage warnings are expected because the run intentionally excludes most Step 03 sections.
- Numeric/table-sensitive claims still require PDF numeric QA downstream.
"""
    (supporting / "extraction_report.md").write_text(report, encoding="utf-8")

    repro = f"""# How to Reproduce - 2016-17 Codex 200-Section Test

Run from repository root:

```powershell
python agentic\\04_claims_json\\runs\\2016-17_claims_codex_200sec_test\\_supporting\\run_codex_200sec_test.py
```

The runner discovers and uses:

- Step 03 sections: `{manifest["source_sections_jsonl"]}`
- Prompt: `{manifest["prompt_path"]}`
- Structured output schema: `{manifest["output_schema_path"]}`
- Validator: `{manifest["validator_script"]}`

The runner builds `source_scope.json`, `jobs.jsonl`, and `job_results.jsonl`,
then rebuilds run-root `claims.jsonl` and runs the validator. It uses
fresh `codex.cmd exec --ephemeral --sandbox read-only` calls with
`--output-schema` for each job.
"""
    (supporting / "how_to_reproduce.md").write_text(repro, encoding="utf-8")

    adv_prompt = """# Adversarial Review Prompt - 2016-17 Codex 200-Section Test

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
"""
    (supporting / "adv_review_prompt.md").write_text(adv_prompt, encoding="utf-8")

    adv_results = """# Adversarial Review Results

Status: NOT RUN.

This bounded test run stopped after extraction and validation as requested.
"""
    (supporting / "adv_review_results.md").write_text(adv_results, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", action="store_true", help="reuse completed matching job results")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--chunk-size", type=int, default=20)
    parser.add_argument("--target-sections", type=int, default=200)
    parser.add_argument("--stop-after-jobs", type=int, default=None)
    parser.add_argument(
        "--finalize-existing",
        action="store_true",
        help="do not call Codex; validate existing job_outputs and merge the selected jobs",
    )
    args = parser.parse_args()

    supporting = Path(__file__).resolve().parent
    run_root = supporting.parent
    repo_root = run_root.parents[3]

    sections_path = repo_root / "agentic/03_section_splitting/runs/2016-17_section_split_pymupdf4llm_hardened/sections.jsonl"
    step03_review = repo_root / "agentic/03_section_splitting/runs/2016-17_section_split_pymupdf4llm_hardened/adv_review_results.md"
    prompt_path = repo_root / "agentic/04_claims_json/extraction_prompt.md"
    schema_path = repo_root / "agentic/04_claims_json/claim_array_output_schema.json"
    codex_wrapper_schema_path = supporting / "codex_claims_output_wrapper_schema.json"
    schema_v01_path = repo_root / "agentic/archive/04_commentary_schema_discovery/schema/commentary_schema_v0.1.json"
    validator_path = repo_root / "agentic/04_claims_json/validate_claims.py"

    if "Status: PASS" not in step03_review.read_text(encoding="utf-8"):
        raise RuntimeError("Step 03 adversarial review is not PASS")

    sections = read_jsonl(sections_path)
    base_prompt = prompt_path.read_text(encoding="utf-8")
    build_codex_wrapper_schema(schema_path, codex_wrapper_schema_path)
    prompt_hash = sha256_bytes(prompt_path.read_bytes())
    schema_hash = sha256_bytes(schema_path.read_bytes())
    codex_wrapper_schema_hash = sha256_bytes(codex_wrapper_schema_path.read_bytes())
    schema_v01_hash = sha256_bytes(schema_v01_path.read_bytes())
    runner_label = "run_codex_200sec_test.py/v1"
    engine_contract = {
        "engine": "codex.cmd exec",
        "fresh_context": "--ephemeral",
        "sandbox": "read-only",
        "output_schema": str(codex_wrapper_schema_path.relative_to(repo_root)).replace("\\", "/"),
        "output_schema_note": "Codex requires top-level object schemas; runner unwraps claims[] into Step 04 artifacts.",
    }

    jobs, source_scope = build_jobs(
        sections=sections,
        prompt_hash=prompt_hash,
        schema_hash=schema_hash,
        runner_label=runner_label,
        engine_contract=engine_contract,
        chunk_size=args.chunk_size,
        target_sections=args.target_sections,
        stop_after_jobs=args.stop_after_jobs,
    )

    write_json(supporting / "source_scope.json", source_scope)
    jobs_path = supporting / "jobs.jsonl"
    jobs_path.write_text("", encoding="utf-8")
    for job in jobs:
        append_jsonl(jobs_path, job)

    job_outputs_dir = supporting / "job_outputs"
    failed_jobs_dir = supporting / "failed_jobs"
    job_outputs_dir.mkdir(exist_ok=True)
    failed_jobs_dir.mkdir(exist_ok=True)
    job_results_path = supporting / "job_results.jsonl"
    run_state_path = supporting / "run_state.json"
    if not args.resume:
        job_results_path.write_text("", encoding="utf-8")
        for cleanup_dir in (job_outputs_dir, failed_jobs_dir):
            for old_file in cleanup_dir.glob("*"):
                if old_file.is_file():
                    old_file.unlink()

    completed_by_id: dict[str, dict] = {}
    if args.resume and job_results_path.exists():
        for record in read_jsonl(job_results_path):
            completed_by_id[record["job_id"]] = record

    completed = []
    failed = []
    for job in jobs:
        prior = completed_by_id.get(job["job_id"])
        if (
            prior
            and prior.get("input_hash") == job["input_hash"]
            and prior.get("prompt_hash") == job["prompt_hash"]
            and prior.get("schema_hash") == job["schema_hash"]
            and prior.get("runner_label") == job["runner_label"]
            and prior.get("engine_contract") == job["engine_contract"]
        ):
            completed.append(prior)
            continue

        output_path = job_outputs_dir / f"{job['job_id']}_claims.json"
        if args.finalize_existing:
            try:
                claims = parse_codex_output(output_path)
                errors = validate_job_claims(job, claims)
                if errors:
                    failure = {
                        "job_id": job["job_id"],
                        "errors": errors,
                        "output_path": str(output_path),
                    }
                    write_json(failed_jobs_dir / f"{job['job_id']}_validation_failure.json", failure)
                    failed.append(failure)
                    break
                result = {
                    "job_id": job["job_id"],
                    "source_year": job["source_year"],
                    "source_file": job["source_file"],
                    "source_md_path": job["source_md_path"],
                    "section_ids": job["section_ids"],
                    "section_count": job["section_count"],
                    "claim_count": len(claims),
                    "claims": claims,
                    "input_hash": job["input_hash"],
                    "prompt_hash": job["prompt_hash"],
                    "schema_hash": job["schema_hash"],
                    "schema_v0_1_hash": schema_v01_hash,
                    "runner_label": job["runner_label"],
                    "engine_contract": job["engine_contract"],
                    "codex_stdout_sha256": "",
                    "codex_stderr_sha256": "",
                    "finalized_from_existing_output": True,
                }
                append_jsonl(job_results_path, result)
                completed.append(result)
                continue
            except Exception as exc:
                failure = {
                    "job_id": job["job_id"],
                    "exception": repr(exc),
                    "output_path": str(output_path),
                }
                write_json(failed_jobs_dir / f"{job['job_id']}_exception.json", failure)
                failed.append(failure)
                break

        prompt = build_prompt(base_prompt, job)
        print(f"Running {job['job_id']} {job['source_file']} sections={job['section_count']}", flush=True)
        try:
            proc = run_codex_job(
                repo_root=repo_root,
                schema_path=codex_wrapper_schema_path,
                prompt=prompt,
                output_path=output_path,
                timeout_seconds=args.timeout_seconds,
            )
            if proc.returncode != 0:
                failure = {
                    "job_id": job["job_id"],
                    "returncode": proc.returncode,
                    "stdout": proc.stdout,
                    "stderr": proc.stderr,
                }
                write_json(failed_jobs_dir / f"{job['job_id']}_failure.json", failure)
                failed.append(failure)
                break
            claims = parse_codex_output(output_path)
            errors = validate_job_claims(job, claims)
            if errors:
                failure = {
                    "job_id": job["job_id"],
                    "errors": errors,
                    "stdout": proc.stdout,
                    "stderr": proc.stderr,
                    "output_path": str(output_path),
                }
                write_json(failed_jobs_dir / f"{job['job_id']}_validation_failure.json", failure)
                failed.append(failure)
                break
            result = {
                "job_id": job["job_id"],
                "source_year": job["source_year"],
                "source_file": job["source_file"],
                "source_md_path": job["source_md_path"],
                "section_ids": job["section_ids"],
                "section_count": job["section_count"],
                "claim_count": len(claims),
                "claims": claims,
                "input_hash": job["input_hash"],
                "prompt_hash": job["prompt_hash"],
                "schema_hash": job["schema_hash"],
                "schema_v0_1_hash": schema_v01_hash,
                "runner_label": job["runner_label"],
                "engine_contract": job["engine_contract"],
                "codex_stdout_sha256": sha256_text(proc.stdout),
                "codex_stderr_sha256": sha256_text(proc.stderr),
            }
            append_jsonl(job_results_path, result)
            completed.append(result)
        except Exception as exc:
            failure = {"job_id": job["job_id"], "exception": repr(exc)}
            write_json(failed_jobs_dir / f"{job['job_id']}_exception.json", failure)
            failed.append(failure)
            break
        finally:
            write_json(
                run_state_path,
                {
                    "updated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                    "total_jobs": len(jobs),
                    "completed_job_count": len(completed),
                    "failed_job_count": len(failed),
                    "completed_job_ids": [r["job_id"] for r in completed],
                    "failed_job_ids": [r["job_id"] for r in failed],
                },
            )

    if failed:
        print(f"Stopped after failed job: {failed[-1]['job_id']}", flush=True)

    all_claims = []
    if len(completed) == len(jobs) and not failed:
        claims_path = run_root / "claims.jsonl"
        claims_path.write_text("", encoding="utf-8")
        for result in completed:
            for claim in result["claims"]:
                append_jsonl(claims_path, claim)
                all_claims.append(claim)

        validation = subprocess.run(
            [
                sys.executable,
                str(validator_path),
                "--claims",
                str(claims_path),
                "--sections",
                str(sections_path),
            ],
            text=True,
            encoding="utf-8",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        output_hash = sha256_bytes(claims_path.read_bytes())
    else:
        validation = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="not all jobs completed")
        output_hash = ""

    manifest = {
        "run_id": "2016-17_claims_codex_200sec_test",
        "run_type": "bounded_headless_codex_test",
        "source_year": "2016-17",
        "source_sections_jsonl": str(sections_path.relative_to(repo_root)).replace("\\", "/"),
        "step03_review": str(step03_review.relative_to(repo_root)).replace("\\", "/"),
        "prompt_path": str(prompt_path.relative_to(repo_root)).replace("\\", "/"),
        "output_schema_path": str(schema_path.relative_to(repo_root)).replace("\\", "/"),
        "schema_path": str(schema_v01_path.relative_to(repo_root)).replace("\\", "/"),
        "validator_script": str(validator_path.relative_to(repo_root)).replace("\\", "/"),
        "prompt_sha256": prompt_hash,
        "output_schema_sha256": schema_hash,
        "codex_wrapper_schema_path": str(codex_wrapper_schema_path.relative_to(repo_root)).replace("\\", "/"),
        "codex_wrapper_schema_sha256": codex_wrapper_schema_hash,
        "schema_v0_1_sha256": schema_v01_hash,
        "runner_label": runner_label,
        "engine_contract": engine_contract,
        "target_sections": args.target_sections,
        "stop_after_jobs": args.stop_after_jobs,
        "closest_to_target_job_count": source_scope["closest_to_target_job_count"],
        "closest_to_target_section_count": source_scope["closest_to_target_section_count"],
        "included_section_count": source_scope["selected_section_count"],
        "selected_job_count": len(jobs),
        "completed_job_count": len(completed),
        "failed_job_count": len(failed),
        "claim_count": len(all_claims),
        "output_file": "claims.jsonl",
        "output_sha256": output_hash,
        "validation_returncode": validation.returncode,
        "run_date": dt.date.today().isoformat(),
        "python_executable": sys.executable,
        "codex_version": subprocess.run(
            ["codex.cmd", "--version"],
            text=True,
            encoding="utf-8",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout.strip(),
        "stop_condition": "bounded test run complete; full 2016-17 extraction not run",
    }
    write_json(supporting / "extraction_manifest.json", manifest)
    write_run_docs(
        run_root=run_root,
        supporting=supporting,
        source_scope=source_scope,
        manifest=manifest,
        validation_stdout=validation.stdout,
        validation_stderr=validation.stderr,
        validation_returncode=validation.returncode,
    )

    print(json.dumps(manifest, indent=2), flush=True)
    return 0 if validation.returncode == 0 and not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
