# MCP Server Database

[![CI](https://github.com/marlonbarreto-git/mcp-server-database/actions/workflows/ci.yml/badge.svg)](https://github.com/marlonbarreto-git/mcp-server-database/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An MCP server that enables LLMs to query databases safely with read-only access, query validation, and schema introspection.

## Overview

MCP Server Database exposes database operations as MCP tools, allowing LLMs to list tables, describe schemas, and execute read-only SQL queries. A query validator blocks destructive keywords (DROP, DELETE, UPDATE, etc.) and prevents multi-statement injection, while the executor enforces row limits to protect against unbounded result sets.

## Architecture

```
┌──────────────────────────────────────────────┐
│            DatabaseMCPServer                 │
│                                              │
│  ┌───────────┐  ┌───────────┐  ┌─────────┐  │
│  │  Schema   │  │  Query    │  │  Query  │  │
│  │  Manager  │  │ Validator │  │Executor │  │
│  │           │  │           │  │         │  │
│  │ list      │  │ block DDL │  │ SQLite  │  │
│  │ describe  │  │ read-only │  │ max 100 │  │
│  └───────────┘  └───────────┘  └─────────┘  │
└──────────────────────────────────────────────┘
       │                │               │
   table info      SELECT/WITH     execute +
   summaries       enforcement     truncate
```

## Features

- Read-only query enforcement (only SELECT and WITH/CTE queries allowed)
- Blocked keyword detection (DROP, DELETE, UPDATE, INSERT, ALTER, etc.)
- Multi-statement injection prevention
- Schema introspection with table listing and column descriptions
- Row limit truncation (max 100 rows per query)
- In-memory SQLite execution engine

## Tech Stack

- Python 3.11+
- Pydantic >= 2.10
- SQLite (stdlib)

## Quick Start

```bash
git clone https://github.com/marlonbarreto-git/mcp-server-database.git
cd mcp-server-database
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Project Structure

```
src/mcp_database/
  __init__.py
  server.py      # DatabaseMCPServer combining all components
  models.py      # ColumnInfo, TableInfo, QueryResult, QueryValidationResult
  executor.py    # QueryExecutor with SQLite backend and row limits
  schema.py      # SchemaManager for table registration and introspection
  validator.py   # QueryValidator with keyword blocking and injection prevention
tests/
  test_server.py
  test_models.py
  test_executor.py
  test_schema.py
  test_validator.py
```

## Testing

```bash
pytest -v --cov=src/mcp_database
```

34 tests covering query execution, validation rules, schema management, blocked keywords, and server integration.

## License

MIT