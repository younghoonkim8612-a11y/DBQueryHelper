"""
CLI helper for the Claude Agent to execute SQL queries.

Usage:
    python execute_sql.py "<connection_name>" "<sql>"

Prints results as a formatted table to stdout.
Exits with code 1 on error.
Does NOT save to query history (app.py handles that with user_request).
"""
import sys
import urllib.parse
import psycopg2
import pandas as pd
import sqlalchemy
from sqlalchemy import text
from tabulate import tabulate
from connection_store import get_connection


def main():
    if len(sys.argv) < 3:
        print("Usage: python execute_sql.py <connection_name> <sql>")
        sys.exit(1)

    connection_name = sys.argv[1]
    sql = sys.argv[2]

    info = get_connection(connection_name)
    if not info:
        print(f"[ERROR] Connection '{connection_name}' not found.")
        sys.exit(1)

    try:
        first_word = sql.strip().split()[0].upper()

        if first_word in ("INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER"):
            conn = psycopg2.connect(
                host=info["host"], port=info["port"],
                dbname=info["database"], user=info["user"],
                password=info["password"],
            )
            with conn.cursor() as cur:
                cur.execute(sql)
                conn.commit()
                rowcount = cur.rowcount
            conn.close()
            print(f"Success — {rowcount} row(s) affected.")
        else:
            encoded_pw = urllib.parse.quote_plus(info["password"])
            db_url = f"postgresql://{info['user']}:{encoded_pw}@{info['host']}:{info['port']}/{info['database']}"
            engine = sqlalchemy.create_engine(db_url)
            with engine.connect() as conn:
                df = pd.read_sql_query(text(sql), conn)
            engine.dispose()
            if df.empty:
                print("(no rows returned)")
            else:
                total = len(df)
                display = df.head(10).copy()
                for col in display.select_dtypes(include="object").columns:
                    display[col] = display[col].astype(str).str[:80]
                print(tabulate(display, headers="keys", tablefmt="psql", showindex=False))
                if total > 10:
                    print(f"\n(showing 10 of {total} rows)")
                else:
                    print(f"\n{total} row(s)")
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
