"""
Live DB에서 스키마 정보를 조회하여 schema reference md 파일을 생성한다.
"""
import re
import urllib.parse
from datetime import datetime
from pathlib import Path

import pandas as pd
import sqlalchemy
from sqlalchemy import text

import connection_store

# 날짜 파티션 테이블 패턴 (예: msg_periodic_rtls_20240821)
_PARTITION_RE = re.compile(r"^(.+)_\d{6,}$")

CWD = Path(__file__).parent
SCHEMA_DIR = CWD / "schemas"
SCHEMA_DIR.mkdir(exist_ok=True)


def _get_engine(info: dict) -> sqlalchemy.Engine:
    encoded_pw = urllib.parse.quote_plus(info["password"])
    url = (
        f"postgresql://{info['user']}:{encoded_pw}"
        f"@{info['host']}:{info['port']}/{info['database']}"
    )
    return sqlalchemy.create_engine(url, connect_args={"connect_timeout": 10})


def _query(conn, sql: str) -> pd.DataFrame:
    return pd.read_sql_query(text(sql), conn)


def list_schemas(connection_name: str) -> list[str]:
    """DB에서 사용자 스키마 목록을 반환한다."""
    info = connection_store.get_connection(connection_name)
    if not info:
        raise ValueError(f"Connection '{connection_name}' not found.")

    engine = _get_engine(info)
    try:
        with engine.connect() as conn:
            return _query(conn, """
                SELECT nspname AS schema_name
                FROM pg_namespace
                WHERE nspname NOT IN ('information_schema', 'pg_catalog', 'pg_toast')
                AND nspname NOT LIKE 'pg_%'
                ORDER BY nspname
            """)["schema_name"].tolist()
    finally:
        engine.dispose()


def _get_db_type(connection_name: str) -> str:
    """포트 기반으로 DB 유형을 반환한다."""
    info = connection_store.get_connection(connection_name)
    port = int(info.get("port", 5432)) if info else 5432
    return "timescale" if port == 6432 else "gis"


def schema_file_path(connection_name: str, schema: str) -> Path:
    db_type = _get_db_type(connection_name)
    type_dir = SCHEMA_DIR / db_type
    type_dir.mkdir(exist_ok=True)
    return type_dir / f"schema_{schema}.md"


def _is_partition_table(table: str, all_tables: set) -> bool:
    """날짜 파티션 테이블인지 판별한다 (부모 테이블이 존재하면 스킵)."""
    m = _PARTITION_RE.match(table)
    if not m:
        return False
    return m.group(1) in all_tables


