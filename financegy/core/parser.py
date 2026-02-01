from bs4 import BeautifulSoup
from datetime import datetime
from financegy.helpers.to_float import to_float
from financegy.helpers.safe_text import safe_text


def parse_get_securities(html: str):
    """Extract security info"""

    try:
        soup = BeautifulSoup(html, "html.parser")
        security_info_html = soup.find("div", class_="securities")

        if not security_info_html:
            return []

        security_info = []
        securities = security_info_html.find_all("div", class_="security group")

        for security in securities:
            symbol = security.find_all("div", class_="acronym inline")[0].get_text(
                strip=True
            )
            name = security.find_all("div", class_="name inline")[0].get_text(
                strip=True
            )

            security_info.append({"symbol": symbol, "name": name})

        return security_info

    except Exception as e:
        print(f"[parse_get_securities] Error parsing securities: {e}")


def parse_get_security_recent_year(html: str):
    """Extract selected security's trade info from current year"""

    try:
        soup = BeautifulSoup(html, "html.parser")

        security_info_html = soup.find("div", class_="year slide")
        if not security_info_html:
            raise ValueError("Could not find 'div.year.slide' section in HTML.")

        trade_data = []

        trades = security_info_html.find_all("tr", class_="trade")
        if not trades:
            raise ValueError("No trade rows found for this security.")

        for trade in trades:
            trade_data.append(
                {
                    "session": safe_text(trade, "session"),
                    "session_date": safe_text(trade, "date"),
                    "last_trade_price": safe_text(trade, "name"),
                    "eps": safe_text(trade, "best bid"),
                    "pe_ratio": safe_text(trade, "vol bid"),
                    "dividends_paid_last_12_months": safe_text(trade, "best offer"),
                    "dividend_yield": safe_text(trade, "vol offer"),
                    "notes": safe_text(trade, "opening price"),
                }
            )

        return trade_data

    except Exception as e:
        print(f"[parse_get_security_recent_year] Error parsing HTML: {e}")
        return None


def parse_get_recent_trade(html: str):
    """Extract selected security's most recent trade info"""
    try:
        soup = BeautifulSoup(html, "html.parser")

        security_info_html = soup.find("div", class_="year slide")
        if not security_info_html:
            raise ValueError("Could not find 'div.year.slide' section in HTML.")

        trades = security_info_html.find_all("tr", class_="trade")
        if not trades:
            raise ValueError("No trade rows found for this security.")

        recent = trades[-1]

        recent_info = {
            "session": safe_text(recent, "session"),
            "session_date": safe_text(recent, "date"),
            "last_trade_price": safe_text(recent, "name"),
            "eps": safe_text(recent, "best bid"),
            "pe_ratio": safe_text(recent, "vol bid"),
            "dividends_paid_last_12_months": safe_text(recent, "best offer"),
            "dividend_yield": safe_text(recent, "vol offer"),
            "notes": safe_text(recent, "opening price"),
        }

        return recent_info

    except Exception as e:
        print(f"[parse_get_recent_trade] Error parsing HTML: {e}")
        return None


def parse_get_previous_close(html: str):
    """Extract selected security's most recent closing price"""
    try:
        soup = BeautifulSoup(html, "html.parser")

        security_info_html = soup.find("div", class_="year slide")
        if not security_info_html:
            raise ValueError("Could not find 'div.year.slide' section in HTML.")

        trades = security_info_html.find_all("tr", class_="trade")
        if not trades:
            raise ValueError("No trade rows found for this security.")

        recent = trades[-1]

        previous_close = {
            "last_trade_price": safe_text(recent, "name"),
        }

        return previous_close

    except Exception as e:
        print(f"[parse_get_previous_close] Error parsing HTML: {e}")
        return None


def parse_get_price_change(html: str):
    """Extract selected security's absolute price difference between the most recent trade and the previous session close"""

    try:
        soup = BeautifulSoup(html, "html.parser")

        security_info_html = soup.find("div", class_="year slide")
        if not security_info_html:
            raise ValueError("Could not find 'div.year.slide' section in HTML.")

        trades = security_info_html.find_all("tr", class_="trade")
        if not trades:
            raise ValueError("No trade rows found for this security.")

        recent = trades[-1]
        previous = trades[-2]

        price_change = {
            "recent_trade": {
                "session": safe_text(recent, "session"),
                "session_date": safe_text(recent, "date"),
                "last_trade_price": safe_text(recent, "name"),
            },
            "previous_trade": {
                "session": safe_text(previous, "session"),
                "session_date": safe_text(previous, "date"),
                "last_trade_price": safe_text(previous, "name"),
            },
            "price_difference": f"{(
                to_float(safe_text(recent, 'name'))
                - to_float(safe_text(previous, 'name'))
            )}",
        }

        return price_change

    except Exception as e:
        print(f"[parse_get_price_change] Error parsing HTML: {e}")
        return None


