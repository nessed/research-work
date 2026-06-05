# /sitrep Skill Pack

A shareable Claude Code skill that produces a concise, **evidence-backed** project
situation report (sitrep): git status, recently modified files, `agentic/` task folders,
reviews, completed work, current state, blockers, the next 3 actions, and a
WhatsApp-ready update for the team. The full report is saved to `agentic/sitreps/`.

The skill is **read-only** except for writing one sitrep file. It never modifies raw
PDFs or raw data, and it never claims work is "validated" unless a real review/check
file says so.

## Install

First, **unzip this pack inside your project folder**, so you have:

```
<your project>/
  sitrep_skill_pack/
    README.md
    install_sitrep_skill.ps1
    sitrep/SKILL.md
```

Then run the installer **either way** — both install into your project root:

### Option A — from project root
```powershell
.\sitrep_skill_pack\install_sitrep_skill.ps1
```

### Option B — from inside the pack
```powershell
cd sitrep_skill_pack
.\install_sitrep_skill.ps1
```

The installer creates `.claude/skills/sitrep/`, copies the skill in, and creates
`agentic/sitreps/` and `agentic/reviews/` in your project root. It's safe to re-run.

## Use

Open Claude Code **from the project root**, then run:

```
/sitrep
```

For a recurring loop run (e.g. every 12 hours):

```
/loop 12h /sitrep
```

## What's in this pack

- `sitrep/SKILL.md` — the skill definition (copied into `.claude/skills/sitrep/` by the installer).
- `install_sitrep_skill.ps1` — the installer script.
- `README.md` — this file.

## Note

The bundled `SKILL.md` is project-specific: it references this project's `agentic/`
layout, the `adv_review_results.md` / `conversion_quality.md` review files, and a
WhatsApp update addressed to "Ali Hasanain / team". To reuse it elsewhere, edit
`.claude/skills/sitrep/SKILL.md` after install to match your paths and team names.
