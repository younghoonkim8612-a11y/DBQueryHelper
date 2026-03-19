"""
AI DB Query Helper — Claude Agent SDK 버전 (Claude Max 구독 사용)

실행:
    PYTHONIOENCODING=utf-8 ./venv/Scripts/python.exe agent_main.py

Claude Code 로그인 상태여야 합니다 (claude 명령어가 동작해야 함).
"""
import os
import sys
import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage, AssistantMessage, TextBlock
from history_manager import HistoryManager
import connection_store

# Claude Agent SDK는 ANTHROPIC_API_KEY가 있으면 API 크레딧을 사용하려 함.
# Max 구독(OAuth)을 사용하려면 환경에서 제거해야 함.
os.environ.pop("ANTHROPIC_API_KEY", None)

from pathlib import Path

SEPARATOR = "─" * 60
CWD = str(Path(__file__).parent)
PYTHON = str(Path(__file__).parent / "venv" / "Scripts" / "python.exe")


def pick_connection() -> str:
    connections = connection_store.list_connections()
    if not connections:
        print("[ERROR] 등록된 연결이 없습니다. 연결 관리 페이지에서 추가하세요.")
        sys.exit(1)

    print("\n사용 가능한 연결:")
    for i, name in enumerate(connections, 1):
        print(f"  {i}. {name}")

    while True:
        raw = input("\n연결 선택 (번호 또는 이름): ").strip()
        if raw.isdigit() and 0 < int(raw) <= len(connections):
            return connections[int(raw) - 1]
        elif raw in connections:
            return raw
        print("잘못된 선택입니다. 다시 입력하세요.")


def get_history_examples(connection_name: str, limit: int = 10) -> str:
    """Return recent successful queries for the given connection as few-shot examples."""
    history = HistoryManager().load_history()
    entries = [
        e for e in history
        if e.get("success") and e.get("connection_name") == connection_name
    ][-limit:]

    if not entries:
        return ""

    lines = ["## Past Successful Queries (use as reference for style and table names)"]
    for e in entries:
        req = e.get("user_request", "")
        prefix = f"-- Request: {req}\n" if req else ""
        lines.append(f"{prefix}-- [{e['timestamp'][:10]}]\n{e['query']}")
    return "\n\n".join(lines)


async def ask(connection_name: str, user_request: str):
    history_section = get_history_examples(connection_name)
    history_block = f"\n\n{history_section}" if history_section else ""

    conn_info = connection_store.get_connection(connection_name)
    port = int(conn_info["port"]) if conn_info else 5432

    if port == 6432:
        schema_file = f"{CWD}/ddw_public_schema_reference.md"
        db_type = "Timescale"
        schema_instruction = """- Always prefix tables with `public.` schema (or omit schema prefix since public is default)
   - This is a Timescale DB for time-series data."""
    else:
        schema_file = f"{CWD}/schema_reference.md"
        db_type = "GIS"
        schema_instruction = """- Always prefix tables with `gisdb.` schema
   - All geometry columns use WGS84 (SRID=4326). For display use ST_AsText(geom)."""

    prompt = f"""You are a PostgreSQL expert for a {db_type} database.

The user is connected to: "{connection_name}" (port {port})
{history_block}

User request: {user_request}

Instructions:
1. Read the schema from: {schema_file}
2. Generate a valid PostgreSQL SQL query for the request.
   {schema_instruction}
   - For inner joins, use implicit join syntax: `SELECT ... FROM table_a a, table_b b WHERE a.id = b.id` — do NOT use INNER JOIN keyword. LEFT JOIN and RIGHT JOIN are fine as-is.
   - Do NOT add LIMIT to the query unless the user explicitly asks for it.
   - Use WITH (CTE) instead of subqueries.
3. Execute the query using this exact command:
   {PYTHON} {CWD}/execute_sql.py "{connection_name}" "<your SQL here>"
4. Show the results to the user in this format:
   - First, print the generated SQL query
   - Then print at most 10 rows of query results. If more rows exist, note the total count.
   - Finally, briefly explain what was returned."""

    print(f"\n[Agent] 처리 중...\n{SEPARATOR}")

    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            model="sonnet",
            cwd=CWD,
            allowed_tools=["Read", "Bash"],
            max_turns=5,
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, flush=True)
        elif isinstance(message, ResultMessage):
            # ResultMessage는 AssistantMessage와 내용이 겹치므로 생략
            pass


async def main():
    print(SEPARATOR)
    print("  DB Query Helper — Claude Agent (Max 구독)")
    print(SEPARATOR)

    connection_name = pick_connection()
    print(f"\n[연결됨] {connection_name}")
    print("자연어로 질문하세요. 종료: :quit\n")

    while True:
        try:
            user_input = input(f"[{connection_name}]> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n종료합니다.")
            break

        if not user_input:
            continue
        if user_input.lower() in (":quit", ":exit"):
            print("종료합니다.")
            break

        print(SEPARATOR)
        await ask(connection_name, user_input)
        print(SEPARATOR + "\n")


if __name__ == "__main__":
    anyio.run(main)
