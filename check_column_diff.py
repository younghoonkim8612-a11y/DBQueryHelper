"""Compare columns between gisdb and gisdb_JED for all migration tables."""
from db_helper import QueryHelper

TABLES = [
    "tml_map", "cog_grp", "yrd_map", "bet_map", "htl_map", "gfc_map",
    "gfc_calibration_map", "leg_map", "ltp_map", "apr_map", "bld_map",
    "fen_map", "prk_map", "ral_map", "rcl_map", "rfi_map", "rpg_map",
    "bk_map", "bit_map", "gat_map", "gco_tbl", "cov_val", "bay_map",
]

QUERY = """
SELECT column_name
FROM information_schema.columns
WHERE table_schema = %s AND table_name = %s
ORDER BY ordinal_position;
"""

helper = QueryHelper("LukasPostgres")
helper.connect()
cur = helper._conn.cursor()

has_diff = False
for table in TABLES:
    cur.execute(QUERY, ("gisdb", table))
    gisdb_cols = [r[0] for r in cur.fetchall()]

    cur.execute(QUERY, ("gisdb_JED", table))
    jed_cols = [r[0] for r in cur.fetchall()]

    only_gisdb = set(gisdb_cols) - set(jed_cols)
    only_jed = set(jed_cols) - set(gisdb_cols)

    if only_gisdb or only_jed:
        has_diff = True
        print(f"\n=== {table} ===")
        if only_gisdb:
            print(f"  gisdb ONLY:     {sorted(only_gisdb)}")
        if only_jed:
            print(f"  gisdb_JED ONLY: {sorted(only_jed)}")

if not has_diff:
    print("All tables have identical columns.")

helper.close()
