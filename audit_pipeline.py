import os
import re

base_dir = r"C:\Users\Ali\Desktop\datalab_ali"
pdf_master_dir = os.path.join(base_dir, r"datalab_master\Master Data\pakistan_economic_survey")
runs_base_dir_02 = os.path.join(base_dir, r"agentic\02_pdf_to_md\runs")
runs_base_dir_03 = os.path.join(base_dir, r"agentic\03_section_splitting\runs")

years = [
    "2015-16", "2016-17", "2017-18", "2018-19", "2019-20", 
    "2020-21", "2021-22", "2022-23", "2023-24", "2024-25"
]

def check_file(folder, filename):
    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        return "No"
    if os.path.getsize(path) == 0:
        return "Empty"
    return "Yes"

out_lines = []
out_lines.append("# Pipeline Completion Audit")
out_lines.append("")
out_lines.append("## Step 02: PDF to Markdown")
out_lines.append("| Year | Run Folder | Raw PDFs | Conv MDs | repro_manifest | conversion_log | qa_results | qa_report | conv script | qa script | adv review | 0-byte MDs | Pg Mismatch | Status |")
out_lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")

for year in years:
    pdf_dir = os.path.join(pdf_master_dir, year)
    run_folder_name = f"{year}_pymupdf4llm_hardened"
    run_dir = os.path.join(runs_base_dir_02, run_folder_name)
    md_dir = os.path.join(run_dir, "converted_md")
    
    pdf_count = 0
    if os.path.isdir(pdf_dir):
        pdf_count = len([f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')])
        
    md_count = 0
    zero_byte_count = 0
    if os.path.isdir(md_dir):
        for f in os.listdir(md_dir):
            if f.lower().endswith('.md'):
                md_count += 1
                if os.path.getsize(os.path.join(md_dir, f)) == 0:
                    zero_byte_count += 1

    manifest_ok = check_file(run_dir, "repro_manifest.json")
    log_ok = check_file(run_dir, "conversion_log.json")
    qa_res_ok = check_file(run_dir, "qa_results.json")
    qa_rep_ok = check_file(run_dir, "qa_report.md")
    script_ok = check_file(run_dir, f"convert_{year.replace('-','_')}_pymupdf4llm.py")
    qa_script_ok = check_file(run_dir, f"qa_{year.replace('-','_')}_pymupdf4llm.py")
    adv_ok = check_file(run_dir, "adv_review_results.md")

    page_marker_mismatches = "N/A"
    qa_path = os.path.join(run_dir, "qa_report.md")
    if os.path.exists(qa_path) and os.path.getsize(qa_path) > 0:
        with open(qa_path, "r", encoding="utf-8") as f:
            content = f.read()
            m = re.search(r"Page-marker mismatches:\s*`?(\d+)`?", content)
            if m:
                page_marker_mismatches = m.group(1)

    checks = [manifest_ok, log_ok, qa_res_ok, qa_rep_ok, script_ok, qa_script_ok]
    if not os.path.exists(run_dir):
        status = "MISSING"
    elif all(c == "Yes" for c in checks) and pdf_count > 0 and pdf_count == md_count and zero_byte_count == 0 and str(page_marker_mismatches) == "0":
        status = "PASS"
    else:
        status = "PARTIAL / NEEDS_REVIEW"

    out_lines.append(f"| {year} | {run_folder_name} | {pdf_count} | {md_count} | {manifest_ok} | {log_ok} | {qa_res_ok} | {qa_rep_ok} | {script_ok} | {qa_script_ok} | {adv_ok} | {zero_byte_count} | {page_marker_mismatches} | {status} |")

out_lines.append("")
out_lines.append("## Step 03: Section Splitting")
out_lines.append("| Year | Run Folder | sections.jsonl | section_manifest | split_report | adv review | section count | incl/excl recorded | Status |")
out_lines.append("|---|---|---|---|---|---|---|---|---|")

for year in years:
    run_folder_name = f"{year}_section_split_pymupdf4llm_hardened"
    run_dir = os.path.join(runs_base_dir_03, run_folder_name)
    
    sec_json_ok = check_file(run_dir, "sections.jsonl")
    sec_man_ok = check_file(run_dir, "section_manifest.json")
    sec_rep_ok = check_file(run_dir, "section_split_report.md")
    adv_ok = check_file(run_dir, "adv_review_results.md")

    section_count = "N/A"
    incl_excl = "No"
    
    rep_path = os.path.join(run_dir, "section_split_report.md")
    if os.path.exists(rep_path) and os.path.getsize(rep_path) > 0:
        with open(rep_path, "r", encoding="utf-8") as f:
            content = f.read()
            m = re.search(r"Sections written:\s*`?(\d+)`?", content)
            if m:
                section_count = m.group(1)
            if "Source Markdown files:" in content or "Excluded Inputs" in content:
                incl_excl = "Yes"

    checks = [sec_json_ok, sec_man_ok, sec_rep_ok]
    if not os.path.exists(run_dir):
        status = "MISSING"
    elif all(c == "Yes" for c in checks) and str(section_count) != "N/A":
        status = "PASS"
    else:
        status = "PARTIAL / NEEDS_REVIEW"

    out_lines.append(f"| {year} | {run_folder_name} | {sec_json_ok} | {sec_man_ok} | {sec_rep_ok} | {adv_ok} | {section_count} | {incl_excl} | {status} |")

output_path = os.path.join(base_dir, "pipeline_completion_audit.md")
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines) + "\n")

print(f"Audit completed: {output_path}")
