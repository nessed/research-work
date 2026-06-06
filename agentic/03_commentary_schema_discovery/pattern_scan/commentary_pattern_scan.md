# Commentary Pattern Scan - PES 2015-16

## Purpose

This is a schema-discovery scan of the 29 converted Pakistan Economic Survey
2015-16 Markdown files. It identifies recurring commentary patterns that can be
standardized for later JSON claim extraction.

This is not a claim extraction pass. It does not build a database, process new
PDFs, or certify table/chart/numeric fidelity. The original PDFs remain source
truth. Converted Markdown is a working text layer for LLM-assisted commentary
work only, and any table values, chart values, or exact figures need separate
source-PDF QA.

Note on paths: active schema-discovery outputs now live under
`agentic/03_commentary_schema_discovery`. The 29 Markdown source files reviewed
were present under `agentic/02_pdf_to_md/2015-16_pymupdf4llm`. Earlier copies
that were briefly written under `processed_pdfs/2015-16_pymupdf4llm` have been
archived under `archive/initial_processed_pdfs_location`.

## Corpus Reviewed

All 29 `.md` chapter/output files were reviewed at a high level:

`Agriculture`, `Annexure_I_Contingent`, `Annexure_Ii_Tax_Expenditure`,
`Annexure_Iii_Poverty`, `Annexure_Iv_War_On_Terror`, `Capital_Markets`,
`Economic_Indicators`, `Education`, `Energy`, `Environment`,
`Fiscal_Development`, `Growth_And_Investment`, `Health`,
`Highlights_2015_16`, `Inflation`, `Manufacturing`, `Money_And_Credit`,
`Overview_Of_The_Economy`, `Population`, `Public_Debt`, `Research_Team`,
`Social_Safety`, `Supplement_2017_18`, `Supplement_2018_19`,
`Supplement_2019_20`, `Supplement_2020_21`, `Supplement_2021_22`, `Trade`,
and `Transport`.

The scan used page markers in the form `<!-- page N -->` where available.

## Pattern Recommendations

### 1. Sector Performance Narrative

- Meaning: Statements describing whether a sector, subsector, or indicator
  improved, declined, recovered, underperformed, or remained stable.
- Example sectors/files: `Agriculture.md`, `Manufacturing.md`,
  `Fiscal_Development.md`, `Trade.md`, `Transport.md`, `Health.md`,
  `Capital_Markets.md`.
- Example quotes:
  - `Agriculture.md`, page 2: "During FY 2016, the performance of agriculture
    sector as a whole remained dismal..."
  - `Health.md`, page 1: "The Government of Pakistan has adopted the SDGs..."
- Recommended schema treatment: `claim_type = "sector_performance"` plus
  `sentiment_signal`, `time_orientation`, and `topic_tags`.
- Confidence: high.
- Risks/ambiguities: Performance statements often embed numbers from tables or
  chart-like text. Store the narrative claim, but mark exact numbers for human
  review unless verified against the PDF.

### 2. Cause-Effect Claim

- Meaning: A causal explanation where one factor is said to affect an outcome.
- Example sectors/files: `Agriculture.md`, `Growth_And_Investment.md`,
  `Inflation.md`, `Trade.md`, `Energy.md`, `Fiscal_Development.md`,
  `Annexure_Iv_War_On_Terror.md`.
- Example quotes:
  - `Agriculture.md`, page 2: "large decline in cotton production... impacted
    negatively on crops..."
  - `Trade.md`, page 17: "with the start of Ramadan and Eid, the flow of
    remittances will increase..."
- Recommended schema treatment: `claim_type = "cause_effect"` with populated
  `cause` and `effect` fields.
- Confidence: high.
- Risks/ambiguities: Some sentences imply causality without clear causal
  language. Extraction should distinguish explicit from inferred causality.

### 3. Policy Action

- Meaning: Actions already taken by government, regulators, ministries, or
  public bodies.
- Example sectors/files: `Agriculture.md`, `Capital_Markets.md`,
  `Education.md`, `Energy.md`, `Health.md`, `Fiscal_Development.md`,
  `Social_Safety.md`.
