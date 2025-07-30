import re
import pandas as pd

# Đường dẫn tới file .bib của bạn
bib_path = "acm.bib"

# Đọc nội dung file
with open(bib_path, encoding="utf-8") as f:
    bib_content = f.read()

# Tách các entry
entries = re.findall(r"@\w+\{[^@]+?\n\}", bib_content, re.DOTALL)

parsed_entries = []
for entry in entries:
    fields = dict()
    lines = entry.splitlines()
    header = lines[0]
    match = re.match(r"@(\w+)\{([^,]+),", header)
    if match:
        fields['entry_type'] = match.group(1)
        fields['citation_key'] = match.group(2)
    for line in lines[1:]:
        field_match = re.match(r'\s*(\w+)\s*=\s*[{"](.*?)[}"],?\s*$', line.strip())
        if field_match:
            key, value = field_match.groups()
            fields[key.lower()] = value
    parsed_entries.append(fields)

# Chuyển sang CSV
df = pd.DataFrame(parsed_entries)
df.to_csv("176_acm_converted.csv", index=False)
