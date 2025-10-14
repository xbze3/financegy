from financegy import *

def test_get_securities():
    result = get_securities()
    assert isinstance(result, list)

def test_get_security_by_symbol():
    result = get_security_by_symbol(symbol="ddl")    
    assert isinstance(result, (str, type(None)))

def test_get_recent_trade():
    result = get_recent_trade(symbol="ddl")
    assert isinstance(result, (dict, type(None)))

def test_get_security_recent_year():
    result = get_security_recent_year(symbol="RBL")
    assert isinstance(result, (list, type(None)))
    
def test_get_session_trades():
    result = get_session_trades(session="1135")
    assert isinstance(result, (list, type(None)))

def test_get_security_session_trade():
    result = get_security_session_trade(symbol="ddl", session="1136")
    assert isinstance(result, (dict, type(None)))

def test_get_trades_for_year():
    result = get_trades_for_year(symbol="ddl", year="2020")
    assert isinstance(result, (list, type(None)))

def test_get_historical_trades():
    result = get_historical_trades(symbol="ddl", start_date="01/06/2020", end_date="01/01/2022")
    assert isinstance(result, (list, type(None)))

def test_search_securities():
    result = search_securities(query="ddl")
    assert isinstance(result, list)

# def test_clear_cache():
#     result = clear_cache()
#     assert isinstance(result, bool)
    