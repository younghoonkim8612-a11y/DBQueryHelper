# DBQueryHelper 리팩토링 계획

**작성일:** 2026-03-13
**목표:** 코드 단순화, 아키텍처 통일, 성능 개선. 기능 변화 없음.

---

## 배경

코드리뷰에서 발견된 주요 이슈:
- `_CustomQueryHelper` (app.py) 와 `QueryHelper` (db_helper.py) 코드 중복
- DBeaver 의존성과 connection_store 혼용으로 인한 복잡성
- 쿼리마다 SQLAlchemy 엔진을 새로 생성하는 성능 낭비
- 경로 하드코딩 (`CWD = "E:/AntigravityProjects/..."`)
- 레거시 Gemini 코드 잔존 (main.py, ai_query_generator.py)

---

## Task 1: 레거시 파일 삭제

**삭제 대상:**
- `main.py` — app.py로 완전 대체됨
- `ai_query_generator.py` — Gemini 기반, 미사용
- `example_usage.py` — DBeaver + .env 방식 예제, outdated

**영향 없음** — 위 파일들은 app.py/agent_main.py에서 import하지 않음.

---

## Task 2: `db_helper.py` 단순화

**제거:**
- `DBConfig` 클래스 전체 (DBeaver `data-sources.json` 파서)
- `_get_password()` 메서드 (connection_store에 포함됨)
- `connect()` / `close()` (SQLAlchemy가 커넥션 관리)

**추가:**
- 모듈 레벨 엔진 캐시: `_engine_cache: dict[str, Engine] = {}`
- `QueryHelper.__init__`에서 `connection_store.get_connection()` 직접 사용

**변경 후 구조:**
```python
_engine_cache: dict[str, Engine] = {}

class QueryHelper:
    def __init__(self, connection_name: str):
        info = connection_store.get_connection(connection_name)
        if not info:
            raise ValueError(f"Connection '{connection_name}' not found.")
        self.connection_name = connection_name
        self._info = info
        self.history = HistoryManager()

    def _get_engine(self) -> Engine:
        if self.connection_name not in _engine_cache:
            encoded_pw = urllib.parse.quote_plus(self._info["password"])
            url = (f"postgresql://{self._info['user']}:{encoded_pw}"
                   f"@{self._info['host']}:{self._info['port']}/{self._info['database']}")
            _engine_cache[self.connection_name] = create_engine(url)
        return _engine_cache[self.connection_name]

    def execute_query(self, sql, params=None, user_request=None) -> DataFrame | None: ...
    def execute_update(self, sql, params=None, user_request=None) -> int | None: ...
```

---

## Task 3: `app.py` 정리

**제거:**
- `_CustomQueryHelper` 클래스 (db_helper.QueryHelper로 통합됨)
- `get_db_config()` 캐시 함수
- `get_all_connections()`의 DBeaver fallback 로직
- `_get_db_url()` 함수 (엔진 캐시로 대체)
- `_run_query_no_history()` 함수 (QueryHelper._get_engine() 직접 사용)

**변경:**
```python
# 변경 전
CWD = "E:/AntigravityProjects/DBQueryHelper"
PYTHON = "./venv/Scripts/python.exe"

# 변경 후
CWD = str(Path(__file__).parent)
PYTHON = str(Path(__file__).parent / "venv" / "Scripts" / "python.exe")
```

**`get_all_connections()` 단순화:**
```python
def get_all_connections() -> list[str]:
    return connection_store.list_connections()  # connection_store가 유일한 소스
```

---

## Task 4: `agent_main.py` + `execute_sql.py` 경로 수정

두 파일 모두:
```python
# 변경 전
CWD = "E:/AntigravityProjects/DBQueryHelper"
PYTHON = "./venv/Scripts/python.exe"

# 변경 후
from pathlib import Path
CWD = str(Path(__file__).parent)
PYTHON = str(Path(__file__).parent / "venv" / "Scripts" / "python.exe")
```

`execute_sql.py` 추가 정리:
- DBeaver fallback 코드 제거 (`_get_conn_info`의 else 분기)
- `connection_store`만 사용

---

## 작업 순서

1. **Task 1** — 레거시 파일 삭제 (위험도 낮음, 빠름)
2. **Task 2** — `db_helper.py` 단순화 (핵심 변경)
3. **Task 3** — `app.py` 정리 (Task 2 완료 후)
4. **Task 4** — 경로 수정 (독립적, 언제든 가능)

---

## 예상 효과

| 항목 | 현재 | 개선 후 |
|------|------|---------|
| 연결 소스 | DBeaver + connection_store 혼용 | connection_store 단일화 |
| QueryHelper 구현체 | 2개 (_CustomQueryHelper, QueryHelper) | 1개 |
| 엔진 생성 | 쿼리마다 새로 생성 | 연결별 1회 캐싱 |
| 경로 | 하드코딩 | 자동 감지 |
| 레거시 파일 | 3개 잔존 | 삭제 |
| db_helper.py 라인 수 | ~200줄 | ~80줄 예상 |
