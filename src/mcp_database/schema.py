from mcp_database.models import TableInfo


class SchemaManager:
    def __init__(self):
        self._tables: dict[str, TableInfo] = {}

    def register_table(self, table: TableInfo) -> None:
        self._tables[table.name] = table

    def list_tables(self) -> list[str]:
        return sorted(self._tables.keys())

    def describe_table(self, table_name: str) -> TableInfo | None:
        return self._tables.get(table_name)

    def get_schema_summary(self) -> str:
        lines = []
        for name in sorted(self._tables):
            table = self._tables[name]
            cols = ", ".join(f"{c.name} ({c.data_type})" for c in table.columns)
            lines.append(f"{name}: {cols}")
        return "\n".join(lines)
