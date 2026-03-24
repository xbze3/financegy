## v4.5 - 2026-03-24

### Added

- `get_year_sessions_snapshot(year)` - Returns trade snapshots for all sessions in a selected year.

### Changed

- Accessing a stale cache entry now triggers a purge of all stale cache files.

### Notes

- Non-breaking update to cache load logic

---

## v4.3 - 2026-03-18

### Added

- `purge_old_cache_files()` - Purges invalid cache files (not from the current week, Monday 00:00 -> Sunday)

### Changed

- Cache expiration logic updated from a fixed time-based system (max_age_days) to a weekly invalidation model (resets every Monday at 00:00)

### Notes

- Non-breaking update to cache invalidation logic

---

## v4.2.3 - 2026-03-13

### Added

- `get_year_sessions()` - Returns all sessions for a selected trading year.

### Notes

- Minor feature addition.

---

## v4.2.1 - 2026-03-06

### Added

- `get_traded_years()` - Returns all traded years for a selected security.

### Notes

- Minor feature addition.

---

## v4.2.0 - 2026-02-28

### Added

- `get_market_snapshot()` - Returns a consolidated market overview including latest price, previous close, price change, percentage change, and YTD high/low.
- `get_movers()` - Returns top gainers, losers, and unchanged securities based on percentage price movement.
- `get_session_date()` - Returns the date for a specified session.
- Enhanced `get_average_price()` to support time-based shortcuts:
    - `1M` - 1 month
    - `3M` - 3 months
    - `6M` - 6 months
    - `1Y` - 1 year

### Changed

- All numeric values now return as floating-point numbers.
    - Prices, percentage changes, volatility, averages, and calculated metrics are normalized to `float`.
    - Removes original string formatting from the GSE website (e.g., comma-separated values).
- `get_average_price()` now accepts:
    - Integer session counts (previous behavior)
    - Time-based shorthand strings (`1M`, `3M`, `6M`, `1Y`)

### Notes

- Minor breaking change: numeric values previously returned as formatted strings are now `float`.
- Function signatures remain backward compatible.
- This release improves analytical flexibility and data consistency for quantitative workflows.

---

## v4.1.0 - 2026-02-17

### Added

- Upgraded caching system to parsing-level caching, storing parsed results instead of raw HTML.
- Cached results now returned directly, reducing redundant parsing and improving performance.

### Changed

- Cache now automatically deletes stale files older than 3 days (updated from 7).
- Functions that previously returned parsed data from raw HTML now use cached parsed results when available.
- Performance improvements: test suite runtime decreased from ~231s (cold start) → ~18s (request-level cache) → ~2.6s (parser-level cache).

### Notes

- All function signatures remain the same; this is a backward-compatible enhancement.
- Users will notice dramatically faster response times, especially for historical or bulk data requests.
