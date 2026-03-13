from financegy.core import request_handler, parser
from financegy.cache import cache_manager
from datetime import datetime
import math


def get_securities(use_cache=True):
    """Get names of all currently traded securities"""

    func_name = "get_securities"

    if use_cache:
        cached = cache_manager.load_cache(func_name)
        if cached:
            return cached

    path = "/securities/"
    html = request_handler.fetch_page(path)

    parsed_data = parser.parse_get_securities(html)
    cache_manager.save_cache(func_name, parsed_data)

    return parsed_data


def get_recent_session(use_cache=True):
    """Get the most recent trading session"""

    func_name = "get_recent_session"

    if use_cache:
        cached = cache_manager.load_cache(func_name)
        if cached:
            return cached

    path = "/trades/"
    html = request_handler.fetch_page(path)

    parsed_data = parser.parse_get_recent_session(html)
    cache_manager.save_cache(func_name, parsed_data)

    return parsed_data


def get_security_by_symbol(symbol: str):
    """Get the security details by its ticker symbol"""

    securities = get_securities()

    symbol = symbol.strip().upper()

    return next(
        (
            security["name"]
            for security in securities
            if security["symbol"].upper() == symbol
        ),
        None,
    )


def get_security_recent_year(symbol: str, use_cache=True):
    """Get the most recent year's trade data for any of the traded securities"""

    func_name = "get_security_recent_year"

    security_name = get_security_by_symbol(symbol)
    security_name = security_name.lower().replace(" ", "-")

    if use_cache:
        cached = cache_manager.load_cache(func_name, symbol)
        if cached:
            return cached

    path = "/security/" + security_name
    html = request_handler.fetch_page(path)

    parsed_data = parser.parse_get_security_recent_year(html)
    cache_manager.save_cache(func_name, parsed_data, symbol)

    return parsed_data


def get_recent_trade(symbol: str, use_cache=True):
    """Get the most recent trade data for any of the traded securities"""

    func_name = "get_recent_trade"

    security_name = get_security_by_symbol(symbol)
    security_name = security_name.lower().replace(" ", "-")

    if use_cache:
        cached = cache_manager.load_cache(func_name, symbol)
        if cached:
            return cached

    path = "/security/" + security_name
    html = request_handler.fetch_page(path)

    parsed_data = parser.parse_get_recent_trade(html)
    cache_manager.save_cache(func_name, parsed_data, symbol)

    return parsed_data


def get_security_earliest_year(symbol: str, use_cache=True):
    """Get the earliest trading year for any of the traded securities"""

    func_name = "get_security_earliest_year"

    security_name = get_security_by_symbol(symbol)
    security_name = security_name.lower().replace(" ", "-")

    if use_cache:
        cached = cache_manager.load_cache(func_name, symbol)
        if cached:
            return cached

    path = f"/security/{security_name}/"
    html = request_handler.fetch_page(path)

    parsed_data = parser.parse_get_security_earliest_year(html)
    cache_manager.save_cache(func_name, parsed_data, symbol)

    return parsed_data


def get_security_latest_year(symbol: str, use_cache=True):
    """Get the latest financial year available for a given security."""

    func_name = "get_security_latest_year"

    security_name = get_security_by_symbol(symbol)
    security_name = security_name.lower().replace(" ", "-")

    if use_cache:
        cached = cache_manager.load_cache(func_name, symbol)
        if cached:
            return cached

    path = f"/security/{security_name}/"
    html = request_handler.fetch_page(path)

    parsed_data = parser.parse_get_security_latest_year(html)
    cache_manager.save_cache(func_name, parsed_data, symbol)

    return parsed_data


def get_previous_close(symbol: str, use_cache=True):
    """Get the most recent closing price for any of the traded securities"""

    func_name = "get_previous_close"

    security_name = get_security_by_symbol(symbol)
    security_name = security_name.lower().replace(" ", "-")

    if use_cache:
        cached = cache_manager.load_cache(func_name, symbol)
        if cached:
            return cached

    path = "/security/" + security_name
    html = request_handler.fetch_page(path)

    parsed_data = parser.parse_get_previous_close(html)
    cache_manager.save_cache(func_name, parsed_data, symbol)

    return parsed_data


def get_price_change(symbol: str, use_cache=True):
    """Get absolute price difference between the most recent trade and the previous session close."""

    func_name = "get_price_change"

    security_name = get_security_by_symbol(symbol)
    security_name = security_name.lower().replace(" ", "-")

    if use_cache:
        cached = cache_manager.load_cache(func_name, symbol)
        if cached:
            return cached

    path = "/security/" + security_name
    html = request_handler.fetch_page(path)

    parsed_data = parser.parse_get_price_change(html)
    cache_manager.save_cache(func_name, parsed_data, symbol)

    return parsed_data


