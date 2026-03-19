"""
DB 연결 정보를 JSON 파일로 관리한다.
DBeaver 의존 없이 독립적으로 연결을 추가/수정/삭제할 수 있다.
"""
import json
import os
from pathlib import Path

STORE_FILE = Path(__file__).parent / "connections.json"


def _load() -> dict:
    if STORE_FILE.exists():
        with open(STORE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save(data: dict):
    with open(STORE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def list_connections() -> list[str]:
    return sorted(_load().keys(), key=str.lower)


def get_connection(name: str) -> dict | None:
    return _load().get(name)


def save_connection(name: str, host: str, port: int, database: str, user: str, password: str):
    """연결 정보를 저장한다. 같은 이름이면 덮어쓴다."""
    data = _load()
    data[name] = {
        "host": host,
        "port": port,
        "database": database,
        "user": user,
        "password": password,
    }
    _save(data)


def delete_connection(name: str) -> bool:
    data = _load()
    if name in data:
        del data[name]
        _save(data)
        return True
    return False


def test_connection(name: str) -> tuple[bool, str]:
    """연결 테스트. (성공여부, 메시지) 반환."""
    import psycopg2
    conn_info = get_connection(name)
    if not conn_info:
        return False, f"연결 '{name}'을 찾을 수 없습니다."
    try:
        conn = psycopg2.connect(
            host=conn_info["host"],
            port=conn_info["port"],
            dbname=conn_info["database"],
            user=conn_info["user"],
            password=conn_info["password"],
            connect_timeout=5,
        )
        conn.close()
        return True, "연결 성공"
    except Exception as e:
        return False, str(e)
