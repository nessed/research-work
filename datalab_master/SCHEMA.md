# Master Data — Provenance, Vintage & Time-Series Schema

**Status:** v0.1 (draft for the team, 4 June 2026). The contract for how every number gets into our database.
**Read with:** `CLAUDE.md` (the rules) in this folder.

---

## The one principle everything follows

> **A single statistic has many *vintages*.** Pakistan revises its data. "Pakistan GDP growth in FY2017‑18" is **not one number** — it is the *target* (Annual Plan), the *provisional* (first Economic Survey), the *revised*, the *final*, and the *latest restated* series. Each was published in a different document at a different time. **We keep all of them.** Overwriting a number with its later revision destroys the thing that makes us unique — and it is exactly the data Ali's vintage-bias research studies.

This forces one rule on the schema: **the primary key of a datapoint includes the document that reported it**, not just the indicator and the year.

---

## Three layers (build them in this order)

### Layer 1 — Document manifest *(already exists — extend it)*

Every year-folder already has a `manifest.csv` with `label, file_name, url`. **Keep that. Extend it** with five columns so each source document is fully reproducible:

```
label, file_name, url, publisher, doc_type, release_date, retrieved_at, sha256
```
- `publisher`   — `finance.gov.pk` | `pbs.gov.pk` | `sbp.org.pk` | …
- `doc_type`    — `economic_survey_chapter` | `statistical_supplement` | `budget_in_brief` | `demands_for_grants` | `proposal_thinktank` | …
- `release_date`— when the **publisher** released it (best known)
- `retrieved_at`— when **we** downloaded it (ISO‑8601)
- `sha256`      — hash of the raw file (proves it hasn't changed)

The manifest is **document-level provenance**. It is the anchor every datapoint points back to.

### Layer 2 — Series registry *(canonical indicators)*

One row per indicator, decoupled from any source's naming. Reuses the convention already in Ittela (`ind.[domain].[measure].[variant]`).

```
series_id, name, sector, unit, ref_period_type, default_base_year, definition, canonical_publisher, notes
```
- `series_id`   — e.g. `ind.gdp.growth.real.annual`, `ind.crops.cotton.production`, `ind.fiscal.revenue.tax.gdp`
- `definition`  — **lock this** (the GNI‑vs‑GDP lesson: per‑capita income in PK surveys = GNI/pop, *not* GDP/pop). One sentence that pins exactly what the number measures.
- `canonical_publisher` — who is the gold source of record when several publish it (PBS vs SBP vs Finance). Dedup rule lives here.

### Layer 3 — Observations *(the time-series facts — the heart)*

One row per (indicator × period × **reporting document**). This is where vintages live.

| column | meaning | example |
|---|---|---|
| `series_id` | FK → registry | `ind.crops.cotton.production` |
| `ref_period` | the period the value describes | `FY2017-18` |
| `ref_period_type` | `fiscal_year` \| `calendar_year` \| `quarter` \| `month` | `fiscal_year` |
| `value` | the number, as printed | `11946` |
| `unit` | unit, as printed | `000 bales` |
| `vintage_type` | maturity of this reading | `provisional` \| `revised` \| `final` \| `target` \| `latest` |
| **`source_publication`** | **the document that reported it — THE vintage key** | `Pakistan Economic Survey 2019-20` |
| `source_doc_year` | the publication's own year | `2019-20` |
| `source_file` | filename in this corpus | `2_agriculture.pdf` |
| `source_url` | from the manifest | `https://www.finance.gov.pk/survey/...` |
| `source_page` | page / table locator | `Table 2.4, PDF p20` |
| `base_year` | price base where relevant | `2015-16` |
| `extraction_method` | `table-parse` \| `ocr` \| `image-read` \| `api` | `table-parse` |
| `extraction_confidence` | `high` \| `medium` \| `low` | `high` |
| `retrieved_at` | when fetched | `2026-06-02` |
| `sha256` | hash of `source_file` | `…` |
| `notes` | anything a reviewer needs | `read from rendered image; level cross-checked` |

> **Primary key = (`series_id`, `ref_period`, `source_publication`).**
> Same indicator + same year + *different reporting document* = a **new row**, never an overwrite. That single choice makes the whole database vintage-aware.

---

## Worked example (real, from this corpus)

Cotton production for **FY2017‑18**, as printed in the **2019‑20** Economic Survey (`pakistan_economic_survey/2019-20/`, Table 2.4):

```
series_id=ind.crops.cotton.production  ref_period=FY2017-18  value=11946  unit=000 bales
vintage_type=final  source_publication="Pakistan Economic Survey 2019-20"
source_file="2_agriculture.pdf"  source_url="https://www.finance.gov.pk/survey/chapter_24/..."
source_page="Table 2.4"  extraction_method=table-parse  extraction_confidence=high
```

The **same** `FY2017-18` cotton figure also appears in the **2023‑24** survey's embedded `Supplement_2017_18.pdf`. If that printed value differs, it is a **second row** (same `series_id` + `ref_period`, `source_publication="Pakistan Economic Survey 2023-24"`) — the *revised* vintage. The diff between the two rows **is** the research signal. Never collapse them.

---

## How this fits what already exists

This is a **generalization of the vintage CSV Ali's Codex build already produced** (`Pakistan/data/tables/macro_gdp-growth-vintages.csv`: `fiscal_year, sector, vintage_type, value, unit, base_year, source, source_file, publication_fy, notes`). The mapping is 1:1 — `fiscal_year`→`ref_period`, `vintage_type`→`vintage_type`, `publication_fy`→`source_doc_year`, `source_file`→`source_file`. So adopting this schema **extends** existing work rather than replacing it; the GDP-growth vintage table is the first proof case.

The "latest restated" series (current best PBS numbers) is just `vintage_type=latest`. Error-vs-latest (the optimism analysis) is computed, not stored: join each vintage row to its `latest` row on (`series_id`,`ref_period`).

---

## Non-negotiable rules (enforced by review)

1. **No value without `source_file` + `source_url` + `source_page`.** If you can't point to where it was printed, it does not go in.
2. **Never overwrite a vintage.** Revisions are new rows. Append-only.
3. **Never fabricate or interpolate.** A gap stays a gap (`value` empty, `notes="not reported"`). No smoothing, no "if the trend continues."
4. **Raw is sacred.** The PDFs and manifests in the year-folders are read-only. Parsed data and extraction code live elsewhere (a `parsed/` zone + code repo), never by editing the raw.
5. **Every extraction is re-runnable.** The recipe (script + the exact source file + page) must let someone else reproduce the row. `extraction_method=image-read`/`ocr` rows get a second set of eyes (`extraction_confidence` + adversarial check) before they're trusted.
6. **Definitions are locked before counting.** Fill `definition` in the registry first; mismatched definitions (GNI vs GDP, nominal vs real, factor cost vs market price, fiscal vs calendar year) are the classic trap.

---

## Canonical ID domains (extend as needed)
`gdp` · `growth` · `inflation` · `fiscal` (revenue/expenditure/deficit/debt) · `external` (bop/trade/reserves/remittances) · `monetary` (m2/credit/policy-rate) · `crops` · `lsm` · `energy` · `social` (education/health/population/poverty) · `labour` · `markets` (kse100). Pattern: `ind.<domain>.<measure>.<variant>`.