def get_price_change_percent(symbol: str, use_cache=True):
    """Get the percentage price change between the most recent trade and the previous session close."""

    func_name = "get_price_change_percent"

    security_name = get_security_by_symbol(symbol)
    security_name = security_name.lower().replace(" ", "-")

    if use_cache:
        cached = cache_manager.load_cache(func_name, symbol)
        if cached:
            return cached

    path = "/security/" + security_name
    html = request_handler.fetch_page(path)

    parsed_data = parser.parse_get_price_change_percent(html)
    cache_manager.save_cache(func_name, parsed_data, symbol)

    return parsed_data


def get_latest_session_for_symbol(symbol: str, use_cache: bool = True):
    """
    Fetch the security page, parse the most recent trade, return its session as int.
    """

    func_name = "get_latest_session_for_symbol"
    symbol = symbol.strip().upper()

    security_name = get_security_by_symbol(symbol)
    security_name = security_name.lower().replace(" ", "-")

    if use_cache:
        cached = cache_manager.load_cache(func_name, symbol)
        if cached:
            return cached

    path = "/security/" + security_name
    html = request_handler.fetch_page(path)

    parsed_data = parser.parse_get_recent_trade(html)
    cache_manager.save_cache(func_name, parsed_data, symbol)

    if not parsed_data or not parsed_data.get("session"):
        raise ValueError(f"Could not determine latest session for {symbol}")

    return parsed_data


def get_sessions_average_price(
    symbol: str, session_start: str, session_end: str, use_cache=True
):
    """Get the average last traded price of the security over a specified session range."""

    func_name = "get_sessions_average_price"
    start = int(session_start)
    end = int(session_end)
    symbol = symbol.strip().upper()

    if end < start:
        raise ValueError("session_end must be >= session_start")

    prices_by_session: dict[int, float] = {}

    for session in range(start, end + 1):
        if use_cache:
            cached = cache_manager.load_cache(func_name, symbol, session)
            if cached:
                price = cached
            else:
                path = f"/financial_session/{session}/"
                html = request_handler.fetch_page(path)
                price = parser.parse_get_sessions_average_price(symbol, html)
                cache_manager.save_cache(func_name, price, symbol, session)
        else:
            path = f"/financial_session/{session}/"
            html = request_handler.fetch_page(path)
            price = parser.parse_get_sessions_average_price(symbol, html)

        if price is not None:
            prices_by_session[session] = price

    if not prices_by_session:
        raise ValueError(f"No prices found for {symbol} in sessions {start}..{end}")

    avg = round(sum(prices_by_session.values()) / len(prices_by_session), 2)

    return {
        "symbol": symbol,
        "session_start": start,
        "session_end": end,
        "observations": len(prices_by_session),
        "average_price": avg,
        "prices_by_session": prices_by_session,
    }


def get_average_price(symbol: str, session_number, use_cache=True):
    """Average LTP over the most recent `session_number` sessions (ending at latest session)."""

    func_name = "get_average_price"
    symbol = symbol.strip().upper()

    if isinstance(session_number, str):
        period = session_number.strip().upper()
        period_map = {
            "1M": 4,
            "3M": 13,
            "6M": 26,
            "1Y": 52,
        }
        if period not in period_map:
            raise ValueError(
                "session_number must be a positive int or one of: 1M, 3M, 6M, 1Y"
            )
        session_number_requested = period
        session_count = period_map[period]
    else:
        session_number_requested = session_number
        session_count = session_number

    if session_count <= 0:
        raise ValueError("session_number must be a positive integer")

    latest = get_latest_session_for_symbol(symbol, use_cache=use_cache)
    end = int(latest["session"])
    start = max(1, end - session_count + 1)
    start_session_date = get_session_date(start)

    prices_by_session = {}

    for session in range(start, end + 1):
        if use_cache:
            cached = cache_manager.load_cache(func_name, symbol, session)
            if cached:
                price = cached
            else:
                path = f"/financial_session/{session}/"
                html = request_handler.fetch_page(path)
                price = parser.parse_get_average_price(symbol, html)
                cache_manager.save_cache(func_name, price, symbol, session)
        else:
            path = f"/financial_session/{session}/"
            html = request_handler.fetch_page(path)
            price = parser.parse_get_average_price(symbol, html)

        if price is not None:
            prices_by_session[session] = price

    if not prices_by_session:
        raise ValueError(f"No prices found for {symbol} in sessions {start}..{end}")

    avg = round(sum(prices_by_session.values()) / len(prices_by_session), 2)

    return {
        "symbol": symbol,
        "latest_session": latest,
        "session_number_requested": session_number_requested,
        "session_start": start,
        "session_end": end,
        "session_start_date": start_session_date,
        "observations": len(prices_by_session),
        "average_price": avg,
        "prices_by_session": prices_by_session,
    }


