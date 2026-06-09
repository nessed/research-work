# input/ — where your Step 03 sections go

Drop a **reviewed (PASS) Step 03** `sections.jsonl` here, one folder per year:

```
input/
  2018-19/
    sections.jsonl
  2016-17/
    sections.jsonl
```

You can copy either:
- just the `sections.jsonl` file into `input/<year>/sections.jsonl`, **or**
- the whole Step 03 run folder and point `--sections` at the folder (the builder
  finds `sections.jsonl` inside it).

The operator prompt (`../PROMPT.md`) lists `input/*` to show which years are
available, then asks you to confirm the target before building jobs.

Nothing here is modified by the pipeline — it is read-only input.
