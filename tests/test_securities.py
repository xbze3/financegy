from financegy import *
import pandas as pd


# def test_get_securities():
#     result = get_securities()
#     assert isinstance(result, list)


# def test_get_security_by_symbol():
#     result = get_security_by_symbol(symbol="ddl")
#     assert isinstance(result, (str, type(None)))


# def test_get_recent_trade():
#     result = get_recent_trade(symbol="dtc")
#     assert isinstance(result, (dict, type(None)))


# def test_get_previous_close():
#     result = get_previous_close(symbol="ddl")
#     assert isinstance(result, (dict, type(None)))


# def test_get_price_change():
#     result = get_price_change(symbol="dtc")
#     assert isinstance(result, (dict, type(None)))


# def test_get_price_change_percent():
#     result = get_price_change_percent(symbol="ddl")
#     assert isinstance(result, (dict, type(None)))


# def test_get_security_recent_year():
#     result = get_security_recent_year(symbol="RBL")
#     assert isinstance(result, (list, type(None)))


# def test_get_session_trades():
#     result = get_session_trades(session="1135")
#     assert isinstance(result, (list, type(None)))


# def test_get_security_session_trade():
#     result = get_security_session_trade(symbol="ddl", session="1053")
#     assert isinstance(result, (dict, type(None)))


# def test_get_sessions_average_price():
#     result = get_sessions_average_price(
#         symbol="ddl", session_start="1053", session_end="1060"
#     )
#     assert isinstance(result, (dict, type(None)))


# def test_get_average_price():
#     result = get_average_price(symbol="ddl", session_number=31)
#     assert isinstance(result, (dict, type(None)))


# def test_get_latest_session_for_symbol():
#     result = get_latest_session_for_symbol(symbol="ddl")
#     assert isinstance(result, (dict, type(None)))


# def test_get_ytd_high_low():
#     result = get_ytd_high_low(symbol="ddl")
#     assert isinstance(result, (dict, type(None)))


# def test_get_security_earliest_year():
#     result = get_security_earliest_year("bdh")
#     assert isinstance(result, str)


# def test_get_security_latest_year():
#     result = get_security_latest_year("bdh")
#     assert isinstance(result, str)


# def test_get_trades_for_year():
#     result = get_trades_for_year(symbol="ddl", year="2020")
#     assert isinstance(result, list)


# def test_get_historical_trades():
#     result = get_historical_trades(
#         symbol="ddl", start_date="06/2020", end_date="01/2022"
#     )
#     assert isinstance(result, list)


# def test_get_security_full_history():
#     result = get_security_full_history("bdh")
#     assert isinstance(result, list)


# def test_get_sessions_volatility():
#     result = get_sessions_volatility(symbol="dtc", session_number=3)
#     assert isinstance(result, dict)


# def test_search_securities():
#     result = search_securities(query="ddl")
#     assert isinstance(result, list)

# def test_get_recent_session():
#     result = get_recent_session()
#     assert isinstance(result, str)


# def test_get_active_securities():
#     result = get_active_securities()
#     assert isinstance(result, list)


# def test_calculate_position_value():
#     result = calculate_position_value("ddl", "10")
#     assert isinstance(result, (dict, type(None)))


# def test_calculate_position_return():
#     result = calculate_position_return("ddl", "10", "31")
#     assert isinstance(result, (dict, type(None)))


# def test_calculate_position_return_percent():
#     result = calculate_position_return_percent("ddl", "10", "31")
#     assert isinstance(result, dict)


# def test_calculate_portfolio_summary():
#     positions = [
#         {"symbol": "DTC", "shares": "100", "purchase_price": "300"},
#         {"symbol": "DDL", "shares": "50", "purchase_price": "250"},
#     ]
#     result = calculate_portfolio_summary(positions)
#     assert isinstance(result, dict)


# def test_to_dataframe():
#     result = to_dataframe(get_securities())
#     assert isinstance(result, pd.DataFrame)


# def test_save_to_csv():
#     result = get_securities()
#     save_to_csv(result, silent=True)
#     assert isinstance(result, list)


# def test_save_excel():
#     result = get_securities()
#     save_to_excel(result, silent=True)
#     assert isinstance(result, list)


# def test_clear_cache():
#     result = clear_cache(silent=True)
#     assert isinstance(result, bool)
