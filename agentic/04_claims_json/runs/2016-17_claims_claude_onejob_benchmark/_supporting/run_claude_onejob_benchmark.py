from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
import time
from collections import OrderedDict
from pathlib import Path


RUN_ID = "2016-17_claims_claude_onejob_benchmark"
CLAUDE_PS1 = r"C:\nvm4w\nodejs\claude.ps1"
SOURCE_FILE = "Agriculture.md"
SECTION_LIMIT = 20

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
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


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


def build_source_scope(sections: list[dict], selected_ids: set[str]) -> dict:
    grouped: OrderedDict[str, list[dict]] = OrderedDict()
    for section in sections:
        grouped.setdefault(section["source_md_path"], []).append(section)

    included_sources = []
    excluded_sources = []
    for source_path, source_sections in grouped.items():
        included = [s for s in source_sections if s["section_id"] in selected_ids]
        excluded = [s for s in source_sections if s["section_id"] not in selected_ids]
        base = {
            "source_md_path": source_path,
            "source_file": source_filename(source_path),
            "source_section_count": len(source_sections),
            "included_section_count": len(included),
            "excluded_section_count": len(excluded),
        }
        if included:
            included_sources.append(
                {
                    **base,
                    "included_section_ids": [s["section_id"] for s in included],
                    "inclusion_reason": "One-job Claude benchmark: first 20 Agriculture.md sections from Step 03.",
                }
            )
        if excluded:
            reason = "Outside one-job Claude benchmark scope; not extracted in this run."
            if source_filename(source_path) == "Pakistan_Es_2016_17_Pdf.md":
                reason = (
                    "Duplicate full-survey Markdown and outside one-job Claude benchmark scope; "
                    "chapter-level files are the extraction source."
                )
            excluded_sources.append({**base, "excluded_section_ids": [s["section_id"] for s in excluded], "reason": reason})

    return {
        "source_year": "2016-17",
        "scope_type": "one_job_claude_benchmark",
        "selected_job_count": 1,
        "selected_section_count": len(selected_ids),
        "selection_rule": "Select Agriculture.md from Step 03 and include its first 20 sections only.",
        "included_sources": included_sources,
        "excluded_sources": excluded_sources,
    }


def build_prompt(base_prompt: str, schema_v01: str, job: dict) -> str:
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
        + "\n\n## Frozen Schema v0.1 JSON\n\n```json\n"
        + schema_v01
        + "\n```\n\n## Current Extraction Job\n\n```json\n"
        + json.dumps(job_payload, ensure_ascii=False, indent=2)
        + "\n```\n\nReturn valid JSON only: a single JSON array of claim records. "
        + "Do not wrap the array in an object. Do not use Markdown fences."
    )


def strip_json_fence(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped, flags=re.IGNORECASE)
        stripped = re.sub(r"\s*```$", "", stripped)
    return stripped.strip()


def parse_claude_stdout(stdout_text: str) -> tuple[list[dict], dict]:
    wrapper = json.loads(stdout_text)
    if wrapper.get("is_error"):
        raise ValueError(f"Claude returned error result: {wrapper.get('result')}")
    result = wrapper.get("result")
    if not isinstance(result, str):
        raise ValueError("Claude wrapper result is not a string")
    payload_text = strip_json_fence(result)
    try:
        payload = json.loads(payload_text)
    except json.JSONDecodeError:
        start = payload_text.find("[")
        end = payload_text.rfind("]")
        if start < 0 or end < start:
            raise
        payload = json.loads(payload_text[start : end + 1])
    if isinstance(payload, dict) and isinstance(payload.get("claims"), list):
        payload = payload["claims"]
    if not isinstance(payload, list):
        raise ValueError("Claude result is not a JSON array or claims object")
    return payload, wrapper


def validate_job_claims(job: dict, claims: list[dict]) -> list[str]:
    errors = []
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
        if not isinstance(source_quote, str) or not quote_is_grounded(source_quote, job["sections"]):
            errors.append(f"{job['job_id']} claim {index}: source_quote not grounded in job sections")
    return errors


