"""
Extracts data from gisdb_JED schema and generates
DELETE + INSERT VALUES SQL for the gisdb schema.

Tables are ordered by PK/FK dependency.
"""

import os
import json
from datetime import datetime, date
from decimal import Decimal
from db_helper import QueryHelper

# ============================================================
# Table dependency definition (based on PK/FK relationships)
# DELETE order: child -> parent (reverse)
# INSERT order: parent -> child (forward)
# ============================================================
TABLES_INSERT_ORDER = [
    # Level 0: independent
    "tml_map",
    "cog_grp",
    # Level 1: depends on tml_map
    "yrd_map",
    "apr_map",
    "htl_map",
    "gfc_map",
    "gfc_calibration_map",
    "leg_map",
    "ltp_map",
    "bld_map",
    "fen_map",
    "prk_map",
    "ral_map",
    "rcl_map",
    "rfi_map",
    "rpg_map",
    # Level 2: depends on Level 1
    "bk_map",      # -> yrd_map
    "bet_map",     # -> apr_map (bet_apr_id -> apr_apr_id)
    "bit_map",     # -> tml_map
    "gat_map",     # -> htl_map
    "gco_tbl",     # -> gfc_map
    "cov_val",     # -> cog_grp
    # Level 3: depends on Level 2
    "bay_map",     # -> bk_map
]

SOURCE_SCHEMA = "gisdb_JED"
TARGET_SCHEMA = "gisdb"
CONNECTION_NAME = "LukasPostgres"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(
    SCRIPT_DIR, "Generated Files",
    datetime.now().strftime("%Y-%m-%d"),
    "JED GIS Insert Script"
)
OUTPUT_FILE = "migrate_gisdb_data.sql"
BATCH_SIZE = 500

# pgRouting topology rebuild queries (run after parent table INSERT)
PGROUTING_TOPOLOGY = {
    "leg_map": "SELECT pgr_createTopology('gisdb.leg_map', 0.000001, 'geom', 'leg_leg_id', 'leg_leg_fd', 'leg_leg_td', rows_where := 'true', clean := true);",
    "rcl_map": "SELECT pgr_createTopology('gisdb.rcl_map', 0.000001, 'geom', 'rcl_rcl_id', 'rcl_rcl_sn', 'rcl_rcl_tn', rows_where := 'true', clean := true);",
}

# Additional tables to DELETE that are rebuilt via pgRouting
PGROUTING_VERTEX_TABLES = [
    "leg_map_vertices_pgr",
    "rcl_map_vertices_pgr",
]


def format_value(val):
    """Convert a Python value to a SQL literal string."""
    if val is None:
        return "NULL"
    if isinstance(val, bool):
        return "TRUE" if val else "FALSE"
    if isinstance(val, (int, float, Decimal)):
        return str(val)
    if isinstance(val, (datetime, date)):
        return f"'{val.isoformat()}'"
    if isinstance(val, dict):
        escaped = json.dumps(val, ensure_ascii=False).replace("'", "''")
        return f"'{escaped}'::jsonb"
    if isinstance(val, list):
        escaped = json.dumps(val, ensure_ascii=False).replace("'", "''")
        return f"'{escaped}'::jsonb"
    if isinstance(val, memoryview):
        return f"'\\x{val.tobytes().hex()}'"
    if isinstance(val, bytes):
        return f"'\\x{val.hex()}'"
    escaped = str(val).replace("'", "''")
    return f"'{escaped}'"


def generate_insert_statements(table_name, columns, rows):
    """Generate batched INSERT statements."""
    if not rows:
        return f"-- {table_name}: no data\n"

    col_list = ", ".join(columns)
    statements = []
    statements.append(f"-- {table_name}: {len(rows)} rows")

    for i in range(0, len(rows), BATCH_SIZE):
        batch = rows[i:i + BATCH_SIZE]
        values_list = []
        for row in batch:
            vals = ", ".join(format_value(v) for v in row)
            values_list.append(f"  ({vals})")

        stmt = f"INSERT INTO {TARGET_SCHEMA}.{table_name} ({col_list})\nVALUES\n"
        stmt += ",\n".join(values_list) + ";\n"
        statements.append(stmt)

    return "\n".join(statements)


def main():
    print(f"=== gisdb_JED -> gisdb Migration SQL Generator ===")
    print(f"Source schema: {SOURCE_SCHEMA}")
    print(f"Target schema: {TARGET_SCHEMA}")
    print(f"Connection: {CONNECTION_NAME}")
    print()

    helper = QueryHelper(CONNECTION_NAME)
    helper.connect()

    try:
        conn = helper._conn
        cur = conn.cursor()

        delete_statements = []
        insert_statements = []

        delete_order = list(reversed(TABLES_INSERT_ORDER))

        print("[1/2] Generating DELETE statements...")
        # Delete pgRouting vertex tables first (children of leg_map/rcl_map)
        for table in PGROUTING_VERTEX_TABLES:
            delete_statements.append(f"DELETE FROM {TARGET_SCHEMA}.{table};")
        for table in delete_order:
            delete_statements.append(f"DELETE FROM {TARGET_SCHEMA}.{table};")

        print("[2/2] Extracting data and generating INSERT statements...")
        for table in TABLES_INSERT_ORDER:
            print(f"  - {SOURCE_SCHEMA}.{table} ...", end=" ")

            cur.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = %s AND table_name = %s
                ORDER BY ordinal_position
            """, (SOURCE_SCHEMA, table))
            columns = [row[0] for row in cur.fetchall()]

            if not columns:
                print(f"table not found (skip)")
                insert_statements.append(f"-- {table}: table not found in {SOURCE_SCHEMA} (skip)")
                delete_statements = [
                    d for d in delete_statements
                    if d != f"DELETE FROM {TARGET_SCHEMA}.{table};"
                ]
                continue

            col_list_sql = ", ".join(f'"{c}"' for c in columns)
            cur.execute(f'SELECT {col_list_sql} FROM "{SOURCE_SCHEMA}"."{table}"')
            rows = cur.fetchall()

            print(f"{len(rows)} rows")

            if not rows:
                insert_statements.append(f"-- {table}: no data")
            else:
                insert_statements.append(
                    generate_insert_statements(table, columns, rows)
                )

            # Add pgRouting topology rebuild after parent table INSERT
            if table in PGROUTING_TOPOLOGY:
                insert_statements.append(
                    f"-- Rebuild pgRouting topology for {table}\n"
                    f"{PGROUTING_TOPOLOGY[table]}"
                )

        # Write SQL file
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("-- ============================================================\n")
            f.write("-- gisdb_JED -> gisdb Data Migration (Auto-generated)\n")
            f.write(f"-- Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-- ============================================================\n")
            f.write("-- This SQL can be executed without access to the gisdb_JED schema.\n")
            f.write("-- Tables are ordered by PK/FK dependency.\n")
            f.write("-- ============================================================\n\n")
            f.write("BEGIN;\n\n")

            f.write("-- ======================\n")
            f.write("-- STEP 1: DELETE (child -> parent order)\n")
            f.write("-- ======================\n\n")
            for stmt in delete_statements:
                f.write(stmt + "\n")

            f.write("\n-- ======================\n")
            f.write("-- STEP 2: INSERT (parent -> child order)\n")
            f.write("-- ======================\n\n")
            for stmt in insert_statements:
                f.write(stmt + "\n\n")

            f.write("COMMIT;\n")

        print(f"\nDone! SQL file generated: {output_path}")

    finally:
        helper.close()


if __name__ == "__main__":
    main()
