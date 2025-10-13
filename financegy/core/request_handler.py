import requests
from ..config import BASE_URL, HEADERS, REQUEST_TIMEOUT

def fetch_page(endpoint: str):
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.text