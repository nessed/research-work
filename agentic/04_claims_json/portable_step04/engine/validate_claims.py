"""
QA validator for claims.jsonl output from step 04 (hardened gate).
Usage:
    python validate_claims.py --claims <path/claims.jsonl> --sections <path/sections.jsonl>
Exits 0 on clean, 1 on any validation failure.

This script is the objective gate for step 04. It enforces exact frozen-schema-v0.1
compliance so that any CLI agent (Claude Code / GPT Codex / Antigravity) producing
claims is held to an identical standard. Do not rewrite this file inside a run; only
run it.
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

# Exact top-level key set from commentary_schema_v0.1 record_template (29 keys).
SCHEMA_KEYS = {
    "source_year", "source_file", "sector", "subsection", "source_page",
    "source_table_or_figure", "evidence_type", "source_quote", "claim_type", "claim",
    "indicator_or_subject", "topic_tags", "sentiment_signal", "time_orientation",
    "actor", "actors", "policy_or_programme", "policy_or_programmes",
    "constraint_or_risk", "cause", "effect", "comparison", "geography",
    "data_status_flags", "numeric_or_table_sensitive", "requires_pdf_numeric_qa",
    "markdown_quality_flags", "confidence", "needs_human_review",
}

# Exact comparison sub-object key set.
COMPARISON_KEYS = {"dimension", "baseline", "comparator", "direction"}

LIST_FIELDS = ("topic_tags", "actors", "policy_or_programmes", "data_status_flags",
               "markdown_quality_flags")
BOOL_FIELDS = ("numeric_or_table_sensitive", "requires_pdf_numeric_qa",
               "needs_human_review")

CLAIM_TYPES = {
    "sector_performance", "cause_effect", "policy_action", "commitment_or_plan",
    "constraint", "risk_or_shock", "outlook", "reform", "investment_priority",
    "programme_or_project", "regional_comparison", "data_caveat",
    "need_for_improvement", "security_cost", "publication_note", "other",
}

EVIDENCE_TYPES = {
    "prose", "table_note", "table_or_indicator", "figure_text",
    "preface_or_publication_note", "table_of_contents", "mixed",
}

SENTIMENT_SIGNALS = {"positive", "negative", "mixed", "neutral", "unclear", ""}

TIME_ORIENTATIONS = {
    "past", "current", "past_or_current", "future", "ongoing",
    "multi_period", "general", "unclear", "",
}

CONFIDENCE_VALUES = {"high", "medium", "low"}

COMPARISON_DIRECTIONS = {
    "increase", "decrease", "improvement", "deterioration",
    "higher_than", "lower_than", "shift", "no_change", "unclear", "",
}

DATA_STATUS_FLAGS = {
    "provisional", "revised", "final", "not_available", "estimated",
    "base_year_change", "definition_note", "rounding_note", "source_note",
    "projection_based", "survey_method_note",
}

MARKDOWN_QUALITY_FLAGS = {
    "broken_words", "table_layout_noise", "figure_text", "page_order_noise",
    "omitted_picture_placeholder", "low_confidence_heading",
}


def load_jsonl(path):
    records = []
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append((i, json.loads(line)))
            except json.JSONDecodeError as e:
                print(f"  ERROR line {i}: invalid JSON -- {e}")
                records.append((i, None))
    return records


def normalize_for_grounding(text):
    text = re.sub(r"\*+", "", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace(chr(0x2018), "'").replace(chr(0x2019), "'")
    text = text.replace(chr(0x201C), '"').replace(chr(0x201D), '"')
    text = text.replace(chr(0x2013), "-").replace(chr(0x2014), "-")
    text = text.replace(chr(0xFFFD), "'")
    text = " ".join(text.split())
    return text.lower()


def check_grounding(source_quote, sections):
    norm_quote = normalize_for_grounding(source_quote)
    for s in sections:
        norm_text = normalize_for_grounding(s["text"])
        if norm_quote in norm_text:
            return True
        sig_words = re.findall(r"\b[a-z]{5,}\b", norm_quote)
        if sig_words:
            hit = sum(1 for w in sig_words if w in norm_text)
            if hit / len(sig_words) >= 0.75:
                return True
    return False


def build_section_index(sections_path):
    index = defaultdict(list)
    with open(sections_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            fname = Path(r.get("source_md_path", "")).name
            index[fname].append({
                "start_page": r.get("start_page"),
                "end_page": r.get("end_page"),
                "text": r.get("text", ""),
            })
    return index


def validate(claims_path, sections_path):
    errors = []
    warnings = []

    print(f"\nLoading claims: {claims_path}")
    claim_rows = load_jsonl(claims_path)
    total = len(claim_rows)
    print(f"  {total} lines loaded")

    parse_errors = sum(1 for _, r in claim_rows if r is None)
    if parse_errors:
        errors.append(f"{parse_errors} lines failed JSON parse")

    valid_rows = [(i, r) for i, r in claim_rows if r is not None]

    section_index = None
    if sections_path:
        print(f"Loading sections: {sections_path}")
        section_index = build_section_index(sections_path)
        print(f"  {sum(len(v) for v in section_index.values())} sections across {len(section_index)} files")

    source_file_counts = defaultdict(int)
    grounding_failures = []

    for line_no, rec in valid_rows:
        src = f"line {line_no} ({rec.get('source_file', '?')} p{rec.get('source_page', '?')})"

        # Exact field set: no missing, no extra.
        present = set(rec.keys())
        for missing in SCHEMA_KEYS - present:
            errors.append(f"{src}: missing field '{missing}'")
        for extra in present - SCHEMA_KEYS:
            errors.append(f"{src}: extra field '{extra}' not in schema v0.1")

        if rec.get("needs_human_review") is not True:
            errors.append(f"{src}: needs_human_review is not true (value: {rec.get('needs_human_review')!r})")

        for bfield in BOOL_FIELDS:
            if not isinstance(rec.get(bfield), bool):
                errors.append(f"{src}: {bfield} must be boolean, got {type(rec.get(bfield)).__name__!r}")

        for afield in LIST_FIELDS:
            if not isinstance(rec.get(afield), list):
                errors.append(f"{src}: {afield} must be a list")

        # comparison: exact 4-key dict, valid direction.
        comp = rec.get("comparison")
        if not isinstance(comp, dict):
            errors.append(f"{src}: comparison must be a dict")
        else:
            comp_keys = set(comp.keys())
            for missing in COMPARISON_KEYS - comp_keys:
                errors.append(f"{src}: comparison missing key '{missing}'")
            for extra in comp_keys - COMPARISON_KEYS:
                errors.append(f"{src}: comparison has extra key '{extra}' not in schema v0.1")
            direction = comp.get("direction", "")
            if direction not in COMPARISON_DIRECTIONS:
                errors.append(f"{src}: comparison.direction '{direction}' not in controlled vocab")

        # Controlled vocabularies.
        if rec.get("claim_type") not in CLAIM_TYPES:
            errors.append(f"{src}: claim_type '{rec.get('claim_type')}' not in controlled vocab")
        if rec.get("evidence_type") not in EVIDENCE_TYPES:
            errors.append(f"{src}: evidence_type '{rec.get('evidence_type')}' not in controlled vocab")
        if rec.get("sentiment_signal", "") not in SENTIMENT_SIGNALS:
            errors.append(f"{src}: sentiment_signal '{rec.get('sentiment_signal')}' not in controlled vocab")
        if rec.get("time_orientation", "") not in TIME_ORIENTATIONS:
            errors.append(f"{src}: time_orientation '{rec.get('time_orientation')}' not in controlled vocab")
        if rec.get("confidence") not in CONFIDENCE_VALUES:
            errors.append(f"{src}: confidence '{rec.get('confidence')}' not in controlled vocab")

        if isinstance(rec.get("data_status_flags"), list):
            for flag in rec["data_status_flags"]:
                if flag not in DATA_STATUS_FLAGS:
                    errors.append(f"{src}: data_status_flag '{flag}' not in controlled vocab")

        if isinstance(rec.get("markdown_quality_flags"), list):
            for flag in rec["markdown_quality_flags"]:
                if flag not in MARKDOWN_QUALITY_FLAGS:
                    errors.append(f"{src}: markdown_quality_flag '{flag}' not in controlled vocab")

        if not str(rec.get("source_quote", "")).strip():
            errors.append(f"{src}: source_quote is empty")
        if not str(rec.get("source_page", "")).strip():
            errors.append(f"{src}: source_page is empty")

        if rec.get("numeric_or_table_sensitive") is True and rec.get("requires_pdf_numeric_qa") is not True:
            errors.append(f"{src}: numeric_or_table_sensitive=true but requires_pdf_numeric_qa is not true")

        # Grounding.
        if section_index is not None:
            source_file = rec.get("source_file", "")
            source_quote = str(rec.get("source_quote", "")).strip()
            source_page_str = rec.get("source_page", "")
            sections_for_file = section_index.get(source_file, [])
            if source_file and source_quote and sections_for_file:
                try:
                    source_page = int(source_page_str)
                    matching = [
                        s for s in sections_for_file
                        if s["start_page"] <= source_page <= s["end_page"]
                    ]
                    if not matching:
                        warnings.append(
                            f"{src}: source_page {source_page} not found in any section for {source_file}"
                        )
                    else:
                        if not check_grounding(source_quote, matching):
                            grounding_failures.append(
                                f"{src}: source_quote not found in sections for page {source_page}"
                            )
                except (ValueError, TypeError):
                    warnings.append(f"{src}: source_page '{source_page_str}' is not an integer")

        source_file_counts[rec.get("source_file", "UNKNOWN")] += 1

    if section_index is not None:
        for fname in section_index:
            if fname not in source_file_counts:
                warnings.append(f"No claims extracted for source file: {fname}")

    print(f"\n{'='*60}")
    print("VALIDATION REPORT")
    print(f"{'='*60}")
    print(f"Total claim records:  {total}")
    print(f"Parse errors:         {parse_errors}")
    print(f"Errors:               {len(errors)}")
    print(f"Grounding failures:   {len(grounding_failures)}")
    print(f"Warnings:             {len(warnings)}")

    print("\nClaims per source file:")
    for fname, count in sorted(source_file_counts.items()):
        print(f"  {count:4d}  {fname}")

    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for e in errors:
            print(f"  [ERROR] {e}")

    if grounding_failures:
        print(f"\nGROUNDING FAILURES ({len(grounding_failures)}):")
        for g in grounding_failures:
            print(f"  [GROUND] {g}")

    if warnings:
        print(f"\nWARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  [WARN] {w}")

    if not errors and not grounding_failures:
        print("\nRESULT: PASS")
        return 0
    print("\nRESULT: FAIL -- fix errors before downstream use")
    return 1


def main():
    parser = argparse.ArgumentParser(description="Validate claims.jsonl output (hardened gate)")
    parser.add_argument("--claims", required=True, help="Path to claims.jsonl")
    parser.add_argument("--sections", required=False, default=None,
                        help="Path to source sections.jsonl (for grounding checks)")
    args = parser.parse_args()
    sys.exit(validate(args.claims, args.sections))


if __name__ == "__main__":
    main()