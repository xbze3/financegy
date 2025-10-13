"""FinanceGY - a Python library for accessing data from the Guyana Stock Exchange."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("financegy")
except PackageNotFoundError:
    __version__ = "0.1.0"

from financegy.modules.securities import get_securities

__all__ = [
    "get_securities",
    "__version__",
]
