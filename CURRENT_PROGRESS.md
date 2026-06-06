# Current Progress

Last updated: 2026-06-07

## Active Area

- Pipeline documentation and Claims JSON preparation.

## Current Status

- PES folder map baseline is complete.
- PDF-to-Markdown runs are organized under `agentic/02_pdf_to_md/runs/`.
- Section splitting runs are organized under `agentic/03_section_splitting/runs/`.
- The active pipeline outline is now: PDF -> MD -> Sections -> Claims JSON -> Normalize -> Export.
- Schema discovery/hardening is completed provenance under `agentic/04_commentary_schema_discovery/`, not an active recurring pipeline stage.
- Markdown remains not certified for tables, charts, images, or numeric claims.

## Next Work

- Start a controlled Claims JSON pilot from reviewed sections when Ali asks.
- Use reviewed section text only for page-cited prose/commentary work.
- Do not normalize, export, or import to a database until Claims JSON extraction has passed review.
