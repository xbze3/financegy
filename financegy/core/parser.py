from bs4 import BeautifulSoup

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
            acronym = security.find_all("div", class_="acronym inline")[0].get_text(strip=True)
            name = security.find_all("div", class_="name inline")[0].get_text(strip=True)

            security_info.append({
                "acronym": acronym,
                "name": name
            })

        
        return security_info
    
    except Exception as e:
        print(f"Error parsing securities: {e}")