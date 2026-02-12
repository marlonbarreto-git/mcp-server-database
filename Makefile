.PHONY: install test lint format typecheck clean

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --tb=short

lint:
	ruff check src/mcp_database/ tests/

format:
	ruff format src/mcp_database/ tests/

typecheck:
	mypy src/mcp_database/

clean:
	rm -rf .mypy_cache .ruff_cache .pytest_cache __pycache__ dist build *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