def _profile_jsonb(conn, schema: str, table: str, jsonb_col: str) -> list[str]:
    """JSONB 컬럼의 내부 키 구조를 샘플링하여 문서화한다 (쿼리당 3초 제한)."""
    lines = []

    conn.execute(text("SET LOCAL statement_timeout = '3s'"))

    # 분류 컬럼 후보 확인 (pg_catalog 사용)
    classify_cols = _query(conn, f"""
        SELECT a.attname AS column_name
        FROM pg_attribute a
        JOIN pg_class c ON c.oid = a.attrelid
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = '{schema}' AND c.relname = '{table}'
        AND a.attname IN ('type', 'eqty', 'topic')
        AND a.attnum > 0 AND NOT a.attisdropped
        ORDER BY a.attname
    """)["column_name"].tolist()

    if classify_cols:
        group_col = classify_cols[0]
        try:
            samples = _query(conn, f"""
                WITH sample AS (
                    SELECT "{group_col}", "{jsonb_col}"
                    FROM "{schema}"."{table}" TABLESAMPLE SYSTEM (1)
                    WHERE "{group_col}" IS NOT NULL AND "{jsonb_col}" IS NOT NULL
                    LIMIT 100
                )
                SELECT DISTINCT ON ("{group_col}") "{group_col}", "{jsonb_col}"
                FROM sample
                ORDER BY "{group_col}"
                LIMIT 10
            """)
        except Exception:
            try:
                samples = _query(conn, f"""
                    WITH recent AS (
                        SELECT "{group_col}", "{jsonb_col}"
                        FROM "{schema}"."{table}"
                        WHERE "{group_col}" IS NOT NULL AND "{jsonb_col}" IS NOT NULL
                        ORDER BY ctid DESC
                        LIMIT 100
                    )
                    SELECT DISTINCT ON ("{group_col}") "{group_col}", "{jsonb_col}"
                    FROM recent
                    ORDER BY "{group_col}"
                    LIMIT 10
                """)
            except Exception:
                conn.execute(text("SET LOCAL statement_timeout = '0'"))
                return lines

        for _, row in samples.iterrows():
            data = row[jsonb_col]
            if not isinstance(data, dict):
                continue
            keys_info = _extract_keys(data)
            lines.append(f"\n**{jsonb_col}** ({group_col}=`{row[group_col]}`):")
            lines.append("```")
            for k, v in keys_info.items():
                lines.append(f"  {k}: {v}")
            lines.append("```")
    else:
        try:
            sample = _query(conn, f"""
                SELECT "{jsonb_col}"
                FROM "{schema}"."{table}" TABLESAMPLE SYSTEM (1)
                WHERE "{jsonb_col}" IS NOT NULL
                LIMIT 1
            """)
            if sample.empty:
                sample = _query(conn, f"""
                    SELECT "{jsonb_col}"
                    FROM "{schema}"."{table}"
                    WHERE "{jsonb_col}" IS NOT NULL
                    ORDER BY ctid DESC
                    LIMIT 1
                """)
        except Exception:
            conn.execute(text("SET LOCAL statement_timeout = '0'"))
            return lines

        if not sample.empty:
            data = sample.iloc[0][jsonb_col]
            if isinstance(data, dict):
                keys_info = _extract_keys(data)
                lines.append(f"\n**{jsonb_col} 구조:**")
                lines.append("```")
                for k, v in keys_info.items():
                    lines.append(f"  {k}: {v}")
                lines.append("```")

    conn.execute(text("SET LOCAL statement_timeout = '0'"))
    return lines


def _extract_keys(data: dict, prefix: str = "") -> dict:
    """JSONB dict에서 키-타입 매핑을 재귀적으로 추출한다."""
    result = {}
    for k, v in data.items():
        full_key = f"{prefix}{k}"
        if isinstance(v, dict):
            result[full_key] = "{...}"
            sub = _extract_keys(v, prefix=f"{full_key}.")
            result.update(sub)
        elif isinstance(v, list):
            result[full_key] = f"[array, len={len(v)}]"
            if v and isinstance(v[0], dict):
                sub = _extract_keys(v[0], prefix=f"{full_key}[].")
                result.update(sub)
        elif isinstance(v, bool):
            result[full_key] = f"boolean (예: {v})"
        elif isinstance(v, int):
            result[full_key] = f"integer (예: {v})"
        elif isinstance(v, float):
            result[full_key] = f"number (예: {v})"
        elif v is None:
            result[full_key] = "null"
        else:
            val_str = str(v)[:50]
            result[full_key] = f'string (예: "{val_str}")'
    return result


