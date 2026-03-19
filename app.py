"""
DB Query Helper — Streamlit UI

실행:
    PYTHONIOENCODING=utf-8 ./venv/Scripts/python.exe -m streamlit run app.py
"""
import os
import re
import asyncio
import threading
from pathlib import Path
import pandas as pd
import streamlit as st

from db_helper import QueryHelper
from history_manager import HistoryManager
from claude_agent_sdk import query as agent_query, ClaudeAgentOptions, AssistantMessage, TextBlock
from sqlalchemy import text
import connection_store

os.environ.pop("ANTHROPIC_API_KEY", None)

CWD = str(Path(__file__).parent)
ERROR_FEEDBACK_FILE = Path(CWD) / "error_feedback.json"
PYTHON = str(Path(__file__).parent / "venv" / "Scripts" / "python.exe")

EXAMPLE_QUESTIONS = [
    "터미널별 에이프런 수 알려줘",
    "bay_map 테이블 구조 보여줘",
    "최근 수정된 데이터 10건 보여줘",
    "gisdb 스키마의 테이블 목록 보여줘",
]

# ── 페이지 설정 ───────────────────────────────────────────────
st.set_page_config(
    page_title="DB Query Helper",
    page_icon="🗄️",
    layout="wide",
)

# ── 연결 목록 ──────────────────────────────────────────────────
def get_all_connections() -> list[str]:
    return connection_store.list_connections()

@st.cache_resource
def get_query_helper(connection_name: str) -> QueryHelper:
    return QueryHelper(connection_name)

@st.cache_data(ttl=60)
def check_connection(connection_name: str) -> bool:
    ok, _ = connection_store.test_connection(connection_name)
    return ok

