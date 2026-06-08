"""
gen_jobs.py  —  build source_scope.json and jobs.jsonl for the 2018-19 full run.

Run from the repo root:
    python agentic/04_claims_json/runs/2018-19_claims_claude_full/_supporting/gen_jobs.py

Inputs:
    agentic/03_section_splitting/runs/2018-19_section_split_pymupdf4llm_hardened/sections.jsonl

Outputs (written to this _supporting/ folder):
    source_scope.json
    jobs.jsonl
"""

import hashlib
import json
from collections import OrderedDict
from pathlib import Path

# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[5]
SECTIONS_JSONL = (
    REPO_ROOT
    / "agentic/03_section_splitting/runs"
    / "2018-19_section_split_pymupdf4llm_hardened/sections.jsonl"
)
PROMPT_FILE = REPO_ROOT / "agentic/04_claims_json/extraction_prompt.md"
SCHEMA_FILE = REPO_ROOT / "agentic/04_claims_json/claim_array_output_schema.json"

OUT_DIR = Path(__file__).resolve().parent        # _supporting/
SCOPE_OUT = OUT_DIR / "source_scope.json"
JOBS_OUT = OUT_DIR / "jobs.jsonl"

SECTIONS_PER_JOB = 20
RUNNER_LABEL = "2018-19_claims_claude_full"
ENGINE_CONTRACT = "claude"
SOURCE_YEAR = "2018-19"

# These source files are excluded from extraction:
# - Economic_Survey_2018_19.md : full-survey PDF export; chapter files are canonical
# - Supplement_2018_19.md      : statistical tables; no narrative claims
# - Annex_I.md                 : statistical annex tables
# - Annex_Ii.md                : statistical annex tables
# - Economic_Indicators_1819.md: indicator tables
EXCLUDED_FILES = {
    "Economic_Survey_2018_19.md",
    "Supplement_2018_19.md",
    "Annex_I.md",
    "Annex_Ii.md",
    "Economic_Indicators_1819.md",
}
EXCLUDED_REASONS = {
    "Economic_Survey_2018_19.md": "Duplicate full-survey Markdown; chapter-level files are the extraction source for this run.",
    "Supplement_2018_19.md": "Statistical tables supplement; contains no narrative claims to extract.",
    "Annex_I.md": "Statistical annex tables; no narrative claims.",
    "Annex_Ii.md": "Statistical annex tables; no narrative claims.",
    "Economic_Indicators_1819.md": "Indicator tables; no narrative claims.",
}
# ---------------------------------------------------------------------------


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_of(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    records = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def build_scope_and_jobs() -> None:
    print(f"Reading sections from {SECTIONS_JSONL} …")
    all_sections = read_jsonl(SECTIONS_JSONL)
    print(f"  {len(all_sections)} total sections")

    prompt_hash = sha256_of(PROMPT_FILE.read_text(encoding="utf-8"))
    schema_hash = sha256_of(SCHEMA_FILE.read_text(encoding="utf-8"))

    # Group sections by source_md_path, preserving first-seen order
    by_source: OrderedDict[str, list[dict]] = OrderedDict()
    for sec in all_sections:
        src = sec["source_md_path"]
        by_source.setdefault(src, []).append(sec)

    included_sources = []
    excluded_sources = []

    jobs: list[dict] = []
    job_counter = 0

    for src_path, sections in by_source.items():
        src_file = Path(src_path).name
        if src_file in EXCLUDED_FILES:
            excluded_sources.append({
                "source_md_path": src_path,
                "source_file": src_file,
                "source_section_count": len(sections),
                "included_section_count": 0,
                "excluded_section_count": len(sections),
                "reason": EXCLUDED_REASONS[src_file],
            })
            continue

        section_ids = [s["section_id"] for s in sections]
        included_sources.append({
            "source_md_path": src_path,
            "source_file": src_file,
            "source_section_count": len(sections),
            "included_section_count": len(sections),
            "excluded_section_count": 0,
            "inclusion_reason": "Chapter-level source file; included in full-year extraction.",
        })

        # Split into jobs of SECTIONS_PER_JOB
        for chunk_start in range(0, len(sections), SECTIONS_PER_JOB):
            chunk = sections[chunk_start : chunk_start + SECTIONS_PER_JOB]
            job_counter += 1
            job_id = f"job_{job_counter:04d}"
            input_text = json.dumps(chunk, ensure_ascii=False)
            input_hash = sha256_of(input_text)
            job = {
                "job_id": job_id,
                "source_year": SOURCE_YEAR,
                "source_md_path": src_path,
                "source_file": src_file,
                "section_ids": [s["section_id"] for s in chunk],
                "n_sections": len(chunk),
                "sections": chunk,
                "input_hash": input_hash,
                "prompt_hash": prompt_hash,
                "schema_hash": schema_hash,
                "runner_label": RUNNER_LABEL,
                "engine_contract": ENGINE_CONTRACT,
            }
            jobs.append(job)

    total_included = sum(s["included_section_count"] for s in included_sources)
    total_excluded = sum(s["excluded_section_count"] for s in excluded_sources)

    scope = {
        "source_year": SOURCE_YEAR,
        "scope_type": "full_year_chapter_files",
        "sections_jsonl": str(SECTIONS_JSONL.relative_to(REPO_ROOT)).replace("\\", "/"),
        "total_sections_in_jsonl": len(all_sections),
        "included_section_count": total_included,
        "excluded_section_count": total_excluded,
        "sections_per_job": SECTIONS_PER_JOB,
        "job_count": len(jobs),
        "included_sources": included_sources,
        "excluded_sources": excluded_sources,
    }

    SCOPE_OUT.write_text(
        json.dumps(scope, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"  Wrote {SCOPE_OUT.name}")
    print(f"  Included: {total_included} sections from {len(included_sources)} source files")
    print(f"  Excluded: {total_excluded} sections from {len(excluded_sources)} source files")

    with JOBS_OUT.open("w", encoding="utf-8") as f:
        for job in jobs:
            f.write(json.dumps(job, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"  Wrote {JOBS_OUT.name}  ({len(jobs)} jobs)")

    # Summary table
    print("\nJobs per source file:")
    for src in included_sources:
        n_jobs = -(-src["included_section_count"] // SECTIONS_PER_JOB)  # ceil div
        print(f"  {src['source_file']:40s}  {src['included_section_count']:4d} sections  {n_jobs:3d} jobs")


if __name__ == "__main__":
    build_scope_and_jobs()
