# Extraction Report — 2016-17 Claims Smoke Test

Run: `2016-17_claims_pymupdf4llm_hardened` (smoke test scope)
Date: 2026-06-07
Model: claude-sonnet-4-6 (agent-assisted, in-session)
Schema: commentary_schema_v0.1

## Scope

Smoke test: 3 documents out of 25 in the 2016-17 sections JSONL.
Documents selected for stylistic diversity:
- Agriculture.md — mixed prose + tables, input-heavy with numeric/policy claims
- Health.md — prose-heavy social sector chapter, programme and indicator claims
- Trade.md — table and number-heavy external sector chapter

## Record Counts

| Source File     | Sections in JSONL | Claims Extracted |
|-----------------|-------------------|------------------|
| Agriculture.md  | 66                | 32               |
| Health.md       | 41                | 20               |
| Trade.md        | 46                | 21               |
| **Total**       | **153**           | **73**           |

Average claims per section: 0.48 (plausible — many sections are table adjacents,
figure stubs, or page-header repetitions that yield no claims).

## Validation Result

PASS — `validate_claims.py` found 0 errors, 0 grounding failures.
22 warnings, all expected coverage warnings for the 22 unextracted files.

## Per-Document Notes

### Agriculture.md (32 claims)
- Coverage spans: sector framing, CPEC outlook, growth performance, cotton/sugarcane/
  rice/wheat/maize/edible-oil commodities, fertilizer policy (subsidy + offtake + DAP
  gap), seed regulations (PBR Act), tractor production, water investment, agricultural
  credit (target + performance + SBP schemes), livestock GDP/livelihoods, UAE poultry
  ban lifted, Royal Friesland FDI, dairy duties, fish exports.
- Almost all claims carry numeric_or_table_sensitive=true (as expected for Agriculture).
- Skipped: table-only rows in section stubs, repeated page-header sections.

### Health.md (20 claims)
- Coverage spans: constitutional rights framing, SDG commitment + operationalization,
  PM National Health Program, polio near-eradication, health facilities ratio, health
  expenditure gap vs WHO benchmark, FP&PHC Lady Health Workers, EPI immunization,
  malaria target, TB burden + incidence, hepatitis program, cancer hospitals, 2016-17
  physical targets, malnutrition prevalence, caloric availability, PSDP nutrition
  allocation, conclusion progress assessment.
- Many sections had broken-word artifacts (e.g., "p **r** ogram") from PDF conversion;
  marked with broken_word_artifact quality flag where present. Grounding still passes
  via fuzzy word-overlap fallback in the validator.
- Source quotes for EPI and Hepatitis sections are slightly truncated (text_cutoff flag)
  because the source section text was itself cut off at the section boundary.

### Trade.md (21 claims)
- Coverage spans: global trade contraction context, export decline, import surge,
  Export-led Growth Package, CPFTA, SAFTA/SAARC export growth, merchandise exports
  (July-March), fish exports, textile recovery, carpet Turkey constraint, export
  concentration (71.8%), GSP+ EU impact (textiles +55%, total +38%), CPEC import
  driver, China import share, trade deficit (+33.1%), current account deficit,
  remittances (marginal decline), capital/financial account surplus + FDI, FX reserves,
  conclusion/outlook.
- All balance-of-payments numerics flagged numeric_or_table_sensitive=true.

## Schema-Fit Notes (Future Schema Consideration)

The following gaps were observed but NOT added as new fields (flagged here instead):
- `source_section_id` would allow machine-traceable linking to the sections.jsonl record.
  Currently, grounding is done via source_file + source_page range. Would be useful in v0.2.
- `section_type` from the sections record (e.g., table_or_figure_adjacent vs
  paragraph_block) is not carried into the claim record. Useful for filtering but not
  added to avoid schema drift.

## QA Summary

- Validator: `validate_claims.py` exits 0 (PASS).
- Manual spot-check: 5 random claims verified by tracing source_quote to sections.jsonl.
- All records have needs_human_review=true.
- All numeric/percentage claims have both numeric_or_table_sensitive=true and
  requires_pdf_numeric_qa=true.
- No table values presented as final certified facts.
- Source quotes are verbatim excerpts, not paraphrases.

## Next Steps

Pending adversarial review PASS, proceed to full 2016-17 extraction (remaining 22 files).