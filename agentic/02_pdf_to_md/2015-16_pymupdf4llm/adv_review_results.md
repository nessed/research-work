# Adversarial Review Results

## Summary

PASS for the requested direct PyMuPDF4LLM conversion comparison run.

The run found 29 PDFs directly inside the `2015-16` input folder and produced
29 Markdown files in the requested output folder. The conversion log records
zero failures. Page markers are present and match logged PDF page counts for all
outputs checked.

This review does not certify table or numeric fidelity.

## Checks Performed

- Confirmed `conversion_log.json` contains `29` entries.
- Confirmed all `29` log entries have `"success": true`.
- Confirmed no failed entries are present.
- Confirmed all logged Markdown output paths exist.
- Confirmed no generated Markdown output has zero length.
- Counted `<!-- page ... -->` markers in each Markdown file.
- Compared marker counts against logged PDF page counts.
- Spot-checked selected source PDFs against generated Markdown using direct
  PyMuPDF first-page extraction.

## Findings

### High Severity

None.

### Medium Severity

Table-heavy files remain risky for direct numeric/table use.

Evidence:

- `Economic_Indicators.pdf` first-page normalized overlap was lower than
  prose-heavy chapters, and the Markdown word count was higher than the direct
  first-page PDF extraction.
- Statistical supplement files are large and table-heavy. PyMuPDF4LLM Markdown
  is not enough to guarantee row/column fidelity.

Impact:

- Do not use these Markdown files as trusted numeric source material.
- Any table values, chart values, or exact figures need separate source-PDF QA.

### Low Severity

Some Markdown includes image placeholder text.

Example pattern:

```text
Picture ... intentionally omitted
```

Impact:

- This is acceptable for prose extraction.
- It may add noise to automated extraction and should be filtered or handled in
  later extraction prompts/scripts.

## Structural Result

| Check | Result |
| --- | --- |
| PDFs found | 29 |
| Markdown outputs | 29 |
| Logged failures | 0 |
| Missing outputs | 0 |
| Zero-length outputs | 0 |
| Page-marker mismatches | 0 |

## Spot-Check Result

| PDF | Pages | First-page overlap |
| --- | ---: | ---: |
| Agriculture.pdf | 41 | 100.0% |
| Growth_And_Investment.pdf | 34 | 82.2% |
| Economic_Indicators.pdf | 6 | 76.0% |
| Research_Team.pdf | 1 | 100.0% |
| Supplement_2021_22.pdf | 216 | 100.0% |

The spot checks support the conclusion that prose is generally preserved well
enough for commentary extraction, but table-heavy content still requires
separate validation.

## Reproducibility Review

PASS with one caveat.

The run now includes `how_to_reproduce.md`, which records:

- source and output folders
- branch at run time
- PyMuPDF4LLM and PyMuPDF versions
- the direct API call used
- the page marker format
- equivalent one-off script code
- final run counts

Caveat:

- The actual one-off script used during the run was removed after execution, so
  reproducibility depends on the equivalent script embedded in
  `how_to_reproduce.md` rather than a retained executable script file.

## Original PDF Safety

No evidence suggests that original PDFs were modified. The conversion and review
steps read from:

```text
datalab_master\Master Data\pakistan_economic_survey\2015-16
```

and wrote artifacts only to:

```text
processed_pdfs\2015-16_pymupdf4llm
```

## Final Assessment

Accept this run as a direct PyMuPDF4LLM comparison artifact for
commentary/prose extraction.

Do not use it as a numeric ingestion source or as source truth for tables.

## Periodic Prose Spot-Check - 2026-06-06

PASS for sampled prose/commentary fidelity.

This additional check used the reproduction guide assumptions and compared
random source-PDF prose blocks against the corresponding Markdown page sections
using explicit page markers.

Method:

- Random seed: `20260606`
- Requested sample: `20` distinct PDFs
- Actual sample: `20` distinct PDFs with prose-like source blocks
- Source extraction: direct PyMuPDF page text/block extraction
- Markdown target: matching `<!-- page N -->` section
- Structural precheck: `29` log entries, `29` successes, `0` failures,
  `0` page-marker mismatches
- Skipped before filling sample: `Economic_Indicators.pdf`,
  `Research_Team.pdf`, and `Annexure_Ii_Tax_Expenditure.pdf` because the
  tightened filter did not find clean prose-like paragraphs

Result summary:

| Status | Count |
| --- | ---: |
| PASS | 17 |
| WARN | 3 |
| FAIL | 0 |

Compact sample evidence:

