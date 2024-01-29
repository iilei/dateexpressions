import datetime as dt
from zoneinfo import ZoneInfo

import pytest
import time_machine

from dateexpressions.parse import parse

UTC_ZONEINFO = ZoneInfo(key="UTC")


@time_machine.travel(
    dt.datetime(2024, 1, 24, 14, 15, 16, tzinfo=UTC_ZONEINFO), tick=False
)
def test_parse():
    """API Tests"""
    assert parse("now") == dt.datetime(2024, 1, 24, 14, 15, 16, tzinfo=UTC_ZONEINFO)
    assert parse("now(Europe/Berlin)") == dt.datetime.now(ZoneInfo(key="Europe/Berlin"))
    assert parse("now(timezone=Europe/Amsterdam)") == dt.datetime.now(
        ZoneInfo(key="Europe/Amsterdam")
    )
    assert parse("now(Europe/Berlin)-1d/d") == dt.datetime(
        2024, 1, 23, 0, 0, tzinfo=ZoneInfo(key="Europe/Berlin")
    )
    assert parse("now-1h/h") == dt.datetime(2024, 1, 24, 13, tzinfo=ZoneInfo(key="UTC"))
    assert parse("now-1w/w+4h  /* beginning of last week, 4 am */") == dt.datetime(
        2024, 1, 15, 4, tzinfo=ZoneInfo(key="UTC")
    )

    with pytest.raises(Exception):
        parse("now-2M")


# def test_main(capsys):
#     """CLI Tests"""
#     # capsys is a pytest fixture that allows asserts against stdout/stderr
#     # https://docs.pytest.org/en/stable/capture.html
#     main(["7"])
#     captured = capsys.readouterr()
#     assert "The 7-th Fibonacci number is 13" in captured.out
