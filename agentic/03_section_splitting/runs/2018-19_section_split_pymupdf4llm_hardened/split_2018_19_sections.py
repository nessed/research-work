from __future__ import annotations

import hashlib
import json
import platform
import re
import subprocess
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


RUN_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = RUN_DIR.parents[3]
PDF_TO_MD_RUN = (
    PROJECT_ROOT / "agentic" / "02_pdf_to_md" / "runs" / "2018-19_pymupdf4llm_hardened"
)
INPUT_MANIFEST_PATH = PDF_TO_MD_RUN / "repro_manifest.json"
INPUT_MD_DIR = PDF_TO_MD_RUN / "converted_md"
SECTIONS_PATH = RUN_DIR / "sections.jsonl"
SECTION_MANIFEST_PATH = RUN_DIR / "section_manifest.json"
SECTION_REPORT_PATH = RUN_DIR / "section_split_report.md"

PAGE_RE = re.compile(r"<!--\s*page\s+(\d+)\s*-->")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
NUMERIC_RE = re.compile(r"(?<![A-Za-z])(?:\d[\d,]*(?:\.\d+)?|\d+(?:st|nd|rd|th)|[ivxlcdm]+)(?:\s*%|\s*percent)?", re.IGNORECASE)
CLAIM_FIELD_NAMES = {
    "claim",
    "claims",
    "summary",
    "interpretation",
    "cause_effect",
    "policy_action",
    "risk",
    "outlook",
    "sentiment",
}
LATER_YEAR_SUPPLEMENT_RE = re.compile(r"^Supplement_20(?:19_20|20_21|21_22)\.pdf$", re.IGNORECASE)


def relative(path: Path) -> str:
    return path.resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


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


def sector_from_md_path(md_path: Path) -> str:
    return md_path.stem.replace("_", " ").strip()


