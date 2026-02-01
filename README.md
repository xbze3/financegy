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

# --------------------------
# Core Data Retrieval
# --------------------------

# Get a list of all traded securities
securities = financegy.get_securities()

# Get the full name of a security by its ticker symbol
security_name = financegy.get_security_by_symbol("DDL")

# Get the most recent trade data for a security
recent_trade = financegy.get_recent_trade("DDL")

# Get the most recent closing/last trade price (same most-recent session)
previous_close = financegy.get_previous_close("DDL")

# Get absolute price change vs previous session close
price_change = financegy.get_price_change("DDL")

# Get percent price change vs previous session close
price_change_percent = financegy.get_price_change_percent("DDL")

# Get all trade data for the most recent year (for the security)
recent_year_trades = financegy.get_security_recent_year("DDL")

# Get trade data for a specific trading session (all securities)
session_trades = financegy.get_session_trades("1136")

# Get trade data for a specific security in a session
security_session_trade = financegy.get_security_session_trade("DDL", "1136")

# Search for securities by name or symbol
search_results = financegy.search_securities("DDL")

# Get all trades for a specific year
year_trades = financegy.get_trades_for_year("DDL", "2019")

# Get historical trades within a date range — supports: yyyy / mm/yyyy / dd/mm/yyyy
historical_trades = financegy.get_historical_trades(
    symbol="DDL",
    start_date="01/06/2020",
    end_date="01/2022"
)

# --------------------------
# Analytics / Calculations
# --------------------------

# Get the latest session info (dict returned from most recent trade)
latest_session = financegy.get_latest_session_for_symbol("DDL")

# Average last traded price over a session range (inclusive)
avg_price_range = financegy.get_sessions_average_price("DDL", "1100", "1136")

# Average last traded price over the last N sessions (ending at latest session)
avg_price_latest = financegy.get_average_price("DDL", 30)

# Volatility over the last N sessions (weekly log-return volatility + annualized)
volatility = financegy.get_sessions_volatility("DDL", 30)

# Year-to-date high and low traded prices
ytd_high_low = financegy.get_ytd_high_low("DDL")

# --------------------------
# Utilities
# --------------------------

# Convert results to a DataFrame
df = financegy.to_dataframe(securities)

# Export to CSV / Excel
financegy.save_to_csv(securities, filename="securities.csv", silent=True)
financegy.save_to_excel(securities, filename="securities.xlsx", silent=True)

# Clear FinanceGY cache directory
financegy.clear_cache(silent=True)
```

---

## API Reference

### Core Data Retrieval

| Function                                              | Description                                                                                           |
| ----------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `get_securities()`                                    | Returns all currently traded securities on the GSE.                                                   |
| `get_security_by_symbol(symbol)`                      | Returns the full security name for a ticker symbol (e.g., `"DDL"` → `"Demerara Distillers Limited"`). |
| `get_recent_trade(symbol)`                            | Returns the most recent trade information for the given security.                                     |
| `get_security_recent_year(symbol)`                    | Returns all trade data for the most recent year available for the selected security.                  |
| `get_session_trades(session)`                         | Returns trade data for **all** securities during a specific trading session.                          |
| `get_security_session_trade(symbol, session)`         | Returns trade data for a **specific** security during a specific session.                             |
| `search_securities(query)`                            | Searches securities whose names or ticker symbols match the given query (partial match).              |
| `get_trades_for_year(symbol, year)`                   | Returns all trade records for a specific security during a given year.                                |
| `get_historical_trades(symbol, start_date, end_date)` | Returns historical trades within the specified date range (`dd/mm/yyyy`, `mm/yyyy`, or `yyyy`).       |

### Analytics / Calculation Functions

| Function                                                         | Description                                                                                      |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `get_previous_close(symbol)`                                     | Returns the most recent closing/last trade price for the security.                               |
| `get_price_change(symbol)`                                       | Returns absolute price difference between the most recent trade and the previous session close.  |
| `get_price_change_percent(symbol)`                               | Returns percent price change between the most recent trade and the previous session close.       |
| `get_latest_session_for_symbol(symbol)`                          | Returns the latest trade dict for the symbol (includes the latest `session`).                    |
| `get_sessions_average_price(symbol, session_start, session_end)` | Returns the average last traded price over a session range (inclusive).                          |
| `get_average_price(symbol, session_number)`                      | Returns the average last traded price over the last **N** sessions ending at the latest session. |
| `get_sessions_volatility(symbol, session_number)`                | Returns volatility over the last **N** sessions using log returns (weekly + annualized).         |
| `get_ytd_high_low(symbol)`                                       | Returns year-to-date highest and lowest traded prices for the security.                          |

### Utilities

| Function                                                               | Description                                                     |
| ---------------------------------------------------------------------- | --------------------------------------------------------------- |
| `to_dataframe(data)`                                                   | Converts FinanceGY list/dict results into a `pandas.DataFrame`. |
| `save_to_csv(data, filename="output.csv", path=None, silent=False)`    | Saves data to a CSV file.                                       |
| `save_to_excel(data, filename="output.xlsx", path=None, silent=False)` | Saves data to an Excel file.                                    |
| `clear_cache(silent=False)`                                            | Completely clears the FinanceGY cache directory.                |

---

## Caching System

FinanceGY includes a lightweight local caching system designed to speed up repeated requests and reduce unnecessary calls.

Whenever you call a data retrieval function (such as `get_securities()` or `get_recent_trade()`), FinanceGY automatically checks whether a cached response already exists for that specific query:

- If a valid cache file (less than 7 days old since sessions are held once per week) is found, the result is returned instantly from the cache.
- If the cache is missing, disabled, or older than one week, FinanceGY fetches fresh data from the GSE and updates the cache automatically.

All cache files are stored in a local `cache/` directory as small JSON files containing the retrieved data and a timestamp.

You can manually clear all cached data at any time:

```python
import financegy

financegy.clear_cache()
```

This will delete all cached files and force the next data request to fetch fresh data directly from the source.

If you prefer to bypass the cache for a specific call, simply pass `use_cache=False` to any function. For example:

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
