# Current Progress

Last updated: 2026-06-07

## Pipeline Status — All Years

| Year | 02 PDF→MD | 03 Sections | 04 Claims |
|---|---|---|---|
| 2015-16 | ✅ done | ❌ not started | ❌ |
| 2016-17 | ✅ done | ✅ PASS (2,121 sections) | ⬜ empty stub |
| 2017-18 | ✅ done | ❌ not started | ❌ |
| 2018-19 | ✅ done | ✅ PASS (2,736 sections) | ❌ |
| 2019-20 | ✅ done | ❌ not started | ❌ |
| 2020-21 | ✅ done | ❌ not started | ❌ |
| 2021-22 | ✅ done | ❌ not started | ❌ |
| 2022-23 | ✅ done | ❌ not started | ❌ |
| 2023-24 | ✅ done | ❌ not started | ❌ |
| 2024-25 | ✅ done | ❌ not started | ❌ |
| **Totals** | **10/10** | **2/10** | **0/10** |

## Active Area

Step 03 (section splitting) — 8 years pending.

## Critical Path

```
[now] → step 03 ×8 remaining years (free, no tokens)
      → write 3 step-04 scaffolding files (one-time)
      → step 04 claims extraction ×10 years (token-heavy)
```

## Notes

- Step 02 uses no LLM tokens (local pymupdf4llm library). All 10 years fully governed and done.
- Step 03 uses no LLM tokens (deterministic regex script). Use `split_2016_17_sections.py` as template.
- Step 04 is the only token-heavy step. Do not start until all years are at step 03.
- Step 04 needs 3 files written before any run: `how_to_reproduce.md`, `extraction_prompt.md`, `adv_review_prompt.md`.
- Per-MD chunking strategy: slice `sections.jsonl` by `source_md_path` at runtime; feed one doc at a time to LLM; cat outputs into one `claims.jsonl` per year.
- Normalization (step 05) is global across all years — do not normalize per-year or per-shard.

## Next Immediate Actions

1. Run step 03 on 2015-16, 2017-18, 2019-20, 2020-21, 2021-22, 2022-23, 2023-24, 2024-25
2. Write step 04 scaffolding files
3. Begin step 04 claims extraction starting from 2016-17
