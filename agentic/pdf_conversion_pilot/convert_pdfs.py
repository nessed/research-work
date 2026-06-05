from pathlib import Path

import pymupdf4llm


ROOT = Path(__file__).resolve().parents[2]

INPUTS = [
    (
        ROOT
        / "datalab_master"
        / "Master Data"
        / "pakistan_economic_survey"
        / "2019-20"
        / "Education.pdf",
        ROOT / "agentic" / "pdf_conversion_pilot" / "education_2019_20.md",
    ),
    (
        ROOT
        / "datalab_master"
        / "Master Data"
        / "pakistan_economic_survey"
        / "2021-22"
        / "Pes13_Transport.pdf",
        ROOT / "agentic" / "pdf_conversion_pilot" / "transport_2021_22.md",
    ),
]


def convert_pdf(input_pdf: Path, output_md: Path) -> None:
    chunks = pymupdf4llm.to_markdown(str(input_pdf), page_chunks=True)
    sections = []

    for index, chunk in enumerate(chunks, start=1):
        page = chunk.get("metadata", {}).get("page", index)
        text = chunk.get("text", "").rstrip()
        sections.append(f"<!-- source_pdf_page: {page} -->\n\n## PDF page {page}\n\n{text}\n")

    output_md.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for input_pdf, output_md in INPUTS:
        if not input_pdf.exists():
            raise FileNotFoundError(input_pdf)
        output_md.parent.mkdir(parents=True, exist_ok=True)
        convert_pdf(input_pdf, output_md)


if __name__ == "__main__":
    main()
