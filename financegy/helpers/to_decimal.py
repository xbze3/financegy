from decimal import Decimal, InvalidOperation


def to_decimal(value, field_name="value"):
    """
    Convert strings/numbers to Decimal safely.
    Handles commas like "3,000.0".
    """
    try:
        clean_value = str(value).replace(",", "")
        return Decimal(clean_value)
    except (InvalidOperation, TypeError) as e:
        raise ValueError(f"Invalid {field_name}: {value}") from e
