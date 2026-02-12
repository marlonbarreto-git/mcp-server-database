"""MCP server combining query execution, validation, and schema introspection."""

from mcp_database.models import QueryValidationResult


class DatabaseMCPServer:
    def __init__(self, executor, validator, schema_manager):
        self.executor = executor
        self.validator = validator
        self.schema_manager = schema_manager

    def handle_list_tables(self) -> list[str]:
        return self.schema_manager.list_tables()

    def handle_describe_table(self, table_name: str) -> dict | None:
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
        validation = self.validator.validate(query)
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
