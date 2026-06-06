# CLAUDE.md — rules for working in `datalab_master`

Guidance for any AI assistant (Claude Code, Codex, Antigravity) working in this folder. `AGENTS.md` is a mirror of this file — edit this one, then copy. These rules are the LUMS Economics Data Lab's working doctrine. **Read them before doing anything here.**

## What this folder is

The Data Lab's **gold-source corpus + the structured database we build from it.** `Master Data/` holds Pakistan's Economic Surveys (2015‑16 → 2024‑25) and Federal Budget documents (2015‑16 → 2025‑26), each year-folder with a `manifest.csv` (`label, file_name, url`) recording where every file came from. Our job is to turn these documents into a **definitive, reproducible, vintage‑aware time series for every statistic** — and to track what the commentary said, and when.

## The golden rule (non-negotiable)

> **Never fabricate a number.** Every data point we publish traces to a raw file from a primary source — with its URL and the page it was printed on. No estimates, no interpolation, no extrapolation. If data is missing, we say "not reported," we do not fill it in.

**Why this is existential:** if we publish even one figure that is substantially off, the Lab's and LUMS's reputation is shot. That is the standard. (See the retraction case at the end.)

## Gold sources only

Primary, citable sources only: **PBS, SBP, Ministry of Finance (budget, Economic Survey, Debt Office), FBR, NEPRA, OGRA, Census**, and for comparators/cross-checks **IMF, World Bank, ADB, UN**. Newspapers, think-tank reposts, Twitter, and aggregators are **never** a primary source for a number. (News/commentary tracking is a *separate* workstream and a separate store — it informs prose, never supplies a figure.)

## Reproducibility is king

Everything we do must be reproducible — meaning we can hand the **recipe** to someone else and they reproduce and verify it.
- **Record every download:** the source URL and the date, in the `manifest.csv`. Save the file in its **original form**.
- **Raw is read-only.** The PDFs and manifests in the year-folders are not edited by anyone except Ali and Arsalan. All manipulation happens with **recorded code on copies**, written to a separate `parsed/` zone — never by editing the raw.
- **Tell your AI tools to ensure reproducibility** and they will: record the script, the exact source file, and the page for every number. See `SCHEMA.md` for the required fields.

## We never ask AI to build a graph "from scratch"

The workflow is fixed:
1. **Download gold-standard data** from the official source (with its URL).
2. **Make the AI build the figure** *from that data* — never invent the data to fit a figure.
3. **Hand the output to a fresh-context, different model for adversarial review and reproduction** — Claude → Codex → Agy → Claude. A second model with no stake re-derives the result and tries to break it before we trust it.

A beautiful chart built on hallucinated numbers is the failure mode we are organized to prevent.

## Definitions before counting

Lock the definition of any headline metric **before** computing on it. The classic traps: **GNI vs GDP** (Pakistan "per capita income" = GNI/pop, *not* GDP/pop), nominal vs real, factor cost vs market price, fiscal vs calendar year, base-year changes. Before publishing a figure, pass it to a model to check how well it matches the same series as reported in **other** sources.

## Vintages: keep every version

Pakistan revises its data, and each Economic Survey re-publishes prior years (the embedded statistical supplements). The same statistic from a different survey is a **different vintage** — we keep all of them, never overwrite. The reporting document is part of a datapoint's identity. This is both a discipline and a research asset. Full rules in **`SCHEMA.md`**.

## Summaries lose signal — note it

When we summarize a document, we lose subtleties by definition. That is acceptable — we can't hold everything at once — but it is something to **know and flag**. Keep different cuts: a data extraction is not a narrative summary is not a cause-effect claim list. Track *what kind* of commentary we produced and when.

## Before anything is published — the mini-gate

Run these on any quantitative claim that leaves the Lab: (1) **definition lock**, (2) **floor/ceiling** sanity (can this number even be true?), (3) **cross-source triangulation** (does an independent source agree?), (4) **tone** matches certainty. If any fails, it is not finished.

## How we work

- **Plan mode first.** For any non-trivial task, enter plan mode and think the approach through before acting. Flag key moments of your plan to Ali.
- **Prefer `.md` over PDF for AI context.** PDFs are heavy on the model's limited context; extract to markdown/tables and work from those.
- **Folder hygiene.** One shared `Master Data/` (read-only raw) + one working folder per person. Don't write into someone else's folder or into raw.
- **CLI over IDE.** We work in Claude Code / Codex CLI.

## The retraction that taught us this (keep it in mind)

We once published a GDP‑per‑capita "mistake" — both Claude and Codex agreed a government figure was wrong — and a friend pointed out the series was **GNI** per capita, not GDP. We had to retract. Lesson: **pay attention to definitions and data-series construction; reproducibility + adversarial cross-checking + definition locks are what stop this.** Reproducibility is king, and AI workflows need strong guardrails.

---
*Companion: `SCHEMA.md` (the data contract). Upstream conventions: the `Pakistan/` research repo's source-priority and naming rules.*
