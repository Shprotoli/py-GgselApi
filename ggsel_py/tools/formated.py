from datetime import datetime, timedelta

# Naive datetimes are treated as Moscow time and sent to the API in UTC
MOSCOW_UTC_OFFSET = timedelta(hours=3)


def format_dt(value: str | datetime) -> str:
    """Converts a datetime to an ISO 8601 string for the API; strings are passed through unchanged"""
    if isinstance(value, datetime):
        value = value - MOSCOW_UTC_OFFSET
        return value.isoformat()
    return value
