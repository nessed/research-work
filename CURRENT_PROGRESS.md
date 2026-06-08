# Current Progress

Last updated: 2026-06-07

## Pipeline Status — All Years

| Year | 02 PDF→MD | 03 Sections | 04 Claims |
|---|---|---|---|
| 2015-16 | ✅ PASS audited | ❌ not started | ❌ |
| 2016-17 | ✅ PASS audited | ✅ PASS (2,121 sections) | ⬜ empty stub |
| 2017-18 | ✅ PASS audited | ❌ not started | ❌ |
| 2018-19 | ✅ PASS audited | ✅ PASS (2,736 sections) | ❌ |
| 2019-20 | ✅ PASS audited | ❌ not started | ❌ |
| 2020-21 | ✅ PASS audited | ❌ not started | ❌ |
| 2021-22 | ✅ PASS audited | ❌ not started | ❌ |
| 2022-23 | ✅ PASS audited | ❌ not started | ❌ |
| 2023-24 | ✅ PASS audited | ❌ not started | ❌ |
| 2024-25 | ✅ PASS audited | ❌ not started | ❌ |
| **Totals** | **10/10 PASS audited** | **2/10 PASS** | **0/10 production-ready** |

## Active Area

Step 03 (section splitting) — 8 years pending.

## Critical Path

```
[now] → step 03 ×8 remaining years (free, no tokens)
      → write 3 step-04 scaffolding files (one-time)
      → step 04 claims extraction ×10 years (token-heavy)
```

## Notes

- Step 02 uses no LLM tokens (local pymupdf4llm library). All 10 years PASS audited.
- Step 03 uses no LLM tokens (deterministic regex script). Use `split_2016_17_sections.py` as template.
- Step 04 is the only token-heavy step. Do not start until Step 02 is audited, all years are at step 03, and an extraction benchmark passes.
- Step 04 needs 3 files written before any run: `how_to_reproduce.md`, `extraction_prompt.md`, `adv_review_prompt.md`.
- Per-MD chunking strategy: slice `sections.jsonl` by `source_md_path` at runtime; feed one doc at a time to LLM; cat outputs into one `claims.jsonl` per year.
- Normalization (step 05) is global across all years — do not normalize per-year or per-shard.

## Next Immediate Actions

1. Build gold-standard extraction benchmark (annotate 20-30 sections manually).
2. Upgrade PDF-to-MD QA script to check first/middle/last pages and separate table checks.
3. Pause all full Step 03 and Step 04 runs until audits pass.
