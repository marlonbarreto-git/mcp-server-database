"""Tests for DatabaseMCPServer — TDD RED phase."""

from unittest.mock import MagicMock

import pytest

from mcp_database.models import (
    ColumnInfo,
    QueryResult,
    QueryValidationResult,
    TableInfo,
)
from mcp_database.server import DatabaseMCPServer


@pytest.fixture
def mock_executor():
    return MagicMock()


@pytest.fixture
def mock_validator():
    return MagicMock()


@pytest.fixture
def mock_schema():
    return MagicMock()


@pytest.fixture
def server(mock_executor, mock_validator, mock_schema):
    return DatabaseMCPServer(
        executor=mock_executor,
        validator=mock_validator,
        schema_manager=mock_schema,
    )


class TestHandleListTables:
    def test_delegates_to_schema_manager(self, server, mock_schema):
        mock_schema.list_tables.return_value = ["users", "orders"]
        result = server.handle_list_tables()
        assert result == ["users", "orders"]
        mock_schema.list_tables.assert_called_once()


class TestHandleDescribeTable:
    def test_returns_dict_for_existing_table(self, server, mock_schema):
        mock_schema.describe_table.return_value = TableInfo(
            name="users",
            columns=[
                ColumnInfo(name="id", data_type="INTEGER", nullable=False),
                ColumnInfo(name="name", data_type="TEXT", nullable=True),
            ],
        )
        result = server.handle_describe_table("users")
        assert result == {
            "name": "users",
            "columns": [
                {"name": "id", "type": "INTEGER", "nullable": False},
                {"name": "name", "type": "TEXT", "nullable": True},
            ],
        }

    def test_returns_none_for_missing_table(self, server, mock_schema):
        mock_schema.describe_table.return_value = None
        result = server.handle_describe_table("nonexistent")
        assert result is None


class TestHandleRunQuery:
    def test_valid_query_returns_result(self, server, mock_validator, mock_executor):
        mock_validator.validate.return_value = QueryValidationResult(valid=True)
        mock_executor.execute.return_value = QueryResult(
            columns=["id", "name"],
            rows=[[1, "Alice"]],
            row_count=1,
            truncated=False,
        )
        result = server.handle_run_query("SELECT * FROM users")
        assert result == {
            "columns": ["id", "name"],
            "rows": [[1, "Alice"]],
            "row_count": 1,
            "truncated": False,
        }

    def test_invalid_query_returns_error(self, server, mock_validator):
        mock_validator.validate.return_value = QueryValidationResult(
            valid=False, errors=["SELECT required"]
        )
        result = server.handle_run_query("bad query")
        assert result == {"error": True, "messages": ["SELECT required"]}
        # executor should NOT be called
        server.executor.execute.assert_not_called()

    def test_execution_error_returns_error_dict(self, server, mock_validator, mock_executor):
        mock_validator.validate.return_value = QueryValidationResult(valid=True)
        mock_executor.execute.side_effect = Exception("table not found")
        result = server.handle_run_query("SELECT * FROM missing")
        assert result["error"] is True
        assert "table not found" in result["messages"]

    def test_blocks_drop_statement(self, server, mock_validator):
        mock_validator.validate.return_value = QueryValidationResult(
            valid=False, errors=["DROP statements are not allowed"]
        )
        result = server.handle_run_query("DROP TABLE users")
        assert result["error"] is True
        assert any("DROP" in msg for msg in result["messages"])
        server.executor.execute.assert_not_called()
