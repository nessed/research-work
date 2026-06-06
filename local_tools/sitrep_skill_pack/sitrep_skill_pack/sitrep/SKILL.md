---
name: sitrep
description: Produce a concise, evidence-backed project sitrep (situation report) for the datalab_ali repo. Works as a running project-memory system: it compares current evidence against the latest previous sitrep in agentic/sitreps/. Checks git status (optional), recently modified files, agentic/ task folders, reviews, and prior sitreps. Reports completed work, what changed since last time, current state, blockers, and the next 3 actions, plus a WhatsApp-ready update for Ali Hasanain / team, and saves the full report to agentic/sitreps/.
---

# /sitrep — Project Situation Report (running project memory)

Produce a short, **evidence-backed** status report for this repo, and compare it against
the most recent previous sitrep so the reports form a running project memory. Every claim
must trace to something on disk (a file, a git fact, a review result). Never fabricate
progress.

## Hard rules
- **Do not modify raw PDFs or raw data.** Never touch `datalab_master/Master Data/` or any `*_PDF/` source folders or `*.pdf` files.
- **Do not fabricate progress.** Only report what the evidence shows. If unclear, say `unclear from evidence`.
- **Do not claim something is "validated", "verified", "passed", or "QA'd"** unless an actual review/check file exists and says so (e.g. an `adv_review_results.md` or `conversion_quality.md` with a clear verdict). If no such file exists, say **"not yet reviewed."**
- **Do not claim commit status if Git is unavailable.**
- **Keep it short.** Bullets over paragraphs. Cite the file/path that backs each point.
- This skill is **read-only** except for writing the single sitrep file under `agentic/sitreps/`.

## Steps

### 1. Gather evidence

**1a. Git status (optional — Git is helpful but not required).**
- First try `git status --short`.
- If Git is unavailable or the folder is not a git repo (command errors / "not a git repository"), **do not fail.** Record this line and switch to filesystem-only mode:
  `Git status unavailable: folder is not a git repo or git is not installed.`
- If Git works, also run `git log --oneline -10` and `git diff --stat HEAD~3..HEAD` (skip the diff if fewer than 3 commits).
- Track which mode you are in; you must report it in **Evidence checked** as either `Git status used` or `Filesystem-only mode used; Git unavailable`.

**1b. Recently modified files** (last ~7 days, excluding raw source and .git).
- List the 15 most recently modified files under the repo, excluding `.git/`, `datalab_master/`, `*.pdf`, and `*_PDF/` folders.
- On Windows PowerShell:
  `Get-ChildItem -Recurse -File -Path agentic,*.md | Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-7) -and $_.FullName -notmatch '\\.git\\|datalab_master|_PDF\\|\.pdf$' } | Sort-Object LastWriteTime -Descending | Select-Object -First 15 LastWriteTime,FullName`

**1c. Project context**: read `PROJECT_CONTEXT.md` — specifically the `LIVE_CONTEXT_OVERWRITE_ON_MAJOR_TASK` section for the declared current state.

**1d. agentic/ task folders**: list the subfolders of `agentic/` and, for each, note which standard files exist:
- `how_to_reproduce.md`
- `adv_review_prompt.md`
- `adv_review_results.md`
- `conversion_quality.md` (if present)
- the main output file, if visible (e.g. `pes_folder_tree.json`, a `converted_md/` folder, etc.)

**1e. Reviews**: gather review/check evidence from BOTH places:
- any files under `agentic/reviews/`
- any `adv_review_results.md` and `conversion_quality.md` inside task folders (this repo's actual convention).
Read the **actual verdicts**. A task is only "reviewed/validated" if one of these files states a clear result.

**1f. Prior sitreps (for the "Changed since last sitrep" diff)**:
- List `agentic/sitreps/` and find the **newest previous** `sitrep_*.md` by filename timestamp.
- **Do not compare the new sitrep to itself** — ignore the file you are about to write; only consider sitreps that already exist on disk before this run.
- Read that newest previous sitrep in full; you will diff it against current evidence in step 3.

### 2. Assess
For each active task folder, classify its honest state using only the evidence:
- **Done & reviewed** — output exists AND a review/check file gives a clear positive verdict.
- **Done, not reviewed** — output exists but no review file (or review is inconclusive).
- **In progress** — partial output / recent edits, no completion.
- **Not started / blocked** — note the blocker if visible.

### 3. Build the "Changed since last sitrep" section
- Look inside `agentic/sitreps/` and use the newest previous sitrep found in step 1f.
- **If no previous sitrep exists**, write exactly:
  `No prior sitrep found; this is the baseline.`
- **If a previous sitrep exists**, compare current evidence against it and list only real, evidence-backed changes:
  - new completed outputs
  - new review verdicts
  - blockers resolved
  - blockers newly added
  - current focus changed
  - next actions changed
- Keep it short and evidence-based. **Do not guess.** If a change cannot be confirmed from a file/commit/review, write `unclear from evidence` rather than inventing one.

### 4. Output to the user
Print this **exact** structure:

```
# SITREP — <YYYY-MM-DD HH:MM>

## Completed (evidence-backed)
- <item> — <file/path or commit>

## Changed since last sitrep
- <short evidence-backed changes, or baseline line>

## Current state
- <2-5 bullets on where things stand>

## Reviewed / validated
- <only items with a real review file + verdict; else: "None validated yet">

## Blockers
- <blocker> — <why / evidence>
OR
- None visible

## Next 3 actions
1. <action>
2. <action>
3. <action>

## WhatsApp update (for Ali Hasanain / team)
<3-6 short lines, plain language, no jargon, copy-paste ready. State what's done,
what's changed, what's in progress, and what's next. Do NOT claim validation unless a
review file backs it.>

## Evidence checked
- <commands/files checked>
- <state whether Git was used or filesystem-only mode was used>
```

In **Evidence checked**, the Git line must read exactly one of:
- `Git status used`
- `Filesystem-only mode used; Git unavailable`

### 5. Save the full sitrep
- Compute the timestamp from the current **local** date/time as `YYYYMMDD_HHMM`.
- Write the **full** report (everything from step 4) to:
  `agentic/sitreps/sitrep_YYYYMMDD_HHMM.md`
- The **last line printed to the user** must confirm the saved path.

## Style
- Evidence first: if you can't point to a file, commit, or review verdict, don't assert it.
- When unsure, say `unclear from evidence` rather than guessing.
- Short. The WhatsApp block must read like a human teammate wrote it.
