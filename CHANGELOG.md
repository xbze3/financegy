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