def get_session_trades(session: str, use_cache=True):
    """Get the session trade data for all the available securities"""

    func_name = "get_session_trades"

    if use_cache:
        cached = cache_manager.load_cache(func_name, session)
        if cached:
            return cached

    path = f"/financial_session/{session}/"
    html = request_handler.fetch_page(path)

    parsed_data = parser.parse_get_session_trades(html)
    cache_manager.save_cache(func_name, parsed_data, session)

    return parsed_data


def get_year_sessions(year: str, use_cache=True):
    """Get all sessions in a selected year"""

    func_name = "get_year_sessions"
    current_year = datetime.now().year

    if year is None:
        raise ValueError("Year cannot be None")

    if not str(year).isdigit():
        raise ValueError(f"Invalid year value: {year}")

    year = int(year)

    if year > current_year:
        raise ValueError(f"Invalid year passed: {year} is in the future")

    if use_cache:
        cached = cache_manager.load_cache(func_name, year)
        if cached:
            return cached

    if year == current_year:
        path = "/financials/"
    else:
        path = f"/financials/{year}-2/"

    html = request_handler.fetch_page(path)

    session_data = parser.parse_get_year_sessions(html)

    if not session_data:
        return None

    year_session_data = []

    for session in session_data:
        year_session_data.append(
            {"session": session, "date": get_session_date(session)}
        )

    parsed_data = {"year": year, "sessions": year_session_data}

    cache_manager.save_cache(func_name, parsed_data, year)

    return parsed_data


def get_traded_years(symbol: str, use_cache=True):
    """Get traded years for specified security"""

    func_name = "get_traded_years"
    symbol = symbol.strip().upper()

    security_name = get_security_by_symbol(symbol)
    security_name = security_name.lower().replace(" ", "-")

    if use_cache:
        cached = cache_manager.load_cache(func_name, symbol)
        if cached:
            return cached

    path = f"/security/{security_name}/"
    html = request_handler.fetch_page(path)

    parsed_data = parser.parse_get_traded_years(html)
    cache_manager.save_cache(func_name, parsed_data, symbol)

    return parsed_data


def get_session_date(session: str, use_cache=True):
    """Get session date"""

    func_name = "get_session_date"

    if use_cache:
        cached = cache_manager.load_cache(func_name, session)
        if cached:
            return cached

    path = f"/financial_session/{session}/"
    html = request_handler.fetch_page(path)

    parsed_data = parser.parse_get_session_date(html)
    cache_manager.save_cache(func_name, parsed_data, session)

    return parsed_data


def get_security_session_trade(symbol: str, session: str, use_cache=True):
    """Get the session trade data for a given security"""

    func_name = "get_security_session_trade"

    symbol = symbol.strip().upper()

    if use_cache:
        cached = cache_manager.load_cache(func_name, symbol, session)
        if cached:
            return cached

    path = f"/financial_session/{session}/"
    html = request_handler.fetch_page(path)

    parsed_data = parser.parse_get_security_session_trade(symbol, html)
    cache_manager.save_cache(func_name, parsed_data, symbol, session)

    return parsed_data


def get_sessions_volatility(symbol: str, session_number: int, use_cache=True):
    """
    Volatility over the last `sessions` observed prices, ending at the latest session.
    Uses log returns and returns weekly volatility (std dev of weekly returns).
    """

    symbol = symbol.strip().upper()

    if session_number <= 1:
        raise ValueError(
            "session_number must be >= 2 (need at least 2 prices to compute returns)."
        )

    latest = get_latest_session_for_symbol(symbol, use_cache=use_cache)
    latest_session = int(latest["session"])

    target_prices = session_number
    prices: list[float] = []
    prices_by_session: dict[int, float] = {}

    func_name = "get_sessions_volatility"
    session = latest_session
    safety_limit = latest_session - (session_number * 5)

    while session >= 1 and session >= safety_limit and len(prices) < target_prices:
        if use_cache:
            cached = cache_manager.load_cache(func_name, symbol, session)
            if cached:
                price = cached
            else:
                path = f"/financial_session/{session}/"
                html = request_handler.fetch_page(path)
                price = parser.parse_get_session_ltp(symbol, html)
                cache_manager.save_cache(func_name, price, symbol, session)
        else:
            path = f"/financial_session/{session}/"
            html = request_handler.fetch_page(path)
            price = parser.parse_get_session_ltp(symbol, html)

        if price is not None:
            prices.append(price)
            prices_by_session[session] = price

        session -= 1

    if len(prices) < 2:
        raise ValueError(
            f"Not enough price data found for {symbol} to compute volatility."
        )

    prices.reverse()

    returns = []
    for i in range(1, len(prices)):
        prev_p = prices[i - 1]
        cur_p = prices[i]
        if prev_p and prev_p > 0 and cur_p and cur_p > 0:
            returns.append(math.log(cur_p / prev_p))

    if len(returns) < 2:
        raise ValueError("Not enough valid returns to compute volatility.")

    mean = sum(returns) / len(returns)
    variance = sum((r - mean) ** 2 for r in returns) / (len(returns) - 1)
    weekly_vol = round(math.sqrt(variance), 2)
    annualized_vol = round(weekly_vol * math.sqrt(52), 2)

    return {
        "symbol": symbol,
        "latest_session": latest_session,
        "requested_sessions": session_number,
        "prices_found": len(prices),
        "returns_count": len(returns),
        "weekly_volatility": weekly_vol,
        "annualized_volatility": annualized_vol,
        "prices_by_session": dict(sorted(prices_by_session.items())),
    }


