# Project Context

## Project Identity

This repository supports Ali's LUMS RA work under Ali Hasanain.

The project concerns Pakistan economic data and AI-assisted research workflows, including Pakistan Economic Surveys, budget documents, official sources, commentary, reproducible analysis, and source-grounded data work.

## Core Operating Principle

Reproducibility is king.

Every meaningful output should be traceable, reviewable, and reproducible from source materials. Raw source files are evidence and should be treated as read-only unless the user explicitly instructs otherwise.

## Agent Behavior

- Do not rush into mass processing.
- Do not overbuild or create unnecessary infrastructure.
- Do not invent facts, sources, counts, or interpretations.
- Do not silently modify raw data.
- Prefer small, scoped, reviewable subtasks.
- Clarify scope before acting when the task is ambiguous.
- Keep responses concise, practical, and tied to the requested work.
- Preserve provenance, filenames, paths, and source layout unless explicitly told to normalize them.

## Agentic Workflow Norm

For important or reusable tasks, create a task folder under `agentic/`.

Task folders should keep derived outputs and, where relevant:

- `manifest.md`
- `review_report.md`
- prompts or other review artifacts needed for reproducibility

`manifest.md` should explain what was produced, which inputs were used, how to reproduce the output, how to validate it, known limitations, and what was out of scope.

Use headless Claude or any cross-agent review only when explicitly approved by the user. Cross-agent review should test outputs against source data where allowed, not only check whether a JSON or report is internally consistent.

## Current Project State

- `agentic/corpus_inventory/` exists.
- `agentic/corpus_inventory/pes_inventory.json` exists.
- `agentic/corpus_inventory/manifest.md` exists.
- Claude headless filesystem review passed.
- `agentic/corpus_inventory/review_report.md` reports `PASS` with `High` confidence.
- Duplicate-looking PES supplements and filename irregularities were flagged.
- Raw `Master Data` files were not modified.

## Permanent Constraints

- Do not modify `Master Data` unless explicitly told.
- Do not inspect PDF contents unless the task says to inspect PDF contents.
- Do not start family mapping unless explicitly assigned.
- Do not start extraction unless explicitly assigned.
- Do not start database imports unless explicitly assigned.
- Do not create automation or large processing flows unless explicitly assigned.
- Keep derived work under `agentic/` unless told otherwise.
