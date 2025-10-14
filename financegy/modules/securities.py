from financegy.core import request_handler, parser
from financegy.cache import cache_manager

def get_securities(use_cache=True):
    """Get names of all currently traded securities"""

    func_name = "get_securities"

    if use_cache:
        cached = cache_manager.load_cache(func_name)
        if cached:
            return parser.parse_get_securities(cached)

    path = "/securities/"
    html = request_handler.fetch_page(path)

    cache_manager.save_cache(func_name, html)

    return parser.parse_get_securities(html);

def get_security_by_symbol(symbol: str, use_cache=True):
    """Get the security details by its ticker symbol"""

    securities = get_securities()

    symbol = symbol.strip().upper()

    return next(
        (security['name'] for security in securities if security["symbol"].upper() == symbol),
        None,
    )

def get_security_recent_year(symbol:str, use_cache=True):
    """Get the most recent year's trade data for any of the traded securities"""

    func_name = "get_security_recent_year"

    security_name = get_security_by_symbol(symbol)
    security_name = security_name.lower().replace(" ", "-")

    if use_cache:
        cached = cache_manager.load_cache(func_name, symbol)
        if cached:
            return parser.parse_get_security_recent_year(cached)

    path = "/security/" + security_name
    html = request_handler.fetch_page(path)

    cache_manager.save_cache(func_name, html, symbol)

    return parser.parse_get_security_recent_year(html)

def get_recent_trade(symbol: str, use_cache=True):
    """Get the most recent trade data for any of the traded securities"""

    func_name = "get_recent_trade"
    
    security_name = get_security_by_symbol(symbol)
    security_name = security_name.lower().replace(" ", "-")

    if use_cache:
        cached = cache_manager.load_cache(func_name, symbol)
        if cached:
            return parser.parse_get_recent_trade(cached)

    path = "/security/" + security_name
    html = request_handler.fetch_page(path)

    cache_manager.save_cache(func_name, html, symbol)

    return parser.parse_get_recent_trade(html)

def get_session_trades(session: str, use_cache=True):
    """Get the session trade data for all the available securities"""

    func_name = "get_session_trades"

    if use_cache:
        cached = cache_manager.load_cache(func_name, session)
        if cached:
            return parser.parse_get_session_trades(cached)

    path = f"/financial_session/{session}/"
    html = request_handler.fetch_page(path)

    cache_manager.save_cache(func_name, html, session)

    return parser.parse_get_session_trades(html)

def get_security_session_trade(symbol: str, session: str, use_cache=True):
    """Get the session trade data for a given security"""

    func_name = "get_security_session_trade"

    symbol = symbol.strip().upper()

    if use_cache:
        cached = cache_manager.load_cache(func_name, symbol, session)
        if cached:
            return parser.parse_get_security_session_trade(symbol, cached)

    path = f"/financial_session/{session}/"
    html = request_handler.fetch_page(path)

    cache_manager.save_cache(func_name, html, symbol, session)

    return parser.parse_get_security_session_trade(symbol, html)

def get_trades_for_year(symbol: str, year: str, use_cache=True):
    """Get security trade information from a specific year"""

    func_name = "get_trades_for_year"

    symbol = symbol.strip().upper()

    if use_cache:
        cached = cache_manager.load_cache(func_name, symbol, year)
        if cached:
            return parser.parse_get_trades_for_year(year, cached)

    security_name = get_security_by_symbol(symbol)
    security_name = security_name.lower().replace(" ", "-")

    path = f"/security/{security_name}/"
    html = request_handler.fetch_page(path)

    cache_manager.save_cache(func_name, html, symbol, year)

    return parser.parse_get_trades_for_year(year, html)

def get_historical_trades(symbol: str, start_date: str, end_date: str, use_cache=True):
    """Get historical trade data for a date range"""

    func_name = "get_historical_trades"

    symbol = symbol.strip().upper()

    if use_cache:
        cached = cache_manager.load_cache(func_name, symbol, start_date, end_date)
        if cached:
            return parser.parse_get_historical_trades(start_date, end_date, cached)

    security_name = get_security_by_symbol(symbol)
    security_name = security_name.lower().replace(" ", "-")

    path = f"/security/{security_name}/"
    html = request_handler.fetch_page(path)

    cache_manager.save_cache(func_name, html, symbol, start_date, end_date)

    return parser.parse_get_historical_trades(start_date, end_date, html)

def search_securities(query: str, use_cache=True):
    """Search securities by symbol or name (partial match)"""

    query = query.lower().strip()
    all_securities = get_securities()

    matches = [
        sec for sec in all_securities
        if query in sec["symbol"].lower() or query in sec["name"].lower()
    ]

    return matches