def get_ytd_high_low(symbol: str, use_cache: bool = True):
    """Return year-to-date highest and lowest traded prices for the security."""

    func_name = "get_ytd_high_low"
    symbol = symbol.strip().upper()

    security_name = get_security_by_symbol(symbol)
    security_name = security_name.lower().replace(" ", "-")

    if use_cache:
        cached = cache_manager.load_cache(func_name, symbol)
        if cached:
            return cached

    path = f"/security/{security_name}/"
    html = request_handler.fetch_page(path)

    parsed_data = parser.parse_get_ytd_high_low(html)
    cache_manager.save_cache(func_name, parsed_data, symbol)

    return parsed_data


def get_trades_for_year(symbol: str, year: str, use_cache=True):
    """Get security trade information from a specific year"""

    func_name = "get_trades_for_year"
    symbol = symbol.strip().upper()

    if use_cache:
        cached = cache_manager.load_cache(func_name, symbol, year)
        if cached:
            return cached

    security_name = get_security_by_symbol(symbol)
    security_name = security_name.lower().replace(" ", "-")

    path = f"/security/{security_name}/"
    html = request_handler.fetch_page(path)

    parsed_data = parser.parse_get_trades_for_year(year, html)
    cache_manager.save_cache(func_name, parsed_data, symbol, year)

    return parsed_data


def get_historical_trades(symbol: str, start_date: str, end_date: str, use_cache=True):
    """Get historical trade data for a date range"""

    func_name = "get_historical_trades"
    symbol = symbol.strip().upper()

    if use_cache:
        cached = cache_manager.load_cache(func_name, symbol, start_date, end_date)
        if cached:
            return cached

    security_name = get_security_by_symbol(symbol)
    security_name = security_name.lower().replace(" ", "-")

    path = f"/security/{security_name}/"
    html = request_handler.fetch_page(path)

    parsed_data = parser.parse_get_historical_trades(start_date, end_date, html)
    cache_manager.save_cache(func_name, parsed_data, symbol, start_date, end_date)

    return parsed_data


def get_security_full_history(symbol: str, use_cache: bool = True):
    """
    Get the full trade history for a security by fetching each available year
    from earliest -> latest and concatenating all trades into one list.
    """

    symbol = symbol.strip().upper()

    try:
        earliest_year = get_security_earliest_year(symbol, use_cache=use_cache)
        if not earliest_year:
            raise ValueError(f"Could not determine earliest year for {symbol}")

        latest_year = get_security_latest_year(symbol, use_cache=use_cache)
        if not latest_year:
            raise ValueError(f"Could not determine latest year for {symbol}")

        if not str(earliest_year).isdigit() or not str(latest_year).isdigit():
            raise ValueError(
                f"Invalid year values for {symbol}: earliest={earliest_year}, latest={latest_year}"
            )

        start = int(earliest_year)
        end = int(latest_year)

        if end < start:
            raise ValueError(
                f"Latest year is earlier than earliest year for {symbol}: {start}..{end}"
            )

        full_trade_data = []

        for year in range(start, end + 1):
            year_trades = get_trades_for_year(symbol, str(year), use_cache=use_cache)

            if year_trades is None:
                continue

            if not isinstance(year_trades, list):
                raise ValueError(
                    f"Expected list of trades for {symbol} year {year}, got {type(year_trades)}"
                )

            full_trade_data.extend(year_trades)

        return full_trade_data

    except Exception as e:
        print(f"[get_security_full_history] Error building full history: {e}")
        return None


def search_securities(query: str):
    """Search securities by symbol or name (partial match)"""

    query = query.lower().strip()
    all_securities = get_securities()

    matches = [
        sec
        for sec in all_securities
        if query in sec["symbol"].lower() or query in sec["name"].lower()
    ]

    return matches
