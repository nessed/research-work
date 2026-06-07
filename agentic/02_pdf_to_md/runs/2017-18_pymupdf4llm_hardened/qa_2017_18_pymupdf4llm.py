from __future__ import annotations

import hashlib
import json
import random
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import fitz


RUN_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = RUN_DIR.parents[3]
SOURCE_DIR = (
    PROJECT_ROOT
    / "datalab_master"
    / "Master Data"
    / "pakistan_economic_survey"
    / "2017-18"
)
CONVERTED_DIR = RUN_DIR / "converted_md"
REPRO_MANIFEST_PATH = RUN_DIR / "repro_manifest.json"
CONVERSION_LOG_PATH = RUN_DIR / "conversion_log.json"
QA_RESULTS_PATH = RUN_DIR / "qa_results.json"
QA_REPORT_PATH = RUN_DIR / "qa_report.md"
SEED = 20260607


PAGE_MARKER_RE = re.compile(r"<!-- page (\d+) -->")
TOKEN_RE = re.compile(r"[A-Za-z0-9]+")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def tokens(text: str) -> list[str]:
    return [match.group(0).lower() for match in TOKEN_RE.finditer(text)]


def token_overlap(source: str, target: str) -> float:
    source_counts = Counter(tokens(source))
    target_counts = Counter(tokens(target))
    total = sum(source_counts.values())
    if total == 0:
        return 0.0
    matched = sum(min(count, target_counts[token]) for token, count in source_counts.items())
    return round(matched / total, 4)


def markdown_pages(text: str) -> dict[int, str]:
    matches = list(PAGE_MARKER_RE.finditer(text))
    pages: dict[int, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        pages[int(match.group(1))] = text[start:end].strip()
    return pages


def pdf_page_text(pdf_path: Path, page_number: int) -> str:
    with fitz.open(pdf_path) as doc:
        page = doc.load_page(page_number - 1)
        return page.get_text("text").strip()


def choose_sample_page(pdf_path: Path, rng: random.Random) -> int | None:
    with fitz.open(pdf_path) as doc:
        candidates: list[int] = []
        for index in range(doc.page_count):
            text = doc.load_page(index).get_text("text")
            if len(tokens(text)) >= 60:
                candidates.append(index + 1)
        if not candidates:
            return None
        return rng.choice(candidates)


def status_from_overlap(overlap: float) -> str:
    if overlap >= 0.80:
        return "PASS"
    if overlap >= 0.60:
        return "WARN"
    return "FAIL"


def structural_checks(repro_manifest: dict[str, Any], conversion_log: list[dict[str, Any]]) -> dict[str, Any]:
    issues: list[str] = []
    entries = repro_manifest["entries"]

    pdf_paths = sorted(SOURCE_DIR.glob("*.pdf"), key=lambda path: path.name.lower())
    if len(entries) != len(pdf_paths):
        issues.append(f"manifest entries {len(entries)} != source PDFs {len(pdf_paths)}")
    if len(conversion_log) != len(pdf_paths):
        issues.append(f"conversion log entries {len(conversion_log)} != source PDFs {len(pdf_paths)}")

    seen_outputs: set[str] = set()
    page_marker_mismatches: list[dict[str, Any]] = []
    missing_outputs: list[str] = []
    zero_byte_outputs: list[str] = []
    hash_mismatches: list[str] = []
    log_hash_mismatches: list[str] = []
    log_entries_by_output = {
        item.get("output_md_path"): item for item in conversion_log if item.get("output_md_path")
    }

    for entry in entries:
        output_path = PROJECT_ROOT / entry["output_md_path"]
        output_key = entry["output_md_path"]
        if output_key in seen_outputs:
            issues.append(f"duplicate output path: {output_key}")
        seen_outputs.add(output_key)

        if not output_path.exists():
            missing_outputs.append(output_key)
            continue
        if output_path.stat().st_size == 0:
            zero_byte_outputs.append(output_key)
        actual_output_sha256 = sha256_file(output_path)
        if actual_output_sha256 != entry["output_sha256"]:
            hash_mismatches.append(output_key)
        log_entry = log_entries_by_output.get(output_key)
        if not log_entry:
            issues.append(f"missing conversion log entry for output: {output_key}")
        elif log_entry.get("success") and log_entry.get("output_sha256") != actual_output_sha256:
            log_hash_mismatches.append(output_key)

        text = output_path.read_text(encoding="utf-8")
        marker_count = len(PAGE_MARKER_RE.findall(text))
        if marker_count != entry["page_count"]:
            page_marker_mismatches.append(
                {
                    "output_md_path": output_key,
                    "page_count": entry["page_count"],
                    "page_markers": marker_count,
                }
            )

    failed_conversions = [item for item in conversion_log if not item.get("success")]
    issues.extend(f"missing output: {item}" for item in missing_outputs)
    issues.extend(f"zero-byte output: {item}" for item in zero_byte_outputs)
    issues.extend(f"hash mismatch: {item}" for item in hash_mismatches)
    issues.extend(f"conversion log output hash mismatch: {item}" for item in log_hash_mismatches)
    issues.extend(
        f"page marker mismatch: {item['output_md_path']}"
        for item in page_marker_mismatches
    )
    issues.extend(f"conversion failed: {item['source_pdf_path']}" for item in failed_conversions)

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "pdfs_found": len(pdf_paths),
        "manifest_entries": len(entries),
        "conversion_log_entries": len(conversion_log),
        "failed_conversions": len(failed_conversions),
        "missing_outputs": missing_outputs,
        "zero_byte_outputs": zero_byte_outputs,
        "hash_mismatches": hash_mismatches,
        "conversion_log_output_hash_mismatches": log_hash_mismatches,
        "page_marker_mismatches": page_marker_mismatches,
    }


