# Claims JSON Extraction Prompt — PES Commentary

Version: v0.1
Schema: `agentic/archive/04_commentary_schema_discovery/schema/commentary_schema_v0.1.json`
Frozen: do not modify fields mid-run. Flag schema gaps in `extraction_report.md`.

---

## Your task

You will receive a batch of section records from a single PES Markdown document.
Each record is one JSON object from `sections.jsonl`. Your job is to read each
section's `text` field and extract structured commentary claims from it.

Run this as a CLI-agent workflow. No API client or API key is required by this
stage prompt. Process one source document internally at a time, then append that
document's records to the year-level Step 04 run output. Govern completion per
source year, not per individual file.

Output one JSON object per distinct commentary claim. Do not output one record
per sentence — one claim can span several sentences. Do not merge unrelated claims
from different paragraphs into one record.

---

## Input format (one document's sections)

Each input record has these fields (already computed — do not re-derive them):
Do not touch raw PDFs while extracting claims. Use the reviewed Step 03 section
records as the working input.

```
section_id        unique ID for the source section
source_year       e.g. "2016-17"
source_md_path    e.g. "agentic/02_pdf_to_md/runs/2016-17_pymupdf4llm_hardened/converted_md/Agriculture.md"
source_pdf_path   e.g. "datalab_master/Master Data/pakistan_economic_survey/2016-17/Agriculture.pdf"
sector            e.g. "Agriculture"  (filename-derived; may be messy for overview/annex files)
heading_text      nearest heading above the section
start_page        start PDF page number (integer)
end_page          end PDF page number (integer)
section_type      "heading_section" | "paragraph_block" | "table_or_figure_adjacent"
numeric_or_table_sensitive  boolean — pre-flagged by the splitter
markdown_quality_flags      list of known conversion issues in this section
text              the Markdown section text to extract claims from
```

---

## Output format — one record per claim

Produce a JSON object matching this template exactly. Do not add new fields.
Leave a field as `""`, `[]`, or `{}` if nothing explicit in the source supports it.
Do not edit the frozen schema mid-run.

```json
{
  "source_year": "",
  "source_file": "",
  "sector": "",
  "subsection": "",
  "source_page": "",
  "source_table_or_figure": "",
  "evidence_type": "",
  "source_quote": "",
  "claim_type": "",
  "claim": "",
  "indicator_or_subject": "",
  "topic_tags": [],
  "sentiment_signal": "",
  "time_orientation": "",
  "actor": "",
  "actors": [],
  "policy_or_programme": "",
  "policy_or_programmes": [],
  "constraint_or_risk": "",
  "cause": "",
  "effect": "",
  "comparison": {
    "dimension": "",
    "baseline": "",
    "comparator": "",
    "direction": ""
  },
  "geography": "",
  "data_status_flags": [],
  "numeric_or_table_sensitive": false,
  "requires_pdf_numeric_qa": true,
  "markdown_quality_flags": [],
  "confidence": "",
  "needs_human_review": true
}
```

---

## Field rules

### Source fields (copy from input section record)
- `source_year` — copy from section record.
- `source_file` — filename only, e.g. `Agriculture.md`. Extract from `source_md_path`.
- `sector` — copy from section record's `sector` field.
- `subsection` — use `heading_text` from the section record. Leave empty if unclear.
- `source_page` — use `start_page` from the section record as a string, e.g. `"3"`.
  If the claim clearly falls on a specific page within a multi-page section, use that.
- `source_table_or_figure` — table/figure identifier only when evidence comes from a
  non-prose object (e.g. `"Table 2.1"`, `"Box 3"`). Leave empty for pure prose.

### Evidence and quote
- `evidence_type` — one of: `"prose"` | `"table_note"` | `"table_or_indicator"` |
  `"figure_text"` | `"preface_or_publication_note"` | `"table_of_contents"` | `"mixed"`.
- `source_quote` — a short, directly lifted passage from the section `text` field that
  grounds the claim. Do NOT paraphrase. Keep it short (one sentence or phrase).
  The quote must be traceable back to the source text verbatim (after whitespace trim).

### Classification
- `claim_type` — pick ONE primary type from this controlled list:
  `"sector_performance"` | `"cause_effect"` | `"policy_action"` |
  `"commitment_or_plan"` | `"constraint"` | `"risk_or_shock"` | `"outlook"` |
  `"reform"` | `"investment_priority"` | `"programme_or_project"` |
  `"regional_comparison"` | `"data_caveat"` | `"need_for_improvement"` |
  `"security_cost"` | `"publication_note"` | `"other"`
  When a claim combines multiple patterns (e.g. action + outlook + effect),
  pick one primary type and use `cause`, `effect`, `topic_tags` for the rest.
- `claim` — concise paraphrase of the claim in your own words. One or two sentences.
- `indicator_or_subject` — the main indicator, metric, demographic group, or topic
  subject when applicable. Leave empty if the claim is purely qualitative.
- `topic_tags` — array of cross-cutting themes. Use existing tags before inventing new
  ones. Examples: `["agriculture", "crops", "water"]`, `["fiscal", "debt"]`,
  `["health", "programme", "bisp"]`, `["trade", "exports", "constraint"]`.
- `sentiment_signal` — one of: `"positive"` | `"negative"` | `"mixed"` | `"neutral"` |
  `"unclear"`. Code from the source wording, not your opinion.
