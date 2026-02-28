def to_float(value):
    if value is None:
        return None

    value = str(value).strip()

    if value in ("", "-", "N/A"):
        return None

    # Remove commas
    value = value.replace(",", "")

    # Remove percentage sign if present
    if value.endswith("%"):
        value = value.replace("%", "").strip()

    try:
        return float(value)
    except ValueError:
        return None
