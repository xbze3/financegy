from financegy import __version__

BASE_URL = "https://guyanastockexchangeinc.com"
HEADERS = {
    "User-Agent": f"FinanceGY/{__version__} (https://github.com/xbze3/financegy)"
}
REQUEST_TIMEOUT = 10