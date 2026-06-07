# Smoke Test Notes — 2016-17 Claims Smoke Test

Date: 2026-06-07
Scope: Agriculture.md, Health.md, Trade.md

## Key observations

### Validator
- validate_claims.py had a syntax error (smart-quote characters embedded by editor in
  Python source). Fixed by rewriting via PowerShell here-string; all string literals
  now use double quotes and chr(0xXXXX) calls for Unicode normalization.
- Unicode apostrophe artifact (U+FFFD in sections.jsonl): fixed via normalize_for_grounding().
- Broken-word PDF artifact (e.g., "b **a** les"): fixed via 75% significant-word
  overlap fallback in check_grounding(). Both fixes validated against Agriculture claims.

### Agriculture (32 claims)
- High numeric density as expected; almost all records have numeric_or_table_sensitive=true.
- CPEC outlook, input-driven growth, commodity-level claims (cotton pest, sugarcane
  record, rice price, maize record, wheat improvement), edible oil import dependence,
  fertilizer subsidy and offtake, seed regulation, tractor surge, water investment,
  agricultural credit, livestock, trade (UAE ban, Royal Friesland, dairy duties, fish).
- No table cells extracted as standalone facts; claims grounded in prose surrounding tables.

### Health (20 claims)
- Lower numeric density; rights-based and programme-oriented claims dominate.
- Broken-word artifacts frequent in Food & Nutrition subsections; broken_word_artifact
  flag set on affected records.
- Two records flagged text_cutoff: EPI section text was cut mid-sentence, and Hepatitis
  section "The program also intends to decrease more than half..." is the end of text.
  Claims are still well-grounded; confidence set to medium for these two.

### Trade (21 claims)
- Table-adjacent sections mostly skipped (table data not claimed as certified facts).
- Balance-of-payments sub-sections yield rich claims; all carry numeric flags.
- Turkey carpet tariff constraint claim notable: specific exogenous policy barrier
  documented and flagged.
- GSP+ EU impact was extracted from a Box section (two claims: total and textile-specific).
- FX reserves record captures both the October peak and the March-end decline.

## Grounding method
- Exact substring match after normalize_for_grounding() (strips **, HTML, normalizes
  Unicode quotes/dashes, replaces U+FFFD with apostrophe).
- Fuzzy fallback: 75% of significant words (len >= 5) must appear in section text.
- All 73 records passed grounding check; validator reports 0 grounding failures.

## Schema-fit observations
- source_section_id not in schema; flagged in extraction_report.md for future v0.2.
- sector field is filename-derived (Agriculture, Health, Trade) and not a normalized
  taxonomy; downstream normalization step will need to handle this.