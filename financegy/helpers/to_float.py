# Function to convert GSE price string to float type


def to_float(value):
    if value is None:
        return None
    value = value.strip()
    if value in ("", "-", "N/A"):
        return None
    return float(value.replace(",", ""))
