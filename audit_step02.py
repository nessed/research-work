import os
import re

base_dir = r"C:\Users\Ali\Desktop\datalab_ali"
pdf_master_dir = os.path.join(base_dir, r"datalab_master\Master Data\pakistan_economic_survey")
runs_base_dir = os.path.join(base_dir, r"agentic\02_pdf_to_md\runs")

years = [
    "2015-16", "2016-17", "2017-18", "2018-19", "2019-20", 
    "2020-21", "2021-22", "2022-23", "2023-24", "2024-25"
]

out_lines = []
out_lines.append("# Step 02 Completion Audit Table")
out_lines.append("")
out_lines.append("| Year | PDF count | MD count | manifest exists/non-empty | conversion log exists/non-empty | QA report exists/non-empty | 0-byte MD files | Page-marker mismatches | Sample pages checked |")
out_lines.append("|---|---|---|---|---|---|---|---|---|")

for year in years:
    pdf_dir = os.path.join(pdf_master_dir, year)
    run_dir = os.path.join(runs_base_dir, f"{year}_pymupdf4llm_hardened")
    md_dir = os.path.join(run_dir, "converted_md")
    
    # PDF count
    pdf_count = 0
    if os.path.isdir(pdf_dir):
        pdf_count = len([f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')])
        
    # MD count and 0-byte count
    md_count = 0
    zero_byte_count = 0
    if os.path.isdir(md_dir):
        for f in os.listdir(md_dir):
            if f.lower().endswith('.md'):
                md_count += 1
                if os.path.getsize(os.path.join(md_dir, f)) == 0:
                    zero_byte_count += 1
                    
    # File checks
    def check_file(filename):
        path = os.path.join(run_dir, filename)
        if not os.path.isfile(path):
            return "No"
        if os.path.getsize(path) == 0:
            return "Empty"
        return "Yes"

    manifest_status = check_file("repro_manifest.json")
    log_status = check_file("conversion_log.json")
    qa_status = check_file("qa_report.md")
    
    # Parse QA report
    page_marker_mismatches = "N/A"
    sample_pages_checked = "N/A"
    qa_path = os.path.join(run_dir, "qa_report.md")
    if os.path.isfile(qa_path) and os.path.getsize(qa_path) > 0:
        with open(qa_path, "r", encoding="utf-8") as f:
            content = f.read()
            m1 = re.search(r"Page-marker mismatches:\s*`?(\d+)`?", content)
            if m1:
                page_marker_mismatches = m1.group(1)
            m2 = re.search(r"Sample count:\s*`?(\d+)`?", content)
            if m2:
                sample_pages_checked = m2.group(1)
                
    out_lines.append(f"| {year} | {pdf_count} | {md_count} | {manifest_status} | {log_status} | {qa_status} | {zero_byte_count} | {page_marker_mismatches} | {sample_pages_checked} |")

output_path = os.path.join(base_dir, "completion_audit_table.md")
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines) + "\n")

print(f"Audit table written to {output_path}")