- `time_orientation` — one of: `"past"` | `"current"` | `"past_or_current"` |
  `"future"` | `"ongoing"` | `"multi_period"` | `"general"` | `"unclear"`.

### Actors and programmes
- `actor` — primary actor when explicitly named (e.g. `"Government of Pakistan"`,
  `"SBP"`, `"SECP"`). Leave empty if not explicit.
- `actors` — array of all explicitly named actors in the local passage.
- `policy_or_programme` — primary named scheme/project/framework when explicit.
- `policy_or_programmes` — array of all named schemes in the local passage.
  Use for programme-heavy sections (Health, Education, Social Safety) where multiple
  schemes are named in one paragraph.

### Causal and comparative
- `constraint_or_risk` — the specific bottleneck, shock, or risk when explicit. Do not
  infer if not stated.
- `cause` — explicit cause only. Leave empty if you are inferring.
- `effect` — explicit effect/outcome only. Leave empty if you are inferring.
- `comparison.dimension` — what is being compared (e.g. `"time"`, `"sector"`,
  `"geography"`, `"gender"`).
- `comparison.baseline` — the baseline value or period.
- `comparison.comparator` — the comparator value or period.
- `comparison.direction` — one of: `"increase"` | `"decrease"` | `"improvement"` |
  `"deterioration"` | `"higher_than"` | `"lower_than"` | `"shift"` | `"no_change"` |
  `"unclear"`.
- `geography` — province, region, urban/rural, country comparator when substantive.
  Leave empty for incidental location mentions.

### QA flags
- `data_status_flags` — array, zero or more from: `"provisional"` | `"revised"` |
  `"final"` | `"not_available"` | `"estimated"` | `"base_year_change"` |
  `"definition_note"` | `"rounding_note"` | `"source_note"` | `"projection_based"` |
  `"survey_method_note"`.
- `numeric_or_table_sensitive` — boolean. Set `true` when the claim depends on any
  number, percentage, target, table, chart, ranking, or exact before/after movement.
  If the input section record has `numeric_or_table_sensitive: true`, default to `true`
  for all records from that section unless the claim is purely qualitative prose.
- `requires_pdf_numeric_qa` — boolean. Set `true` whenever `numeric_or_table_sensitive`
  is `true`. Also set `true` for table-heavy sections even if no specific value is
  extracted.
- `markdown_quality_flags` — copy relevant flags from the input section's
  `markdown_quality_flags` list if they affect this record. Leave empty if not relevant.
- `confidence` — one of: `"high"` | `"medium"` | `"low"`. This is your confidence in
  the extraction and classification, NOT in whether the government claim is true.
- `needs_human_review` — always `true` for this RA workflow. Never set to `false`.

---

## What to skip

- Do NOT extract claims from table-of-contents lines or page header/footer artifacts.
- Do NOT extract from `<!-- page N -->` markers themselves.
- Do NOT extract table cell values as final facts. If a section is purely table rows
  with no prose, output a single `data_caveat` or `table_or_indicator` record noting
  the table's existence, or skip the section if it has no extractable prose claim.
- Sections with `section_type = "table_or_figure_adjacent"` often contain layout
  noise. Extract prose commentary if present; flag with `evidence_type = "table_note"`
  or `"table_or_indicator"` as appropriate.
- Annex and supplement sections produce fewer prose claims. For these, prefer
  `data_caveat` or `publication_note` types over forcing sector-narrative types.
- Do NOT infer fields not stated in the source text. If an actor, cause, or effect is
  not explicitly present in the quote or surrounding passage, leave the field empty.
- Do NOT add fields not in the schema template above, even if they seem useful.
  Flag the gap in the run's `extraction_report.md` instead.

---

## Output instructions

Return a JSON array of claim records. Each element is one claim object matching the
template above. Output valid JSON only — no prose commentary, no markdown fences,
no trailing commas. One array per document batch.

The final Step 04 run root contains only `claims.jsonl`; put the manifest,
report, how-to, review files, logs, scripts, notes, and intermediate files under
`_supporting/`. Validate `claims.jsonl` with `validate_claims.py`; the validator
is the objective gate. Do not proceed if validation or review fails. Do not
normalize, export, or prepare Step 05/06 outputs in this stage.

Example minimal valid output:

```json
[
  {
    "source_year": "2016-17",
    "source_file": "Agriculture.md",
    "sector": "Agriculture",
    "subsection": "Performance during 2016-17",
    "source_page": "1",
    "source_table_or_figure": "",
    "evidence_type": "prose",
    "source_quote": "Agriculture is the lifeline of Pakistan's economy accounting for 19.5 percent of the gross domestic product",
    "claim_type": "sector_performance",
    "claim": "The PES frames agriculture as central to Pakistan's economy, citing its share of GDP and employment.",
    "indicator_or_subject": "agriculture GDP share",
    "topic_tags": ["agriculture", "gdp", "employment"],
    "sentiment_signal": "neutral",
    "time_orientation": "current",
    "actor": "",
    "actors": [],
    "policy_or_programme": "",
    "policy_or_programmes": [],
    "constraint_or_risk": "",
    "cause": "",
    "effect": "",
    "comparison": {"dimension": "", "baseline": "", "comparator": "", "direction": ""},
    "geography": "Pakistan",
    "data_status_flags": [],
    "numeric_or_table_sensitive": true,
    "requires_pdf_numeric_qa": true,
    "markdown_quality_flags": [],
    "confidence": "high",
    "needs_human_review": true
  }
]
```
