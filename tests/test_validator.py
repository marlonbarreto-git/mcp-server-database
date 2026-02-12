from mcp_database.validator import QueryValidator


class TestQueryValidator:
    def setup_method(self):
        self.validator = QueryValidator()

    def test_valid_select_query(self):
        result = self.validator.validate("SELECT * FROM users")
        assert result.valid is True
        assert result.errors == []

    def test_valid_select_with_where(self):
        result = self.validator.validate("SELECT id, name FROM users WHERE id = 1")
        assert result.valid is True
        assert result.errors == []

    def test_valid_with_cte(self):
        query = "WITH cte AS (SELECT id FROM users) SELECT * FROM cte"
        result = self.validator.validate(query)
        assert result.valid is True
        assert result.errors == []

    def test_blocks_drop(self):
        result = self.validator.validate("DROP TABLE users")
        assert result.valid is False
        assert any("DROP" in e for e in result.errors)

    def test_blocks_delete(self):
        result = self.validator.validate("DELETE FROM users")
        assert result.valid is False
        assert any("DELETE" in e for e in result.errors)

    def test_blocks_update(self):
        result = self.validator.validate("UPDATE users SET name = 'x'")
        assert result.valid is False
        assert any("UPDATE" in e for e in result.errors)

    def test_blocks_insert(self):
        result = self.validator.validate("INSERT INTO users VALUES (1)")
        assert result.valid is False
        assert any("INSERT" in e for e in result.errors)

    def test_empty_query_invalid(self):
        result = self.validator.validate("")
        assert result.valid is False
        assert any("Empty" in e for e in result.errors)

    def test_multiple_statements_blocked(self):
        result = self.validator.validate("SELECT 1; DROP TABLE x")
        assert result.valid is False
        assert any("Multiple" in e or "DROP" in e for e in result.errors)
