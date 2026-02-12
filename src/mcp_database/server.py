"""MCP server combining query execution, validation, and schema introspection."""

from mcp_database.executor import QueryExecutor
from mcp_database.models import QueryValidationResult
from mcp_database.schema import SchemaManager
from mcp_database.validator import QueryValidator


class DatabaseMCPServer:
    """Facade that wires together execution, validation, and schema layers."""

    def __init__(
        self,
        executor: QueryExecutor,
        validator: QueryValidator,
        schema_manager: SchemaManager,
    ) -> None:
        self.executor = executor
        self.validator = validator
        self.schema_manager = schema_manager

    def handle_list_tables(self) -> list[str]:
        """Return the names of all registered tables."""
        return self.schema_manager.list_tables()

    def handle_describe_table(self, table_name: str) -> dict | None:
        """Return column details for a table, or None if not found.

        Args:
            table_name: The table to describe.

        Returns:
            A dict with table name and columns, or None.
        """
        table = self.schema_manager.describe_table(table_name)
        if table is None:
            return None
        return {
            "name": table.name,
            "columns": [
                {"name": c.name, "type": c.data_type, "nullable": c.nullable}
                for c in table.columns
            ],
        }

    def handle_run_query(self, query: str) -> dict:
        """Validate and execute a SQL query, returning results or errors.

        Args:
            query: The SQL query string to run.

        Returns:
            A dict with query results or error messages.
        """
        validation: QueryValidationResult = self.validator.validate(query)
        if not validation.valid:
            return {"error": True, "messages": validation.errors}
        try:
            result = self.executor.execute(query)
            return {
                "columns": result.columns,
                "rows": result.rows,
                "row_count": result.row_count,
                "truncated": result.truncated,
            }
        except Exception as e:
            return {"error": True, "messages": [str(e)]}
