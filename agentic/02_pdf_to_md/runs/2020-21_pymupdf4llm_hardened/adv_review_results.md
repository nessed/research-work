# Adversarial Review Results

## Reviewer Invocation

- Requested reviewer order: call Claude first; if Claude fails or is blocked,
  call a Codex sub-agent.
- Claude attempt:
  `claude --help`
- Claude result:
  blocked by PowerShell execution policy:
  `claude.ps1 cannot be loaded because running scripts is disabled on this system`
- Fallback reviewer:
  Codex sub-agent `019e9ff5-7131-7130-8c60-beed940c1bc8`

## Reviewer Findings

**PASS/FAIL Summary**

Overall: **FAIL for the strict “does not process other years” review criterion**, otherwise the Step 02 conversion evidence is structurally sound.

Findings, ordered by severity:

1. **Scope/documentation contradiction: other-year supplements were processed.**  
   The run says it does not process any year other than `2020-21`, but the selected PDFs include `Supplement_2017_18.pdf`, `Supplement_2018_19.pdf`, `Supplement_2019_20.pdf`, and `Supplement_2021_22.pdf`. They are direct files in the `2020-21` source folder, so this may be intentional by folder-scope, but it violates or at least contradicts the explicit “does not process other years” criterion. Downstream users could accidentally treat cross-year supplement material as 2020-21 commentary source.

2. **Run folder is missing `adv_review_results.md`.**  
   The base Step 02 guide lists `adv_review_results.md` as part of the required run layout. I did not create it because the instruction was read-only.

**Checks Passed**

- Manifest identifies 29 selected PDFs with path, size, page count, mtime, and SHA256.
- Current raw PDFs match manifest size, mtime, SHA256, and page count: **0 mismatches**.
- Direct selected source PDFs: **29**.
- Converted Markdown files: **29**.
- Conversion log entries: **29**, failures: **0**.
- Every selected PDF has exactly one Markdown output.
- Output Markdown size/hash values match manifest: **0 mismatches**.
- Page markers are present and sequential; marker counts match PDF page counts: **0 mismatches**.
- `qa_results.json`, `qa_report.md`, and `conversion_quality.md` explicitly mark numeric/table/chart/ranking/total/footnote fidelity as **NOT_CERTIFIED** and require PDF verification.
- `how_to_reproduce.md` points to `agentic/02_pdf_to_md/README.md` as canonical and does not redefine Step 02.
- No evidence of section splitting, claim extraction, JSON normalization, export, or downstream processing in the retained scripts.

**Prose Fidelity Sample**

I independently sampled PDF text against Markdown pages outside the run’s own QA sample set. All sampled overlaps were `1.0`, including `Overview.pdf` p3, `Growth.pdf` p10, `Fiscal.pdf` p11, `Pes_2020_21.pdf` p350, `Statistical_Supplement.pdf` p152, and others.

**Residual Risks**

- Prose fidelity was checked against PDF-extracted text, not rendered-page OCR/manual visual proofreading.
- Tables, charts, images, footnotes, rankings, totals, and numeric claims remain uncertified.
- Some extracted prose carries PDF text-layer artifacts such as private-use bullets; suitable for working text, not polished quotation without PDF review.

**Acceptability**

Acceptable for LUMS Data Lab commentary work **only with a scope caveat**: downstream use should explicitly exclude or separately label the cross-year supplement PDFs. For strict 2020-21-only acceptance, this run should be treated as **not acceptable until the scope contradiction is resolved**.

## Follow-Up Applied After Review

After receiving the read-only review, this run's `conversion_quality.md` and
`how_to_reproduce.md` were updated to make the cross-year supplement caveat
explicit. The converted scope was not changed: the run still contains all 29
direct PDFs from the `2020-21` source folder.
