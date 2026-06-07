from __future__ import annotations

import csv
import hashlib
import json
import platform
import subprocess
import sys
from argparse import ArgumentParser
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import fitz
import pymupdf4llm


RUN_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = RUN_DIR.parents[3]
SOURCE_DIR = (
    PROJECT_ROOT
    / "datalab_master"
    / "Master Data"
    / "pakistan_economic_survey"
    / "2022-23"
)
CONVERTED_DIR = RUN_DIR / "converted_md"
SOURCE_MANIFEST_CSV = SOURCE_DIR / "manifest.csv"
REPRO_MANIFEST_PATH = RUN_DIR / "repro_manifest.json"
CONVERSION_LOG_PATH = RUN_DIR / "conversion_log.json"


def relative(path: Path) -> str:
    return path.resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def package_version(name: str) -> str:
    try:
        import importlib.metadata as metadata

        return metadata.version(name)
    except Exception as exc:
        return f"unknown: {exc}"


def git_value(args: list[str]) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return None
    value = result.stdout.strip()
    return value or None


def git_dirty() -> bool | None:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return None
    return bool(result.stdout.strip())


def load_source_manifest() -> dict[str, dict[str, str]]:
    if not SOURCE_MANIFEST_CSV.exists():
        return {}
    with SOURCE_MANIFEST_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return {row["file_name"]: row for row in rows if row.get("file_name")}


def page_count(pdf_path: Path) -> int:
    with fitz.open(pdf_path) as doc:
        return doc.page_count


def page_marker_count(md_path: Path) -> int:
    return md_path.read_text(encoding="utf-8").count("<!-- page ")


def chunk_page_number(chunk: dict[str, Any], fallback: int) -> int:
    metadata = chunk.get("metadata") or {}
    for key in ("page", "page_number", "page_no"):
        value = metadata.get(key)
        if isinstance(value, int):
            return value
    return fallback


def markdown_with_page_markers(pdf_path: Path) -> tuple[str, int]:
    chunks = pymupdf4llm.to_markdown(str(pdf_path), page_chunks=True)
    sections: list[str] = []

    if isinstance(chunks, list):
        for index, chunk in enumerate(chunks, start=1):
            if isinstance(chunk, dict):
                page_no = chunk_page_number(chunk, index)
                text = chunk.get("text") or ""
            else:
                page_no = index
                text = str(chunk)
            sections.append(f"<!-- page {page_no} -->\n\n{text.strip()}")
        return "\n\n".join(sections).rstrip() + "\n", len(chunks)

    text = str(chunks).rstrip() + "\n"
    return text, 0