def generate_schema_md(connection_name: str, schemas: list[str],
                       profile_jsonb: bool = False) -> list[str]:
    """
    지정된 스키마별로 개별 파일을 생성한다.
    pg_catalog 기반으로 한 번에 조회하여 성능 최적화.
    profile_jsonb=True이면 JSONB 컬럼 내부 구조도 샘플링한다 (느릴 수 있음).
    """
    info = connection_store.get_connection(connection_name)
    if not info:
        raise ValueError(f"Connection '{connection_name}' not found.")

    engine = _get_engine(info)
    output_files = []
    try:
        with engine.connect() as conn:
            for schema in schemas:
                lines = [
                    f"# Schema: {schema} — {connection_name}",
                    f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    "",
                ]

                # 1) 테이블 목록 (pg_catalog - 빠름)
                tables = _query(conn, f"""
                    SELECT c.relname AS table_name
                    FROM pg_class c
                    JOIN pg_namespace n ON n.oid = c.relnamespace
                    WHERE n.nspname = '{schema}'
                    AND c.relkind = 'r'
                    ORDER BY c.relname
                """)["table_name"].tolist()

                all_tables_set = set(tables)
                base_tables = [t for t in tables if not _is_partition_table(t, all_tables_set)]

                if not base_tables:
                    lines.append("_(테이블 없음)_")
                else:
                    skipped = len(tables) - len(base_tables)
                    if skipped:
                        lines.append(f"_({skipped}개 날짜 파티션 테이블 생략)_\n")

                    # 2) 모든 컬럼 정보를 한 번에 조회
                    all_cols = _query(conn, f"""
                        SELECT c.relname AS table_name,
                               a.attname AS column_name,
                               pg_catalog.format_type(a.atttypid, a.atttypmod) AS data_type,
                               CASE WHEN a.attnotnull THEN 'NO' ELSE 'YES' END AS is_nullable,
                               a.attnum
                        FROM pg_attribute a
                        JOIN pg_class c ON c.oid = a.attrelid
                        JOIN pg_namespace n ON n.oid = c.relnamespace
                        WHERE n.nspname = '{schema}'
                        AND c.relkind = 'r'
                        AND a.attnum > 0
                        AND NOT a.attisdropped
                        ORDER BY c.relname, a.attnum
                    """)

                    # 3) 모든 PK를 한 번에 조회
                    all_pks = _query(conn, f"""
                        SELECT c.relname AS table_name, a.attname AS column_name
                        FROM pg_index i
                        JOIN pg_class c ON c.oid = i.indrelid
                        JOIN pg_namespace n ON n.oid = c.relnamespace
                        JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum = ANY(i.indkey)
                        WHERE n.nspname = '{schema}'
                        AND i.indisprimary
                        ORDER BY c.relname, a.attnum
                    """)

                    # 4) 모든 FK를 한 번에 조회
                    all_fks = _query(conn, f"""
                        SELECT DISTINCT
                            c.relname AS table_name,
                            a.attname AS column_name,
                            cf.relname AS foreign_table,
                            af.attname AS foreign_column
                        FROM pg_constraint con
                        JOIN pg_class c ON c.oid = con.conrelid
                        JOIN pg_namespace n ON n.oid = c.relnamespace
                        JOIN pg_class cf ON cf.oid = con.confrelid
                        JOIN pg_attribute a ON a.attrelid = con.conrelid
                            AND a.attnum = ANY(con.conkey)
                        JOIN pg_attribute af ON af.attrelid = con.confrelid
                            AND af.attnum = ANY(con.confkey)
                        WHERE n.nspname = '{schema}'
                        AND con.contype = 'f'
                        ORDER BY c.relname, a.attname
                    """)

                    for table in base_tables:
                        lines.append(f"### {schema}.{table}")

                        # 컬럼
                        cols = all_cols[all_cols["table_name"] == table]
                        lines.append("| Column | Type | Nullable |")
                        lines.append("|--------|------|----------|")
                        for _, row in cols.iterrows():
                            lines.append(f"| {row['column_name']} | {row['data_type']} | {row['is_nullable']} |")

                        # JSONB 프로파일링 (선택적)
                        if profile_jsonb:
                            jsonb_cols = cols[cols["data_type"] == "jsonb"]["column_name"].tolist()
                            for jcol in jsonb_cols:
                                try:
                                    jsonb_lines = _profile_jsonb(conn, schema, table, jcol)
                                    lines.extend(jsonb_lines)
                                except Exception:
                                    pass

                        # PK
                        pks = all_pks[all_pks["table_name"] == table]
                        if not pks.empty:
                            lines.append(f"\n**Primary Key:** {', '.join(pks['column_name'].tolist())}")

                        # FK
                        fks = all_fks[all_fks["table_name"] == table]
                        if not fks.empty:
                            lines.append("\n**Foreign Keys:**")
                            for _, row in fks.iterrows():
                                lines.append(f"- {row['column_name']} → {schema}.{row['foreign_table']}({row['foreign_column']})")

                        lines.append("")

                out = schema_file_path(connection_name, schema)
                out.write_text("\n".join(lines), encoding="utf-8")
                output_files.append(str(out))
    finally:
        engine.dispose()

    return output_files
