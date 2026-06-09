# Operator Prompt — Step 04 Claims JSON (portable)

Paste everything below into Claude Code (or Opus) running in this `portable_step04/`
folder on the machine logged into the Claude Max account.

---

You are running **Step 04 (Claims JSON extraction)** of the Pakistan Economic
Survey commentary pipeline, from this self-contained portable package. Your job is
to turn an already-completed, reviewed **Step 03 `sections.jsonl`** into a final
`claims.jsonl` for one year, then validate it. Nothing more.

**Hard rules — do not break these:**
- Do **NOT** normalize (that is Step 05) and do **NOT** export to any table/database (Step 06).
- Do **NOT** read, move, rename, or modify any raw PDFs. You work only from `sections.jsonl`.
- Do **NOT** invent claims, sections, pages, or quotes. Every claim must be grounded in the provided section text.
- Do **NOT** run a full year until the tiny smoke test in `sample/README.md` passes on this machine.
- Use the Claude Code subscription via normal **non-bare** `claude -p`. Do **NOT** use `--bare`. No Anthropic API key is required.

**Do this, in order:**

1. **Show available inputs.** List the folders under `input/`. Each subfolder is a
   year that has a `sections.jsonl` ready (e.g. `input/2018-19/sections.jsonl`).
   If `input/` is empty, tell me to drop a reviewed Step 03 `sections.jsonl` into
   `input/<year>/` (see `input/README.md`) and stop.

2. **Ask me which year to run** and **confirm the exact target file** you will use
   (the resolved path to that year's `sections.jsonl`). Wait for my confirmation.

3. **Ask me which source files to exclude, if any** (statistical supplements,
   annex/indicator tables, and duplicate full-survey Markdown have no narrative
   claims and are normally excluded). Each exclusion needs a short reason; you will
   pass them as `--exclude "FILENAME=REASON"`. If I say "none", include everything.

4. **Follow `REPRODUCE.md` exactly** to: check Python and Claude auth, build jobs,
   run extraction (`--engine claude --chunk 3 --concurrency 1`), finalize, and
   validate. Run the tiny smoke from `sample/README.md` **first**.

5. **Report** the run folder path, job counts, claim count, validator result
   (PASS/FAIL), and any files in `_supporting/failed_jobs/`. Then stop. Do not
   continue to Step 05/06.

Point of truth for every command is `REPRODUCE.md` in this folder.
