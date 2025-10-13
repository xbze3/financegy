from financegy import *
from bs4 import BeautifulSoup

# def test_get_securities():
#     result = get_securities()
#     assert isinstance(result, list)

# def test_get_security_by_symbol():
#     result = get_security_by_symbol(symbol="ddl")
#     assert isinstance(result, (str, type(None)))

# def test_get_security_recent():
#     result = get_security_recent(symbol="ddl")
#     assert isinstance(result, (dict, type(None)))

# def test_get_security_recent_year():
#     result = get_security_recent_year(symbol="ddl")
#     assert isinstance(result, (list, type(None)))
    
# def test_get_securites_session():
#     result = get_securites_session(session="1136")
#     assert isinstance(result, (list, type(None)))

def test_get_security_session():
    result = get_security_session(symbol="ddl", session="1136")
    assert isinstance(result, (dict, type(None)))
    
    

