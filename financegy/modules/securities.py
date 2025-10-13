from financegy.core import request_handler, parser


def get_securities():
    """Get names of all currently traded securities"""
    path = "/securities/"
    html = request_handler.fetch_page(path)
    return parser.parse_get_securities(html);

