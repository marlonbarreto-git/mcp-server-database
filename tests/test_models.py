from mcp_database.models import ColumnInfo, TableInfo, QueryResult, QueryValidationResult


def test_column_info_defaults():
    col = ColumnInfo(name="id", data_type="INTEGER")
    assert col.name == "id"
    assert col.data_type == "INTEGER"
    assert col.nullable is True


def test_column_info_non_nullable():
    col = ColumnInfo(name="id", data_type="INTEGER", nullable=False)
    assert col.nullable is False


def test_table_info_defaults():
    table = TableInfo(name="users")
    assert table.name == "users"
    assert table.columns == []


def test_table_info_with_columns():
    cols = [ColumnInfo(name="id", data_type="INTEGER"), ColumnInfo(name="name", data_type="TEXT")]
    table = TableInfo(name="users", columns=cols)
    assert len(table.columns) == 2
    assert table.columns[0].name == "id"


def test_query_result_defaults():
    result = QueryResult(columns=["id"], rows=[[1]])
    assert result.row_count == 0
    assert result.truncated is False


def test_query_validation_result_valid():
    result = QueryValidationResult(valid=True)
    assert result.valid is True
    assert result.errors == []


def test_query_validation_result_invalid():
    result = QueryValidationResult(valid=False, errors=["bad query"])
    assert result.valid is False
    assert result.errors == ["bad query"]
