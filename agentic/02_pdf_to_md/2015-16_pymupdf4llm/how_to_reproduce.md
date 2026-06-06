# How To Reproduce

This folder contains a one-off direct PyMuPDF4LLM conversion run for the
Pakistan Economic Survey `2015-16` PDFs.

## Scope

- Input folder:
  `C:\Users\Ali\Desktop\datalab_ali\datalab_master\Master Data\pakistan_economic_survey\2015-16`
- Output folder:
  `C:\Users\Ali\Desktop\datalab_ali\processed_pdfs\2015-16_pymupdf4llm`
- PDFs selected:
  all `*.pdf` files directly inside the input folder only
- Original PDFs:
  not modified, renamed, moved, or deleted
- Existing project scripts:
  not used, including anything under `agentic/`

## Environment Observed

- PyMuPDF4LLM: `1.27.2.3`
- PyMuPDF: `1.27.2.3`
- Branch at run time: `new-conversion`

## Conversion Method

Each PDF was converted directly with:

```python
pymupdf4llm.to_markdown(str(pdf_path), page_chunks=True)
```

The page chunks were joined with explicit page markers:

```markdown
<!-- page 1 -->
```

Outputs were written as:

```text
processed_pdfs\2015-16_pymupdf4llm\<original_pdf_name_without_ext>.md
```

The run also wrote:

```text
processed_pdfs\2015-16_pymupdf4llm\conversion_log.json
```

Each log entry records:

- source PDF path
- output Markdown path
- success/failure
- page count, when available
- error message, if failed

## Equivalent One-Off Script

Run this from the repository root if the same environment is available:

```python
from __future__ import annotations

import json
from pathlib import Path

import fitz
import pymupdf4llm


INPUT_DIR = Path(
    r"C:\Users\Ali\Desktop\datalab_ali\datalab_master\Master Data\pakistan_economic_survey\2015-16"
)
OUTPUT_DIR = Path(
    r"C:\Users\Ali\Desktop\datalab_ali\processed_pdfs\2015-16_pymupdf4llm"
)
LOG_PATH = OUTPUT_DIR / "conversion_log.json"


def get_page_count(pdf_path: Path) -> int | None:
    try:
        with fitz.open(pdf_path) as doc:
            return doc.page_count
    except Exception:
        return None


def chunk_page_number(chunk: dict, fallback: int) -> int:
    metadata = chunk.get("metadata") or {}
    for key in ("page", "page_number", "page_no"):
        value = metadata.get(key)
        if isinstance(value, int):
            return value
    return fallback


def markdown_with_page_markers(pdf_path: Path) -> str:
    chunks = pymupdf4llm.to_markdown(str(pdf_path), page_chunks=True)
    pages = []

    if isinstance(chunks, list):
        for index, chunk in enumerate(chunks, start=1):
            if isinstance(chunk, dict):
                page_no = chunk_page_number(chunk, index)
                text = chunk.get("text") or ""
            else:
                page_no = index
                text = str(chunk)
            pages.append(f"<!-- page {page_no} -->\n\n{text.strip()}")
        return "\n\n".join(pages).rstrip() + "\n"

    return str(chunks).rstrip() + "\n"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf_paths = sorted(INPUT_DIR.glob("*.pdf"), key=lambda p: p.name.lower())
    log = []

    for pdf_path in pdf_paths:
        output_path = OUTPUT_DIR / f"{pdf_path.stem}.md"
        entry = {
            "source_pdf_path": str(pdf_path),
            "output_md_path": str(output_path),
            "success": False,
            "page_count": get_page_count(pdf_path),
            "error_message": None,
        }

        try:
            output_path.write_text(
                markdown_with_page_markers(pdf_path),
                encoding="utf-8",
                newline="\n",
            )
            entry["success"] = True
        except Exception as exc:
            entry["error_message"] = str(exc)

        log.append(entry)

    LOG_PATH.write_text(
        json.dumps(log, indent=2, ensure_ascii=False),
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
```

## Run Result

- Total PDFs found: `29`
- Total converted: `29`
- Failures: `0`