def prose_fidelity_checks(repro_manifest: dict[str, Any]) -> dict[str, Any]:
    rng = random.Random(SEED)
    samples: list[dict[str, Any]] = []

    for entry in repro_manifest["entries"]:
        source_pdf = PROJECT_ROOT / entry["source_pdf_path"]
        output_md = PROJECT_ROOT / entry["output_md_path"]
        sample_page = choose_sample_page(source_pdf, rng)
        if sample_page is None:
            samples.append(
                {
                    "source_file_name": entry["source_file_name"],
                    "status": "SKIP",
                    "reason": "no page with at least 60 extractable tokens",
                }
            )
            continue

        source_text = pdf_page_text(source_pdf, sample_page)
        md_sections = markdown_pages(output_md.read_text(encoding="utf-8"))
        md_text = md_sections.get(sample_page, "")
        overlap = token_overlap(source_text, md_text)
        samples.append(
            {
                "source_file_name": entry["source_file_name"],
                "page": sample_page,
                "status": status_from_overlap(overlap),
                "token_overlap": overlap,
                "source_snippet": " ".join(source_text.split())[:240],
                "markdown_snippet": " ".join(md_text.split())[:240],
            }
        )

    counts = Counter(sample["status"] for sample in samples)
    return {
        "status": "FAIL" if counts.get("FAIL", 0) else "PASS",
        "seed": SEED,
        "sample_count": len(samples),
        "status_counts": dict(sorted(counts.items())),
        "samples": samples,
    }


def placeholder_checks(repro_manifest: dict[str, Any]) -> dict[str, Any]:
    pattern = re.compile(r"Picture .*? intentionally omitted", re.IGNORECASE)
    files: list[dict[str, Any]] = []
    total = 0
    for entry in repro_manifest["entries"]:
        output_md = PROJECT_ROOT / entry["output_md_path"]
        text = output_md.read_text(encoding="utf-8")
        count = len(pattern.findall(text))
        total += count
        if count:
            files.append({"output_md_path": entry["output_md_path"], "count": count})
    return {
        "status": "INFO",
        "total_omitted_picture_placeholders": total,
        "files": files,
        "research_use_note": "Charts/images are not certified from Markdown and require separate PDF review before use in research claims.",
    }


def table_numeric_policy() -> dict[str, str]:
    return {
        "status": "NOT_CERTIFIED",
        "policy": "Markdown is not certified for table, chart, numeric, row/column, total, ranking, or footnote fidelity.",
        "required_follow_up": "Any numeric or table-derived claim must be verified against the source PDF and, where needed, rendered page evidence.",
    }


def write_report(results: dict[str, Any]) -> None:
    structural = results["structural_checks"]
    prose = results["prose_fidelity_checks"]
    placeholders = results["placeholder_checks"]
    table_policy = results["table_numeric_policy"]

    lines = [
        "# QA Report",
        "",
        "## Summary",
        "",
        f"- Generated UTC: `{results['generated_at_utc']}`",
        f"- Overall status: `{results['overall_status']}`",
        f"- Structural checks: `{structural['status']}`",
        f"- Prose fidelity checks: `{prose['status']}`",
        f"- Table/numeric certification: `{table_policy['status']}`",
        "",
        "## Structural Checks",
        "",
        f"- PDFs found: `{structural['pdfs_found']}`",
        f"- Manifest entries: `{structural['manifest_entries']}`",
        f"- Conversion log entries: `{structural['conversion_log_entries']}`",
        f"- Failed conversions: `{structural['failed_conversions']}`",
        f"- Page-marker mismatches: `{len(structural['page_marker_mismatches'])}`",
        f"- Missing outputs: `{len(structural['missing_outputs'])}`",
        f"- Zero-byte outputs: `{len(structural['zero_byte_outputs'])}`",
        f"- Hash mismatches: `{len(structural['hash_mismatches'])}`",
        f"- Conversion log output hash mismatches: `{len(structural['conversion_log_output_hash_mismatches'])}`",
        "",
        "## Prose Fidelity",
        "",
        f"- Random seed: `{prose['seed']}`",
        f"- Sample count: `{prose['sample_count']}`",
        f"- Status counts: `{prose['status_counts']}`",
        "",
        "| PDF | Page | Status | Token overlap |",
        "| --- | ---: | --- | ---: |",
    ]
    for sample in prose["samples"]:
        page = sample.get("page", "")
        overlap = sample.get("token_overlap", "")
        lines.append(
            f"| {sample['source_file_name']} | {page} | {sample['status']} | {overlap} |"
        )

    lines.extend(
        [
            "",
            "## Images And Charts",
            "",
            f"- Omitted picture placeholders: `{placeholders['total_omitted_picture_placeholders']}`",
            f"- Policy: {placeholders['research_use_note']}",
            "",
            "## Table And Numeric Use",
            "",
            table_policy["policy"],
            "",
            table_policy["required_follow_up"],
        ]
    )
    QA_REPORT_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    repro_manifest = load_json(REPRO_MANIFEST_PATH)
    conversion_log = load_json(CONVERSION_LOG_PATH)
    structural = structural_checks(repro_manifest, conversion_log)
    prose = prose_fidelity_checks(repro_manifest)
    placeholders = placeholder_checks(repro_manifest)
    table_policy = table_numeric_policy()

    overall_status = "PASS" if structural["status"] == "PASS" and prose["status"] == "PASS" else "FAIL"
    results = {
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "overall_status": overall_status,
        "structural_checks": structural,
        "prose_fidelity_checks": prose,
        "placeholder_checks": placeholders,
        "table_numeric_policy": table_policy,
    }
    QA_RESULTS_PATH.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
        newline="\n",
    )
    write_report(results)
    print(f"overall_status={overall_status}")
    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
