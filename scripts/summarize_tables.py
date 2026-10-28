import re

tables = [
    'tabCRM Lead',
    'tabCRM Deal',
    'tabCRM Deal Status',
    'tabCRM Lead Status',
    'tabCRM Organization',
    'tabContact',
    'tabCRM Task',
    'tabCRM Call Log',
    'tabCRM Service Level Agreement',
    'tabCRM Service Level Priority'
]

with open('backup/crm_schema_only.sql', 'r', encoding='utf-8') as f:
    content = f.read()

for t in tables:
    m = re.search(r'CREATE TABLE `' + t + r'` \((.*?)\) ENGINE', content, re.S)
    if m:
        cols = []
        for line in m.group(1).split('\n'):
            line = line.strip()
            if line.startswith('`'):
                col_name = line.split()[0].replace('`', '')
                col_type = line.split()[1]
                cols.append(f"{col_name} ({col_type})")
        print(f"\n### {t}")
        print(", ".join(cols[:25]))
