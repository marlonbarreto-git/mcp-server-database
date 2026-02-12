import re

from mcp_database.models import QueryValidationResult


class QueryValidator:
    BLOCKED_KEYWORDS = {"DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "CREATE", "GRANT", "REVOKE"}

    def validate(self, query: str) -> QueryValidationResult:
        errors = []
        normalized = query.strip().upper()

        if not normalized:
            errors.append("Empty query")
            return QueryValidationResult(valid=False, errors=errors)

        # Must start with SELECT or WITH (CTE)
        if not (normalized.startswith("SELECT") or normalized.startswith("WITH")):
            errors.append("Only SELECT queries are allowed")

        # Check for blocked keywords
        tokens = set(re.findall(r'\b[A-Z]+\b', normalized))
        blocked_found = tokens & self.BLOCKED_KEYWORDS
        if blocked_found:
            errors.append(f"Blocked keywords found: {', '.join(sorted(blocked_found))}")

        # Check for semicolons (prevent injection of multiple statements)
        if ";" in query.rstrip().rstrip(";"):
            errors.append("Multiple statements not allowed")

        return QueryValidationResult(valid=len(errors) == 0, errors=errors)