def main() -> int:
    parser = ArgumentParser(
        description="Convert PES 2022-23 PDFs with PyMuPDF4LLM and write reproducibility evidence."
    )
    parser.add_argument(
        "--reuse-existing",
        action="store_true",
        help="Do not reconvert Markdown files that already exist; generate logs/manifests from existing outputs.",
    )
    args = parser.parse_args()

    if not SOURCE_DIR.exists():
        raise FileNotFoundError(SOURCE_DIR)

    CONVERTED_DIR.mkdir(parents=True, exist_ok=True)
    source_manifest = load_source_manifest()
    pdf_paths = sorted(SOURCE_DIR.glob("*.pdf"), key=lambda path: path.name.lower())

    conversion_log: list[dict[str, Any]] = []
    manifest_entries: list[dict[str, Any]] = []

    for pdf_path in pdf_paths:
        output_path = CONVERTED_DIR / f"{pdf_path.stem}.md"
        manifest_row = source_manifest.get(pdf_path.name, {})
        started_at = datetime.now(UTC).isoformat(timespec="seconds")
        entry: dict[str, Any] = {
            "source_pdf_path": relative(pdf_path),
            "source_file_name": pdf_path.name,
            "output_md_path": relative(output_path),
            "success": False,
            "page_count": None,
            "converted_page_chunks": None,
            "started_at_utc": started_at,
            "finished_at_utc": None,
            "error_message": None,
        }

        try:
            source_page_count = page_count(pdf_path)
            if args.reuse_existing and output_path.exists():
                chunk_count = page_marker_count(output_path)
            else:
                print(f"converting {pdf_path.name}", flush=True)
                markdown, chunk_count = markdown_with_page_markers(pdf_path)
                output_path.write_text(markdown, encoding="utf-8", newline="\n")

            entry.update(
                {
                    "success": True,
                    "page_count": source_page_count,
                    "converted_page_chunks": chunk_count,
                    "output_bytes": output_path.stat().st_size,
                    "reused_existing_output": bool(args.reuse_existing and output_path.exists()),
                }
            )
        except Exception as exc:
            entry["error_message"] = repr(exc)
        finally:
            entry["finished_at_utc"] = datetime.now(UTC).isoformat(timespec="seconds")

        conversion_log.append(entry)

        output_sha256 = sha256_file(output_path) if output_path.exists() else None
        manifest_entries.append(
            {
                "label": manifest_row.get("label"),
                "source_url": manifest_row.get("url"),
                "source_pdf_path": relative(pdf_path),
                "source_file_name": pdf_path.name,
                "source_size_bytes": pdf_path.stat().st_size,
                "source_mtime_utc": datetime.fromtimestamp(
                    pdf_path.stat().st_mtime
                ).astimezone(UTC).isoformat(timespec="seconds"),
                "source_sha256": sha256_file(pdf_path),
                "page_count": entry["page_count"],
                "output_md_path": relative(output_path),
                "output_size_bytes": output_path.stat().st_size
                if output_path.exists()
                else None,
                "output_sha256": output_sha256,
                "conversion_success": entry["success"],
                "error_message": entry["error_message"],
            }
        )

    repro_manifest = {
        "task": "2022-23_pymupdf4llm_hardened",
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "project_root": str(PROJECT_ROOT),
        "source_dir": relative(SOURCE_DIR),
        "source_manifest_csv": relative(SOURCE_MANIFEST_CSV)
        if SOURCE_MANIFEST_CSV.exists()
        else None,
        "converted_dir": relative(CONVERTED_DIR),
        "pdf_selection_rule": "all *.pdf files directly inside source_dir, sorted case-insensitively by filename",
        "generation_mode": "reuse_existing_outputs" if args.reuse_existing else "full_conversion",
        "scope_guardrails": [
            "Only direct child PDFs in the 2022-23 source folder were selected.",
            "Raw PDFs were read only and were not moved, renamed, edited, deleted, normalized, or deduplicated.",
            "Markdown is working text only; numeric/table/chart/ranking/footnote content is NOT_CERTIFIED unless separately QA'd against source PDFs.",
        ],
        "environment": {
            "python_executable": sys.executable,
            "python_version": sys.version,
            "platform": platform.platform(),
            "pymupdf": package_version("pymupdf"),
            "pymupdf4llm": package_version("pymupdf4llm"),
        },
        "git": {
            "branch": git_value(["branch", "--show-current"]),
            "commit": git_value(["rev-parse", "HEAD"]),
            "dirty": git_dirty(),
        },
        "totals": {
            "pdfs_found": len(pdf_paths),
            "converted": sum(1 for item in conversion_log if item["success"]),
            "failures": sum(1 for item in conversion_log if not item["success"]),
        },
        "selected_pdfs": [path.name for path in pdf_paths],
        "entries": manifest_entries,
    }

    CONVERSION_LOG_PATH.write_text(
        json.dumps(conversion_log, indent=2, ensure_ascii=False),
        encoding="utf-8",
        newline="\n",
    )
    REPRO_MANIFEST_PATH.write_text(
        json.dumps(repro_manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
        newline="\n",
    )

    failures = [item for item in conversion_log if not item["success"]]
    print(
        f"PDFs found: {len(pdf_paths)}; converted: {len(pdf_paths) - len(failures)}; failures: {len(failures)}"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
