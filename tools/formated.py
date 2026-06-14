from datetime import datetime, timedelta


def format_dt(value: str | datetime) -> str:
    if isinstance(value, datetime):
        value = value - timedelta(hours=3)
        return value.isoformat()
    return value