- Example quotes:
  - `Agriculture.md`, page 1: "the government announced Kissan Package in
    September, 2015."
  - `Capital_Markets.md`, page 8: "SECP has reviewed the existing framework..."
- Recommended schema treatment: `claim_type = "policy_action"` with `actor`,
  `policy_or_programme`, and `time_orientation = "past_or_current"`.
- Confidence: high.
- Risks/ambiguities: Some passages mix announcement, implementation, and
  intent. The schema should allow `time_orientation` and `confidence`.

### 4. Government Commitment Or Future Plan

- Meaning: Statements about what the government, ministry, regulator, or sector
  actor will do, plans to do, aims to do, or is expected to do.
- Example sectors/files: `Agriculture.md`, `Energy.md`, `Transport.md`,
  `Education.md`, `Environment.md`, `Public_Debt.md`.
- Example quotes:
  - `Agriculture.md`, page 1: "The government would bear the Rs 2.5 billion
    premium on the agricultural insurance..."
  - `Transport.md`, page 9: "Concessional Rights were transferred... to the new
    operator..."
- Recommended schema treatment: `claim_type = "commitment_or_plan"` with
  `time_orientation = "future"` or `"ongoing"`.
- Confidence: high.
- Risks/ambiguities: "Will" can describe a forecast, legal entitlement, or
  commitment. Extraction should not force all future-tense language into policy.

### 5. Constraint Or Bottleneck

- Meaning: Claimed barriers limiting performance or implementation.
- Example sectors/files: `Agriculture.md`, `Energy.md`,
  `Growth_And_Investment.md`, `Education.md`, `Health.md`,
  `Social_Safety.md`, `Transport.md`.
- Example quotes:
  - `Agriculture.md`, page 5: "payment difficulties restricted acreage..."
  - `Agriculture.md`, page 12: "due to lack of finances, the project could not
    be implemented."
- Recommended schema treatment: `claim_type = "constraint"` with
  `constraint_or_risk`.
- Confidence: high.
- Risks/ambiguities: A constraint can also be a cause. Keep `claim_type`
  primary, but allow `cause` and `effect` to be filled.

### 6. Risk Or Shock Explanation

- Meaning: External or internal shocks used to explain performance, policy
  response, or risk exposure.
- Example sectors/files: `Agriculture.md`, `Annexure_Iv_War_On_Terror.md`,
  `Environment.md`, `Growth_And_Investment.md`, `Trade.md`,
  `Fiscal_Development.md`.
- Example quotes:
  - `Agriculture.md`, page 1: "climate-temperature, precipitation, floods..."
  - `Agriculture.md`, page 1: "climate change and global slowdown in commodity
    prices..."
- Recommended schema treatment: `claim_type = "risk_or_shock"` with
  `constraint_or_risk`, and optionally `cause` / `effect`.
- Confidence: high.
- Risks/ambiguities: Some risks are actual shocks, while others are background
  vulnerability. Use `time_orientation` and `confidence`.

### 7. Outlook Or Expectation

- Meaning: Forecasts, expected outcomes, future prospects, or anticipated
  trends.
- Example sectors/files: `Agriculture.md`, `Inflation.md`,
  `Capital_Markets.md`, `Energy.md`, `Trade.md`, `Public_Debt.md`.
- Example quotes:
  - `Agriculture.md`, page 10: "Urea offtake is expected to be around..."
  - `Agriculture.md`, page 14: "EI Nino is expected to affect temperature and
    precipitation patterns..."
- Recommended schema treatment: `claim_type = "outlook"` with
  `time_orientation = "future"` and `sentiment_signal`.
- Confidence: high.
- Risks/ambiguities: Outlook passages often contain exact values. Store the
  qualitative expectation, and flag numeric detail for human review.

### 8. Sentiment Or Tone Signal

- Meaning: Optimistic, pessimistic, improving, deteriorating, or mixed language
  attached to a sector or policy area.
