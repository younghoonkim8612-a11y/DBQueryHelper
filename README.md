# DB Query Helper

PostgreSQL 데이터베이스에 자연어로 질의할 수 있는 AI 기반 쿼리 도구입니다.
Streamlit 웹 UI를 통해 DB 연결 관리, 자연어 → SQL 변환, 실행, 결과 확인까지 한 곳에서 처리합니다.

## 주요 기능

- **자연어 → SQL 변환** — Claude AI가 스키마를 참고하여 SQL을 생성하고 실행합니다
- **자동 오류 수정** — 쿼리 실행 실패 시 AI가 에러를 분석하고 자동으로 수정합니다 (최대 2회)
- **오류 학습** — 실패한 쿼리와 에러를 기록하여 동일 실수를 반복하지 않습니다
- **스키마 자동 생성** — DB에서 테이블/컬럼/PK/FK 정보를 조회하여 참조 문서를 생성합니다
- **JSONB 프로파일링** — JSONB 컬럼의 내부 키 구조를 샘플링하여 문서화합니다
- **GIS 마이그레이션** — FK 의존성 순서를 자동 계산하여 스키마 간 데이터 이전 SQL을 생성합니다
- **안전 장치** — DROP/TRUNCATE/ALTER 차단, 복수 쿼리(;) 방지, 대용량 테이블 필터 강제

## 프로젝트 구조

```
DBQueryHelper/
├── app.py                      # Streamlit 메인 앱 (자연어 쿼리 UI)
├── pages/
│   └── 1_🔌_연결_관리.py        # DB 연결 관리 페이지
├── db_helper.py                # QueryHelper — DB 연결 및 쿼리 실행
├── connection_store.py         # connections.json 기반 연결 정보 관리
├── history_manager.py          # 쿼리 히스토리 관리 (최근 500건)
├── schema_generator.py         # DB 스키마 → Markdown 문서 생성
├── generate_gisdb_insert_sql.py # GIS 스키마 간 데이터 마이그레이션 SQL 생성
├── check_*.py                  # 스키마 비교/검증 유틸리티
├── schemas/
│   ├── timescale/              # Timescale DB 스키마 참조 문서
│   └── gis/                    # GIS DB 스키마 참조 문서
├── setup.bat                   # 초기 설정 스크립트
├── run.bat                     # 앱 실행 스크립트
└── requirements.txt
```

## 설치

### 사전 요구사항

- Python 3.11 이상
- PostgreSQL 데이터베이스 접속 정보
- [Claude Code CLI](https://www.npmjs.com/package/@anthropic-ai/claude-code) (AI 쿼리 생성에 필요, Max 구독)

### 설치 방법

```bash
# 자동 설치
setup.bat

# 또는 수동 설치
python -m venv venv
venv\Scripts\pip.exe install -r requirements.txt
```

### 환경 설정

`.env` 파일을 프로젝트 루트에 생성합니다:

```env
# DB 비밀번호 (연결 이름의 공백은 _로 치환)
DB_PASSWORD_My_Database=yourpassword
```

## 실행

```bash
# 실행 스크립트
run.bat

# 또는 직접 실행
set PYTHONIOENCODING=utf-8
venv\Scripts\python.exe -m streamlit run app.py
```

브라우저에서 `http://localhost:8501`로 접속합니다.

## 사용법

1. **연결 관리** 페이지에서 PostgreSQL 연결 정보를 등록합니다
2. 메인 페이지에서 연결을 선택합니다
3. 자연어로 질문을 입력합니다 (예: "apron_map 테이블에서 T1 터미널 데이터 보여줘")
4. AI가 SQL을 생성하고 실행 결과를 표시합니다
5. 결과를 CSV로 다운로드할 수 있습니다

## 기술 스택

| 구분 | 기술 |
|------|------|
| AI | Claude API (claude-agent-sdk) |
| Web UI | Streamlit |
| DB 드라이버 | psycopg2, SQLAlchemy |
| 데이터 처리 | pandas |
| 대상 DB | PostgreSQL, TimescaleDB, PostGIS |

## 라이선스

Private repository — 내부 사용 전용
