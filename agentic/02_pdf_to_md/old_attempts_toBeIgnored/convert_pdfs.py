from __future__ import annotations

import argparse
import json
import random
from datetime import datetime
from pathlib import Path
from typing import Any

import fitz
import pymupdf4llm


SEED = 20260605
RUN_NAME = "2026-06-05_6pdf_cross_year_pilot"
SECTOR_PATTERNS = {
    "education": "education",
    "transport": "transport",
}

TASK_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TASK_DIR.parents[1]
JSON_MAP = PROJECT_ROOT / "agentic" / "01_pes_folder_map" / "pes_folder_tree.json"
SOURCE_ROOT = (
    PROJECT_ROOT
    / "datalab_master"
    / "Master Data"
    / "pakistan_economic_survey"
)
RUNS_DIR = TASK_DIR / "runs"


def relative_to_project(path: Path) -> str:
    return path.resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()


def unique_run_dir(run_name: str) -> Path:
    base = RUNS_DIR / run_name
    if not base.exists():
        return base

    suffix = 2
    while True:
        candidate = RUNS_DIR / f"{run_name}_v{suffix}"
        if not candidate.exists():
            return candidate
        suffix += 1


def load_folder_map() -> dict[str, Any]:
    with JSON_MAP.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def find_sector_candidates(folder_map: dict[str, Any], sector: str) -> list[dict[str, Any]]:
    pattern = SECTOR_PATTERNS[sector]
    candidates: list[dict[str, Any]] = []

    for year_entry in folder_map["years"]:
        matches = [
            pdf
            for pdf in year_entry["pdfs"]
            if pattern in pdf["name"].lower()
        ]
        if not matches:
            continue
        if len(matches) > 1:
            raise ValueError(
                f"Multiple {sector} candidates in {year_entry['year']}: "
                f"{[pdf['name'] for pdf in matches]}"
            )
        pdf = matches[0]
        source_pdf = PROJECT_ROOT / pdf["relative_path"].replace("/", "\\")
        candidates.append(
            {
                "sector": sector,
                "year": year_entry["year"],
                "pdf_name": pdf["name"],
                "map_relative_path": pdf["relative_path"],
                "source_pdf": source_pdf,
                "size_bytes": pdf["size_bytes"],
            }
        )

    return candidates


def select_pdfs(folder_map: dict[str, Any]) -> list[dict[str, Any]]:
    rng = random.Random(SEED)
    education_candidates = find_sector_candidates(folder_map, "education")
    transport_candidates = find_sector_candidates(folder_map, "transport")

    selected_education = rng.sample(education_candidates, 3)
    education_years = {item["year"] for item in selected_education}
    remaining_transport = [
        item for item in transport_candidates if item["year"] not in education_years
    ]
    selected_transport = rng.sample(remaining_transport, 3)

    selected = selected_education + selected_transport
    for item in selected:
        source_pdf = item["source_pdf"]
        if not source_pdf.exists():
            raise FileNotFoundError(source_pdf)
        if SOURCE_ROOT.resolve() not in source_pdf.resolve().parents:
            raise ValueError(f"Selected PDF is outside source root: {source_pdf}")

    return sorted(selected, key=lambda item: (item["sector"], item["year"]))


def convert_pdf(input_pdf: Path, output_md: Path) -> dict[str, int]:
    chunks = pymupdf4llm.to_markdown(str(input_pdf), page_chunks=True)
    sections = []

    for index, chunk in enumerate(chunks, start=1):
        page = chunk.get("metadata", {}).get("page", index)
        text = chunk.get("text", "").rstrip()
        sections.append(
            f"<!-- source_pdf_page: {page} -->\n\n"
            f"## PDF page {page}\n\n"
            f"{text}\n"
        )

    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text("\n".join(sections), encoding="utf-8")

    with fitz.open(input_pdf) as doc:
        source_page_count = doc.page_count

    return {
        "source_page_count": source_page_count,
        "converted_page_chunks": len(chunks),
        "output_bytes": output_md.stat().st_size,
    }


def write_selected_map(
    run_dir: Path,
    selected: list[dict[str, Any]],
    converted: list[dict[str, Any]],
) -> None:
    payload = {
        "task": "02_pdf_to_md",
        "run_name": run_dir.name,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "seed": SEED,
        "selection_rules": [
            "Select candidates from agentic/01_pes_folder_map/pes_folder_tree.json first.",
            "Use one Education PDF from each of 3 random years.",
            "Use one Transport PDF from each of 3 random years.",
            "Use distinct years across all 6 pilot PDFs.",
            "Verify every selected PDF exists under datalab_master/Master Data/pakistan_economic_survey/.",
        ],
        "source_root": relative_to_project(SOURCE_ROOT),
        "json_map": relative_to_project(JSON_MAP),
        "run_folder": relative_to_project(run_dir),
        "selected_pdfs": converted,
    }
    (run_dir / "selected_pdf_map.json").write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )


def run_conversion(run_dir: Path) -> list[dict[str, Any]]:
    folder_map = load_folder_map()
    selected = select_pdfs(folder_map)
    converted: list[dict[str, Any]] = []

    for item in selected:
        output_md = (
            run_dir
            / "converted_md"
            / item["year"]
            / f"{item['sector']}.md"
        )
        stats = convert_pdf(item["source_pdf"], output_md)
        converted.append(
            {
                "sector": item["sector"],
                "year": item["year"],
                "pdf_name": item["pdf_name"],
                "map_relative_path": item["map_relative_path"],
                "source_pdf": relative_to_project(item["source_pdf"]),
                "source_size_bytes": item["size_bytes"],
                "output_md": relative_to_project(output_md),
                **stats,
            }
        )

    write_selected_map(run_dir, selected, converted)
    return converted


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the reproducible 6-PDF PyMuPDF4LLM pilot."
    )
    parser.add_argument(
        "--run-name",
        default=RUN_NAME,
        help=f"Base run folder name under runs/ (default: {RUN_NAME})",
    )
    args = parser.parse_args()

    run_dir = unique_run_dir(args.run_name)
    run_dir.mkdir(parents=True, exist_ok=False)
    converted = run_conversion(run_dir)

    print(f"Run folder: {relative_to_project(run_dir)}")
    for item in converted:
        print(f"{item['sector']} {item['year']}: {item['output_md']}")


if __name__ == "__main__":
    main()