def main() -> int:
    supporting = Path(__file__).resolve().parent
    run_root = supporting.parent
    repo_root = run_root.parents[3]

    sections_path = repo_root / "agentic/03_section_splitting/runs/2016-17_section_split_pymupdf4llm_hardened/sections.jsonl"
    step03_review = repo_root / "agentic/03_section_splitting/runs/2016-17_section_split_pymupdf4llm_hardened/adv_review_results.md"
    prompt_path = repo_root / "agentic/04_claims_json/extraction_prompt.md"
    output_schema_path = repo_root / "agentic/04_claims_json/claim_array_output_schema.json"
    schema_v01_path = repo_root / "agentic/archive/04_commentary_schema_discovery/schema/commentary_schema_v0.1.json"
    validator_path = repo_root / "agentic/04_claims_json/validate_claims.py"

    if "Status: PASS" not in step03_review.read_text(encoding="utf-8"):
        raise RuntimeError("Step 03 adversarial review is not PASS")

    sections = read_jsonl(sections_path)
    selected_sections = [s for s in sections if source_filename(s["source_md_path"]) == SOURCE_FILE][:SECTION_LIMIT]
    if len(selected_sections) != SECTION_LIMIT:
        raise RuntimeError(f"Expected {SECTION_LIMIT} selected sections, got {len(selected_sections)}")

    prompt_hash = sha256_bytes(prompt_path.read_bytes())
    output_schema_hash = sha256_bytes(output_schema_path.read_bytes())
    schema_v01_hash = sha256_bytes(schema_v01_path.read_bytes())
    engine_contract = {
        "engine": "claude -p",
        "launcher": CLAUDE_PS1,
        "model": "sonnet",
        "effort": "medium",
        "max_turns": 1,
        "output_format": "json",
        "json_schema": str(output_schema_path.relative_to(repo_root)).replace("\\", "/"),
        "bare": False,
        "concurrency": 1,
    }

    serializable_input = {
        "source_md_path": selected_sections[0]["source_md_path"],
        "section_ids": [s["section_id"] for s in selected_sections],
        "sections": selected_sections,
    }
    job = {
        "job_id": "job_0001",
        "source_year": selected_sections[0]["source_year"],
        "source_file": SOURCE_FILE,
        "source_md_path": selected_sections[0]["source_md_path"],
        "source_index": 1,
        "source_job_index": 1,
        "section_ids": [s["section_id"] for s in selected_sections],
        "sections": selected_sections,
        "section_count": len(selected_sections),
        "input_hash": sha256_text(json.dumps(serializable_input, ensure_ascii=False, sort_keys=True)),
        "prompt_hash": prompt_hash,
        "schema_hash": output_schema_hash,
        "schema_v0_1_hash": schema_v01_hash,
        "runner_label": "run_claude_onejob_benchmark.py/v1",
        "engine_contract": engine_contract,
    }

    source_scope = build_source_scope(sections, set(job["section_ids"]))
    write_json(supporting / "source_scope.json", source_scope)
    (supporting / "jobs.jsonl").write_text("", encoding="utf-8")
    append_jsonl(supporting / "jobs.jsonl", job)

    job_outputs_dir = supporting / "job_outputs"
    failed_jobs_dir = supporting / "failed_jobs"
    job_outputs_dir.mkdir(exist_ok=True)
    failed_jobs_dir.mkdir(exist_ok=True)
    job_results_path = supporting / "job_results.jsonl"
    job_results_path.write_text("", encoding="utf-8")

    prompt = build_prompt(
        prompt_path.read_text(encoding="utf-8"),
        schema_v01_path.read_text(encoding="utf-8").strip(),
        job,
    )
    prompt_path_for_run = job_outputs_dir / "job_0001_prompt.txt"
    prompt_path_for_run.write_text(prompt, encoding="utf-8")

    cmd = [
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        CLAUDE_PS1,
        "-p",
        "--model",
        "sonnet",
        "--effort",
        "medium",
        "--max-turns",
        "1",
        "--output-format",
        "json",
        "--json-schema",
        output_schema_path.read_text(encoding="utf-8"),
    ]

    start = time.perf_counter()
    proc = subprocess.run(
        cmd,
        input=prompt,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=repo_root,
    )
    elapsed = time.perf_counter() - start

    raw_stdout_path = job_outputs_dir / "job_0001_claude_stdout.json"
    raw_stderr_path = job_outputs_dir / "job_0001_claude_stderr.txt"
    raw_stdout_path.write_text(proc.stdout, encoding="utf-8")
    raw_stderr_path.write_text(proc.stderr, encoding="utf-8")

    failed = []
    claims = []
    wrapper = {}
    job_validation_errors = []
    if proc.returncode == 0:
        try:
            claims, wrapper = parse_claude_stdout(proc.stdout)
            write_json(job_outputs_dir / "job_0001_claims.json", claims)
            job_validation_errors = validate_job_claims(job, claims)
            if job_validation_errors:
                failed.append({"job_id": job["job_id"], "errors": job_validation_errors})
        except Exception as exc:
            failed.append({"job_id": job["job_id"], "exception": repr(exc)})
    else:
        failed.append({"job_id": job["job_id"], "returncode": proc.returncode, "stderr": proc.stderr})

    if failed:
        write_json(failed_jobs_dir / "job_0001_failure.json", failed[-1])

    claims_path = run_root / "claims.jsonl"
    claims_path.write_text("", encoding="utf-8")
    if not failed:
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
            "claude_stdout_sha256": sha256_text(proc.stdout),
            "claude_stderr_sha256": sha256_text(proc.stderr),
            "claude_wrapper": {
                "type": wrapper.get("type"),
                "subtype": wrapper.get("subtype"),
                "is_error": wrapper.get("is_error"),
                "duration_ms": wrapper.get("duration_ms"),
                "duration_api_ms": wrapper.get("duration_api_ms"),
                "num_turns": wrapper.get("num_turns"),
                "total_cost_usd": wrapper.get("total_cost_usd"),
                "session_id": wrapper.get("session_id"),
            },
            "elapsed_seconds": elapsed,
        }
        append_jsonl(job_results_path, result)
        for claim in claims:
            append_jsonl(claims_path, claim)

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
        cwd=repo_root,
    )

    manifest = {
        "run_id": RUN_ID,
        "run_type": "one_job_claude_benchmark",
        "source_year": "2016-17",
        "source_sections_jsonl": str(sections_path.relative_to(repo_root)).replace("\\", "/"),
        "step03_review": str(step03_review.relative_to(repo_root)).replace("\\", "/"),
        "prompt_path": str(prompt_path.relative_to(repo_root)).replace("\\", "/"),
        "output_schema_path": str(output_schema_path.relative_to(repo_root)).replace("\\", "/"),
        "schema_path": str(schema_v01_path.relative_to(repo_root)).replace("\\", "/"),
        "validator_script": str(validator_path.relative_to(repo_root)).replace("\\", "/"),
        "prompt_sha256": prompt_hash,
        "output_schema_sha256": output_schema_hash,
        "schema_v0_1_sha256": schema_v01_hash,
        "runner_label": job["runner_label"],
        "engine_contract": engine_contract,
        "selected_job_count": 1,
        "completed_job_count": 0 if failed else 1,
        "failed_job_count": len(failed),
        "included_section_count": len(selected_sections),
        "claim_count": len(claims) if not failed else 0,
        "claude_returncode": proc.returncode,
        "runtime_seconds": round(elapsed, 3),
        "job_validation_error_count": len(job_validation_errors),
        "validation_returncode": validation.returncode,
        "output_file": "claims.jsonl",
        "output_sha256": sha256_bytes(claims_path.read_bytes()),
        "run_date": dt.date.today().isoformat(),
        "python_executable": sys.executable,
        "stop_condition": "one real Step 04 Claude benchmark job complete; job 2 and full 2016-17 were not run",
    }
    write_json(supporting / "extraction_manifest.json", manifest)
    write_json(
        supporting / "run_state.json",
        {
            "updated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "total_jobs": 1,
            "completed_job_count": manifest["completed_job_count"],
            "failed_job_count": manifest["failed_job_count"],
            "completed_job_ids": [] if failed else [job["job_id"]],
            "failed_job_ids": [f["job_id"] for f in failed],
        },
    )

    status = "PASS" if validation.returncode == 0 and not failed else "FAIL"
    report = f"""# Extraction Report - 2016-17 Claude One-Job Benchmark

Status: {status}

This is a one-job benchmark only. It does not run job 2, full-year 2016-17
extraction, adversarial review, or Step 05.

## Scope

- Source file: {SOURCE_FILE}
- Included sections: {len(selected_sections)}
- Job count: 1
- Selection rule: first 20 Agriculture.md sections from reviewed Step 03 JSONL

## Claude Invocation

- Engine: normal `claude -p`
- Model: sonnet
- Effort: medium
- Max turns: 1
- Output format: json
- JSON schema: `{manifest["output_schema_path"]}`
- Bare mode: no
- Concurrency: 1
- Runtime seconds: {manifest["runtime_seconds"]}
- Claude exit code: {proc.returncode}

## Results

- Completed jobs: {manifest["completed_job_count"]}
- Failed jobs: {manifest["failed_job_count"]}
- Claim records: {manifest["claim_count"]}
- Job-local validation errors: {manifest["job_validation_error_count"]}
- Final validator return code: {validation.returncode}

## Validator Output

```text
{validation.stdout.strip()}
{validation.stderr.strip()}
```
"""
    (supporting / "extraction_report.md").write_text(report, encoding="utf-8")

    repro = f"""# How to Reproduce - 2016-17 Claude One-Job Benchmark

Run from repository root:

```powershell
python agentic\\04_claims_json\\runs\\2016-17_claims_claude_onejob_benchmark\\_supporting\\run_claude_onejob_benchmark.py
```

The runner performs exactly one Claude extraction job over the first 20
`Agriculture.md` sections from the 2016-17 Step 03 `sections.jsonl`, then runs
the canonical Step 04 validator. It stops after this one-job benchmark.
"""
    (supporting / "how_to_reproduce.md").write_text(repro, encoding="utf-8")

    print(json.dumps(manifest, ensure_ascii=False, indent=2), flush=True)
    print("\nVALIDATOR STDOUT:\n" + validation.stdout, flush=True)
    if validation.stderr:
        print("\nVALIDATOR STDERR:\n" + validation.stderr, flush=True)
    return 0 if validation.returncode == 0 and not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
