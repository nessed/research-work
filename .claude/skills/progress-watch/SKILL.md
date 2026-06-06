---
name: progress-watch
description: Hourly auto-refreshing progress tracker for datalab_ali. Extends sitrep logic with a tighter 2-hour change window, overwrites a single CURRENT_PROGRESS.md at the repo root so it is always fresh, and saves a timestamped copy to agentic/sitreps/ for history. Designed to run unattended via /schedule, or manually on demand.
---

# /progress-watch — Hourly Progress Tracker (auto-refreshing)

Produce a short, **evidence-backed** progress snapshot for this repo and overwrite
`CURRENT_PROGRESS.md` so it is always the latest view. Every claim must trace to
something on disk (a file, a git fact, a review result). Never fabricate progress.

This skill extends `/sitrep` with two differences:
1. "Recently changed" uses a **2-hour window** (not 7 days) for precision.
2. The report overwrites `CURRENT_PROGRESS.md` at the repo root **and** saves a
   timestamped copy under `agentic/sitreps/`.

## Hard rules
- **Do not modify raw PDFs or raw data.** Never touch `datalab_master/Master Data/` or any `*_PDF/` source folders or `*.pdf` files.
- **Do not fabricate progress.** Only report what the evidence shows. If unclear, say `unclear from evidence`.
- **Do not claim something is "validated", "verified", "passed", or "QA'd"** unless an actual review/check file exists and says so (e.g. an `adv_review_results.md` or `conversion_quality.md` with a clear verdict). If no such file exists, say **"not yet reviewed."**
- **Do not claim commit status if Git is unavailable.**
- **Keep it short.** Bullets over paragraphs. Cite the file/path that backs each point.
- **Always overwrite `CURRENT_PROGRESS.md`** — even if nothing changed, so the timestamp stays current.
- **Exclude `CURRENT_PROGRESS.md`** from the recent-changes scan (it is rewritten each run and would always appear).
- **Do not read full converted markdown files or large PDF-derived outputs** — use only file counts, filenames, and log/review summaries to save tokens.
- This skill is **read-only** except for writing: (a) `CURRENT_PROGRESS.md` (overwrite) and (b) the timestamped sitrep under `agentic/sitreps/`.

## Steps

### 1. Gather evidence

**1a. Git status (optional — Git is helpful but not required).**
- First try `git status --short`.
- If Git is unavailable or the folder is not a git repo (command errors / "not a git repository"), **do not fail.** Record this line and switch to filesystem-only mode:
  `Git status unavailable: folder is not a git repo or git is not installed.`
- If Git works, also run `git log --oneline -10` and `git diff --stat HEAD~3..HEAD` (skip the diff if fewer than 3 commits).
- Track which mode you are in; you must report it in **Evidence checked** as either `Git status used` or `Filesystem-only mode used; Git unavailable`.

**1b. Recently changed files — 2-hour window (primary delta signal).**
- List files modified in the **last 2 hours**, excluding `.git/`, `datalab_master/`, `*.pdf`, `*_PDF/` folders, and `CURRENT_PROGRESS.md` itself.
- On Windows PowerShell:
  `Get-ChildItem -Recurse -File -Path "C:\Users\Ali\Desktop\datalab_ali" | Where-Object { $_.LastWriteTime -gt (Get-Date).AddHours(-2) -and $_.FullName -notmatch '\.git\\|datalab_master|_PDF\\|\.pdf$|CURRENT_PROGRESS\.md' } | Sort-Object LastWriteTime -Descending | Select-Object -First 20 LastWriteTime,FullName`
- Report filenames and timestamps only — do not read the file contents.
- If no files changed in 2 hours, record: `No files modified in the last 2 hours.`

**1c. Project context**: read `PROJECT_CONTEXT.md` — specifically the `LIVE_CONTEXT_OVERWRITE_ON_MAJOR_TASK` section for the declared current state. If this section is absent, note it. Do not read the full file if it is large; the LIVE_CONTEXT section is enough.