- Example sectors/files: `Agriculture.md`, `Overview_Of_The_Economy.md`,
  `Manufacturing.md`, `Capital_Markets.md`, `Trade.md`,
  `Fiscal_Development.md`.
- Example quotes:
  - `Agriculture.md`, page 2: "performance of agriculture sector as a whole
    remained dismal..."
  - `Overview_Of_The_Economy.md`, page 2: "revived confidence of the
    investors..."
- Recommended schema treatment: field `sentiment_signal`; not usually its own
  claim type unless the sentence is primarily evaluative.
- Confidence: high.
- Risks/ambiguities: Survey language can be promotional. Sentiment should be
  coded from the source wording, not from the model's opinion.

### 9. Reform Or Regulatory Narrative

- Meaning: Institutional reform, legal/regulatory framework changes,
  modernization, governance, transparency, or efficiency narratives.
- Example sectors/files: `Capital_Markets.md`, `Agriculture.md`,
  `Money_And_Credit.md`, `Education.md`, `Energy.md`,
  `Fiscal_Development.md`.
- Example quotes:
  - `Agriculture.md`, page 11: "The Seed Amendment Bill, 2015 was passed..."
  - `Capital_Markets.md`, page 8: "bring further efficiency and transparency
    in the book building process..."
- Recommended schema treatment: `claim_type = "reform"` plus `actor`,
  `policy_or_programme`, and tags such as `regulation`, `governance`,
  `transparency`.
- Confidence: high.
- Risks/ambiguities: Reform language can be broad and aspirational. Keep
  source quotes and require human review for strong conclusions.

### 10. Investment Or Development Priority

- Meaning: Priority areas, allocations, infrastructure development, investment
  focus, packages, or development initiatives.
- Example sectors/files: `Agriculture.md`, `Energy.md`, `Transport.md`,
  `Education.md`, `Health.md`, `Public_Debt.md`, `Highlights_2015_16.md`.
- Example quotes:
  - `Agriculture.md`, page 1: "a mega relief package... for small farmers..."
  - `Highlights_2015_16.md`, page 15: "earmarking of almost 80 percent of CPEC
    estimated outlay for electricity sector..."
- Recommended schema treatment: `claim_type = "investment_priority"` with
  `policy_or_programme` and `topic_tags`.
- Confidence: high.
- Risks/ambiguities: Many examples include financial amounts. Do not treat the
  amounts as final without PDF/table QA.

### 11. Programme Or Project Mention

- Meaning: Named schemes, projects, packages, institutions, or interventions.
- Example sectors/files: `Agriculture.md`, `Social_Safety.md`,
  `Education.md`, `Energy.md`, `Transport.md`, `Health.md`,
  `Environment.md`.
- Example quotes:
  - `Agriculture.md`, page 1: "Prime Minister's Agriculture Package..."
  - `Social_Safety.md`, page 3: "BISP..."
- Recommended schema treatment: field `policy_or_programme`; repeated named
  programmes may later justify a separate programme lookup table.
- Confidence: high.
- Risks/ambiguities: Programme names vary across years and can appear as
  acronyms. Normalize later, not during this discovery pass.

### 12. Regional Or Provincial Comparison

- Meaning: Commentary that distinguishes provinces, regions, urban/rural areas,
  districts, or administrative units.
- Example sectors/files: `Agriculture.md`, `Education.md`,
  `Annexure_Iii_Poverty.md`, `Population.md`, `Health.md`,
  `Fiscal_Development.md`.
- Example quotes:
  - `Agriculture.md`, page 12: "seed certification services in Gilgit
    Baltistan..."
  - `Agriculture.md`, page 14: "above normal precipitation is expected in NE
    and Central Punjab, Upper KP and Kashmir."
- Recommended schema treatment: tags in `topic_tags`; add optional
  `geography` in the draft schema.
- Confidence: medium.
- Risks/ambiguities: Some regional references are incidental locations; others
  are real comparisons. A separate geography field is useful, but extraction
  should not over-interpret location mentions.

### 13. Data Definition Or Caveat

- Meaning: Provisional estimates, revised figures, definitional notes, source
  caveats, non-comparability, or missing data warnings.
