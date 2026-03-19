# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Model Usage Policy

To optimize token usage, use **claude-sonnet-4-6** for the following tasks:
- Bash/shell command execution (running scripts, git commands, etc.)
- Running tests
- File search and exploration (Glob, Grep)
- Simple code edits and fixes

Use **claude-opus-4-6** only for complex reasoning tasks such as architecture decisions, multi-file refactoring, or generating new features.

## Running Scripts

This project uses a local virtual environment. Always use the venv Python:

```bash
# Run any script
./venv/Scripts/python.exe <script_name>.py

# With UTF-8 encoding (required for SQL output with special characters)
PYTHONIOENCODING=utf-8 ./venv/Scripts/python.exe generate_gisdb_insert_sql.py
```

There is no build system, test suite, or linter configured.

## Architecture

### Core Classes (`db_helper.py`)

**`DBConfig`** — Reads DBeaver's `data-sources.json` from `%APPDATA%/DBeaverData/workspace6/General/.dbeaver/` to extract PostgreSQL connection definitions (host, port, database, user). Connection names must match exactly as named in DBeaver.

**`QueryHelper`** — Wraps a named DBeaver connection. Retrieves passwords from `.env` using the naming convention `DB_PASSWORD_<connection_name_with_spaces_replaced_by_underscores>`. Uses `psycopg2` for mutations (`execute_update`) and `SQLAlchemy`+`pandas` for selects (`execute_query` returns a DataFrame). Supports context manager usage. All queries are logged to `query_history.json` via `HistoryManager`.

**`HistoryManager`** (`history_manager.py`) — Appends each query to `query_history.json`, keeping the last 500 entries.

### Migration Engine (`generate_gisdb_insert_sql.py`)

The primary utility in this project. It:
1. Queries two schemas (`gisdb_JED` → source, `gisdb` → target) on the same server
2. Resolves FK dependency order using topological sort across 23 GIS tables
3. Generates `DELETE + INSERT VALUES` SQL in batches of 500 rows
4. Handles PostGIS geometry via `ST_GeomFromText` / `ST_SetSRID`
5. Outputs files to `Generated Files/<date>/JED GIS Insert Script/`

### Inspection Utilities

- `check_missing_tables.py` — Compare table presence across schemas
- `check_column_diff.py` — Diff column definitions between schemas
- `check_bet_columns.py` — Focus diff on `bet_map` table
- `check_fk_constraints.py` — Analyze FK constraints across schemas

## AI Query Generation

### Running the interactive REPL
```bash
PYTHONIOENCODING=utf-8 ./venv/Scripts/python.exe main.py
```

Requires `ANTHROPIC_API_KEY` in `.env`. The REPL accepts natural language and converts it to SQL via Claude Opus, executes it, and displays results. On failure it automatically asks the model to fix the query (up to 2 retries).

### Key files
| File | Purpose |
|------|---------|
| `ai_query_generator.py` | `AIQueryGenerator` class — natural language → SQL via Claude Opus with adaptive thinking. Includes self-correction loop. |
| `main.py` | Interactive REPL: connection selection, natural language input, result display via `tabulate`. |

### REPL commands
`:conn <name>`, `:list`, `:history`, `:reset` (clear AI context), `:quit`

### Using `AIQueryGenerator` programmatically
```python
from ai_query_generator import AIQueryGenerator
from db_helper import QueryHelper

gen = AIQueryGenerator()
helper = QueryHelper("CAU_GISDB_Prod")
sql, df = gen.generate_and_execute(helper, "Show me all apron maps for terminal T1")
```

`generate_and_execute` streams the SQL generation to console, executes it, retries on error, and returns `(sql, DataFrame)`. Call `gen.reset()` between unrelated questions to clear conversation context.

## Adding a New Database Connection

1. Add the connection in DBeaver (it must be a PostgreSQL connection)
2. Add the password to `.env`: `DB_PASSWORD_<Connection_Name_With_Underscores>=yourpassword`
3. Use it: `QueryHelper("Connection Name")` (spaces in name are fine)

## Key Data Domain

All GIS tables follow conventions:
- `geom` column (PostGIS geometry, **WGS84 / SRID=4326**)
- Audit columns: `*_cre_ui`, `*_cre_da`, `*_upd_ui`, `*_upd_da`
- FK dependency order (root → leaf): `tml_map`/`cog_grp` → yard/apron/hotel/etc. maps → `bk_map`/`bet_map` → `bay_map`

Schema reference: `schema_reference.md` (gisdb) and `ddw_public_schema_reference.md` (DDW alternative).