**1d. agentic/ task folders**: list the subfolders of `agentic/` and, for each, note which standard files exist (names only, no content):
- `how_to_reproduce.md`
- `adv_review_prompt.md`
- `adv_review_results.md`
- `conversion_quality.md` (if present)
- the main output file or folder (name/count only)

**1e. Reviews**: gather review/check evidence from BOTH places:
- any files under `agentic/reviews/`
- any `adv_review_results.md` and `conversion_quality.md` inside task folders
Read the **actual verdicts** in these files (they are short). A task is only "reviewed/validated" if one of these files states a clear result.

**1f. Prior report (diff baseline):**
- Check whether `CURRENT_PROGRESS.md` exists at the repo root. If it does, read its `Last updated:` line and the section headers to use as a diff baseline — do **not** re-read the full body.
- Also list `agentic/sitreps/` filenames and find the newest `sitrep_*.md` by filename timestamp.
- Use `CURRENT_PROGRESS.md` as the primary diff baseline if it exists; otherwise use the newest sitrep as fallback.
- If neither exists, write: `No prior report found; this is the baseline.`

### 2. Assess
For each active task folder, classify its honest state using only the evidence:
- **Done & reviewed** — output exists AND a review/check file gives a clear positive verdict.
- **Done, not reviewed** — output exists but no review file (or review is inconclusive).
- **In progress** — partial output / recent edits, no completion signal.
- **Not started / blocked** — note the blocker if visible.

### 3. Build the "Changed since last report" section
- Compare current evidence against the baseline from step 1f.
- **If no prior report exists**, write: `No prior report found; this is the baseline.`
- **If a prior report exists**, list only real, evidence-backed changes:
  - files newly modified in the last 2 hours
  - new completed outputs
  - new review verdicts
  - blockers resolved or newly added
  - current focus changed
  - next actions changed
- Keep it short. **Do not guess.** Write `unclear from evidence` rather than inventing.

### 4. Compose the report
Compose the full report with this **exact** structure:

```
# PROGRESS WATCH — <YYYY-MM-DD HH:MM> (auto-refreshed hourly)
> Last updated: <YYYY-MM-DD HH:MM local time>. Overwritten each run — see agentic/sitreps/ for history.

## Completed (evidence-backed)
- <item> — <file/path or commit>

## Changed since last report
- <short evidence-backed changes, or baseline line>

## Active in last 2 hours
- <files modified in last 2 hours with timestamps; or "No files modified in the last 2 hours.">

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
- 2-hour window used for recent-changes scan
```

In **Evidence checked**, the Git line must read exactly one of:
- `Git status used`
- `Filesystem-only mode used; Git unavailable`

### 5. Write the outputs (in this order)

**5a. Overwrite `CURRENT_PROGRESS.md`.**
- Write the full report from step 4 to:
  `C:\Users\Ali\Desktop\datalab_ali\CURRENT_PROGRESS.md`
- Always overwrite. Do not append.
- If the write fails (file is locked), print:
  `WARNING: Could not write CURRENT_PROGRESS.md — file may be open in another program. Timestamped sitrep saved instead.`
  Then continue to step 5b regardless.

**5b. Save a timestamped copy to history.**
- Compute the timestamp from the current **local** date/time as `YYYYMMDD_HHMM`.
- Ensure `agentic/sitreps/` exists (create it if missing).
- Write the **same** full report to:
  `agentic/sitreps/sitrep_YYYYMMDD_HHMM.md`

**5c. Confirm both writes.**
The **last lines printed to the user** must be:
```
CURRENT_PROGRESS.md overwritten: C:\Users\Ali\Desktop\datalab_ali\CURRENT_PROGRESS.md
Timestamped copy saved: agentic/sitreps/sitrep_YYYYMMDD_HHMM.md
```

## Style
- Evidence first: if you can't point to a file, commit, or review verdict, don't assert it.
- When unsure, say `unclear from evidence` rather than guessing.
- Short. The WhatsApp block must read like a human teammate wrote it.
- Do not read full converted markdown files or PDF-derived outputs; use filenames and counts only.
