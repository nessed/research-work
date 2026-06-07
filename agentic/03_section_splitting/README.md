# Section Splitting

Section splitting converts converted Markdown into smaller source-tagged
sections.

Pipeline position:

```text
Raw PDF
-> PDF-to-Markdown with page markers
-> Section splitting
-> Claim extraction
-> JSON normalization
-> Database/table export
```

This folder contains the section-splitting spec and all run folders.

## Purpose

The splitter takes a `converted_md/` folder from a reviewed PDF-to-MD run and
produces smaller sections that preserve source grounding. Each section must
retain the source year, source Markdown path, source PDF path, sector, heading,
page span, text, and quality flags.

Section splitting must not create claims, summaries, interpretations, or
database-ready facts. It only prepares source-tagged text units for later claim
extraction.

## Runs

Run folders live under:

```text
agentic/03_section_splitting/runs/<year>_<tool>_<label>/
```

Each run folder must contain:

- `sections.jsonl` — one JSON object per source-tagged section
- `section_manifest.json` — inputs, outputs, counts, hashes, environment
- `section_split_report.md` — counts, warnings, skipped files, QA summary
- `how_to_reproduce.md` — exact input folder, script command, QA, result
- `adv_review_prompt.md` — run-specific review prompt
- `adv_review_results.md` — fresh-context reviewer findings

Use `2016-17_section_split_pymupdf4llm_hardened` (PASS, 2,121 sections) as the
template run.

## Files

- `section_schema.json`
  Defines the required output fields for each section.
- `split_rules.md`
  Defines simple deterministic splitting rules.
- `how_to_reproduce.md`
  Stage-level execution guide; run-specific paths and commands live in each
  run folder's own `how_to_reproduce.md`.
- `adv_review_prompt.md`
  Base review prompt for a fresh-context adversarial reviewer.
- `runs/`
  One subfolder per completed or in-progress section split run.