| PDF | Page | Result | Overlap | Exact phrase | Source snippet |
| --- | ---: | --- | ---: | --- | --- |
| Agriculture.pdf | 6 | WARN | 87.3% | no | Rice is an important food an Pakistan and it is the second wheat. It accounts for 3.1 per added in agriculture and 0.6 During 2015-16, rice |
| Annexure_I_Contingent.pdf | 2 | PASS | 100.0% | yes | objectives, volume procured, and domestic and international prices. The guarantees were issued against the commodity financing operations undertaken by TCP, PASSCO and provincia... |
| Manufacturing.pdf | 2 | PASS | 98.6% | yes | and chemical and in addition construction activities, Punjab government Apna Rozgar Scheme and improved availability of gas supplies facilitated fertilizer and cement sector. Th... |
| Supplement_2017_18.pdf | 35 | PASS | 100.0% | yes | sown at least once during the previous year Cultivated Area is that area which was sown at least during the year under reference or during the |
| Money_And_Credit.pdf | 3 | PASS | 90.3% | no | The NDA of the banking sy increase of Rs.676.6 billion dur FY 2016 against an increase of R the same period of last year. Hi on |
| Transport.pdf | 9 | PASS | 98.6% | yes | On 16th May, 2013, the ports Concessional Rights were transferred from Port of Singapore Authority (PSA) to the new operator viz, M/s China Overseas Ports Holding |
| Growth_And_Investment.pdf | 19 | WARN | 81.6% | no | encourage FDI and pro attracting FDI into Pakistan promote the linkages be foreign-owned private en supplier, sub-contractor or the country. Investment po a comprehensive frame... |
| Highlights_2015_16.pdf | 15 | PASS | 100.0% | yes | at the earliest. The other measures include earmarking of almost 80 percent of CPEC estimated outlay for electricity sector, import of LNG, extended cooperation with USA |
| Supplement_2018_19.pdf | 127 | PASS | 100.0% | yes | Rs. million B. OECD (b) E.C.O (c) Other Asian (d) Other African Total (a) Consortium Years Iran Turkey Total Afgha- Others Total Egypt Came- Sierra- Others |
| Social_Safety.pdf | 3 | WARN | 84.6% | no | BISP in its initial phase transfers using Pakistan P across Pakistan. But later efficiency and transparen beneficiaries, BISP sta payments mechanism in Smart Card and Mobile |
| Overview_Of_The_Economy.pdf | 2 | PASS | 100.0% | yes | The enabling environment has also revived confidence of the investors, on the back of successful operation Zarb-e-Azb which remained instrumental in creating an enabling environ... |
| Supplement_2021_22.pdf | 160 | PASS | 100.0% | yes | 3. Figures of Private School data from 2000-01 to 2004-05 is based on 'Census of Private Education Institution 1999-2000', Pakistan Bureau of Statistics, Islamabad. 4. Figures |
| Energy.pdf | 11 | PASS | 100.0% | yes | Alternative Energy Development Board (AEDB) is the sole representing agency of the federal government that was established with the main objective to facilitate, promote and enc... |
| Fiscal_Development.pdf | 7 | PASS | 100.0% | yes | against 3.8 percent of GDP during the comparable period of last year. The improvement in fiscal accounts came from10.4 percent growth in total revenues, of which |
| Environment.pdf | 11 | PASS | 100.0% | yes | Pakistan is the sixth largest nation of the world in terms of population size, having tremendous amount of natural resources, a variety of ecological regions and |
| Supplement_2019_20.pdf | 181 | PASS | 100.0% | yes | Previously, NTRC was collecting and providing data on road length with the classification of High Type (metalled roads/ asphalt/ cement roads) and Low Type (all unmetalled |
| Health.pdf | 1 | PASS | 99.2% | yes | The post MDGs Development Agenda Sustainable Development Goals (SDGs) has came into effect on 1st January, 2016. The Government of Pakistan has adopted the SDGs and |
| Capital_Markets.pdf | 5 | PASS | 100.0% | yes | Chemicals: In this sector 27 companies are listed having total paid up capital of Rs.34,434.65 million and the market capitalization of Rs.179,548.75 million. The profit after |
| Education.pdf | 6 | PASS | 93.0% | no | The overall education situation indicators such as likely enrolm institutes and teachers has improvement. The total numb during 2015 was recorded at compared to 42.09 million |
| Trade.pdf | 3 | PASS | 100.0% | yes | exports related production sector. The Committee has been tasked to device steps and measures which could enhance exports in short-term on one hand and deepen the |

Interpretation:

- The sampled Markdown pages preserve the tested prose well enough for
  commentary extraction.
- WARN rows are not missing-text failures; they reflect fragmented source-PDF
  extraction or line/block ordering noise where page-level overlap remained
  high.
- This check still does not validate table, chart, figure, or exact numeric
  fidelity.

