import string
from datetime import datetime, timezone

__all__ = ["get_base62_date"]


def _base62_encode(num):
    # Define the character set for base-62 encoding
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    result = []

    # Convert to base-62
    while num > 0:
        num, rem = divmod(num, 62)
        result.append(chars[rem])

    # Return the result reversed (since we've computed it backwards)
    return "".join(reversed(result))


def get_base62_date():
    # Get the current date
    current_date = datetime.now(timezone.utc)
    # Format the date as YYYYMMDD
    date_str = current_date.strftime("%Y%m%d")
    # Convert the date string to an integer
    date_int = int(date_str)
    # Convert the integer to a hexadecimal string
    return _base62_encode(date_int)
