"""Check bet_map columns in both schemas."""
from db_helper import QueryHelper

QUERY = """
SELECT table_schema, column_name, data_type
FROM information_schema.columns
WHERE table_name = 'bet_map'
    AND table_schema IN ('gisdb', 'gisdb_JED')
ORDER BY table_schema, ordinal_position;
"""

helper = QueryHelper("LukasPostgres")
helper.connect()
cur = helper._conn.cursor()
cur.execute(QUERY)
rows = cur.fetchall()

current_schema = None
for schema, col, dtype in rows:
    if schema != current_schema:
        print(f"\n=== {schema}.bet_map ===")
        current_schema = schema
    print(f"  {col} ({dtype})")

helper.close()
