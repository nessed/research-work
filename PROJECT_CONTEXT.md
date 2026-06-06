# PROJECT_CONTEXT

## FIXED_CONTEXT_DO_NOT_EDIT
This section is stable. Future agents must not change it unless Ali explicitly asks.

- This is Ali's LUMS RA work under Ali Hasanain.
- Project focus: Pakistan economic data, Pakistan Economic Surveys, budget docs, official sources, commentary, reproducible AI-assisted research.
- Raw source truth lives under: `datalab_master/Master Data/`
- Derived work lives under: `agentic/`
- Raw source files must stay untouched unless Ali explicitly says otherwise.
- Reproducibility is mandatory.
- Every important output must be traceable, reviewable, and reproducible from source materials.
- Sir's current assignment for Ali is task #2: absorb and track what Pakistan Economic Survey commentary said at what time.
- This is separate from task #1, which is numeric/time-series ingestion into the database.
- PDFs are raw source, but too heavy and messy for repeated LLM use.
- Markdown/text is the working format for LLM commentary work.
- Commentary will be used through summaries and structured extractions, with awareness that summaries cause signal loss.
- Later commentary extraction should focus on cause-effect claims, policy actions, constraints, outlooks, risks, sector narratives, optimism/pessimism signals, and recurring narratives.
- Any extracted claim must stay source-grounded with page references and source quotes.
- Tables, numeric values, and chart-derived values are weak unless separately verified.
- Important outputs should be reviewed by a fresh-context adversarial agent when approved.
- Never create publishable figures, claims, or conclusions from AI alone.

## STANDARD_AGENTIC_TASK_FILES
This section defines the standard files for major AI-assisted subtasks under `agentic/`.

Every major task folder under `agentic/` should contain:

- `how_to_reproduce.md`
  Recipe for how the output was created and how another agent or person can reproduce and verify it.

- `adv_review_prompt.md`
  Prompt or instructions for a fresh-context adversarial reviewer agent.

- `adv_review_results.md`
  The reviewer agent's findings and results.

- One clear task-specific output file or folder.
  Examples:
  - `pes_folder_tree.json`
  - `converted_md/`
  - `sample_claims.json`
  - `schema.json`

Optional files only when needed:

- `script.py` or a clearly named script file if code was used.
- `conversion_quality.md` if the task is a conversion or QA task.
- `notes.md` only for brief human decisions, not long chat history.

Naming rules:

- Do not use vague names like `manifest.md` or `review_report.md` going forward.
- Use self-explanatory names.
- Do not create these files for tiny one-off actions.
- Create them for major task milestones only.
- Future agents should follow this naming standard unless Ali explicitly changes it.

## LIVE_CONTEXT_OVERWRITE_ON_MAJOR_TASK
This section is changeable. Overwrite it only after major task milestones, not after every minor action.

Current live state:

- Active area: `agentic/02_pdf_to_md/runs/2015-16_pymupdf4llm_hardened/`
- Current major task: maintain a hardened, reproducible 2015-16 PES Markdown working corpus for commentary extraction pilots.
- Completed baseline: `agentic/01_pes_folder_map/`
- Folder map output: `pes_folder_tree.json`
- Folder map result: PASS / High confidence; 10 year folders, 287 PDFs, no filesystem count/path/size mismatches.
- Current PDF-to-MD run: hardened PyMuPDF4LLM 2015-16 run with retained conversion/QA scripts, manifest/log evidence, and PASS headless QA for structure and deterministic prose fidelity.
- Current schema work: `agentic/03_commentary_schema_discovery/` has a frozen working schema v0.1 plus stress tests and extraction pilot outputs.
- Raw PDFs were not modified.
- No final commentary extraction, mass processing, family mapping, or database import has started.

Update policy: overwrite this LIVE section only after a major task milestone. Keep only current status, key outputs, blockers, and next immediate task. Move old detail into the relevant task folder, not this file.

## PERMANENT_CONSTRAINTS

- Do not modify `Master Data` unless Ali explicitly says so.
- Do not start mass processing unless Ali explicitly asks.
- Do not start family mapping unless assigned.
- Do not start database imports unless assigned.
- Do not treat converted Markdown as source truth; original PDFs remain source truth.
- Do not trust table values from Markdown without separate table QA.
- Keep derived work under `agentic/`.
- Keep context concise and token-efficient.

Reference renames already applied:

- `corpus_inventory` -> `01_pes_folder_map`
- `pes_inventory.json` -> `pes_folder_tree.json`
- `manifest.md` -> `how_to_reproduce.md`
- `review_prompt.md` -> `adv_review_prompt.md`
- `review_report.md` -> `adv_review_results.md`
- `pdf_conversion_pilot` -> `02_pdf_to_md`
