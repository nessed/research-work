---
name: sitrep
description: Produce a concise, evidence-backed project sitrep (situation report) for the datalab_ali repo. Checks git status, recently modified files, agentic/ task folders, reviews, and prior sitreps. Reports completed work, current state, blockers, and the next 3 actions, plus a WhatsApp-ready update for Ali Hasanain / team, and saves the full report to agentic/sitreps/.
---

# /sitrep — Project Situation Report

Produce a short, **evidence-backed** status report for this repo. Every claim must trace to
something on disk (a file, a git fact, a review result). Never fabricate progress.

## Hard rules
- **Do not modify raw PDFs or raw data.** Never touch `datalab_master/Master Data/` or any `*_PDF/` source folders or `*.pdf` files.
- **Do not fabricate progress.** Only report what the evidence shows.
- **Do not claim something is "validated", "verified", "passed", or "QA'd"** unless an actual review/check file exists and says so (e.g. an `adv_review_results.md` or `conversion_quality.md` with a clear verdict). If no such file exists, say **"not yet reviewed."**
- **Keep it short.** Bullets over paragraphs. Cite the file/path that backs each point.
- This skill is **read-only** except for writing the single sitrep file under `agentic/sitreps/`.

## Steps

### 1. Gather evidence (read-only)
Run these and read the results. Do not act on them, just collect facts.

- **Git status & recent commits**
  - `git status --short`
  - `git log --oneline -10`
  - `git diff --stat HEAD~3..HEAD` (skip if fewer than 3 commits)
- **Recently modified files** (last ~7 days, excluding raw source and .git)
  - List the 15 most recently modified files under the repo, excluding `.git/`, `datalab_master/`, `*.pdf`, and `*_PDF/` folders.
  - On Windows PowerShell:
    `Get-ChildItem -Recurse -File -Path agentic,*.md | Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-7) -and $_.FullName -notmatch '\\.git\\|datalab_master|_PDF\\|\.pdf$' } | Sort-Object LastWriteTime -Descending | Select-Object -First 15 LastWriteTime,FullName`
- **Project context**: read `PROJECT_CONTEXT.md` — specifically the `LIVE_CONTEXT_OVERWRITE_ON_MAJOR_TASK` section for the declared current state.
- **agentic/ task folders**: list the subfolders of `agentic/` and, for each, note which standard files exist (`how_to_reproduce.md`, `adv_review_prompt.md`, `adv_review_results.md`, the main output file).
- **Reviews**: gather review/check evidence from BOTH places:
  - any files under `agentic/reviews/`
  - any `adv_review_results.md` and `conversion_quality.md` inside task folders (this repo's actual convention).
  Read the verdicts. A task is only "reviewed/validated" if one of these files states a clear result.
- **Prior sitreps**: list `agentic/sitreps/` and read the most recent one (if any) to report what changed since then.

### 2. Assess
For each active task folder, decide its honest state using only the evidence:
- **Done & reviewed** — output exists AND a review/check file gives a clear positive verdict.
- **Done, not reviewed** — output exists but no review file (or review is inconclusive).
- **In progress** — partial output / recent edits, no completion.
- **Not started / blocked** — note the blocker if visible.

### 3. Output to the user
Print this exact structure, kept tight:

```
# SITREP — <YYYY-MM-DD HH:MM>

## Completed (evidence-backed)
- <item> — <file/path or commit>

## Current state
- <2-5 bullets on where things stand; cite PROJECT_CONTEXT LIVE section + files>

## Reviewed / validated
- <only items with a real review file + verdict; else: "None validated yet">

## Blockers
- <blocker> — <why / evidence>   (or "None visible")

## Next 3 actions
1. <action>
2. <action>
3. <action>

## WhatsApp update (for Ali Hasanain / team)
<3-6 short lines, plain language, no jargon, copy-paste ready. State what's done,
what's in progress, and what's next. Do NOT claim validation unless a review file backs it.>
```

### 4. Save the full sitrep
- Compute the timestamp from the current date/time as `YYYYMMDD_HHMM`.
- Write the **full** report (everything from step 3) to:
  `agentic/sitreps/sitrep_YYYYMMDD_HHMM.md`
- Confirm the saved path to the user on the last line.

## Style
- Evidence first: if you can't point to a file, commit, or review verdict, don't assert it.
- When unsure, say "unclear from evidence" rather than guessing.
- Short. The WhatsApp block must read like a human teammate wrote it.
