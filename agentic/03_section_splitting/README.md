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

This folder defines the section-splitting engine/spec only. It does not contain
split output data.

## Purpose

The splitter should take a `converted_md/` folder from a reviewed PDF-to-MD run
and produce smaller sections that preserve source grounding. Each section must
retain the source year, source Markdown path, source PDF path, sector, heading,
page span, text, and quality flags.

Section splitting must not create claims, summaries, interpretations, or
database-ready facts. It only prepares source-tagged text units for later claim
extraction.

## Current Status

- Spec only.
- No data has been processed.
- No run folder exists yet.
- No `sections.jsonl` exists yet.
- Raw PDFs and converted Markdown files are not modified.

## Files

- `section_schema.json`
  Defines the required output fields for each future section.
- `split_rules.md`
  Defines simple deterministic splitting rules.
- `how_to_reproduce.md`
  Explains how a future run should be executed and documented.
- `adv_review_prompt.md`
  Prompt for a future read-only adversarial reviewer.
