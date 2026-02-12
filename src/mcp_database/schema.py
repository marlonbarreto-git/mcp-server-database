"""Schema manager -- tracks registered tables and their column metadata."""

from mcp_database.models import TableInfo


class SchemaManager:
    """Registry of known database tables and their schemas."""

    def __init__(self) -> None:
        self._tables: dict[str, TableInfo] = {}

    def register_table(self, table: TableInfo) -> None:
        """Add or replace a table in the schema registry.

        Args:
            table: The table metadata to register.
        """
        self._tables[table.name] = table

    def list_tables(self) -> list[str]:
        """Return a sorted list of registered table names."""
        return sorted(self._tables.keys())

    def describe_table(self, table_name: str) -> TableInfo | None:
        """Return metadata for a table, or None if not registered.

        Args:
            table_name: The name of the table to look up.

        Returns:
            TableInfo if found, None otherwise.
        """
        return self._tables.get(table_name)

    def get_schema_summary(self) -> str:
        """Return a human-readable summary of all registered tables."""
        lines = []
        for name in sorted(self._tables):
            table = self._tables[name]
            cols = ", ".join(f"{c.name} ({c.data_type})" for c in table.columns)
            lines.append(f"{name}: {cols}")
        return "\n".join(lines)
