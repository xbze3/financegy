from financegy.core import request_handler, parser

def get_securities():
    """Get names of all currently traded securities"""
    path = "/securities/"
    html = request_handler.fetch_page(path)
    return parser.parse_get_securities(html);

def get_security_by_symbol(symbol: str):
    """Get the security details by its ticker symbol"""
    securities = get_securities()

    symbol = symbol.strip().upper()

    return next(
        (security['name'] for security in securities if security["symbol"].upper() == symbol),
        None,
    )

def get_security_recent_year(symbol:str):
    """Get the most recent year's trade data for any of the traded securities"""

    security_name = get_security_by_symbol(symbol)
    security_name = security_name.lower().replace(" ", "-")

    path = "/security/" + security_name
    html = request_handler.fetch_page(path)
    return parser.parse_get_security_recent_year(html)

def get_security_recent(symbol: str):
    """Get the most recent trade data for any of the traded securities"""
    
    security_name = get_security_by_symbol(symbol)
    security_name = security_name.lower().replace(" ", "-")

    path = "/security/" + security_name
    html = request_handler.fetch_page(path)
    return parser.parse_get_security_recent(html)

def get_securites_session(session: str):
    """Get the session trade data for all the available securities"""

    path = f"/financial_session/{session}/"
    html = request_handler.fetch_page(path)
    return parser.parse_get_securites_session(html)