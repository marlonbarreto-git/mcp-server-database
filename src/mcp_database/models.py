from dataclasses import dataclass, field


@dataclass
class ColumnInfo:
    name: str
    data_type: str
    nullable: bool = True


@dataclass
class TableInfo:
    name: str
    columns: list[ColumnInfo] = field(default_factory=list)


@dataclass
class QueryResult:
    columns: list[str]
    rows: list[list]
    row_count: int = 0
    truncated: bool = False


@dataclass
class QueryValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