def parse_get_price_change_percent(html: str):
    """Extract selected security's percentage price difference between the most recent trade and the previous session close"""

    try:
        soup = BeautifulSoup(html, "html.parser")

        security_info_html = soup.find("div", class_="year slide")
        if not security_info_html:
            raise ValueError("Could not find 'div.year.slide' section in HTML.")

        trades = security_info_html.find_all("tr", class_="trade")
        if not trades:
            raise ValueError("No trade rows found for this security.")

        recent = trades[-1]
        previous = trades[-2]

        price_change_percent = {
            "recent_trade": {
                "session": safe_text(recent, "session"),
                "session_date": safe_text(recent, "date"),
                "last_trade_price": safe_text(recent, "name"),
            },
            "previous_trade": {
                "session": safe_text(previous, "session"),
                "session_date": safe_text(previous, "date"),
                "last_trade_price": safe_text(previous, "name"),
            },
            "price_change_percent": f"{round(((to_float(safe_text(recent, 'name')) - to_float(safe_text(previous, 'name'))) /  to_float(safe_text(previous, 'name'))) * 100, 2)}",
        }

        return price_change_percent

    except Exception as e:
        print(f"[parse_get_price_change_percent] Error parsing HTML: {e}")
        return None


def parse_get_sessions_average_price(symbol: str, html: str):
    """Extract average traded price of the security over a specified session range."""

    try:
        soup = BeautifulSoup(html, "html.parser")

        session_div = soup.find("div", class_="session")
        if not session_div:
            raise ValueError("Could not find 'div.session' section in HTML.")

        rows = session_div.find_all("tr", class_="trade")
        if not rows:
            raise ValueError("No trade rows found in session data.")

        for row in rows:
            row_symbol = safe_text(row, "mnemonic")
            if row_symbol == symbol:
                return to_float(safe_text(row, "name"))

        return None

    except Exception as e:
        print(f"[parse_get_sessions_average_price] Error parsing HTML: {e}")
        return None


def parse_get_average_price(symbol: str, html: str):
    """
    From a /financial_session/{session}/ page, return the last_trade_price (LTP)
    for the given symbol. Returns None if not found/unparseable.
    """
    try:
        soup = BeautifulSoup(html, "html.parser")

        session_div = soup.find("div", class_="session")
        if not session_div:
            raise ValueError("Could not find 'div.session' section in HTML.")

        rows = session_div.find_all("tr", class_="trade")
        if not rows:
            raise ValueError("No trade rows found in session data.")

        for row in rows:
            row_symbol = safe_text(row, "mnemonic")
            if row_symbol == symbol:
                return to_float(safe_text(row, "name"))

        return None
    except Exception as e:
        print(f"[parse_get_average_price] Error parsing HTML: {e}")
        return None


def parse_get_session_ltp(symbol: str, html: str):
    """From a /financial_session/{session}/ page, return LTP for symbol."""

    try:
        soup = BeautifulSoup(html, "html.parser")

        session_div = soup.find("div", class_="session")
        if not session_div:
            return None

        rows = session_div.find_all("tr", class_="trade")
        if not rows:
            return None

        for row in rows:
            if safe_text(row, "mnemonic") == symbol:
                return to_float(safe_text(row, "name"))

        return None
    except Exception as e:
        print(f"[parse_get_session_ltp] Error parsing HTML: {e}")
        return None


def parse_get_ytd_high_low(html: str):
    """
    Parse the current-year trade rows in the security page HTML and return
    YTD high/low with session/date metadata.
    """

    try:
        year = str(datetime.now().year)

        trades = parse_get_trades_for_year(year, html)
        if not trades:
            return None

        best_high = None
        best_low = None

        for t in trades:
            price = to_float(t.get("last_trade_price"))
            if price is None:
                continue

            entry = {
                "price": price,
                "session": t.get("session"),
                "session_date": t.get("session_date"),
            }

            if best_high is None or price > best_high["price"]:
                best_high = entry

            if best_low is None or price < best_low["price"]:
                best_low = entry

        if best_high is None or best_low is None:
            return None

        return {
            "year": int(year),
            "high": best_high,
            "low": best_low,
        }

    except Exception as e:
        print(f"[parse_get_ytd_high_low] Error parsing HTML: {e}")
        return None


def parse_get_session_trades(html: str):
    """Extract session data for all securities"""

    try:
        soup = BeautifulSoup(html, "html.parser")

        sessions_info_html = soup.find("div", class_="session")
        if not sessions_info_html:
            raise ValueError("Could not find 'div.session' section in HTML.")

        sessions = sessions_info_html.find_all("tr", class_="trade")
        if not sessions:
            raise ValueError("No session data found.")

        session_data = []

        for session in sessions:
            session_data.append(
                {
                    "symbol": safe_text(session, "mnemonic"),
                    "last_trade_price": safe_text(session, "name"),
                    "eps": safe_text(session, "best bid"),
                    "pe_ratio": safe_text(session, "vol bid"),
                    "dividends_paid_last_12_months": safe_text(session, "best offer"),
                    "dividend_yield": safe_text(session, "vol offer"),
                    "notes": safe_text(session, "opening price"),
                }
            )

        return session_data

    except Exception as e:
        print(f"[parse_get_securities_session] Error parsing HTML: {e}")
        return None


