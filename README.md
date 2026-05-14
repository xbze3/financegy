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

# Get active market securities (symbol + company name) from the most recent session page
active_securities = financegy.get_active_securities()

# Get the most recent trading session number
recent_session = financegy.get_recent_session()

# Get all sessions for a selected trading year
year_sessions = get_year_sessions("2020")

# Get trade snapshots for all sessions in a selected year
year_sessions_snapshot = get_year_sessions_snapshot("2020")

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

# Get all trade years for a selected security
traded_years = financegy.get_traded_years("DDL")

# Get the earliest financial year available for the security
earliest_year = financegy.get_security_earliest_year("DDL")

# Get the latest financial year available for the security
latest_year = financegy.get_security_latest_year("DDL")

# Get the full trade history for a security (all years combined)
full_history = financegy.get_security_full_history("DDL")

# Get trade data for a specific trading session (all securities)
session_trades = financegy.get_session_trades("1136")

# Get the date for a specified trading session.
session_date = financegy.get_session_date("1136")

# Get trade data for a specific security in a session
security_session_trade = financegy.get_security_session_trade("DDL", "1136")

# Search for securities by name or symbol
search_results = financegy.search_securities("DDL")

# Get all trades for a specific year
year_trades = financegy.get_trades_for_year("DDL", "2019")

# Get historical trades within a date range - supports: yyyy / mm/yyyy / dd/mm/yyyy
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

# Average last traded price over the last N sessions or 1M, 3M, 6M 1Y (ending at latest session)
avg_price_latest = financegy.get_average_price("DDL", "1M")

# Volatility over the last N sessions (weekly log-return volatility + annualized)
volatility = financegy.get_sessions_volatility("DDL", 30)

# Year-to-date high and low traded prices
ytd_high_low = financegy.get_ytd_high_low("DDL")

# Get top market gainers and losers (based on % price change)
movers = financegy.get_movers()

# Get overall market snapshot (Symbol | Name | LTP | Prev Close | Price Change | PC% | YTD High | YTD Low)
market_snapshot = financegy.get_market_snapshot()

# --------------------------
# Portfolio / Position Calculations
# --------------------------

# Calculate the current market value of a position
position_value = financegy.calculate_position_value("DDL", shares=50)

# Calculate unrealized gain or loss for a position
position_return = financegy.calculate_position_return(
    symbol="DDL",
    shares=50,
    purchase_price=250
)

# Calculate percentage return for a position
position_return_percent = financegy.calculate_position_return_percent(
    symbol="DDL",
    shares=50,
    purchase_price=250
)

# Portfolio-level summary
portfolio = [
    {"symbol": "DTC", "shares": 100, "purchase_price": 300},
    {"symbol": "DDL", "shares": 50, "purchase_price": 250},
]

portfolio_summary = financegy.calculate_portfolio_summary(portfolio)

# --------------------------
# Utilities
# --------------------------

# Convert results to a DataFrame
df = financegy.to_dataframe(securities)

# Export to CSV / Excel
financegy.save_to_csv(securities, filename="securities.csv", silent=True)
financegy.save_to_excel(securities, filename="securities.xlsx", silent=True)

# Purge invalid cache files (not from the current week)
financegy.purge_old_cache_files()

