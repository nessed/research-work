# Claims JSON Extraction Prompt - PES Commentary

Version: v0.1
Schema: `agentic/archive/04_commentary_schema_discovery/schema/commentary_schema_v0.1.json`
Frozen: do not modify fields mid-run. Flag schema gaps in `extraction_report.md`.

## Your Task

You will receive one extraction job: a batch of Step 03 section records from one
PES Markdown document. Each record is one JSON object from `sections.jsonl`.
Read each section's `text` field and extract structured commentary claims from
only those provided section records.


Run this as a fresh-context CLI-agent job. No API client or API key is required
by this stage prompt. Do not rely on memory from earlier jobs. Do not extract
claims from sections that are not included in the current job. A separate runner
will validate this job, store the accepted result, and later merge all accepted
job results into the year-level Step 04 `claims.jsonl`.

Output one JSON object per distinct commentary claim. Do not output one record
per sentence; one claim can span several sentences. Do not merge unrelated
claims from different paragraphs into one record.

Every output record must be grounded in one of the current job's section
records. If a plausible claim would require context from a prior or later job,
skip it unless the current section text itself supports the claim.

## Input Format

Each input record has these fields. They are already computed; do not re-derive
them.

```text
section_id        unique ID for the source section
source_year       e.g. "2016-17"
source_md_path    source Markdown path
source_pdf_path   original PDF path
sector            filename-derived chapter/sector label
heading_text      nearest heading above the section
start_page        start PDF page number
end_page          end PDF page number
section_type      heading_section | paragraph_block | table_or_figure_adjacent
numeric_or_table_sensitive  boolean pre-flagged by the splitter
markdown_quality_flags      known conversion issues in this section
text              Markdown section text to extract claims from
```

Do not touch raw PDFs while extracting claims. Use the reviewed Step 03 section
records as the working input.

## Output Format

Return a JSON array. Each array element must match this object shape exactly.
Do not add fields. Leave a field as `""`, `[]`, or `{}` if nothing explicit in
the source supports it.

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

## Field Rules

### Source Fields

- `source_year`: copy from the section record.
- `source_file`: filename only, extracted from `source_md_path`, e.g.
  `Agriculture.md`.
- `sector`: copy from the section record.
- `subsection`: use `heading_text`. Leave empty if unclear.
- `source_page`: use `start_page` as a string unless the claim clearly falls on
  another page inside the section page range.
- `source_table_or_figure`: table, figure, box, or chart identifier only when
  evidence comes from that object. Leave empty for prose.

### Evidence and Quote

- `evidence_type`: one of `prose`, `table_note`, `table_or_indicator`,
  `figure_text`, `preface_or_publication_note`, `table_of_contents`, `mixed`.
- `source_quote`: a short literal excerpt from the current job's section text.
  Do not paraphrase. Keep it short enough to be useful for grounding.

### Classification

- `claim_type`: one of `sector_performance`, `cause_effect`, `policy_action`,
  `commitment_or_plan`, `constraint`, `risk_or_shock`, `outlook`, `reform`,
  `investment_priority`, `programme_or_project`, `regional_comparison`,
  `data_caveat`, `need_for_improvement`, `security_cost`, `publication_note`,
  `other`.
- `claim`: concise paraphrase of the source-grounded commentary claim.
- `indicator_or_subject`: main indicator, metric, demographic group, or topic.
- `topic_tags`: array of topical labels.
- `sentiment_signal`: one of `positive`, `negative`, `mixed`, `neutral`,
  `unclear`, or empty string.
- `time_orientation`: one of `past`, `current`, `past_or_current`, `future`,
  `ongoing`, `multi_period`, `general`, `unclear`, or empty string.

### Actors and Programmes

- `actor`: primary explicit actor. Leave empty if not explicit.
- `actors`: all explicitly named actors in the local passage.
- `policy_or_programme`: primary named scheme, project, package, or framework.
- `policy_or_programmes`: all named schemes, projects, packages, or frameworks
  in the local passage.

### Causal and Comparative Fields

- `constraint_or_risk`: explicit bottleneck, shock, shortage, risk, or
  implementation constraint.
- `cause`: explicit cause only. Leave empty if inferred.
- `effect`: explicit effect or outcome only. Leave empty if inferred.
- `comparison.dimension`: what is compared, such as time, geography, sector, or
  gender.
- `comparison.baseline`: baseline value or period.
- `comparison.comparator`: comparator value or period.
- `comparison.direction`: one of `increase`, `decrease`, `improvement`,
  `deterioration`, `higher_than`, `lower_than`, `shift`, `no_change`,
  `unclear`, or empty string.
- `geography`: province, region, urban/rural area, district, country, or
  comparator geography when substantive.

### QA Flags

- `data_status_flags`: zero or more of `provisional`, `revised`, `final`,
  `not_available`, `estimated`, `base_year_change`, `definition_note`,
  `rounding_note`, `source_note`, `projection_based`, `survey_method_note`.
- `numeric_or_table_sensitive`: true when the claim depends on any number,
  percentage, target, table, chart, ranking, or exact before/after movement.
  If the source section is numeric/table-sensitive, default to true unless the
  claim is purely qualitative prose.
- `requires_pdf_numeric_qa`: true whenever `numeric_or_table_sensitive` is true.
  Also true for table-heavy claims even when no specific value is extracted.
- `markdown_quality_flags`: copy only relevant schema-approved flags from the
  source section if they affect the record.
- `confidence`: one of `high`, `medium`, `low`. This is extraction confidence,
  not truth confidence.
- `needs_human_review`: always true.

## What To Skip

- Do not extract claims from table-of-contents lines or page header/footer
  artifacts.
- Do not extract from page marker comments themselves.
- Do not extract table cell values as certified facts.
- If a section is purely table rows with no prose claim, either skip it or emit
  one table metadata/data caveat record.
- Do not infer actors, causes, effects, or policies not stated in the current
  job's section text.
- Do not add schema fields. Document schema gaps in the run report instead.

## Output Instructions

Return valid JSON only: one JSON array of claim records for the current job. Do
not include prose commentary, Markdown fences, file paths, logs, or trailing
commas.

The runner, not the model, writes `_supporting/job_results.jsonl` and final
`claims.jsonl`. Do not describe file operations in the response.
