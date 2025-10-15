# 🏦 FinanceGY

**FinanceGY** is an unofficial Python library for accessing financial data from the **Guyana Stock Exchange (GSE)**. It provides a simple and consistent interface for retrieving information on traded securities, recent trade data, and session details, all programmatically.

---

## Installation

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
recent_trade = financegy.get_recent_trade("DDL")

# Get all trade data for the most recent year
recent_year = financegy.get_security_recent_year("DDL")

# Get trade data for a specific trading session
session_trades = financegy.get_session_trades("1136")

# Get session trade data for a specific security
security_session_trade = financegy.get_security_session_trade("DDL", "1136")

# Search for securities by name or symbol
search_results = financegy.search_securities("DDL")

# Get all trades for a given year
year_trades = financegy.get_trades_for_year("DDL", "2019")

# Get historical trades within a date range (dd/mm/yyyy)
historical_trades = financegy.get_historical_trades(
    symbol="DDL",
    start_date="01/06/2020",
    end_date="01/01/2022"
)
```

---

## Function Overview

#### `get_securities()`

Returns a list of all currently traded securities on the Guyana Stock Exchange.

#### `get_security_by_symbol(symbol: str)`

Retrieves the full name of a security using its ticker symbol (e.g., `"DDL"` → `"Demerara Distillers Limited"`).

#### `get_recent_trade(symbol: str)`

Returns the most recent trade information for the given security.

#### `get_security_recent_year(symbol: str)`

Fetches all trade data for the most recent year of the selected security.

#### `get_session_trades(session: str)`

Retrieves trade data for _all_ securities during a specific trading session.

#### `get_security_session_trade(symbol: str, session: str)`

Retrieves trade data for a specific security in a given trading session.

#### `search_securities(query: str)`

Searches for securities whose names or ticker symbols match the given query.

#### `get_trades_for_year(symbol: str, year: str)`

Returns all trade records for a specific security during a given year.

#### `get_historical_trades(symbol: str, start_date: str, end_date: str)`

Fetches historical trade data for a security within the specified date range (`dd/mm/yyyy` format).

---

## Caching System

FinanceGY includes a lightweight local caching system designed to speed up repeated requests and reduce unnecessary calls to the Guyana Stock Exchange (GSE).

Whenever you call a data retrieval function (such as `get_securities()` or `get_recent_trade()`), FinanceGY automatically checks whether a cached response already exists for that specific query:

-   If a valid cache file (less than 7 days old) is found, the result is returned instantly from the cache.
-   If the cache is missing, disabled, or older than one week, FinanceGY fetches fresh data from the GSE and updates the cache automatically.

All cache files are stored in a local `cache/` directory as small JSON files containing the retrieved data and a timestamp. This ensures that frequently accessed data loads quickly while staying reasonably up to date.

You can manually clear all cached data at any time:

```python
import financegy

financegy.clear_cache()
```

This will delete all cached files and force the next data request to fetch fresh data directly from the source.

If you prefer to **bypass the cache** for a specific call, simply pass `use_cache=False` to any function. For example:

```python
# Force a fresh fetch from the GSE, ignoring cached data
recent_trade = financegy.get_recent_trade("DDL", use_cache=False)
```

By default, caching is enabled for all supported functions unless explicitly turned off.

---

## License

This project is licensed under the **MIT License**

---

## Example Use Case

```python
import financegy

ddl_recent = financegy.get_security_recent("DDL")
print(ddl_recent)
```