def parse_get_security_session_trade(symbol: str, html: str):
    """Extract session data for given security"""

    try:
        soup = BeautifulSoup(html, "html.parser")

        sessions_info_html = soup.find("div", class_="session")
        if not sessions_info_html:
            raise ValueError("Could not find 'div.session' section in HTML.")

        sessions = sessions_info_html.find_all("tr", class_="trade")
        if not sessions:
            raise ValueError("No session data found.")

        for session in sessions:
            session_symbol = safe_text(session, "mnemonic")

            if session_symbol == symbol:
                session_data = {
                    "symbol": safe_text(session, "mnemonic"),
                    "last_trade_price": safe_text(session, "name"),
                    "eps": safe_text(session, "best bid"),
                    "pe_ratio": safe_text(session, "vol bid"),
                    "dividends_paid_last_12_months": safe_text(session, "best offer"),
                    "dividend_yield": safe_text(session, "vol offer"),
                    "notes": safe_text(session, "opening price"),
                }

        return session_data

    except Exception as e:
        print(f"[parse_get_security_session] Error parsing HTML: {e}")
        return None


def parse_get_trades_for_year(year: str, html: str):
    """Get security trade information from a specific year"""

    try:
        soup = BeautifulSoup(html, "html.parser")

        security_info_html = soup.find("div", class_="year slide", id=year)
        if not security_info_html:
            raise ValueError("Could not find 'div.year.slide' section in HTML.")

        trade_data = []

        trades = security_info_html.find_all("tr", class_="trade")
        if not trades:
            raise ValueError("No trade rows found for this security.")

        for trade in trades:
            trade_data.append(
                {
                    "session": safe_text(trade, "session"),
                    "session_date": safe_text(trade, "date"),
                    "last_trade_price": safe_text(trade, "name"),
                    "eps": safe_text(trade, "best bid"),
                    "pe_ratio": safe_text(trade, "vol bid"),
                    "dividends_paid_last_12_months": safe_text(trade, "best offer"),
                    "dividend_yield": safe_text(trade, "vol offer"),
                    "notes": safe_text(trade, "opening price"),
                }
            )

        return trade_data

    except Exception as e:
        print(f"[parse_get_security_recent_year] Error parsing HTML: {e}")
        return None


def parse_get_historical_trades(start_date: str, end_date: str, html: str):
    """Parse historical trade data from HTML between given dates (DD/MM/YYYY)"""

    def normalize_date(date_str: str) -> str:
        parts = date_str.split("/")
        if len(parts) == 1:
            day, month, year = "01", "01", parts[0]
        elif len(parts) == 2:
            day, month, year = "01", parts[0], parts[1]
        elif len(parts) == 3:
            day, month, year = parts
        else:
            raise ValueError(f"Invalid date format: {date_str}")

        try:
            datetime(int(year), int(month), int(day))
        except ValueError as e:
            raise ValueError(f"Invalid date generated from {date_str}: {e}")

        return f"{day.zfill(2)}/{month.zfill(2)}/{year}"

    try:
        start_date = normalize_date(start_date)
        end_date = normalize_date(end_date)
        start = datetime.strptime(start_date, "%d/%m/%Y")
        end = datetime.strptime(end_date, "%d/%m/%Y")

        soup = BeautifulSoup(html, "html.parser")
        year_sections = soup.find_all("div", class_="year slide")
        if not year_sections:
            raise ValueError("No 'div.year.slide' sections found in HTML.")

        trade_data = []

        for section in year_sections:
            year_id = section.get("id")
            if not year_id or not year_id.isdigit():
                continue

            year_int = int(year_id)
            if year_int < start.year or year_int > end.year:
                continue

            trades = section.find_all("tr", class_="trade")
            for trade in trades:
                date_text = safe_text(trade, "date")
                if not date_text:
                    continue

                try:
                    trade_date = datetime.strptime(date_text, "%d/%m/%Y")
                except ValueError:
                    continue

                if start <= trade_date <= end:
                    trade_data.append(
                        {
                            "session": safe_text(trade, "session"),
                            "session_date": safe_text(trade, "date"),
                            "last_trade_price": safe_text(trade, "name"),
                            "eps": safe_text(trade, "best bid"),
                            "pe_ratio": safe_text(trade, "vol bid"),
                            "dividends_paid_last_12_months": safe_text(
                                trade, "best offer"
                            ),
                            "dividend_yield": safe_text(trade, "vol offer"),
                            "notes": safe_text(trade, "opening price"),
                        }
                    )

        trade_data.sort(key=lambda x: datetime.strptime(x["session_date"], "%d/%m/%Y"))
        return trade_data

    except Exception as e:
        print(f"[parse_get_historical_trades] Error parsing HTML: {e}")
        return None
