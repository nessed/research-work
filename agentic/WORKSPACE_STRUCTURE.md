# Workspace Structure

This file defines the canonical folder layout for `datalab_ali`.

## Instruction File Hierarchy

Read files in this order when starting work on a pipeline step:

1. Global rules — `PROJECT_CONTEXT.md` (FIXED_CONTEXT + PERMANENT_CONSTRAINTS),
   `datalab_master/CLAUDE.md`
2. Pipeline workflow — `agentic/PIPELINE_PLANNING_REPORT.md`
3. Folder layout — `agentic/WORKSPACE_STRUCTURE.md` (this file)
4. Reproducibility index — `agentic/REPRODUCIBILITY.md`
5. Step instructions — `agentic/0N_<stepname>/README.md` and step spec files
   (e.g. `split_rules.md`, `section_schema.json`)
6. Run template — one reviewed run under `agentic/0N_<stepname>/runs/`
7. Active status — `CURRENT_PROGRESS.md` (snapshot only, not instructions)

Run evidence (manifests, QA reports, `adv_review_results.md`, `sections.jsonl`,
etc.) lives under run folders and must not be edited by future pipeline agents.
Situation reports under `agentic/sitreps/` are auto-generated history; do not
treat them as instructions.

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
  - Canonical PDF-to-Markdown stage instructions, run folders, and archived
    conversion attempts.
- `03_section_splitting/`
  - Markdown-to-section specs, future runs, QA, and review evidence.
- `04_claims_json/`
  - Claims JSON extraction stage. Work has not started.
- `05_normalize/`
  - Normalize reviewed Claims JSON. Work has not started.
- `06_export/`
  - Export reviewed normalized JSON. Work has not started.
- `archive/`
  - Archived or completed provenance, including schema discovery and hardening.
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

Completed design/provenance folders may remain in place when their outputs are
still referenced by later stages. They should be labelled as provenance, not as
active pipeline stages.

## Derived Outputs

New derived research outputs should go under `agentic/`. Root-level derived
folders such as `processed_pdfs/` are not active destinations.

## Research Use Rule

Original PDFs remain source truth. Markdown is a working text layer for
page-cited prose/commentary extraction. Tables, chart values, exact numbers,
rankings, totals, and footnotes require separate source-PDF QA.

