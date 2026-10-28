import gzip
import re
import os

backup_gz = os.path.join("backup", "crm_database.sql.gz")
full_sql = os.path.join("backup", "crm_database.sql")
schema_sql = os.path.join("backup", "crm_schema_only.sql")
core_sql = os.path.join("backup", "crm_core_crm_tables.sql")

print("1. Decompressing full database SQL dump...")
with gzip.open(backup_gz, "rb") as f_in:
    with open(full_sql, "wb") as f_out:
        while chunk := f_in.read(1024 * 1024):
            f_out.write(chunk)

full_size_mb = os.path.getsize(full_sql) / (1024 * 1024)
print(f"Full DB decompressed: {full_sql} ({full_size_mb:.2f} MB)")

print("2. Parsing tables and extracting schema...")
table_schemas = {}
table_inserts = {}
all_tables = []

with open(full_sql, "r", encoding="utf-8", errors="ignore") as f:
    current_table = None
    collecting_create = False
    create_lines = []

    for line in f:
        m_create = re.match(r"^CREATE TABLE [`\"]([^`\"]+)[`\"]", line, re.I)
        if m_create:
            current_table = m_create.group(1)
            all_tables.append(current_table)
            collecting_create = True
            create_lines = [line]
            continue

        if collecting_create:
            create_lines.append(line)
            if re.match(r"^\)\s*(ENGINE|DEFAULT CHARSET|COLLATE|;)", line, re.I) or line.strip().endswith(";"):
                table_schemas[current_table] = "".join(create_lines)
                collecting_create = False
            continue

        m_insert = re.match(r"^INSERT INTO [`\"]([^`\"]+)[`\"]", line, re.I)
        if m_insert:
            tbl = m_insert.group(1)
            if tbl not in table_inserts:
                table_inserts[tbl] = []
            table_inserts[tbl].append(line)

print(f"Total tables detected: {len(all_tables)}")

# Write Schema-Only file
with open(schema_sql, "w", encoding="utf-8") as f:
    f.write("-- PC CRM Complete Schema Only (No Records)\n")
    f.write("-- Generated for Dashboard & Analytics Design\n\n")
    for tbl in all_tables:
        if tbl in table_schemas:
            f.write(f"-- --------------------------------------------------------\n")
            f.write(f"-- Table structure for `{tbl}`\n")
            f.write(f"-- --------------------------------------------------------\n")
            f.write(table_schemas[tbl])
            f.write("\n\n")

print(f"Schema only written to: {schema_sql} ({os.path.getsize(schema_sql)/(1024*1024):.2f} MB)")

# Core CRM tables filter
core_patterns = [
    r"tabCRM.*",
    r"tabLead.*",
    r"tabDeal.*",
    r"tabContact.*",
    r"tabOrganization.*",
    r"tabTask.*",
    r"tabActivity.*",
    r"tabCall Log.*",
    r"tabUser.*",
    r"tabNote.*",
    r"tabCommunication.*"
]

core_tables = [t for t in all_tables if any(re.match(p, t, re.I) for p in core_patterns)]
print(f"Core CRM tables identified ({len(core_tables)}): {core_tables}")

with open(core_sql, "w", encoding="utf-8") as f:
    f.write("-- PC CRM Core CRM Entities (Schema + Dummy Data)\n\n")
    for tbl in core_tables:
        f.write(f"-- ========================================================\n")
        f.write(f"-- Table `{tbl}`\n")
        f.write(f"-- ========================================================\n")
        if tbl in table_schemas:
            f.write(table_schemas[tbl])
            f.write("\n\n")
        if tbl in table_inserts:
            for ins in table_inserts[tbl]:
                f.write(ins)
            f.write("\n\n")

print(f"Core CRM tables and data written to: {core_sql} ({os.path.getsize(core_sql)/(1024):.2f} KB)")