def clean_heading(text: str) -> str:
    text = re.sub(r"[*_`#]+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:240]


def page_blocks(markdown: str) -> list[tuple[int, str]]:
    matches = list(PAGE_RE.finditer(markdown))
    blocks: list[tuple[int, str]] = []
    for index, match in enumerate(matches):
        page_no = int(match.group(1))
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        blocks.append((page_no, markdown[start:end].strip()))
    return blocks


def split_paragraphs(text: str, max_chars: int = 4500) -> list[str]:
    paragraphs = [item.strip() for item in re.split(r"\n\s*\n", text) if item.strip()]
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0
    for paragraph in paragraphs:
        addition = len(paragraph) + 2
        if current and current_len + addition > max_chars:
            chunks.append("\n\n".join(current).strip())
            current = []
            current_len = 0
        current.append(paragraph)
        current_len += addition
    if current:
        chunks.append("\n\n".join(current).strip())
    return chunks or ([text.strip()] if text.strip() else [])


def split_page_text(page_text: str, fallback_heading: str) -> list[dict[str, str]]:
    lines = page_text.splitlines()
    units: list[dict[str, str]] = []
    current_heading = fallback_heading
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_lines
        text = "\n".join(current_lines).strip()
        if text:
            for chunk in split_paragraphs(text):
                units.append({"heading_text": current_heading, "text": chunk})
        current_lines = []

    for line in lines:
        heading_match = HEADING_RE.match(line.strip())
        if heading_match:
            flush()
            current_heading = clean_heading(heading_match.group(2)) or fallback_heading
            current_lines.append(line)
        else:
            current_lines.append(line)
    flush()

    if not units and page_text.strip():
        units.append({"heading_text": fallback_heading, "text": page_text.strip()})
    return units


def quality_flags(text: str, page_numbers: list[int]) -> list[str]:
    flags: set[str] = set()
    lines = text.splitlines()
    pipe_lines = sum(1 for line in lines if "|" in line)
    numeric_count = len(NUMERIC_RE.findall(text))
    if pipe_lines >= 2 or re.search(r"\bTable\s+\d", text, re.IGNORECASE):
        flags.add("table_layout_noise")
    if re.search(r"\b(Figure|Fig\.|Chart|Graph)\s+\d", text, re.IGNORECASE):
        flags.add("figure_text")
    if re.search(r"Picture .*? intentionally omitted", text, re.IGNORECASE):
        flags.add("omitted_picture_placeholder")
    if re.search(r"[A-Za-z]-\s+[A-Za-z]", text):
        flags.add("broken_words")
    if re.search(r"[Ã‚Ã¢][\u0080-\u00bf\u20ac\u201a-\u201e]|\ufffd", text):
        flags.add("encoding_artifact")
    if len(set(page_numbers)) != len(page_numbers):
        flags.add("page_order_noise")
    if numeric_count >= 12:
        flags.add("numeric_dense_text")
    return sorted(flags) or ["none"]


def numeric_sensitive(text: str) -> bool:
    if NUMERIC_RE.search(text):
        return True
    if "|" in text:
        return True
    if re.search(r"\b(Table|Figure|Fig\.|Chart|Graph|percent|percentage|total|ranking)\b", text, re.IGNORECASE):
        return True
    return False


def section_type(text: str, flags: list[str]) -> str:
    if "table_layout_noise" in flags or "figure_text" in flags:
        return "table_or_figure_adjacent"
    first = text.lstrip().splitlines()[0] if text.strip() else ""
    if first.startswith("#"):
        return "heading_section"
    return "paragraph_block"


def included_entries(repro_manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        entry
        for entry in repro_manifest["entries"]
        if not LATER_YEAR_SUPPLEMENT_RE.match(entry["source_file_name"])
    ]


def excluded_entries(repro_manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        entry
        for entry in repro_manifest["entries"]
        if LATER_YEAR_SUPPLEMENT_RE.match(entry["source_file_name"])
    ]


def build_sections(repro_manifest: dict[str, Any]) -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    for entry in included_entries(repro_manifest):
        md_path = PROJECT_ROOT / entry["output_md_path"]
        sector = sector_from_md_path(md_path)
        fallback_heading = sector
        markdown = md_path.read_text(encoding="utf-8")
        blocks = page_blocks(markdown)
        if not blocks and markdown.strip():
            blocks = [(1, markdown.strip())]

        per_file_index = 0
        for page_no, page_text in blocks:
            for unit in split_page_text(page_text, fallback_heading):
                text = unit["text"].strip()
                if not text:
                    continue
                per_file_index += 1
                flags = quality_flags(text, [page_no])
                section_id = (
                    f"pes_2018_19__{md_path.stem.lower()}__"
                    f"{per_file_index:04d}__p{page_no:03d}"
                )
                sections.append(
                    {
                        "section_id": section_id,
                        "source_year": "2018-19",
                        "source_md_path": entry["output_md_path"],
                        "source_pdf_path": entry["source_pdf_path"],
                        "sector": sector,
                        "heading_text": unit["heading_text"],
                        "start_page": page_no,
                        "end_page": page_no,
                        "section_type": section_type(text, flags),
                        "text": text,
                        "numeric_or_table_sensitive": numeric_sensitive(text),
                        "markdown_quality_flags": flags,
                    }
                )
    return sections


def qa_sections(sections: list[dict[str, Any]], repro_manifest: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    ids = [section["section_id"] for section in sections]
    duplicates = sorted(section_id for section_id, count in Counter(ids).items() if count > 1)
    if duplicates:
        issues.extend(f"duplicate section_id: {section_id}" for section_id in duplicates[:20])

    scoped_entries = included_entries(repro_manifest)
    valid_md_paths = {entry["output_md_path"] for entry in scoped_entries}
    valid_pdf_paths = {entry["source_pdf_path"] for entry in scoped_entries}
    page_counts_by_pdf = {entry["source_pdf_path"]: int(entry["page_count"]) for entry in scoped_entries}
    required_fields = {
        "section_id",
        "source_year",
        "source_md_path",
        "source_pdf_path",
        "sector",
        "heading_text",
        "start_page",
        "end_page",
        "section_type",
        "text",
        "numeric_or_table_sensitive",
        "markdown_quality_flags",
    }

    for index, section in enumerate(sections, start=1):
        keys = set(section)
        missing = required_fields - keys
        forbidden = keys & CLAIM_FIELD_NAMES
        if missing:
            issues.append(f"section {index} missing fields: {sorted(missing)}")
        if forbidden:
            issues.append(f"section {index} has forbidden claim/summary fields: {sorted(forbidden)}")
        if section.get("source_year") != "2018-19":
            issues.append(f"section {index} invalid source_year: {section.get('source_year')}")
        if section.get("source_md_path") not in valid_md_paths:
            issues.append(f"section {index} invalid source_md_path: {section.get('source_md_path')}")
        if section.get("source_pdf_path") not in valid_pdf_paths:
            issues.append(f"section {index} invalid source_pdf_path: {section.get('source_pdf_path')}")
        start_page = section.get("start_page")
        end_page = section.get("end_page")
        page_count = page_counts_by_pdf.get(section.get("source_pdf_path"), 0)
        if not isinstance(start_page, int) or not isinstance(end_page, int):
            issues.append(f"section {index} non-integer page span")
        elif start_page < 1 or end_page < start_page or end_page > page_count:
            issues.append(
                f"section {index} invalid page span {start_page}-{end_page} for {page_count} pages"
            )
        if not section.get("heading_text"):
            issues.append(f"section {index} missing heading_text")
        if not section.get("sector"):
            issues.append(f"section {index} missing sector")
        if not isinstance(section.get("numeric_or_table_sensitive"), bool):
            issues.append(f"section {index} invalid numeric_or_table_sensitive")
        flags = section.get("markdown_quality_flags")
        if not isinstance(flags, list) or not flags:
            issues.append(f"section {index} invalid markdown_quality_flags")
        if not isinstance(section.get("text"), str) or not section["text"].strip():
            issues.append(f"section {index} empty text")

    by_file = Counter(section["source_md_path"] for section in sections)
    missing_files = sorted(valid_md_paths - set(by_file))
    if missing_files:
        issues.extend(f"no sections for input Markdown: {path}" for path in missing_files)

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "sections_total": len(sections),
        "source_md_files": len(valid_md_paths),
        "source_md_files_with_sections": len(by_file),
        "sections_by_file": dict(sorted(by_file.items())),
        "numeric_or_table_sensitive_sections": sum(
            1 for section in sections if section["numeric_or_table_sensitive"]
        ),
        "markdown_quality_flag_counts": dict(
            sorted(Counter(flag for section in sections for flag in section["markdown_quality_flags"]).items())
        ),
        "section_type_counts": dict(sorted(Counter(section["section_type"] for section in sections).items())),
        "forbidden_claim_summary_fields_present": bool(any(set(section) & CLAIM_FIELD_NAMES for section in sections)),
    }


def write_outputs(sections: list[dict[str, Any]], manifest: dict[str, Any]) -> None:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    with SECTIONS_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        for section in sections:
            handle.write(json.dumps(section, ensure_ascii=False, sort_keys=True) + "\n")

    section_manifest = dict(manifest)
    section_manifest["output_sha256"] = sha256_file(SECTIONS_PATH)
    section_manifest["output_size_bytes"] = SECTIONS_PATH.stat().st_size
    SECTION_MANIFEST_PATH.write_text(
        json.dumps(section_manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
        newline="\n",
    )

    qa = manifest["qa_results"]
    lines = [
        "# Section Split Report",
        "",
        "## Summary",
        "",
        f"- Generated UTC: `{manifest['generated_at_utc']}`",
        f"- Overall status: `{qa['status']}`",
        f"- Source year: `2018-19`",
        f"- Source PDF-to-MD run: `{manifest['input_pdf_to_md_run']}`",
        f"- Source Markdown files: `{qa['source_md_files']}`",
        f"- Markdown files with sections: `{qa['source_md_files_with_sections']}`",
        f"- Later-year supplement Markdown files excluded: `{len(manifest['excluded_input_entries'])}`",
        f"- Sections written: `{qa['sections_total']}`",
        f"- Numeric/table-sensitive sections: `{qa['numeric_or_table_sensitive_sections']}`",
        f"- Forbidden claim/summary fields present: `{qa['forbidden_claim_summary_fields_present']}`",
        "",
        "## QA Checks",
        "",
        f"- Unique `section_id`: `{'PASS' if not qa['issues'] else 'SEE_ISSUES'}`",
        "- Valid `source_year`: checked for every section.",
        "- Valid `source_md_path`: checked against the PDF-to-MD manifest.",
        "- Valid `source_pdf_path`: checked against the PDF-to-MD manifest.",
        "- Valid `start_page`/`end_page`: checked against source PDF page counts.",
        "- `heading_text` and `sector`: required and preserved where available.",
        "- `numeric_or_table_sensitive`: boolean required for every section.",
        "- `markdown_quality_flags`: non-empty list required for every section.",
        "- No claim, summary, interpretation, outlook, risk, sentiment, or policy-action fields are allowed.",
        "",
        "## Counts",
        "",
        f"- Section type counts: `{qa['section_type_counts']}`",
        f"- Markdown quality flag counts: `{qa['markdown_quality_flag_counts']}`",
        "",
        "## Excluded Inputs",
        "",
    ]
    if manifest["excluded_input_entries"]:
        lines.extend(
            f"- `{item['source_md_path']}`: {item['reason']}"
            for item in manifest["excluded_input_entries"]
        )
    else:
        lines.append("- None.")
    lines.extend(["", "## Issues", ""])
    if qa["issues"]:
        lines.extend(f"- {issue}" for issue in qa["issues"][:100])
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## Research Use Limits",
            "",
            "Sections are source-tagged Markdown text units only. They are not claims,",
            "summaries, interpretations, conclusions, or database-ready facts. Any",
            "table, chart, numeric, ranking, total, or footnote content remains",
            "uncertified until separately checked against the source PDF.",
        ]
    )
    SECTION_REPORT_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    repro_manifest = load_json(INPUT_MANIFEST_PATH)
    sections = build_sections(repro_manifest)
    qa = qa_sections(sections, repro_manifest)
    included = included_entries(repro_manifest)
    excluded = excluded_entries(repro_manifest)
    manifest = {
        "task": "2018-19_section_split_pymupdf4llm_hardened",
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "project_root": str(PROJECT_ROOT),
        "input_pdf_to_md_run": relative(PDF_TO_MD_RUN),
        "input_repro_manifest": relative(INPUT_MANIFEST_PATH),
        "input_converted_md_dir": relative(INPUT_MD_DIR),
        "output_sections_jsonl": relative(SECTIONS_PATH),
        "source_year": "2018-19",
        "split_rules": {
            "input_scope": "reviewed 2018-19 PDF-to-MD outputs excluding later-year Supplement_2019_20, Supplement_2020_21, and Supplement_2021_22 files that live in the 2018-19 source folder",
            "page_tracking": "existing <!-- page N --> markers",
            "primary_boundaries": "Markdown headings within each page",
            "fallback_boundaries": "paragraph blocks capped around 4500 characters",
            "source_text_policy": "verbatim or near-verbatim Markdown text only; no summaries or interpretations",
            "section_id_policy": "stable per source Markdown filename, section order, and start page",
        },
        "environment": {
            "python_executable": sys.executable,
            "python_version": sys.version,
            "platform": platform.platform(),
        },
        "git": {
            "branch": git_value(["branch", "--show-current"]),
            "commit": git_value(["rev-parse", "HEAD"]),
        },
        "input_entries": [
            {
                "source_pdf_path": entry["source_pdf_path"],
                "source_md_path": entry["output_md_path"],
                "source_md_sha256": entry["output_sha256"],
                "page_count": entry["page_count"],
            }
            for entry in included
        ],
        "excluded_input_entries": [
            {
                "source_pdf_path": entry["source_pdf_path"],
                "source_md_path": entry["output_md_path"],
                "reason": "later-year supplement file in 2018-19 folder; excluded to keep section layer source_year homogeneous",
            }
            for entry in excluded
        ],
        "qa_results": qa,
    }
    write_outputs(sections, manifest)
    print(f"section_status={qa['status']}; sections={len(sections)}")
    return 0 if qa["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
