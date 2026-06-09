import json
import os
import hashlib

run_dir = r"C:\Users\Ali\Desktop\datalab_ali\agentic\03_section_splitting\runs\2023-24_section_split_pymupdf4llm_hardened"
manifest_path = os.path.join(run_dir, "section_manifest.json")
report_path = os.path.join(run_dir, "section_split_report.md")
sections_path = os.path.join(run_dir, "sections.jsonl")

# 1. Check sections.jsonl counts and unique IDs
sections = []
with open(sections_path, 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():
            sections.append(json.loads(line))

section_ids = [s['section_id'] for s in sections]
unique_ids = set(section_ids)

print(f"Total lines in sections.jsonl: {len(sections)}")
print(f"Unique section IDs: {len(unique_ids)}")
if len(sections) != len(unique_ids):
    print("FAIL: duplicate section IDs found!")

# 2. Reconcile counts
with open(manifest_path, 'r', encoding='utf-8') as f:
    manifest = json.load(f)

manifest_count = manifest['qa_results']['sections_total']
print(f"Manifest sections_total: {manifest_count}")

report_count = 0
with open(report_path, 'r', encoding='utf-8') as f:
    for line in f:
        if "Sections written:" in line:
            report_count = int(line.split(":")[-1].strip().replace('`', ''))

print(f"Report sections written: {report_count}")

if not (len(sections) == manifest_count == report_count):
    print("FAIL: Counts do not reconcile!")

# 3. Verify fields
allowed_fields = {
    "section_id", "source_year", "source_md_path", "source_pdf_path", "sector",
    "heading_text", "start_page", "end_page", "section_type", "text",
    "numeric_or_table_sensitive", "markdown_quality_flags"
}
has_extra_fields = False
for s in sections:
    extra = set(s.keys()) - allowed_fields
    if extra:
        has_extra_fields = True
        print(f"Extra fields found in {s['section_id']}: {extra}")
        break

if has_extra_fields:
    print("FAIL: Extra claim/summary fields found!")
else:
    print("PASS: No forbidden fields.")

# 4. Check paths exist (we'll just check a few or all)
all_md_exist = True
project_root = r"C:\Users\Ali\Desktop\datalab_ali"
for md_rel in manifest['qa_results']['sections_by_file'].keys():
    md_abs = os.path.join(project_root, md_rel)
    if not os.path.exists(md_abs):
        print(f"FAIL: MD path does not exist: {md_abs}")
        all_md_exist = False

if all_md_exist:
    print("PASS: All source_md_paths exist.")

# 5. Check numeric flagging
# Just a basic check: are there sections with numbers that are not flagged?
# Actually, the prompt says "Table-heavy, figure-heavy, numeric-heavy, chart-adjacent, or exact-value sections are flagged"
# We can check if any text has a digit but numeric_or_table_sensitive is False.
unflagged_numeric = 0
for s in sections:
    if not s.get('numeric_or_table_sensitive', False):
        if any(char.isdigit() for char in s.get('text', '')):
            unflagged_numeric += 1

print(f"Unflagged sections containing digits: {unflagged_numeric}")

print("Done.")
