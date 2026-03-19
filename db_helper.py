import os
import urllib.parse
import psycopg2
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, text

import connection_store
from history_manager import HistoryManager

# 연결별 SQLAlchemy 엔진 캐시 (쿼리마다 새로 생성하지 않음)
_engine_cache: dict[str, sqlalchemy.Engine] = {}


class QueryHelper:
    def __init__(self, connection_name: str):
        info = connection_store.get_connection(connection_name)
        if not info:
            raise ValueError(f"Connection '{connection_name}' not found in connection store.")
        self.connection_name = connection_name
        self._info = info
        self.history = HistoryManager()

    def _get_engine(self) -> sqlalchemy.Engine:
        """연결별 엔진을 캐시에서 가져오거나 새로 생성한다."""
        if self.connection_name not in _engine_cache:
            encoded_pw = urllib.parse.quote_plus(self._info["password"])
            url = (
                f"postgresql://{self._info['user']}:{encoded_pw}"
                f"@{self._info['host']}:{self._info['port']}/{self._info['database']}"
            )
            _engine_cache[self.connection_name] = create_engine(url)
        return _engine_cache[self.connection_name]

    def execute_query(self, query: str, params=None, user_request: str = None) -> pd.DataFrame | None:
        """SELECT 쿼리를 실행하고 DataFrame을 반환한다."""
        try:
            with self._get_engine().connect() as conn:
                df = pd.read_sql_query(text(query), conn, params=params)
            self.history.save_query(query, self.connection_name, success=True, user_request=user_request)
            return df
        except Exception as e:
            print(f"Error executing query: {e}")
            self.history.save_query(query, self.connection_name, success=False, error_message=str(e), user_request=user_request)
            return None

    def execute_update(self, query: str, params=None, user_request: str = None) -> int | None:
        """INSERT/UPDATE/DELETE 쿼리를 실행하고 영향받은 행 수를 반환한다."""
        try:
            conn = psycopg2.connect(
                host=self._info["host"],
                port=self._info["port"],
                dbname=self._info["database"],
                user=self._info["user"],
                password=self._info["password"],
            )
            with conn.cursor() as cur:
                cur.execute(query, params)
                conn.commit()
                rowcount = cur.rowcount
            conn.close()
            self.history.save_query(query, self.connection_name, success=True, user_request=user_request)
            return rowcount
        except Exception as e:
            print(f"Error executing update: {e}")
            self.history.save_query(query, self.connection_name, success=False, error_message=str(e), user_request=user_request)
            return None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass
