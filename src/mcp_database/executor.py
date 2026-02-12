"""Query executor -- executes SQL against an in-memory SQLite database."""

import sqlite3

from mcp_database.models import QueryResult

MAX_RESULT_ROWS = 100


class QueryExecutor:
    """Executes read-only SQL queries and returns structured results."""

    def __init__(self, db_path: str = ":memory:") -> None:
        self._conn: sqlite3.Connection = sqlite3.connect(db_path)

    def execute(self, query: str) -> QueryResult:
        """Run a SQL query and return columns, rows, and truncation info.

        Args:
            query: The SQL statement to execute.

        Returns:
            A QueryResult with the fetched data.
        """
        cursor = self._conn.execute(query)
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        all_rows = cursor.fetchall()
        truncated = len(all_rows) > MAX_RESULT_ROWS
        rows = [list(r) for r in all_rows[:MAX_RESULT_ROWS]]
        return QueryResult(
            columns=columns,
            rows=rows,
            row_count=len(rows),
            truncated=truncated,
        )

    def execute_setup(self, sql: str) -> None:
        """Run a setup script (e.g. CREATE TABLE) without returning results.

        Args:
            sql: One or more SQL statements to execute as a script.
        """
        self._conn.executescript(sql)

    def close(self) -> None:
        """Close the underlying database connection."""
        self._conn.close()
