from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

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
            symbol = security.find_all("div", class_="acronym inline")[0].get_text(strip=True)
            name = security.find_all("div", class_="name inline")[0].get_text(strip=True)

            security_info.append({
                "symbol": symbol,
                "name": name
            })

        
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
        
        def safe_text(parent, class_name):
            cell = parent.find("td", class_=class_name)
            return cell.get_text(strip=True) if cell else None
        
        for trade in trades:
            trade_data.append({
            "session": safe_text(trade, "session"),
            "date": safe_text(trade, "date"),
            "ltp": safe_text(trade, "name"),
            "best_bid": safe_text(trade, "best bid"),
            "vol_bid": safe_text(trade, "vol bid"),
            "best_offer": safe_text(trade, "best offer"),
            "vol_offer": safe_text(trade, "vol offer"),
            "opening_price": safe_text(trade, "opening price"),
            })

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

        def safe_text(parent, class_name):
            cell = parent.find("td", class_=class_name)
            return cell.get_text(strip=True) if cell else None

        recent_info = {
            "session": safe_text(recent, "session"),
            "date": safe_text(recent, "date"),
            "ltp": safe_text(recent, "name"),
            "best_bid": safe_text(recent, "best bid"),
            "vol_bid": safe_text(recent, "vol bid"),
            "best_offer": safe_text(recent, "best offer"),
            "vol_offer": safe_text(recent, "vol offer"),
            "opening_price": safe_text(recent, "opening price"),
        }

        return recent_info

    except Exception as e:
        print(f"[parse_get_security_recent] Error parsing HTML: {e}")
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

        def safe_text(parent, class_name):
            cell = parent.find("td", class_=class_name)
            return cell.get_text(strip=True) if cell else None

        session_data = []

        for session in sessions:
            session_data.append({
            "symbol": safe_text(session, "mnemonic"),
            "ltp": safe_text(session, "name"),
            "best_bid": safe_text(session, "best bid"),
            "vol_bid": safe_text(session, "vol bid"),
            "best_offer": safe_text(session, "best offer"),
            "vol_offer": safe_text(session, "vol offer"),
            "opening_price": safe_text(session, "opening price"),
            })

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
        
        def safe_text(parent, class_name):
            cell = parent.find("td", class_=class_name)
            return cell.get_text(strip=True) if cell else None


        for session in sessions:
            session_symbol = safe_text(session, "mnemonic")

            if (session_symbol == symbol):
                session_data = {
                    "symbol": safe_text(session, "mnemonic"),
                    "ltp": safe_text(session, "name"),
                    "best_bid": safe_text(session, "best bid"),
                    "vol_bid": safe_text(session, "vol bid"),
                    "best_offer": safe_text(session, "best offer"),
                    "vol_offer": safe_text(session, "vol offer"),
                    "opening_price": safe_text(session, "opening price"),
                }
        
        return session_data
    
    except Exception as e:
        print(f"[parse_get_security_session] Error parsing HTML: {e}")
        return None
    
def parse_get_trades_for_year(year: str, path: str):
    """Get security trade information from a specific year"""

    trades = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(path, timeout=30000) 

            page.wait_for_selector("div.slide", timeout=10000)

            year_div = page.locator('div.slide', has_text=year).first
            if not year_div:
                print(f"[ERROR] No div found for year: {year}")
                return trades

            year_div.click()
            page.wait_for_timeout(500)
            page.wait_for_selector("div.year.slide", timeout=10000)

            html = page.content()
            trades = parse_get_security_recent_year(html)

    except PlaywrightTimeoutError as e:
        print(f"[TIMEOUT ERROR] Page or element took too long to load: {e}")
    except Exception as e:
        print(f"[ERROR] Failed to get trades for year {year}: {e}")
    finally:
        try:
            browser.close()
        except Exception:
            pass

    return trades