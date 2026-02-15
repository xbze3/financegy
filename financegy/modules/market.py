from financegy.modules import securities as sec
from financegy.cache import cache_manager
from financegy.core import parser, request_handler


def get_active_securities(use_cache: bool = True):
    """Get all active securities"""

    func_name = "get_active_securities"

    if use_cache:
        cached = cache_manager.load_cache(func_name)
        if cached:
            return parser.parse_get_active_securities(cached)

    most_recent_session = sec.get_recent_session()

    path = f"/trade_session/{most_recent_session}"
    html = request_handler.fetch_page(path)

    cache_manager.save_cache(func_name, html)

    return parser.parse_get_active_securities(html)
