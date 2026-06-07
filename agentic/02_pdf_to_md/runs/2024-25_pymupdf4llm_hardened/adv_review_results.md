# Adversarial Review Results

## Review Method

- Claude was called first with `claude -p`, but the local PowerShell shim was
  blocked by execution policy: `claude.ps1 cannot be loaded because running
  scripts is disabled on this system`.
- Codex fallback was attempted with `codex.cmd exec` in read-only mode. It
  launched, but API websocket/network access was blocked by local permissions.
- Escalated external-network review was rejected because it would send local
  workspace contents outside the approved environment.
- A fresh-context local read-only sub-agent reviewer was used as the safer
  fallback. The reviewer was instructed not to edit files and to verify only the
  `2024-25` Step 02 run.

## Findings

1. **FAIL: required review artifact is missing.** The base guide requires
   `adv_review_results.md` in each run folder. The run folder contains
   `adv_review_prompt.md` but no `adv_review_results.md`. This makes the run
   incomplete as a finalized Step 02 package.

2. **WARN: NOT_CERTIFIED warnings are run-level, not embedded in each Markdown
   output.** The warnings are explicit in `qa_report.md` and
   `how_to_reproduce.md`. The reviewer found no `NOT_CERTIFIED` / `not
   certified` strings inside `converted_md/*.md`. This is acceptable if
   downstream users always keep the QA docs with the Markdown, but risky if
   individual `.md` files are used alone.

## PASS/FAIL Summary

- Structural and fidelity checks: **PASS**
- Run-package compliance at review time: **FAIL** due to missing
  `adv_review_results.md`
- Acceptable for LUMS Data Lab commentary work: **conditionally yes for
  page-cited prose/commentary only**, but the run package was not complete until
  this review-results artifact was saved.

## Concrete Evidence Checked

- Live counts reconcile: `28` direct source PDFs, `28` Markdown outputs, `28`
  manifest entries, `28` conversion-log entries.
- Source non-PDFs excluded as documented: `manifest.csv`,
  `Statistical_Supplement.zip`.
- Every direct source PDF has exactly one same-stem Markdown output; no missing
  or extra outputs.
- Independently recomputed source sizes, source SHA256s, output sizes, output
  SHA256s, PDF page counts, and Markdown page-marker counts: no mismatches.
- Page markers are sequential and match PDF page counts for all `28` outputs.
- Conversion log records `28` successes, `0` failures, with
  `reused_existing_output: true`.
- Spot hashes checked include:
  - `Agriculture.pdf`: `4,624,958` bytes, `39` pages, SHA256
    `2cd7386a1d374d6a9295401eddf64dd7bbdb8cd1d32b340245c4f4893630ab09`;
    output SHA256
    `302f3a2d95e4267c4c93576e5549fc83b0205ee74c1a621a65116f36ecef423d`.
  - `Transport_And_Communication.pdf`: `1,331,186` bytes, `26` pages, SHA256
    `781d921b300decbc1c0040d75eeb490241284d22caa527884897c156e92c2efa`;
    output SHA256
    `eb1171b72a700af70e95911a8705ba7fbd089bd9df6905fae1f624626329e459`.
- Prose fidelity spot checks against PDFs:
  - `Growth_And_Investment.pdf` page `11`: token overlap `1.0`.
  - `Trade_And_Payments.pdf` page `6`: token overlap `1.0`.
  - `Overview_2024_25.pdf` page `16`: token overlap `0.9737`.
  - `Annex_Ii_Tax_Expenditure.pdf` page `1` has only `4` extractable tokens;
    QA skip rationale is reasonable.
- Raw PDF protection: live source hashes match manifest; reproduction docs
  state originals were not modified. The reviewer found no PDFs copied into the
  run folder.
- Reproducibility instructions are present, including conversion,
  `--reuse-existing`, QA command, environment references, and result summary.

## Residual Risks

Numeric/table/chart/ranking/footnote content remains **NOT_CERTIFIED**. QA
reports `1212` omitted picture placeholders. Any numeric or table-derived claim
still needs direct PDF verification and preferably rendered page evidence.

The run folder was untracked in git at review time:
`?? agentic/02_pdf_to_md/runs/2024-25_pymupdf4llm_hardened/`, so
reproducibility evidence was not yet version-controlled in the local repo state
the reviewer saw.

## Final Disposition

After saving this file, the missing required review artifact has been supplied.
The substantive review result is PASS for Step 02 working-text use, with the
explicit limitation that Markdown numeric/table/chart/ranking/footnote content
is not certified and raw PDFs remain source truth.