# Clear FinanceGY cache directory
financegy.clear_cache(silent=True)
```

---

## API Reference

### Core Data Retrieval

| Function                                              | Description                                                                          |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------ |
| `get_securities()`                                    | Returns all currently traded securities on the GSE.                                  |
| `get_active_securities()`                             | Returns active securities (symbol and company name) from the most recent session.    |
| `get_recent_session()`                                | Returns the most recent trading session number.                                      |
| `get_session_date()`                                  | Returns the date for a specified trading session.                                    |
| `get_security_by_symbol(symbol)`                      | Returns the full security name for a ticker symbol.                                  |
| `get_recent_trade(symbol)`                            | Returns the most recent trade information for the given security.                    |
| `get_security_recent_year(symbol)`                    | Returns all trade data for the most recent year available for the selected security. |
| `get_traded_years(symbol)`                            | Returns all trade years for a selected security.                                     |
| `get_security_earliest_year(symbol)`                  | Returns the earliest financial year available for the selected security.             |
| `get_security_latest_year(symbol)`                    | Returns the latest financial year available for the selected security.               |
| `get_security_full_history(symbol)`                   | Returns the full trade history for the selected security across all available years. |
| `get_session_trades(session)`                         | Returns trade data for all securities during a specific trading session.             |
| `get_year_sessions(year)`                             | Returns all sessions for a selected trading year.                                    |
| `get_year_sessions_snapshot(year)`                    | Returns trade snapshots for all sessions in a selected year.                         |
| `get_security_session_trade(symbol, session)`         | Returns trade data for a specific security during a specific session.                |
| `search_securities(query)`                            | Searches securities whose names or ticker symbols match the given query.             |
| `get_trades_for_year(symbol, year)`                   | Returns all trade records for a specific security during a given year.               |
| `get_historical_trades(symbol, start_date, end_date)` | Returns historical trades within the specified date range.                           |

### Analytics / Calculation Functions

| Function                                                         | Description                                                                                                               |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `get_previous_close(symbol)`                                     | Returns the most recent closing/last trade price.                                                                         |
| `get_price_change(symbol)`                                       | Returns absolute price difference vs previous session close.                                                              |
| `get_price_change_percent(symbol)`                               | Returns percent price change vs previous session close.                                                                   |
| `get_latest_session_for_symbol(symbol)`                          | Returns the latest trade dictionary for the symbol.                                                                       |
| `get_sessions_average_price(symbol, session_start, session_end)` | Returns the average last traded price over a session range.                                                               |
| `get_average_price(symbol, session_number)`                      | Returns the average last traded price over the last N sessions or 1M, 3M, 6M or 1Y.                                       |
| `get_sessions_volatility(symbol, session_number)`                | Returns volatility (log-return + annualized) over the last N sessions.                                                    |
| `get_ytd_high_low(symbol)`                                       | Returns year-to-date highest and lowest traded prices.                                                                    |
| `get_movers()`                                                   | Returns top market gainers, losers, and unchanged securities (% change).                                                  |
| `get_market_snapshot()`                                          | Returns overall market snapshot (Symbol, Company Name, LTP, Prev Close, Price Change, Price Change %, YTD High, YTD Low). |

### Portfolio / Position Functions

| Function                                                            | Description                                                                     |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `calculate_position_value(symbol, shares)`                          | Calculates the current market value of a position using the latest trade price. |
| `calculate_position_return(symbol, shares, purchase_price)`         | Calculates the unrealized gain or loss for a position.                          |
| `calculate_position_return_percent(symbol, shares, purchase_price)` | Calculates the percentage return for a position.                                |
| `calculate_portfolio_summary(positions)`                            | Computes a full portfolio summary including totals and per-position breakdown.  |

### Utilities

| Function                                                               | Description                                                    |
| ---------------------------------------------------------------------- | -------------------------------------------------------------- |
| `to_dataframe(data)`                                                   | Converts FinanceGY list/dict results into a pandas DataFrame.  |
| `save_to_csv(data, filename="output.csv", path=None, silent=False)`    | Saves data to a CSV file.                                      |
| `save_to_excel(data, filename="output.xlsx", path=None, silent=False)` | Saves data to an Excel file.                                   |
| `purge_old_cache_files()`                                              | Purges invalid cache files from the FinanceGY cache directory. |
| `clear_cache(silent=False)`                                            | Completely clears the FinanceGY cache directory.               |

---

## Caching System

FinanceGY includes a lightweight local caching system designed to speed up repeated requests and reduce unnecessary API calls.

Whenever you call a data retrieval function (such as `get_securities()` or `get_recent_trade()`), FinanceGY automatically checks whether a cached response already exists for that specific query:

If a valid cache file from the current week (Monday-Sunday) is found, the result is returned instantly from the cache.

If the cache is missing, corrupted, or belongs to a previous week, it is automatically deleted, and fresh data is fetched from the GSE and stored.

Cache validity is determined based on a weekly cycle. At Monday 00:00, all previously stored cache entries are considered expired. Stale cache files are removed automatically when accessed, ensuring the cache remains clean and up to date without requiring manual intervention.

All cache files are stored in a local `cache/` directory as small JSON files containing the retrieved data and a timestamp.

You can manually clear all cached data at any time:

```python
import financegy

financegy.clear_cache()
```

This will delete all cached files and force the next data request to fetch fresh data directly from the source.

You can also choose to only clear invalid cache files (not from the current week).:

```python
import financegy

financegy.purge_old_cache_files()
```

**Note:** This will be done automatically if the system ever tries to access a cache file and finds it is stale.\*

If you prefer to bypass the cache for a specific call, simply pass `use_cache=False` to any function. For example:

```python
# Force a fresh fetch from the GSE, ignoring cached data
recent_trade = financegy.get_recent_trade("DDL", use_cache=False)
```

By default, caching is enabled for all supported functions unless explicitly turned off.

---

## Example Use Case

```python
import financegy

ddl_recent = financegy.get_security_recent("DDL")
print(ddl_recent)
```
