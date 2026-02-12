from mcp_database.models import ColumnInfo, TableInfo
from mcp_database.schema import SchemaManager


class TestSchemaManager:
    def setup_method(self):
        self.manager = SchemaManager()

    def _make_table(self, name: str, cols: list[tuple[str, str]] | None = None) -> TableInfo:
        columns = [ColumnInfo(name=c[0], data_type=c[1]) for c in (cols or [])]
        return TableInfo(name=name, columns=columns)

    def test_register_and_list_tables(self):
        self.manager.register_table(self._make_table("users"))
        self.manager.register_table(self._make_table("orders"))
        tables = self.manager.list_tables()
        assert "users" in tables
        assert "orders" in tables

    def test_describe_existing_table(self):
        table = self._make_table("users", [("id", "INTEGER"), ("name", "TEXT")])
        self.manager.register_table(table)
        result = self.manager.describe_table("users")
        assert result is not None
        assert result.name == "users"
        assert len(result.columns) == 2

    def test_describe_nonexistent_returns_none(self):
        result = self.manager.describe_table("nonexistent")
        assert result is None

    def test_list_tables_sorted(self):
        self.manager.register_table(self._make_table("zebra"))
        self.manager.register_table(self._make_table("alpha"))
        self.manager.register_table(self._make_table("middle"))
        assert self.manager.list_tables() == ["alpha", "middle", "zebra"]

    def test_get_schema_summary_format(self):
        table = self._make_table("users", [("id", "INTEGER"), ("name", "TEXT")])
        self.manager.register_table(table)
        summary = self.manager.get_schema_summary()
        assert "users:" in summary
        assert "id (INTEGER)" in summary
        assert "name (TEXT)" in summary

    def test_register_overwrites_existing(self):
        self.manager.register_table(self._make_table("users", [("id", "INTEGER")]))
        self.manager.register_table(self._make_table("users", [("id", "INTEGER"), ("name", "TEXT")]))
        result = self.manager.describe_table("users")
        assert len(result.columns) == 2
