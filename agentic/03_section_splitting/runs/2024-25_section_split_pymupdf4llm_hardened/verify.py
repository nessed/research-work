import json
import os

run_dir = "C:/Users/Ali/Desktop/datalab_ali/agentic/03_section_splitting/runs/2024-25_section_split_pymupdf4llm_hardened"
manifest_path = os.path.join(run_dir, "section_manifest.json")
jsonl_path = os.path.join(run_dir, "sections.jsonl")

with open(manifest_path, 'r', encoding='utf-8') as f:
    manifest = json.load(f)

sections = []
with open(jsonl_path, 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():
            sections.append(json.loads(line))

# Check 1
section_ids = [s['section_id'] for s in sections]
print("Check 1 (Unique IDs):", len(section_ids) == len(set(section_ids)))

# Check 2 & 3
c2_pass = True
c3_pass = True
base_dir = "C:/Users/Ali/Desktop/datalab_ali"
for s in sections:
    md_path = os.path.join(base_dir, s['source_md_path'])
    pdf_path = os.path.join(base_dir, s['source_pdf_path'])
    if not os.path.exists(md_path): c2_pass = False
    if not os.path.exists(pdf_path): c3_pass = False
print("Check 2 (MD exists):", c2_pass)
print("Check 3 (PDF exists):", c3_pass)

# Check 4
c4_pass = all(s['start_page'] <= s['end_page'] and s['start_page'] > 0 for s in sections)
print("Check 4 (Pages valid):", c4_pass)

# Check 6
forbidden = {'claim', 'summary', 'interpretation', 'conclusion', 'fact'}
c6_pass = True
for s in sections:
    keys = set(s.keys())
    if keys.intersection(forbidden):
        c6_pass = False
print("Check 6 (No claims):", c6_pass)

# Check 7
c7_pass = all('numeric_or_table_sensitive' in s and isinstance(s['numeric_or_table_sensitive'], bool) for s in sections)
print("Check 7 (Numeric flag):", c7_pass)

# Check 8
c8_pass = all('markdown_quality_flags' in s and isinstance(s['markdown_quality_flags'], list) for s in sections)
print("Check 8 (Quality flags):", c8_pass)

# Check 10
manifest_count = manifest['qa_results']['sections_total']
print("Check 10 (Counts reconcile):", len(sections) == manifest_count == 1227)
