from datetime import datetime

from tools.formated import format_dt


def test_format_dt_handles_datetime():
    assert format_dt(datetime(2024, 1, 1, 3, 0, 0)) == "2024-01-01T00:00:00"


def test_format_dt_passes_through_strings():
    assert format_dt("2024-01-01T00:00:00") == "2024-01-01T00:00:00"
