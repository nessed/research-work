# How to Reproduce — 2016-17 Claims Smoke Test

Run: `2016-17_claims_pymupdf4llm_hardened` (smoke test)
Date: 2026-06-07

## Source

- Input sections JSONL:
  `agentic/03_section_splitting/runs/2016-17_section_split_pymupdf4llm_hardened/sections.jsonl`
  (PASS-reviewed, 2,121 sections, 25 source files)
- Schema: `agentic/archive/04_commentary_schema_discovery/schema/commentary_schema_v0.1.json`
- Extraction prompt: `agentic/04_claims_json/extraction_prompt.md`
- Model: `claude-sonnet-4-6`

## Smoke Test Scope

Three source files extracted:
- Agriculture.md (66 sections → 32 claims)
- Health.md (41 sections → 20 claims)
- Trade.md (46 sections → 21 claims)

## Steps to Reproduce

1. Filter sections.jsonl by source_md_path for each target document.
   The run folder contains pre-filtered smoke input files:
   - smoke_agriculture_sections.jsonl (66 lines)
   - smoke_health_sections.jsonl (41 lines)
   - smoke_trade_sections.jsonl (46 lines)

2. Apply extraction_prompt.md to each document's sections using claude-sonnet-4-6.
   Output per document was written to:
   - smoke_agriculture_claims.jsonl (32 records, via gen_agriculture_claims.py)
   - smoke_health_claims.jsonl (20 records, via gen_health_claims.py)
   - smoke_trade_claims.jsonl (21 records, direct in-session generation)

3. Combine into final root claims.jsonl:
   python -c "
   import json
   files = ['smoke_agriculture_claims.jsonl','smoke_health_claims.jsonl','smoke_trade_claims.jsonl']
   with open('../claims.jsonl','w',encoding='utf-8') as out:
       for fn in files:
           for line in open(fn,encoding='utf-8'):
               if line.strip(): out.write(line)
   "

4. Validate:
   python agentic/04_claims_json/validate_claims.py \
     --claims agentic/04_claims_json/runs/2016-17_claims_pymupdf4llm_hardened/claims.jsonl \
     --sections agentic/03_section_splitting/runs/2016-17_section_split_pymupdf4llm_hardened/sections.jsonl

   Result: PASS (0 errors, 0 grounding failures, 22 expected coverage warnings)

## Caveats

- In-session generation means exact claim wording may vary on re-run; source quotes
  are verbatim and grounding is validator-confirmed.
- broken_word_artifact sections (PDF bold-letter spacing) use the validator fuzzy
  75% word-overlap fallback for grounding.
- Source quotes for two Health sections (EPI, Hepatitis) are slightly truncated because
  the section text was cut off at the section boundary (text_cutoff flag set).
- SHA-256 of root claims.jsonl: dd65e72b7f6dd39bc8b1e267c5b921e12324c111fef6ad9d6a4236fbce2f358e
