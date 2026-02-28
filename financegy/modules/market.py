from financegy.modules import securities as sec
from financegy.cache import cache_manager
from financegy.core import parser, request_handler


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
        pct = sec.get_price_change_percent(symbol)
        data = {
            "symbol": symbol,
            "price_change_percent": pct["price_change_percent"],
            "last_trade_price": pct["recent_trade"]["last_trade_price"],
            "previous_close": pct["previous_trade"]["last_trade_price"],
        }

        if pct["price_change_percent"] is None:
            continue

        if pct["price_change_percent"] > 0:
            gainers.append(data)

        elif pct["price_change_percent"] < 0:
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
