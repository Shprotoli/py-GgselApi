from typing import Union

from datetime import datetime, timedelta


def format_dt(value: Union[str | datetime]) -> str:
    if isinstance(value, datetime):
        value = value - timedelta(hours=3)
        return value.isoformat()
    return value