# ── 에러 피드백 ────────────────────────────────────────────────
def save_error_feedback(sql: str, error: str, connection_name: str):
    """쿼리 실행 실패 시 에러를 기록하여 다음 생성에 참조한다."""
    import json
    feedbacks = []
    if ERROR_FEEDBACK_FILE.exists():
        try:
            feedbacks = json.loads(ERROR_FEEDBACK_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            feedbacks = []

    # 에러 메시지에서 핵심만 추출 (첫 줄)
    error_summary = error.strip().split("\n")[0][:200]

    feedbacks.append({
        "sql": sql.strip()[:500],
        "error": error_summary,
        "connection": connection_name,
        "timestamp": __import__("datetime").datetime.now().isoformat()[:10],
    })

    # 최근 20건만 유지
    feedbacks = feedbacks[-20:]
    ERROR_FEEDBACK_FILE.write_text(
        json.dumps(feedbacks, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def load_error_feedback(connection_name: str, limit: int = 5) -> list[dict]:
    """최근 에러 피드백을 로드한다."""
    import json
    if not ERROR_FEEDBACK_FILE.exists():
        return []
    try:
        feedbacks = json.loads(ERROR_FEEDBACK_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        return []
    # 해당 연결의 에러만 최근 N건
    return [f for f in feedbacks if f.get("connection") == connection_name][-limit:]


# ── 이력 ──────────────────────────────────────────────────────
def get_history(connection_name: str, limit: int = 15):
    history = HistoryManager().load_history()
    return [
        e for e in history
        if e.get("success") and e.get("connection_name") == connection_name
    ][-limit:]

# ── 포트 기반 스키마 감지 ──────────────────────────────────────
def _get_port(connection_name: str) -> int:
    info = connection_store.get_connection(connection_name)
    return int(info.get("port", 5432)) if info else 5432


def _get_db_type(connection_name: str) -> str:
    """포트 기반으로 DB 유형을 반환한다."""
    port = _get_port(connection_name)
    return "timescale" if port == 6432 else "gis"


def _get_schemas_from_file(connection_name: str) -> list[str]:
    """DB 유형별 스키마 파일에서 스키마 목록을 반환한다."""
    db_type = _get_db_type(connection_name)
    type_dir = Path(CWD) / "schemas" / db_type
    if not type_dir.exists():
        return []
    return sorted(p.stem[len("schema_"):] for p in type_dir.glob("schema_*.md"))

# ── 스키마 조회 다이얼로그 ────────────────────────────────────
@st.dialog("📋 스키마 조회", width="large")
def show_schema_dialog(connection_name: str):
    from schema_generator import list_schemas, generate_schema_md, schema_file_path
    from datetime import datetime

    existing_schemas = _get_schemas_from_file(connection_name)

    with st.expander("🔄 스키마 업데이트", expanded=not existing_schemas):
        try:
            available = list_schemas(connection_name)
        except Exception as e:
            st.error(f"스키마 목록 조회 실패: {e}")
            return

        update_schemas = st.multiselect("업데이트할 스키마", available, default=available)
        do_jsonb = st.checkbox("JSONB 컬럼 내부 구조 프로파일링", value=False,
                               help="JSONB 컬럼의 키 구조를 샘플링합니다. 대용량 테이블이 있으면 시간이 걸릴 수 있습니다.")
        if st.button("업데이트 실행", disabled=not update_schemas):
            with st.spinner("DB에서 스키마 읽는 중..."):
                try:
                    generate_schema_md(connection_name, update_schemas, profile_jsonb=do_jsonb)
                    _load_schema.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"업데이트 실패: {e}")

    if not existing_schemas:
        st.warning("스키마 파일이 없습니다. 위에서 업데이트를 실행하세요.")
        return

    view_schema = st.selectbox("스키마", existing_schemas)
    schema_file = schema_file_path(connection_name, view_schema)

    mtime = schema_file.stat().st_mtime
    st.caption(f"마지막 업데이트: {datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')}")

    content = schema_file.read_text(encoding="utf-8")
    tables = [line[4:] for line in content.splitlines() if line.startswith("### ")]

    selected_table = st.selectbox("테이블", ["전체"] + tables)

    if selected_table == "전체":
        st.markdown(content)
    else:
        lines = content.splitlines()
        start = None
        section = []
        for i, line in enumerate(lines):
            if line == f"### {selected_table}":
                start = i
            elif start is not None and line.startswith("### ") and i != start:
                break
            if start is not None:
                section.append(line)
        st.markdown("\n".join(section))


# ── 프롬프트 생성 (SQL만 생성, 실행하지 않음) ─────────────────
@st.cache_resource
def _load_schema(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def build_prompt(connection_name: str, user_request: str, selected_schemas: list[str] | None = None) -> str:
    history = get_history(connection_name)
    history_block = ""
    if history:
        lines = ["## Past Successful Queries (reference for style and table names)"]
        for e in history:
            req = e.get("user_request", "")
            prefix = f"-- Request: {req}\n" if req else ""
            lines.append(f"{prefix}-- [{e['timestamp'][:10]}]\n{e['query']}")
        history_block = "\n\n" + "\n\n".join(lines)

    # 현재 세션 대화 이력 (최근 10개)
    conv_block = ""
    msgs = st.session_state.get("messages", [])
    recent = msgs[-10:]
    if recent:
        conv_lines = ["## Current Conversation"]
        for m in recent:
            role = "User" if m["role"] == "user" else "Assistant"
            conv_lines.append(f"**{role}:** {m['content'][:500]}")
            if m.get("sql"):
                conv_lines.append(f"```sql\n{m['sql']}\n```")
        conv_block = "\n\n" + "\n".join(conv_lines)

    # 에러 피드백 (과거 실패에서 학습)
    error_feedbacks = load_error_feedback(connection_name)
    error_block = ""
    if error_feedbacks:
        err_lines = ["## Recent Query Errors (AVOID these mistakes)"]
        for ef in error_feedbacks:
            err_lines.append(f"- SQL: `{ef['sql'][:150]}...`\n  Error: {ef['error']}")
        error_block = "\n\n" + "\n".join(err_lines)

    port = _get_port(connection_name)
    db_type = "Timescale" if port == 6432 else "GIS"
    geo_instruction = "   - All geometry columns use WGS84 (SRID=4326). For display use ST_AsText(geom)." if port != 6432 else ""

    from schema_generator import schema_file_path
    if selected_schemas:
        parts = []
        for s in selected_schemas:
            f = schema_file_path(connection_name, s)
            try:
                parts.append(_load_schema(str(f)))
            except FileNotFoundError:
                parts.append(f"(스키마 '{s}' 파일 없음 — 📋 스키마 조회에서 업데이트하세요.)")
        schema_content = "\n\n".join(parts)
    else:
        schema_content = "(대상 스키마가 선택되지 않았습니다.)"

    return f"""You are a PostgreSQL expert for a {db_type} database.

The user is connected to: "{connection_name}" (port {port})
{history_block}
{error_block}
{conv_block}

## Database Schema
{schema_content}

User request: {user_request}

Instructions:
1. Generate a valid PostgreSQL SQL query for the request using the schema above.
   - Always use the fully qualified `schema.table` name as shown in the schema reference above. Always double-quote the schema name to preserve case: `"schema".table`.
   - Target schemas: {', '.join(selected_schemas) if selected_schemas else 'all schemas in the reference above'}.
   - If the same table name exists in multiple target schemas and it is unclear which one to use, ask the user to clarify before generating the query.
{geo_instruction}
   - CRITICAL: Only use column names that EXACTLY match the schema reference above. NEVER invent, guess, or assume column names like 'time', 'rcvdt', 'timestamp', 'id', etc. The ONLY columns that exist are the ones listed in the schema tables. For time-based filtering, check the schema for the actual timestamp column name (e.g., 'utct', 'create_time'). If unsure, ask the user.
   - For inner joins, use implicit join syntax: `SELECT ... FROM table_a a, table_b b WHERE a.id = b.id` — do NOT use INNER JOIN keyword. LEFT JOIN and RIGHT JOIN are fine as-is.
   - Do NOT add LIMIT to the query unless the user explicitly asks for it.
   - Use WITH (CTE) instead of subqueries.
   - For large time-series tables (msg_periodic_rtls, msg_tiot_event, msg_event_history, etc.), ALWAYS include a date range filter (e.g., utct >= ... AND utct < ...) in the WHERE clause. If the user does not specify a date range or equipment filter, ASK before generating the query — querying without filters will crash the DB server.
   - For GIS tables with geometry columns, avoid heavy PostGIS computations (ST_Azimuth, ST_ExteriorRing, ST_Buffer, etc.) on ALL rows without a WHERE filter. Use LIMIT or a tml_id/bk_id filter to restrict the scope. Heavy geometry functions on large datasets will crash the DB server.
2. Respond with:
   - A brief one-line explanation of what the query does
   - The SQL query inside a ```sql code block
   Do NOT execute the query."""

# ── 에이전트 실행 (SQL 생성만) ─────────────────────────────────
async def _run_agent_async(prompt: str) -> str:
    collected = []
    async for message in agent_query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            model="sonnet",
            cwd=CWD,
            max_turns=1,
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    collected.append(block.text)
    return "\n".join(collected)


def run_agent(prompt: str) -> str:
    result = [None]
    error = [None]

    def _thread():
        if hasattr(asyncio, "WindowsProactorEventLoopPolicy"):
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result[0] = loop.run_until_complete(_run_agent_async(prompt))
        except Exception as e:
            error[0] = e
        finally:
            loop.close()

    t = threading.Thread(target=_thread)
    t.start()
    t.join()

    if error[0]:
        raise error[0]
    return result[0]

# ── 쿼리 실행 ─────────────────────────────────────────────────
def _get_sql_type(sql: str) -> str:
    """주석을 건너뛰고 실제 SQL 키워드를 반환한다."""
    for line in sql.strip().splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("--"):
            return stripped.split()[0].upper()
    return ""


_DANGEROUS_SQL = {"DROP", "TRUNCATE", "ALTER"}

def execute_sql_preview(connection_name: str, sql: str, limit: int = 10):
    """SQL에 LIMIT를 붙여 미리보기용 결과만 가져온다. 이력 저장 안 함."""
    try:
        first_word = _get_sql_type(sql)

        # 파괴적 DDL 차단
        if first_word in _DANGEROUS_SQL:
            return None, f"⚠️ {first_word} 문은 안전을 위해 실행이 차단됩니다. DBeaver에서 직접 실행하세요."

        if first_word in ("INSERT", "UPDATE", "DELETE", "CREATE"):
            helper = get_query_helper(connection_name)
            rowcount = helper.execute_update(sql)
            if rowcount is None:
                return None, "실행 실패 (로그 확인)"
            return None, f"{rowcount}행 영향받음"

        # SELECT/WITH — 세미콜론 및 복수 쿼리 방지
        clean_sql = sql.rstrip().rstrip(";")
        if ";" in clean_sql:
            return None, "⚠️ 복수 쿼리(;)는 지원되지 않습니다. 쿼리를 하나씩 실행하세요."
        limited_sql = f"SELECT * FROM ({clean_sql}) _preview LIMIT {limit}"
        with get_query_helper(connection_name)._get_engine().connect() as conn:
            df = pd.read_sql_query(text(limited_sql), conn)
        return df, None
    except Exception as e:
        return None, str(e)

# ── 결과 렌더링 ───────────────────────────────────────────────
def render_result(msg: dict, msg_idx: int, connection_name: str):
    """메시지의 SQL 실행 결과를 렌더링한다."""
    sql = msg.get("sql")
    if not sql:
        return

    first_word = _get_sql_type(sql)

    if not msg.get("executed"):
        if st.button("▶ 실행", key=f"exec_{msg_idx}", type="primary"):
            st.session_state.pending_execute = msg_idx
            st.rerun()
        return

    # 실행 완료 → 결과 표시
    if msg.get("exec_error"):
        st.error(msg["exec_error"])
        return

    if first_word in ("SELECT", "WITH"):
        df = msg.get("df")
        if df is not None and not df.empty:
            st.data_editor(df, use_container_width=True, disabled=True, key=f"df_{msg_idx}")
            col1, col2 = st.columns([1, 5])
            with col1:
                csv_data = df.to_csv(index=False).encode("utf-8-sig")
                st.download_button(
                    "📥 CSV 다운로드",
                    data=csv_data,
                    file_name="query_result.csv",
                    mime="text/csv",
                    key=f"dl_{msg_idx}",
                )
            with col2:
                st.caption("미리보기 (최대 10행)")
        else:
            st.info("결과가 없습니다.")
    else:
        st.success(msg.get("exec_msg", "실행 완료"))

# ── 사용자 입력 처리 ──────────────────────────────────────────
def process_user_input(user_input: str, connection_name: str, selected_schemas: list[str] | None = None):
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.status("SQL 생성 중...", expanded=True) as status:
            prompt = build_prompt(connection_name, user_input, selected_schemas)
            response_text = run_agent(prompt)
            status.update(label="SQL 생성 완료", state="complete")

        st.markdown(response_text)

        sql_match = re.search(r"```sql\s*([\s\S]+?)```", response_text, re.IGNORECASE)
        extracted_sql = sql_match.group(1).strip() if sql_match else None

        msg_idx = len(st.session_state.messages)
        if extracted_sql:
            render_result({"sql": extracted_sql, "executed": False}, msg_idx, connection_name)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text,
        "sql": extracted_sql,
        "executed": False,
        "df": None,
        "exec_error": None,
        "exec_msg": None,
    })

# ── 실행 버튼 처리 ────────────────────────────────────────────
def handle_pending_execute(connection_name: str):
    """pending_execute 인덱스의 SQL을 실행하고 메시지를 업데이트한다."""
    idx = st.session_state.pop("pending_execute")
    if idx >= len(st.session_state.get("messages", [])):
        return
    msg = st.session_state.messages[idx]
    sql = msg["sql"]
    first_word = _get_sql_type(sql)

    with st.spinner("실행 중..."):
        df, err_or_msg = execute_sql_preview(connection_name, sql)

    if first_word in ("SELECT", "WITH"):
        if err_or_msg:
            msg["exec_error"] = err_or_msg
        else:
            msg["df"] = df
    else:
        # DML: df is None on success, err_or_msg contains "N행 영향받음" or error
        if err_or_msg and not err_or_msg.startswith("⚠️") and "행 영향받음" not in str(err_or_msg):
            msg["exec_error"] = err_or_msg
        else:
            msg["exec_msg"] = err_or_msg or "실행 완료"

    msg["executed"] = True

    # 에러 피드백 자동 기록
    if msg.get("exec_error"):
        save_error_feedback(sql, msg["exec_error"], connection_name)

    # 이력 저장
    if not msg.get("exec_error"):
        user_msg = next(
            (m["content"] for m in reversed(st.session_state.messages[:idx]) if m["role"] == "user"),
            None
        )
        HistoryManager().save_query(sql, connection_name, success=True, user_request=user_msg)

# ── 사이드바 ──────────────────────────────────────────────────
connections = get_all_connections()

with st.sidebar:
    st.title("🗄️ DB Query Helper")
    st.caption("Claude Sonnet (Max 구독)")

    connection_name = st.selectbox(
        "데이터베이스 연결", connections, index=None, placeholder="연결을 선택하세요...",
    )

    if connection_name:
        if check_connection(connection_name):
            st.success("🟢 연결됨", icon="✅")
        else:
            st.error("🔴 연결 실패", icon="❌")

        available_schemas = _get_schemas_from_file(connection_name)
        if not available_schemas:
            try:
                from schema_generator import list_schemas
                available_schemas = list_schemas(connection_name)
            except Exception:
                available_schemas = []
        if available_schemas:
            selected_schemas = st.multiselect(
                "대상 스키마", available_schemas, default=available_schemas,
                placeholder="스키마를 선택하세요..."
            )
        else:
            selected_schemas = []
            st.caption("스키마 목록을 불러올 수 없습니다.")
    else:
        selected_schemas = []

    if st.button("🗑️ 대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.button("📋 스키마 조회", use_container_width=True):
        if connection_name:
            show_schema_dialog(connection_name)
        else:
            st.warning("연결을 먼저 선택하세요.")

    st.divider()
    st.subheader("최근 쿼리 이력")
    history_entries = get_history(connection_name, limit=10) if connection_name else []
    if history_entries:
        for idx, e in enumerate(reversed(history_entries)):
            label = e.get("user_request", e["timestamp"][5:16])
            with st.expander(f"📋 {label[:40]}", expanded=False):
                if e.get("user_request"):
                    st.caption(f"💬 {e['user_request']}")
                st.code(e["query"], language="sql")
                if st.button("▶ 재실행", key=f"rerun_{idx}", use_container_width=True):
                    st.session_state.pending_input = e.get("user_request", e["query"])
                    st.rerun()
    else:
        st.caption("아직 실행한 쿼리가 없습니다.")

# ── 메인 영역 ─────────────────────────────────────────────────
if not connection_name:
    st.info("👈 사이드바에서 데이터베이스 연결을 선택하세요.")
    st.stop()

st.header(f"💬 {connection_name}")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_connection" not in st.session_state:
    st.session_state.last_connection = connection_name

if st.session_state.last_connection != connection_name:
    st.session_state.messages = []
    st.session_state.last_connection = connection_name

# 실행 버튼 클릭 처리 (렌더링 전에)
if "pending_execute" in st.session_state:
    handle_pending_execute(connection_name)
    st.rerun()

# 이전 채팅 표시
for msg_idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            st.markdown(msg["content"])
            if msg.get("sql"):
                render_result(msg, msg_idx, connection_name)
        else:
            st.write(msg["content"])

# 빈 상태: 예시 질문 버튼 표시
if not st.session_state.messages:
    st.markdown("#### 💡 예시 질문으로 시작해보세요")
    cols = st.columns(2)
    for i, question in enumerate(EXAMPLE_QUESTIONS):
        with cols[i % 2]:
            if st.button(question, key=f"example_{i}", use_container_width=True):
                st.session_state.pending_input = question
                st.rerun()

if "pending_input" in st.session_state:
    pending = st.session_state.pop("pending_input")
    process_user_input(pending, connection_name, selected_schemas)
    st.rerun()

if user_input := st.chat_input("자연어로 질문하세요 (예: 터미널별 에이프런 수 알려줘)"):
    process_user_input(user_input, connection_name, selected_schemas)
    st.rerun()
