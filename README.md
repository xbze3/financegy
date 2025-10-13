# 🏦 FinanceGY

**FinanceGY** is an **unofficial Python library** for accessing financial data from the **Guyana Stock Exchange (GSE)**.  
It provides a simple and consistent interface for retrieving information on traded securities, recent trade data, and session details, all programmatically.

---

## Installation

_(Once published on PyPI)_

```bash
pip install financegy
```

---

## Quick Start

```python
import financegy

# Get a list of all traded securities
securities = financegy.get_securities()

# Get the name of a security by its ticker symbol
security_name = financegy.get_security_by_symbol("DDL")

# Get the most recent trade data for a security
recent = financegy.get_security_recent("DDL")

# Get all trade data for the most recent year
recent_year = financegy.get_security_recent_year("DDL")

# Get trade data for a specific trading session
session_data = financegy.get_securites_session("2024-12-15")

# Get session trade data for a specific security
security_session = financegy.get_security_session("DDL", "2024-12-15")
```

---

## Function Overview

### `get_securities()`

Returns a list of all currently traded securities on the Guyana Stock Exchange.

### `get_security_by_symbol(symbol: str)`

Retrieves the full name of a security using its ticker symbol (e.g., `"DDL"` → `"Demerara Distillers Limited"`).

### `get_security_recent(symbol: str)`

Returns the most recent trade information for the given security.

### `get_security_recent_year(symbol: str)`

Fetches all trade data for the most recent year of the selected security.

### `get_securites_session(session: str)`

Retrieves trade data for _all_ securities during a specific trading session.

### `get_security_session(symbol: str, session: str)`

Retrieves trade data for a specific security in a given trading session.

---

## License

This project is licensed under the **MIT License** — allowing modification, redistribution, and commercial use with proper credit.

---

## Example Use Case

```python
import financegy

ddl_recent = financegy.get_security_recent("DDL")
print(ddl_recent)
```
