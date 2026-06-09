#!/usr/bin/env python3
"""build_jobs.py - generic, year-agnostic Step 04 job builder.

Pipeline position:
    Step 03 sections.jsonl -> [THIS SCRIPT] -> _supporting/jobs.jsonl
    -> run_step04.py -> _supporting/job_results.jsonl
    -> finalize_claims.py -> claims.jsonl -> validate_claims.py

This is the portable replacement for the per-year `gen_jobs.py` scripts. It takes
ANY reviewed Step 03 `sections.jsonl` (or a Step 03 run folder containing one) and
a target year/label, then writes the two inputs `run_step04.py` consumes:

    <run-dir>/_supporting/source_scope.json
    <run-dir>/_supporting/jobs.jsonl

Exclusions are explicit and reason-bearing. Nothing is ever silently skipped:
every excluded file must be given as `--exclude "FILENAME=REASON"`; a bare
`--exclude FILENAME` (no reason) is a hard error. All exclusions, with reasons and
section counts, are recorded in `source_scope.json`.

Pure standard library.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import OrderedDict
from pathlib import Path


# --------------------------------------------------------------------------- #
# IO helpers
# --------------------------------------------------------------------------- #
def sha256_of(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


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
                sys.exit(f"{path}:{line_no}: invalid JSON in sections file: {exc}")
    return records


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# Input resolution
# --------------------------------------------------------------------------- #
def resolve_sections_path(raw: str) -> Path:
    """Accept a direct sections.jsonl path OR a Step 03 run folder containing one."""
    p = Path(raw).resolve()
    if p.is_dir():
        candidate = p / "sections.jsonl"
        if not candidate.exists():
            sys.exit(f"--sections is a folder but no sections.jsonl inside: {p}")
        return candidate
    if not p.exists():
        sys.exit(f"--sections not found: {p}")
    return p


def parse_excludes(raw_excludes: list[str]) -> dict[str, str]:
    """Each entry must be FILENAME=REASON. Bare FILENAME (no '=') is rejected so
    every exclusion carries an explicit human reason into source_scope.json."""
    mapping: dict[str, str] = {}
    for entry in raw_excludes or []:
        if "=" not in entry:
            sys.exit(
                f"--exclude must be 'FILENAME=REASON' (got '{entry}'). "
                "Every exclusion needs an explicit reason; bare filenames are rejected."
            )
        name, reason = entry.split("=", 1)
        name, reason = name.strip(), reason.strip()
        if not name or not reason:
            sys.exit(f"--exclude '{entry}': both FILENAME and REASON must be non-empty.")
        mapping[name] = reason
    return mapping


def source_filename(source_md_path: str) -> str:
    return Path(str(source_md_path).replace("\\", "/")).name


# --------------------------------------------------------------------------- #
# Job building
# --------------------------------------------------------------------------- #
def build(args: argparse.Namespace) -> int:
    sections_path = resolve_sections_path(args.sections)
    excludes = parse_excludes(args.exclude)

    prompt_path = Path(args.prompt_file).resolve()
    schema_path = Path(args.schema_file).resolve()
    for label, p in (("--prompt-file", prompt_path), ("--schema-file", schema_path)):
        if not p.exists():
            sys.exit(f"{label} not found: {p}")

    run_dir = Path(args.run_dir).resolve()
    supporting = run_dir / "_supporting"
    supporting.mkdir(parents=True, exist_ok=True)

    print(f"Reading sections from {sections_path}")
    all_sections = read_jsonl(sections_path)
    print(f"  {len(all_sections)} total section records")

    prompt_hash = sha256_of(prompt_path.read_text(encoding="utf-8"))
    schema_hash = sha256_of(schema_path.read_text(encoding="utf-8"))

    # Group by source_md_path, preserving first-seen order.
    by_source: "OrderedDict[str, list[dict]]" = OrderedDict()
    for sec in all_sections:
        src = sec.get("source_md_path")
        if not src:
            sys.exit("a section record is missing 'source_md_path'; input is not a valid Step 03 sections.jsonl")
        by_source.setdefault(src, []).append(sec)

    # Validate that every requested exclude name actually exists in the input.
    present_files = {source_filename(s) for s in by_source}
    unknown = [name for name in excludes if name not in present_files]
    if unknown:
        sys.exit(
            "these --exclude filenames are not present in the sections file: "
            f"{unknown}\npresent files: {sorted(present_files)}"
        )

    included_sources: list[dict] = []
    excluded_sources: list[dict] = []
    jobs: list[dict] = []
    job_counter = 0

    for src_path, sections in by_source.items():
        src_file = source_filename(src_path)
        if src_file in excludes:
            excluded_sources.append({
                "source_md_path": src_path,
                "source_file": src_file,
                "source_section_count": len(sections),
                "included_section_count": 0,
                "excluded_section_count": len(sections),
                "reason": excludes[src_file],
            })
            continue

        included_sources.append({
            "source_md_path": src_path,
            "source_file": src_file,
            "source_section_count": len(sections),
            "included_section_count": len(sections),
            "excluded_section_count": 0,
            "inclusion_reason": "Included in Step 04 extraction scope.",
        })

        for start in range(0, len(sections), args.sections_per_job):
            chunk = sections[start : start + args.sections_per_job]
            job_counter += 1
            job_id = f"job_{job_counter:04d}"
            input_hash = sha256_of(json.dumps(chunk, ensure_ascii=False, sort_keys=True))
            jobs.append({
                "job_id": job_id,
                "source_year": args.year,
                "source_file": src_file,
                "source_md_path": src_path,
                "section_ids": [s.get("section_id") for s in chunk],
                "n_sections": len(chunk),
                "sections": chunk,
                "input_hash": input_hash,
                "prompt_hash": prompt_hash,
                "schema_hash": schema_hash,
                "runner_label": args.run_label or run_dir.name,
                "engine_contract": args.engine_contract,
            })

    total_included = sum(s["included_section_count"] for s in included_sources)
    total_excluded = sum(s["excluded_section_count"] for s in excluded_sources)

    scope = {
        "source_year": args.year,
        "scope_type": "portable_build_jobs",
        "sections_jsonl": str(sections_path),
        "total_sections_in_jsonl": len(all_sections),
        "included_section_count": total_included,
        "excluded_section_count": total_excluded,
        "sections_per_job": args.sections_per_job,
        "job_count": len(jobs),
        "prompt_file": str(prompt_path),
        "prompt_sha256": prompt_hash,
        "schema_file": str(schema_path),
        "schema_sha256": schema_hash,
        "included_sources": included_sources,
        "excluded_sources": excluded_sources,
    }

    scope_out = supporting / "source_scope.json"
    jobs_out = supporting / "jobs.jsonl"
    write_json(scope_out, scope)
    with jobs_out.open("w", encoding="utf-8") as f:
        for job in jobs:
            f.write(json.dumps(job, ensure_ascii=False, separators=(",", ":")) + "\n")

    if not jobs:
        sys.exit("no jobs produced: every source file was excluded or the input was empty.")

    print(f"  Wrote {scope_out}")
    print(f"  Wrote {jobs_out}  ({len(jobs)} jobs)")
    print(f"  Included: {total_included} sections from {len(included_sources)} files")
    print(f"  Excluded: {total_excluded} sections from {len(excluded_sources)} files")
    if excluded_sources:
        print("  Exclusions (with reasons):")
        for e in excluded_sources:
            print(f"    - {e['source_file']}: {e['reason']}")
    print("\nJobs per included source file:")
    for src in included_sources:
        n_jobs = -(-src["included_section_count"] // args.sections_per_job)  # ceil div
        print(f"  {src['source_file']:40s} {src['included_section_count']:4d} sections  {n_jobs:3d} jobs")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generic Step 04 job builder: Step 03 sections.jsonl -> jobs.jsonl"
    )
    parser.add_argument("--sections", required=True,
                        help="path to sections.jsonl OR a Step 03 run folder containing one")
    parser.add_argument("--run-dir", required=True, help="Step 04 run folder to create/use")
    parser.add_argument("--year", required=True, help="source year/label, e.g. 2018-19")
    parser.add_argument("--sections-per-job", type=int, default=20)
    parser.add_argument("--exclude", action="append", default=[],
                        help='exclude a source file: "FILENAME=REASON" (reason required, repeatable)')
    parser.add_argument("--prompt-file", required=True, help="config/extraction_prompt.md")
    parser.add_argument("--schema-file", required=True, help="config/claim_array_output_schema.json")
    parser.add_argument("--run-label", default=None, help="runner_label stamped on jobs (default: run-dir name)")
    parser.add_argument("--engine-contract", default="claude", help="provenance label (default: claude)")
    return parser.parse_args(argv)


if __name__ == "__main__":
    raise SystemExit(build(parse_args()))
