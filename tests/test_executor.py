"""Tests for QueryExecutor — TDD RED phase."""

import pytest

from mcp_database.executor import QueryExecutor
from mcp_database.models import QueryResult


@pytest.fixture
def executor():
    ex = QueryExecutor()
    ex.execute_setup("""
        CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT);
        INSERT INTO users (id, name, email) VALUES (1, 'Alice', 'alice@example.com');
        INSERT INTO users (id, name, email) VALUES (2, 'Bob', 'bob@example.com');
        INSERT INTO users (id, name, email) VALUES (3, 'Charlie', 'charlie@example.com');
    """)
    return ex


class TestExecuteSimpleQuery:
    def test_returns_all_rows(self, executor):
        result = executor.execute("SELECT id, name FROM users ORDER BY id")
        assert isinstance(result, QueryResult)
        assert result.row_count == 3
        assert result.rows == [[1, "Alice"], [2, "Bob"], [3, "Charlie"]]
        assert result.truncated is False


class TestExecuteWithWhere:
    def test_filters_rows(self, executor):
        result = executor.execute("SELECT name FROM users WHERE id = 2")
        assert result.row_count == 1
        assert result.rows == [["Bob"]]
        assert result.truncated is False


class TestExecuteReturnsColumnNames:
    def test_column_names_match(self, executor):
        result = executor.execute("SELECT id, name, email FROM users LIMIT 1")
        assert result.columns == ["id", "name", "email"]


class TestExecuteSetupCreatesTables:
    def test_setup_creates_table(self):
        ex = QueryExecutor()
        ex.execute_setup("CREATE TABLE products (sku TEXT, price REAL);")
        result = ex.execute("SELECT * FROM products")
        assert result.columns == ["sku", "price"]
        assert result.rows == []
        assert result.row_count == 0
        ex.close()


class TestExecuteTruncatesAtMax:
    def test_truncates_beyond_max_rows(self):
        ex = QueryExecutor()
        inserts = ";\n".join(
            f"INSERT INTO big (val) VALUES ({i})" for i in range(200)
        )
        ex.execute_setup(f"CREATE TABLE big (val INTEGER);\n{inserts};")
        result = ex.execute("SELECT val FROM big")
        assert result.truncated is True
        assert result.row_count == 100
        assert len(result.rows) == 100
        ex.close()
