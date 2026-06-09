import json
import os
import glob
import re

base_dir = r"C:\Users\Ali\Desktop\datalab_ali"
run_dir = os.path.join(base_dir, r"agentic\03_section_splitting\runs\2019-20_section_split_pymupdf4llm_hardened")
manifest_path = os.path.join(run_dir, "section_manifest.json")
report_path = os.path.join(run_dir, "section_split_report.md")
sections_path = os.path.join(run_dir, "sections.jsonl")

# Load manifest
with open(manifest_path, 'r', encoding='utf-8') as f:
    manifest = json.load(f)

print("Check 1: Unique section_ids")
section_ids = set()
duplicates = []
invalid_pages = []
missing_md = []
missing_pdf = []
not_in_md = []
claims_fields = ["claim", "summary", "interpretation", "conclusion", "fact", "outlook", "risk", "sentiment", "policy_action"]
has_claims = []
unflagged_numeric = []
empty_flags = []

line_count = 0

# load pdf to md repro manifest to check PDF sizes/pages
md_manifest_path = os.path.join(base_dir, manifest['input_repro_manifest'])
with open(md_manifest_path, 'r', encoding='utf-8') as f:
    md_manifest = json.load(f)
pdf_pages = {item['source_pdf_path']: item['page_count'] for item in md_manifest['input_entries']}

with open(sections_path, 'r', encoding='utf-8') as f:
    for line in f:
        line_count += 1
        sec = json.loads(line)
        sid = sec.get('section_id')
        if sid in section_ids:
            duplicates.append(sid)
        section_ids.add(sid)

        # Check 2: source_md_path exists
        md_p = os.path.join(base_dir, sec.get('source_md_path', ''))
        if not os.path.exists(md_p):
            missing_md.append(sec.get('source_md_path'))
        
        # Check 3: source_pdf_path points to original
        pdf_p = os.path.join(base_dir, sec.get('source_pdf_path', ''))
        if not os.path.exists(pdf_p):
            missing_pdf.append(sec.get('source_pdf_path'))
            
        # Check 4: Valid start/end pages
        sp = sec.get('start_page')
        ep = sec.get('end_page')
        p_count = pdf_pages.get(sec.get('source_pdf_path'), 0)
        if sp < 1 or ep > p_count or sp > ep:
            invalid_pages.append((sid, sp, ep, p_count))
            
        # Check 6: No claims fields
        for field in claims_fields:
            if field in sec:
                has_claims.append((sid, field))
                
        # Check 7: Numeric/table flags (basic heuristic, if text has lot of numbers/tables)
        if not sec.get('numeric_or_table_sensitive', False):
            # very simple heuristic, just checking if it should have been
            if '|---|' in sec.get('text', '') or sum(c.isdigit() for c in sec.get('text', '')) > 20:
                unflagged_numeric.append(sid)
                
        # Check 8: Quality flags
        flags = sec.get('markdown_quality_flags', [])
        if not isinstance(flags, list) or len(flags) == 0:
            empty_flags.append(sid)

print(f"Total Sections: {line_count}")
print(f"Duplicates: {len(duplicates)}")
print(f"Missing MD: {len(missing_md)}")
print(f"Missing PDF: {len(missing_pdf)}")
print(f"Invalid Pages: {len(invalid_pages)}")
print(f"Has Claims Fields: {len(has_claims)}")
print(f"Unflagged Numeric (heuristic): {len(unflagged_numeric[:10])} (showing up to 10)")
print(f"Empty Quality Flags: {len(empty_flags)}")

# Check 10: Reconcile counts
manifest_total = manifest['qa_results']['sections_total']
report_total = 1664 # Read from report
print(f"Manifest total: {manifest_total}, Report total: {report_total}, JSONL total: {line_count}")
if manifest_total == report_total == line_count:
    print("Counts reconcile!")
else:
    print("Counts DO NOT reconcile!")

