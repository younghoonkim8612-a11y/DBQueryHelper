"""Check all tables in gisdb_JED vs current migration list."""
from db_helper import QueryHelper

MIGRATION_TABLES = [
    "tml_map", "cog_grp", "yrd_map", "apr_map", "htl_map", "gfc_map",
    "gfc_calibration_map", "leg_map", "ltp_map", "bld_map", "fen_map",
    "prk_map", "ral_map", "rcl_map", "rfi_map", "rpg_map",
    "bk_map", "bet_map", "bit_map", "gat_map", "gco_tbl", "cov_val", "bay_map",
]

QUERY = """
SELECT table_name
FROM information_schema.tables
WHERE table_schema = %s AND table_type = 'BASE TABLE'
ORDER BY table_name;
"""

helper = QueryHelper("LukasPostgres")
helper.connect()
cur = helper._conn.cursor()

for schema in ["gisdb_JED", "gisdb"]:
    cur.execute(QUERY, (schema,))
    tables = [r[0] for r in cur.fetchall()]
    missing = [t for t in tables if t not in MIGRATION_TABLES]
    print(f"\n=== {schema}: {len(tables)} tables total ===")
    if missing:
        print(f"  NOT in migration list ({len(missing)}):")
        for t in missing:
            print(f"    - {t}")

helper.close()
