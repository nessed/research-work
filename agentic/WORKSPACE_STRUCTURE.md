# Workspace Structure

This file defines the canonical folder layout for `datalab_ali`.

## Root

- `.claude/`
  - Local Claude settings and skills. Keep at root.
- `PROJECT_CONTEXT.md`
  - Stable project context and live status.
- `CURRENT_PROGRESS.md`
  - Short current progress snapshot.
- `datalab_master/`
  - Raw source materials. Do not move, rename, normalize, or delete files under
    `datalab_master/Master Data/`.
- `agentic/`
  - Reproducible AI-assisted research artifacts.
- `Work Reports/`
  - Human-facing work reports.
- `local_tools/`
  - Local tools and installers that are not research outputs.

## Agentic Work

- `01_pes_folder_map/`
  - Source filesystem inventory and review evidence.
- `02_pdf_to_md/`
  - PDF-to-Markdown runs and archived conversion attempts.
- `03_commentary_schema_discovery/`
  - Commentary pattern scan, schema work, stress tests, and extraction pilots.
- `reviews/`
  - Cross-cutting adversarial reviews.
- `sitreps/`
  - Situation reports.

## Active Vs Archive

Active task folders must contain the current output plus reproducibility and
review files. Archive folders preserve superseded evidence and must include a
README explaining original path, new path, reason, date, and status.

Do not mix active outputs with old attempts. Do not delete old research evidence
unless Ali explicitly asks and the deletion is recorded elsewhere.

## Derived Outputs

New derived research outputs should go under `agentic/`. Root-level derived
folders such as `processed_pdfs/` are not active destinations.

## Research Use Rule

Original PDFs remain source truth. Markdown is a working text layer for
page-cited prose/commentary extraction. Tables, chart values, exact numbers,
rankings, totals, and footnotes require separate source-PDF QA.