- Example sectors/files: `Economic_Indicators.md`, supplements,
  `Agriculture.md`, `Inflation.md`, `Public_Debt.md`, `Education.md`.
- Example quotes:
  - `Agriculture.md`, page 4: "P: Provisional..."
  - `Supplement_2021_22.md`, page 160: "Figures of Private School data..."
- Recommended schema treatment: `claim_type = "data_caveat"` or separate
  table later if numeric database ingestion begins.
- Confidence: high.
- Risks/ambiguities: These are essential for data work but lower priority for
  prose commentary. Keep them separate from substantive policy claims.

### 14. Need For Improvement Statement

- Meaning: Normative or diagnostic statements saying a sector needs
  improvement, strengthening, enhancement, capacity building, or modernization.
- Example sectors/files: `Agriculture.md`, `Education.md`, `Health.md`,
  `Energy.md`, `Capital_Markets.md`, `Transport.md`.
- Example quotes:
  - `Agriculture.md`, page 1: "improving agricultural productivity..."
  - `Agriculture.md`, page 17: "remove the bottlenecks and enhance access to
    financial services..."
- Recommended schema treatment: `claim_type = "need_for_improvement"` with
  `constraint_or_risk` and `effect` if explicit.
- Confidence: medium.
- Risks/ambiguities: Sometimes this is a policy goal, sometimes a critique.
  Sentiment and time orientation help disambiguate.

### 15. Security Or Conflict Cost Narrative

- Meaning: Commentary linking terrorism, conflict, security operations, or war
  costs to economic outcomes.
- Example sectors/files: `Annexure_Iv_War_On_Terror.md`,
  `Overview_Of_The_Economy.md`, `Growth_And_Investment.md`,
  `Fiscal_Development.md`.
- Example quotes:
  - `Overview_Of_The_Economy.md`, page 2: "successful operation Zarb-e-Azb..."
  - `Annexure_Iv_War_On_Terror.md`: war-on-terror annex material appears as a
    focused security/economic-cost source.
- Recommended schema treatment: `claim_type = "risk_or_shock"` with tag
  `security`, or a specific `claim_type = "security_cost"` if this theme is a
  major research interest.
- Confidence: medium.
- Risks/ambiguities: Some claims are macro-context rather than sector-specific.
  Avoid forcing them into a sector performance structure.

## Universal Vs Sector-Specific Patterns

Universal or near-universal across prose chapters:

- Sector performance narrative
- Cause-effect claim
- Policy action
- Government commitment or plan
- Constraint or bottleneck
- Risk or shock explanation
- Outlook or expectation
- Sentiment signal
- Programme/project mention

Common but less universal:

- Reform or regulatory narrative
- Investment/development priority
- Regional/provincial comparison
- Need for improvement statement
- Data definition or caveat

More sector-specific:

- Weather, climate, and crop shock narratives: strongest in `Agriculture` and
  `Environment`.
- Monetary/fiscal/accounting caveats: strongest in `Money_And_Credit`,
  `Fiscal_Development`, `Public_Debt`, `Economic_Indicators`, and supplements.
- Social programme delivery narratives: strongest in `Social_Safety`,
  `Health`, and `Education`.
- Infrastructure/project narratives: strongest in `Energy`, `Transport`, and
  `Highlights_2015_16`.
- Regulatory-market reform narratives: strongest in `Capital_Markets`,
  `Money_And_Credit`, and `Agriculture`.

## Practical Schema Implications

Recommended base extraction unit: one source-grounded commentary claim, with
one source quote and one page marker.

Recommended core fields:

- bibliographic/source fields: year, file, sector, subsection, page
- evidence fields: source quote, extracted claim, human review flag
- classification fields: claim type, topic tags, sentiment, time orientation
- analytical fields: actor, programme/policy, constraint/risk, cause, effect
- QA fields: confidence, table/numeric caveat flag

Do not make every pattern a top-level field. Most should be controlled values
in `claim_type` or `topic_tags`. Use separate tables later only for repeated
entities such as programmes/projects, actors/institutions, or geography.
