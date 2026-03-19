"""gisdb_JED schema FK constraints check."""
from db_helper import QueryHelper

FK_QUERY = """
SELECT
    tc.table_name AS child_table,
    kcu.column_name AS fk_column,
    ccu.table_name AS parent_table,
    ccu.column_name AS parent_column,
    tc.constraint_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage ccu
    ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
    AND tc.table_schema = %s
ORDER BY child_table, parent_table;
"""

PK_QUERY = """
SELECT
    tc.table_name,
    kcu.column_name,
    tc.constraint_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
WHERE tc.constraint_type = 'PRIMARY KEY'
    AND tc.table_schema = %s
ORDER BY tc.table_name, kcu.ordinal_position;
"""

SCHEMA = "gisdb"

helper = QueryHelper("LukasPostgres")
helper.connect()
conn = helper._conn
cur = conn.cursor()

print(f"=== {SCHEMA} PK Constraints ===")
cur.execute(PK_QUERY, (SCHEMA,))
rows = cur.fetchall()
if not rows:
    print("  (none)")
for r in rows:
    print(f"  {r[0]}.{r[1]}  [{r[2]}]")

print(f"\n=== {SCHEMA} FK Constraints ===")
cur.execute(FK_QUERY, (SCHEMA,))
rows = cur.fetchall()
if not rows:
    print("  (none)")
for r in rows:
    print(f"  {r[0]}.{r[1]} -> {r[2]}.{r[3]}  [{r[4]}]")

helper.close()
