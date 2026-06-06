# 2016-17 Schema Stress-Test Notes

## Scope

This is schema hardening only. It uses four diverse sample groups from the
reviewed 2016-17 section layer:

```text
agentic/03_section_splitting/runs/2016-17_section_split_pymupdf4llm_hardened/
```

No full claim extraction, production JSON normalization, database/table export,
or final research dataset was created. The original PDFs remain source truth.
Markdown tables, charts, and numeric values remain uncertified unless
separately QA'd against PDFs.

## Samples Chosen

1. `2016_17_sample_01_agriculture_finance_policy`
   - Sections:
     `pes_2016_17__agriculture__0049__p016`,
     `pes_2016_17__agriculture__0050__p017`
   - Why: prose-heavy agriculture narrative with named SBP/SECP initiatives,
     credit schemes, constraints, actors, and programme details.

2. `2016_17_sample_02_economic_indicators_dense_tables`
   - Sections:
     `pes_2016_17__economic_indicators__0001__p001`,
     `pes_2016_17__economic_indicators__0002__p002`
   - Why: dense table/numeric material with footnotes and status markers. This
     stresses the schema's ability to flag, not trust, table-derived content.

3. `2016_17_sample_03_transport_digital_policy_programmes`
   - Sections:
     `pes_2016_17__transport_and_communications__0053__p014`,
     `pes_2016_17__transport_and_communications__0054__p014`,
     `pes_2016_17__transport_and_communications__0119__p024`
   - Why: policy/programme-heavy text covering Digital Pakistan Policy,
     e-commerce regulation, and BISP disbursement systems.

4. `2016_17_sample_04_transport_weak_markdown_infrastructure_tables`
   - Sections:
     `pes_2016_17__transport_and_communications__0013__p005`,
     `pes_2016_17__transport_and_communications__0053__p014`
   - Why: weak Markdown case with table layout noise, broken words, and an
     encoding artifact.

## Schema Stress Result

The existing `commentary_schema_v0.1.json` mostly holds for the selected
2016-17 samples.

Fields already adequate:

- `source_year`, `source_file`, `sector`, `subsection`, and `source_page` cover
  provenance needs when populated from section metadata.
- `evidence_type` can distinguish prose, table/indicator material, figure text,
  mixed evidence, and table notes.
- `source_table_or_figure` and `indicator_or_subject` are necessary for the
  Economic Indicators samples.
- `topic_tags`, `actor`/`actors`, and `policy_or_programme`/
  `policy_or_programmes` cover the agriculture and transport policy samples.
- `comparison`, `data_status_flags`, `numeric_or_table_sensitive`, and
  `requires_pdf_numeric_qa` remain essential for table/numeric-heavy material.
- `markdown_quality_flags` is the right location for conversion weaknesses.

One schema hardening change is justified:

- Add `encoding_artifact` to the controlled vocabulary for
  `markdown_quality_flags`. The 2016-17 section splitter observed this flag in
  Transport and Communications text, including the Digital Pakistan Policy
  sample. Without it, extractors can still store the flag as free text, but the
  controlled vocabulary would lag actual QA evidence.

No other schema draft changes are justified from these four samples. The
samples reinforce existing guidance that table/indicator material should usually
produce data-caveat or source-metadata records unless a separate PDF numeric QA
task is approved.

## QA / Review Notes

- The sample manifest references reviewed section IDs only.
- Later-year supplement files were excluded from the section layer before these
  samples were selected.
- The selected sections are source-tagged text units, not extracted claims.
- No pilot claims were created from these samples.
- Any future extraction from these samples must keep source quotes short,
  page-cited, and flagged for PDF numeric QA whenever numbers/tables/charts are
  involved.
