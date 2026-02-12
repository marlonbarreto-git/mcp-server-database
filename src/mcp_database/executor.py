"""Query executor — executes SQL against an in-memory SQLite database."""

import sqlite3

from mcp_database.models import QueryResult


class QueryExecutor:
    def __init__(self, db_path: str = ":memory:"):
        self._conn = sqlite3.connect(db_path)
        self._max_rows = 100

    def execute(self, query: str) -> QueryResult:
        cursor = self._conn.execute(query)
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        all_rows = cursor.fetchall()
        truncated = len(all_rows) > self._max_rows
        rows = [list(r) for r in all_rows[: self._max_rows]]
        return QueryResult(
            columns=columns,
            rows=rows,
            row_count=len(rows),
            truncated=truncated,
        )

    def execute_setup(self, sql: str) -> None:
        self._conn.executescript(sql)

    def close(self):
        self._conn.close()
