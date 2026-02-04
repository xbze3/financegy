from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from financegy.modules import securities


def _to_decimal(value, field_name="value"):
    """
    Convert strings/numbers to Decimal safely.
    Handles commas like "3,000.0".
    """
    try:
        clean_value = str(value).replace(",", "")
        return Decimal(clean_value)
    except (InvalidOperation, TypeError) as e:
        raise ValueError(f"Invalid {field_name}: {value}") from e


def calculate_position_value(symbol: str, shares):
    try:
        shares = _to_decimal(shares, "shares")
        if shares <= 0:
            raise ValueError("Shares must be greater than zero")

        last_trade = securities.get_recent_trade(symbol)
        last_trade_price = _to_decimal(
            last_trade.get("last_trade_price"), "last_trade_price"
        )

        position_value = last_trade_price * shares

        return {
            "last_trade": last_trade,
            "position_value": str(position_value),
        }

    except (ValueError, KeyError, TypeError) as e:
        raise ValueError(f"[calculate_position_value] Invalid input or data: {e}")


def calculate_position_return(symbol: str, shares, purchase_price):
    try:
        shares = _to_decimal(shares, "shares")
        purchase_price = _to_decimal(purchase_price, "purchase_price")

        if shares <= 0:
            raise ValueError("Shares must be greater than zero")
        if purchase_price <= 0:
            raise ValueError("Purchase price must be greater than zero")

        last_trade = securities.get_recent_trade(symbol)
        last_trade_price = _to_decimal(
            last_trade.get("last_trade_price"), "last_trade_price"
        )

        position_return = (last_trade_price - purchase_price) * shares

        return {
            "last_trade": last_trade,
            "position_return": str(position_return),
        }

    except (ValueError, KeyError, TypeError) as e:
        raise ValueError(f"[calculate_position_return] Invalid input or data: {e}")


def calculate_position_return_percent(symbol, shares, purchase_price):
    try:
        shares = _to_decimal(shares, "shares")
        purchase_price = _to_decimal(purchase_price, "purchase_price")

        if shares <= 0:
            raise ValueError("Shares must be greater than zero")
        if purchase_price <= 0:
            raise ValueError("Purchase price must be greater than zero")

        last_trade = securities.get_recent_trade(symbol)
        last_trade_price = _to_decimal(
            last_trade.get("last_trade_price"), "last_trade_price"
        )

        return_percent = (
            (last_trade_price - purchase_price) / purchase_price
        ) * Decimal("100")

        return {
            "last_trade": last_trade,
            "position_return_percent": str(round(return_percent, 2)),
        }

    except (ValueError, KeyError, TypeError) as e:
        raise ValueError(
            f"[calculate_position_return_percent] Invalid input or data: {e}"
        )


def calculate_portfolio_summary(positions: list[dict]):
    try:
        total_invested = Decimal("0")
        total_value = Decimal("0")
        detailed_positions = []

        for pos in positions:
            symbol = pos["symbol"]
            shares = _to_decimal(pos.get("shares"), f"shares for {symbol}")
            purchase_price = _to_decimal(
                pos.get("purchase_price"), f"purchase_price for {symbol}"
            )

            if shares <= 0:
                raise ValueError(f"Invalid shares for {symbol}")
            if purchase_price <= 0:
                raise ValueError(f"Invalid purchase price for {symbol}")

            last_trade = securities.get_recent_trade(symbol)
            last_trade_price = _to_decimal(
                last_trade.get("last_trade_price"), f"last_trade_price for {symbol}"
            )

            invested = shares * purchase_price
            current_value = shares * last_trade_price
            gain_loss = current_value - invested

            total_invested += invested
            total_value += current_value

            detailed_positions.append(
                {
                    "symbol": symbol,
                    "shares": str(shares),
                    "purchase_price": str(purchase_price),
                    "last_trade_price": str(last_trade_price),
                    "invested": str(invested),
                    "current_value": str(current_value),
                    "gain_loss": str(gain_loss),
                }
            )

        total_gain_loss = total_value - total_invested

        if total_invested != 0:
            return_percent = (
                total_gain_loss / total_invested * Decimal("100")
            ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        else:
            return_percent = Decimal("0.00")

        return {
            "summary": {
                "total_invested": str(total_invested),
                "current_value": str(total_value),
                "total_gain_loss": str(total_gain_loss),
                "return_percent": str(return_percent),
            },
            "positions": detailed_positions,
        }

    except (ValueError, KeyError, TypeError) as e:
        raise ValueError(f"[calculate_portfolio_summary] Invalid portfolio data: {e}")
