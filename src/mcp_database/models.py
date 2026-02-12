"""Domain models for query results and schema metadata."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ColumnInfo:
    """Metadata about a single database column."""

    name: str
    data_type: str
    nullable: bool = True


@dataclass
class TableInfo:
    """Metadata about a database table and its columns."""

    name: str
    columns: list[ColumnInfo] = field(default_factory=list)


@dataclass
class QueryResult:
    """Result set returned after executing a SQL query."""

    columns: list[str]
    rows: list[list[Any]]
    row_count: int = 0
    truncated: bool = False


@dataclass
class QueryValidationResult:
    """Outcome of validating a SQL query before execution."""

    valid: bool
    errors: list[str] = field(default_factory=list)
