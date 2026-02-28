from financegy.modules import securities as sec
from financegy.cache import cache_manager
from financegy.core import parser, request_handler
from financegy.helpers.to_float import to_float


def get_market_snapshot(use_cache: bool = True):
    """Get market snapshot (Symbol | Name | LTP | Prev Close | Price Change | PC% | YTD High | YTD Low)"""

    func_name = "get_market_snapshot"

    if use_cache:
        cached = cache_manager.load_cache(func_name)
        if cached:
            return cached

    active_securities = get_active_securities()

    security_snapshot = []

    for security in active_securities:
        symbol = security["symbol"]
        security_name = security["name"]

        pct = sec.get_price_change_percent(symbol, use_cache=use_cache)
        ytd_high_low = sec.get_ytd_high_low(symbol)

        if not pct:
            continue

        change_pct = None
        prev_raw = None
        recent_raw = None

        if pct:
            change_pct = pct.get("price_change_percent")
            prev_raw = pct.get("previous_trade", {}).get("last_trade_price")
            recent_raw = pct.get("recent_trade", {}).get("last_trade_price")

        prev_price = to_float(prev_raw)
        recent_price = to_float(recent_raw)

        price_change = None
        if prev_price is not None and recent_price is not None:
            price_change = recent_price - prev_price

        ytd_low = None
        ytd_high = None
        if ytd_high_low:
            low = ytd_high_low.get("low")
            high = ytd_high_low.get("high")
            ytd_low = low.get("price") if low else None
            ytd_high = high.get("price") if high else None

        data = {
            "symbol": symbol,
            "name": security_name,
            "last_trade_price": recent_raw,
            "previous_close": prev_raw,
            "price_change": price_change,
            "price_change_percent": change_pct,
            "ytd_low": ytd_low,
            "ytd_high": ytd_high,
        }

        security_snapshot.append(data)

    parsed_data = security_snapshot
    cache_manager.save_cache(func_name, parsed_data)

    return parsed_data


def get_movers(use_cache: bool = True):
    """Get the top market gainers and losers (%)"""

    func_name = "get_top_movers"

    if use_cache:
        cached = cache_manager.load_cache(func_name)
        if cached:
            return cached

    active_securities = get_active_securities()

    gainers = []
    losers = []
    no_change = []

    for security in active_securities:
        symbol = security["symbol"]
        pct = sec.get_price_change_percent(symbol, use_cache=use_cache)
        if not pct:
            continue

        change_pct = pct.get("price_change_percent")
        if change_pct is None:
            continue

        prev_raw = pct["previous_trade"].get("last_trade_price")
        recent_raw = pct["recent_trade"].get("last_trade_price")

        try:
            prev_price = to_float(prev_raw)
            recent_price = to_float(recent_raw)
        except (TypeError, ValueError):
            prev_price = None
            recent_price = None

        price_change = None

        if prev_price is not None and recent_price is not None:
            price_change = recent_price - prev_price

        data = {
            "symbol": symbol,
            "price_change": price_change,
            "price_change_percent": change_pct,
            "last_trade_price": recent_raw,
            "previous_close": prev_raw,
        }

        if change_pct > 0:
            gainers.append(data)
        elif change_pct < 0:
            losers.append(data)
        else:
            no_change.append(data)

    parsed_data = {"gainers": gainers, "losers": losers, "no_change": no_change}
    cache_manager.save_cache(func_name, parsed_data)

    return parsed_data


def get_active_securities(use_cache: bool = True):
    """Get all active securities"""

    func_name = "get_active_securities"

    if use_cache:
        cached = cache_manager.load_cache(func_name)
        if cached:
            return cached

    most_recent_session = sec.get_recent_session()

    path = f"/trade_session/{most_recent_session}"
    html = request_handler.fetch_page(path)

    parsed_data = parser.parse_get_active_securities(html)
    cache_manager.save_cache(func_name, parsed_data)

    return parsed_data
