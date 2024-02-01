import datetime as dt
from zoneinfo import ZoneInfo

import pytest
import time_machine

from dateexpressions.parse import main, parse

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

    assert parse("now/M+1M:sat-1w /* last saturday this month */") == dt.datetime(
        2024, 1, 27, tzinfo=UTC_ZONEINFO
    )

    assert parse("now+20d/M:tue") == dt.datetime(2024, 2, 6, tzinfo=UTC_ZONEINFO)
    assert parse("now+20d/M:sat") == dt.datetime(2024, 2, 3, tzinfo=UTC_ZONEINFO)
    assert parse(
        "now/h+30m+15s /* beginning of the current hour, added 30m and 15s */"
    ) == dt.datetime(2024, 1, 24, 14, 30, 15, tzinfo=UTC_ZONEINFO)

    assert parse(
        "/h /* beginning of the current hour - 'now' and UTC both are implicit, no need to state it */"
    ) == dt.datetime(2024, 1, 24, 14, tzinfo=UTC_ZONEINFO)

    with pytest.raises(Exception):
        # Because a month is not a fixed duration, Deltas with unit=Month are only
        # applicable directly after a `Floor to Month` Operation
        parse("now-1M")


@time_machine.travel(dt.datetime(2024, 1, 2, 14, 15, 16, tzinfo=UTC_ZONEINFO), tick=False)
def test_main(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["now-78h/h"])
    captured = capsys.readouterr()
    assert "2023-12-30 08:00:00+00:00" in captured.out
